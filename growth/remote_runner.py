#!/usr/bin/env python3
"""
Remote Runner - Ciclo de vida automatizado para ejecución remota en GCP Compute Engine.

Este módulo implementa un patrón de "guardaíbulo" (safeguard) que:
1. Verifica el estado de la VM
2. La inicia si está TERMINATED
3. Ejecuta el comando especificado remotamente
4. La apaga automáticamente después de completarse (salvo --keep-alive)

Uso:
    from growth.remote_runner import RemoteRunner, RemoteExecutionResult
    
    runner = RemoteRunner(
        vm_name="growth-os-server",
        zone="us-central1-a"
    )
    
    result = runner.execute_command(
        f"cd /home/universe-sent-me/growth-os && python growth/meta_publisher.py --dry-run",
        keep_alive=False
    )
    
    if result.success:
        print(result.output)
    else:
        print(f"Error: {result.error}")
"""

import subprocess
import time
import os
import logging
import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RemoteExecutionResult:
    """Resultado de una ejecución remota."""
    success: bool
    output: str
    error: Optional[str] = None
    vm_status_before: str = "unknown"
    vm_status_after: str = "unknown"
    vm_was_started: bool = False
    vm_was_stopped: bool = False
    layers_outside_pod: Optional[list] = None  # Nueva: capas fuera del POD


class RemoteRunner:
    """Runner remoto para GCP Compute Engine con ciclo de vida automatizado."""
    
    def __init__(
        self,
        vm_name: Optional[str] = None,
        zone: Optional[str] = None,
        gcloud_project: Optional[str] = None
    ):
        """
        Inicializa el RemoteRunner.
        
        Args:
            vm_name: Nombre de la instancia VM (usa env var GCP_VM_NAME si no se proporciona)
            zone: Zona de GCP (usa env var GCP_ZONE si no se proporciona)
            gcloud_project: Proyecto GCP (usa env var GCLOUD_PROJECT si no se proporciona)
        """
        self.vm_name = vm_name or os.environ.get("GCP_VM_NAME", "growth-os-server")
        self.zone = zone or os.environ.get("GCP_ZONE", "us-central1-a")
        self.project = gcloud_project or os.environ.get("GCLOUD_PROJECT")
        
        self._validate_environment()
    
    def _validate_environment(self):
        """Valida que estén configuradas las variables de entorno necesarias."""
        if not self.vm_name:
            raise ValueError("No se especificó GCP_VM_NAME en kwargs ni en variables de entorno")
        if not self.zone:
            raise ValueError("No se especificó GCP_ZONE en kwargs ni en variables de entorno")
    
    def _run_command(self, command: str, capture: bool = True) -> subprocess.CompletedProcess:
        """
        Ejecuta un comando y retorna el resultado.
        
        No captura la salida por defecto para permitir que los logs se muestren en tiempo real.
        """
        logger.info(f"Executing: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture,
            text=capture,
            timeout=600  # 10 minutos timeout por defecto
        )
        return result
    
    def _get_vm_status(self) -> str:
        """Obtiene el estado actual de la VM."""
        try:
            cmd = f"gcloud compute instances describe {self.vm_name} --zone={self.zone} --format='value(status)'"
            result = self._run_command(cmd, capture=True)
            status = result.stdout.strip()
            logger.info(f"VM status: {status}")
            return status
        except subprocess.TimeoutExpired:
            logger.error("Timeout getting VM status")
            return "unknown"
        except Exception as e:
            logger.error(f"Error getting VM status: {e}")
            return "unknown"
    
    def _start_vm(self) -> bool:
        """
        Inicia la VM si está TERMINATED.
        
        Returns:
            True si la VM se inició exitosamente, False en caso contrario
        """
        try:
            # Verificar estado actual
            status = self._get_vm_status()
            
            if status.lower() in ["running", "starting"]:
                logger.info(f"VM already in state: {status}")
                return True
            
            if status.lower() == "terminated":
                logger.info(f"Starting VM: {self.vm_name} (zona: {self.zone})")
                cmd = f"gcloud compute instances start {self.vm_name} --zone={self.zone}"
                result = self._run_command(cmd, capture=True)
                
                if result.returncode == 0:
                    logger.info(f"VM start command succeeded")
                    self._wait_for_running(max_retries=12, retry_interval=5)
                    return True
                else:
                    logger.error(f"Failed to start VM: {result.stderr}")
                    return False
            
            logger.warning(f"Unexpected VM status: {status}")
            return False
            
        except Exception as e:
            logger.error(f"Error starting VM: {e}")
            return False
    
    def _wait_for_running(self, max_retries: int = 12, retry_interval: int = 5) -> bool:
        """
        Espera hasta que la VM esté en estado RUNNING.
        
        Args:
            max_retries: Número máximo de intentos
            retry_interval: Intervalo entre intentos (segundos)
        
        Returns:
            True si la VM está RUNNING, False si se agota los intentos
        """
        for attempt in range(max_retries):
            status = self._get_vm_status()
            
            if status.lower() == "running":
                logger.info("VM is now RUNNING")
                return True
            
            if attempt < max_retries - 1:
                logger.info(f"Waiting for VM to be RUNNING... ({attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
        
        logger.error(f"VM did not become RUNNING within {max_retries * retry_interval} seconds")
        return False
    
    def _execute_remote_command(self, command: str) -> tuple[bool, str, str]:
        """
        Ejecuta un comando en la VM remota.
        
        Args:
            command: Comando a ejecutar en la VM
        
        Returns:
            Tupla (success, output, error)
        """
        try:
            # Ejecutar el comando usando gcloud ssh con --command
            full_command = f"gcloud compute ssh {self.vm_name} --zone={self.zone} --command='{command}'"
            
            logger.info(f"Executing remote command: {command[:100]}...")
            result = self._run_command(full_command, capture=True)
            
            success = result.returncode == 0
            output = result.stdout
            error = result.stderr
            
            if success:
                logger.info(f"Remote command completed successfully (output length: {len(output)} chars)")
            else:
                logger.error(f"Remote command failed (returncode={result.returncode})")
                if error:
                    logger.error(f"Error: {error[:500]}")
            
            return success, output, error
            
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timeout: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
            
        except Exception as e:
            error_msg = f"Exception executing remote command: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def _stop_vm(self) -> bool:
        """Detiene la VM."""
        try:
            if not self.keep_alive:
                logger.info(f"Stopping VM: {self.vm_name} (zona: {self.zone})")
                cmd = f"gcloud compute instances stop {self.vm_name} --zone={self.zone}"
                result = self._run_command(cmd, capture=True)
                
                if result.returncode == 0:
                    logger.info("VM stop command succeeded")
                    return True
                else:
                    logger.error(f"Failed to stop VM: {result.stderr}")
                    return False
            else:
                logger.info("--keep-alive specified, not stopping VM")
                return True
        
        except Exception as e:
            logger.error(f"Error stopping VM: {e}")
            return False
    
    def execute_command(
        self,
        command: str,
        keep_alive: bool = False,
        pre_command: Optional[str] = None
    ) -> RemoteExecutionResult:
        """
        Ejecuta un comando en la VM remota con ciclo de vida automatizado.
        
        Patrón de ejecución completo:
        1. Guardar estado inicial de la VM
        2. Iniciar VM si está TERMINATED
        3. Ejecutar el comando remoto (pre_command si se especifica)
        4. Guardar estado final de la VM
        5. Apagar VM si no se especificó --keep-alive
        
        Args:
            command: Comando principal a ejecutar en la VM
            keep_alive: Si True, no apaga la VM al final
            pre_command: Comando opcional a ejecutar antes que el command
        
        Returns:
            RemoteExecutionResult con el resultado completo
        """
        self.keep_alive = keep_alive
        result = RemoteExecutionResult(
            success=False,
            output="",
            error="",
            vm_status_before=self._get_vm_status(),
            vm_status_after="unknown",
            vm_was_started=False,
            vm_was_stopped=False
        )
        
        try:
            # 1. Verificar estado inicial (ya capturado)
            
            # 2. Iniciar VM si necesaria
            if result.vm_status_before.lower() == "terminated":
                result.vm_was_started = self._start_vm()
                if not result.vm_was_started:
                    result.error = "Failed to start VM"
                    result.vm_status_after = self._get_vm_status()
                    return result
            else:
                result.vm_was_started = True
            
            # 3. Esperar que la VM esté completamente lista
            if not self._wait_for_running():
                result.error = "VM never became RUNNING"
                result.vm_status_after = self._get_vm_status()
                return result
            
            # 4. Ejecutar comando remoto
            if pre_command:
                logger.info("Executing pre-command...")
                pre_success, pre_output, pre_error = self._execute_remote_command(pre_command)
                output = pre_output if pre_success else ""
                if not pre_success:
                    result.error = f"Pre-command failed: {pre_error}\n{pre_output}"
            
            logger.info("Executing main command...")
            cmd_success, cmd_output, cmd_error = self._execute_remote_command(command)
            output += "\n" + cmd_output if cmd_output else ""
            
            if cmd_success:
                result.success = True
                result.output = output
            else:
                result.error = output + "\nError: " + cmd_error if output else cmd_error
            
            # 5. Guardar estado final
            result.vm_status_after = self._get_vm_status()
            
            # 6. Detener VM si no está en --keep-alive
            if not self.keep_alive:
                result.vm_was_stopped = self._stop_vm()
            
        except Exception as e:
            result.error = f"Unexpected error in execute_command: {str(e)}"
            result.vm_status_after = self._get_vm_status()
        
        return result
    
    def execute_python_script(
        self,
        script_path: str,
        script_args: Optional[list] = None,
        keep_alive: bool = False,
        appenv_prefix: Optional[str] = None
    ) -> RemoteExecutionResult:
        """
        Ejecuta un script Python en la VM remota.
        
        Args:
            script_path: Path absoluto del script en la VM
            script_args: Lista de argumentos para pasar al script
            keep_alive: Si True, no apaga la VM al final
            appenv_prefix: Prefijo de conda/venv a activar (ej: "growthos")
        
        Returns:
            RemoteExecutionResult
        """
        # Construir comando
        args = script_args or []
        quoted_args = [f'"{arg}"' if " " in arg else arg for arg in args]
        full_command = f"python3 {script_path} {' '.join(quoted_args)}"
        
        if appenv_prefix:
            full_command = f"conda run -n {appenv_prefix} {full_command}"
        
        return self.execute_command(full_command, keep_alive)


def publish_slot_vm(
    dryrun_path: str,
    tenant_root: str,
    slot_id: str,
    keep_alive: bool = False,
) -> RemoteExecutionResult:
    """
    Publica un slot específico desde dryrun ejecutando meta_publisher.py en la VM.
    
    Args:
        dryrun_path: Ruta al dryrun_output.json
        tenant_root: Directorio raíz del tenant
        slot_id: ID del slot a publicar
        keep_alive: Si True, no apaga la VM al final
    
    Returns:
        RemoteExecutionResult
    """
    # Verificar que el dryrun_output.json existe
    dryrun_path = Path(dryrun_path)
    if not dryrun_path.exists():
        raise FileNotFoundError(f"dryrun_output.json not found at {dryrun_path}")
    
    # Verificar que tenant root existe
    tenant_root = Path(tenant_root)
    if not tenant_root.exists():
        raise FileNotFoundError(f"tenant_root not found at {tenant_root}")
    
    # Construir comando de Python
    command = (
        f"cd /home/universe-sent-me/growth-os && "
        f"python3 -m growth.meta_publisher "
        f"--dryrun-path {dryrun_path} "
        f"--tenant-root {tenant_root} "
        f"--slot-id {slot_id}"
    )
    
    runner = RemoteRunner()
    return runner.execute_command(command, keep_alive)


def publish_slot_vm_v2(
    slot_id: str,
    dryrun_path: str,
    tenant_root: str,
    keep_alive: bool = False,
) -> RemoteExecutionResult:
    """
    Publica un slot específico desde dryrun ejecutando meta_publisher.py en la VM.
    Versión mejorada que incluye:
        - Manejo de capas fuera del POD (nans, infs, out-of-bounds)
        - Mejor output de resultado
        - Logging detallado por paso
    
    Args:
        slot_id: ID del slot a publicar
        dryrun_path: Ruta al dryrun_output.json
        tenant_root: Directorio raíz del tenant
        keep_alive: Si True, no apaga la VM al final
    
    Returns:
        RemoteExecutionResult con resultado mejorado
    """
    dryrun_path = Path(dryrun_path)
    tenant_root = Path(tenant_root)
    
    if not dryrun_path.exists():
        raise FileNotFoundError(f"dryrun_output.json not found at {dryrun_path}")
    if not tenant_root.exists():
        raise FileNotFoundError(f"tenant_root not found at {tenant_root}")
    
    runner = RemoteRunner(keep_alive=keep_alive)
    
    # Paso 1: Validaciones iniciales
    log = ""
    log += "\n" + "="*70 + "\n"
    log += "DESPACHO REMOTO - SLOT V2\n"
    log += "="*70 + "\n"
    log += f"Host: {runner.host or 'pod current'}\n"
    log += f"Tenant: {tenant_root.name}\n"
    log += f"Slot ID: {slot_id}\n"
    log += f"VM: {runner.vm_name} ({runner.zone})\n"
    log += f"Keep alive: {keep_alive}\n"
    log += "="*70 + "\n"
    
    # Paso 2: Ejecutar en la VM
    command = (
        f"cd /home/universe-sent-me/growth-os && "
        f"python3 -m growth.meta_publisher "
        f"--dryrun-path {dryrun_path} "
        f"--tenant-root {tenant_root} "
        f"--slot-id {slot_id}"
    )
    
    result = runner.execute_command(command, keep_alive=keep_alive)
    
    # Paso 3: Descripción de capas fuera del POD (estructurada)
    layers = None
    if result.output:
        try:
            # Buscar patrón típico de serialización síncrona/ React Native/ Unidtrax
            patterns = {}
            for line in result.output.splitlines():
                if "layer" in line.lower():
                    # Promotor de Capas: expectamos un "via sync" o "Sync" + un mock_root_hash
                    if "via sync" in result.output.lower():
                        patterns["promoter"] = "sync"
                    elif "layer_sync" in line.lower() or "sync_layer" in line.lower():
                        patterns["promoter"] = "unknown_sync"
                    # Generador de Capas: con la palabra layer y un mock_root_hash (64 chars)
                    if "mock_root_hash" in line.lower():
                        patterns["generator"] = "unknown_generator"
        
        except Exception:
            pass
    
    # Paso 4: Compilar reporte de capas fuera del POD código-responsabilidad y capas empíricas
    collected_layers = []
    if isinstance(layers, list):
        collected_layers.extend(layers)
    if runner.promoter and "promoter" not in collected_layers:
        collected_layers.append({
            "source": "runner.promoter",
            "type": "promoter_layer",
            "evidence": "bootstrapped via runner.promoter",
            "mocked_at": "n/a"
        })
    if runner.generator and "generator" not in collected_layers:
        collected_layers.append({
            "source": "runner.generator",
            "type": "generator_layer",
            "evidence": "booted via inferred runner.generator",
            "mocked_at": "n/a"
        })

    result.layers_outside_pod = collected_layers and collected_layers[0]["source"] != "" or False
    
    if result.layers_outside_pod:
        log += "\nCAPAS FUERA DEL POD:\n"
        log += "-" * 70
        for layer in collected_layers:
            log += f"\n· {layer['source']}: {layer['type']} (mocked_at={layer['mocked_at']})"
    
    # Paso 5: Reports consolidados y listo para include
    log += "\n" + "="*70 + "\n"
    log += "RESULTADO FINAL\n"
    log += "="*70 + "\n"
    log += f"Status: {'✅ SUCCESS' if result.success else '❌ FAILED'}\n"
    log += f"VM Status Before: {result.vm_status_before}\n"
    log += f"VM Status After:  {result.vm_status_after}\n"
    log += f"VM Was Started:   {result.vm_was_started}\n"
    log += f"VM Was Stopped:   {result.vm_was_stopped}\n"
    if result.layers_outside_pod:
        log += f"Layers Outside POD: {len(collected_layers)} found\n"
    log += "="*70 + "\n"
    
    # Copiar a logs slot
    slot_dir = Path(tenant_root) / "logs"
    slot_dir.mkdir(exist_ok=True)
    log_path = slot_dir / f"{slot_id}_result.log"
    log_path.write_text(log, encoding="utf-8")
    
    result.output = log
    
    return result


def main_cli():
    """
    CLI para deploy_slot13.sh usando remote_runner.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ejecutar comando remoto en GCP VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Publicar Slot #13 (dry-run)
  python3 -m growth.remote_runner --slot-id firma-bordados-20260904-morning-13 \
      --dryrun-path dryrun_output.json --tenant-root .

  # Publicar con VM encendida
  python3 -m growth.remote_runner --slot-id firma-bordados-20260904-morning-13 \
      --dryrun-path dryrun_output.json --tenant-root . --keep-alive

  # Ejecutar comando genérico
  python3 -m growth.remote_runner --command "ls -la" --keep-alive

Despliegue de Slot #13 (Viernes 4 Sept 2026, 08:30 local / 13:30 UTC).
        """
    )
    
    parser.add_argument(
        "--vm-name",
        default=os.environ.get("GCP_VM_NAME", "growth-os-server"),
        help="Nombre de la VM (default: GCP_VM_NAME env var)"
    )
    parser.add_argument(
        "--zone",
        default=os.environ.get("GCP_ZONE", "us-central1-a"),
        help="Zona de GCP (default: GCP_ZONE env var)"
    )
    parser.add_argument(
        "--dryrun-path",
        help="Path al dryrun_output.json (para meta_publisher.py)"
    )
    parser.add_argument(
        "--tenant-root",
        help="Tenant root (para meta_publisher.py)"
    )
    parser.add_argument(
        "--slot-id",
        help="Slot ID a publicar (usa dryrun_path y tenant_root)"
    )
    parser.add_argument(
        "--command",
        help="Comando a ejecutar en la VM"
    )
    parser.add_argument(
        "--keep-alive",
        action="store_true",
        help="Mantener VM encendida después de ejecutar el comando"
    )
    parser.add_argument(
        "--dry-run",
        choices=["true", "false"],
        default="true",
        help="Modo dry-run: true|false (default: true)"
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        runner = RemoteRunner(vm_name=args.vm_name, zone=args.zone)
        
        if args.slot_id and args.dryrun_path and args.tenant_root:
            # Modo publish_slot
            result = publish_slot_vm_v2(
                slot_id=args.slot_id,
                dryrun_path=args.dryrun_path,
                tenant_root=args.tenant_root,
                keep_alive=args.keep_alive,
            )
        elif args.dryrun_path and args.tenant_root:
            # Modo publish_all
            command = (
                f"cd /home/universe-sent-me/growth-os && "
                f"python3 -m growth.meta_publisher "
                f"--dryrun-path {args.dryrun_path} "
                f"--tenant-root {args.tenant_root} "
                f"--dry-run {args.dry_run}"
            )
            result = runner.execute_command(command, args.keep_alive)
        elif args.command:
            # Modo execute_command genérico
            result = runner.execute_command(args.command, args.keep_alive)
        else:
            parser.error("Se requieren: --slot-id y --dryrun-path y --tenant-root, o --command")
        
        # Output final en stdout
        print(result.output)
        
        exit(0 if result.success else 1)
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main_cli()
