#!/usr/bin/env bash
# ==============================================================================
# Deploy Pending Week - Programa en lote las publicaciones pendientes
# Slots: #10, #11, #12, #14, #15, #16, #17, #18, #19, #20 (omit #13)
# ==============================================================================

set -euo pipefail

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GROWTH_OS_ROOT="$SCRIPT_DIR"
DRYRUN_PATH="$GROWTH_OS_ROOT/dryrun_output.json"
TENANT_ROOT="$GROWTH_OS_ROOT/tenants/firma-bordados"

# Slots a desplegar (omitiendo #13 ya programado)
SLOTS=(
    "firma-bordados-20260903-morning-10"   # #10 PHOTO
    "firma-bordados-20260903-afternoon-11" # #11 PHOTO
    "firma-bordados-20260904-evening-12"   # #12 PHOTO (user says TEXT_ONLY but actual is media)
    "firma-bordados-20260904-afternoon-14" # #14 PHOTO
    "firma-bordados-20260905-evening-15"   # #15 VIDEO_REEL
    "firma-bordados-20260905-morning-16"   # #16 PHOTO
    "firma-bordados-20260905-afternoon-17" # #17 TEXT_ONLY
    "firma-bordados-20260906-morning-18"   # #18 TEXT_ONLY
    "firma-bordados-20260906-afternoon-19" # #19 TEXT_ONLY
    "firma-bordados-20260907-evening-20"   # #20 TEXT_ONLY
)

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de GCP (desde .env del tenant)
source "$TENANT_ROOT/.env" 2>/dev/null || true

VM_NAME="${GCP_VM_NAME:-universe-20260902-105559}"
ZONE="${GCP_ZONE:-us-south1-b}"
PROJECT="${GCLOUD_PROJECT:-growth-os-373890354472}"

echo -e "${BLUE}==============================================================${NC}"
echo -e "${BLUE}  DEPLOY PENDING WEEK - Growth OS${NC}"
echo -e "${BLUE}==============================================================${NC}"
echo ""
echo "VM: $VM_NAME ($ZONE)"
echo "Project: $PROJECT"
echo "Slots a desplegar: ${#SLOTS[@]}"
echo ""

# Función: Verificar estado de la VM
get_vm_status() {
    gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format='value(status)' 2>/dev/null || echo "unknown"
}

# Función: Iniciar VM si está TERMINATED
start_vm_if_needed() {
    local status=$(get_vm_status)
    echo -e "${YELLOW}Estado VM: $status${NC}"
    
    if [[ "$status" == "TERMINATED" ]]; then
        echo -e "${YELLOW}Iniciando VM...${NC}"
        gcloud compute instances start "$VM_NAME" --zone="$ZONE" --quiet
        
        # Esperar a RUNNING
        local retries=12
        while [[ $retries -gt 0 ]]; do
            status=$(get_vm_status)
            if [[ "$status" == "RUNNING" ]]; then
                echo -e "${GREEN}VM RUNNING${NC}"
                return 0
            fi
            echo "Esperando RUNNING... ($retries intentos restantes)"
            sleep 5
            ((retries--))
        done
        echo -e "${RED}ERROR: VM no llegó a RUNNING${NC}"
        return 1
    elif [[ "$status" == "RUNNING" ]]; then
        echo -e "${GREEN}VM ya está RUNNING${NC}"
        return 0
    else
        echo -e "${YELLOW}VM en estado inesperado: $status${NC}"
        return 1
    fi
}

# Función: Detener VM
stop_vm() {
    echo -e "${YELLOW}Deteniendo VM para congelar consumo...${NC}"
    gcloud compute instances stop "$VM_NAME" --zone="$ZONE" --quiet
    echo -e "${GREEN}VM detenida${NC}"
}

# Función: Sincronizar assets a la VM
sync_assets_to_vm() {
    echo -e "${BLUE}Sincronizando assets multimedia a la VM...${NC}"
    
    # Assets base del tenant (Firma Bordados en Google Drive)
    # Usamos rsync a través de gcloud compute scp
    # Nota: La VM debe tener acceso a Google Drive montado o sincronizamos los archivos
    
    # Lista de archivos únicos necesarios para los slots
    local assets=(
        "01_lunes_detalle_uniforme.png"
        "IMG-20260821-WA0003.jpg"
        "2026-08-25_calidad_logo_bordado.png"
        "FB_IMG_1787256185059.jpg"
        "FB_IMG_1787256197738.jpg"
        "03_miercoles_nombres_bordados.png"
        "2026-08-27_iniciales_monogramas.png"
        "FB_IMG_1787256206553.jpg"
        "04_jueves_que_personalizarias.png"
        "file_000000001ca481fd88fd4c3d4fc21d8a.png"
        "FB_IMG_1787256161650.jpg"
        "05_sabado_etiqueta_negocio_local.png"
        "2026-08-29_guia_pedido.png"
        "Firma_Bordados_1.mp4"
        "06_domingo_agenda_pedido_v2_contacto.png"
    )
    
    # Crear directorio temporal en la VM
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="mkdir -p /home/universe-sent-me/growth-os/tenants/firma-bordados/assets/Firma\ Bordados" --quiet
    
    # Sincronizar cada archivo
    for asset in "${assets[@]}"; do
        # Buscar el archivo en la estructura local (Google Drive)
        local found=false
        for search_path in \
            "$TENANT_ROOT/assets/Firma Bordados/$asset" \
            "$TENANT_ROOT/assets/Firma Bordados/Publicaciones Agosto/24 al 30 Agosto 2026/03 Creativos Ejecutivos/$asset" \
            "$TENANT_ROOT/assets/Firma Bordados/Publicaciones Agosto/Reels/$asset"; do
            if [[ -f "$search_path" ]]; then
                echo "  Syncing: $asset"
                gcloud compute scp "$search_path" "$VM_NAME:/home/universe-sent-me/growth-os/tenants/firma-bordados/assets/Firma Bordados/$asset" --zone="$ZONE" --quiet
                found=true
                break
            fi
        done
        if [[ "$found" == "false" ]]; then
            echo -e "${YELLOW}  Advertencia: $asset no encontrado localmente${NC}"
        fi
    done
    
    echo -e "${GREEN}Sincronización de assets completada${NC}"
}

# Función: Publicar un slot en la VM (modo real)
publish_slot_vm() {
    local slot_id="$1"
    echo -e "${BLUE}Publicando slot: $slot_id${NC}"
    
    local cmd="cd /home/universe-sent-me/growth-os && python3 -m growth.meta_publisher \
        --dryrun-path $DRYRUN_PATH \
        --tenant-root $TENANT_ROOT \
        --slot-id $slot_id \
        --dry-run false"
    
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="$cmd" --quiet
}

# ==============================================================================
# MAIN
# ==============================================================================

# Verificar que dryrun existe
if [[ ! -f "$DRYRUN_PATH" ]]; then
    echo -e "${RED}ERROR: $DRYRUN_PATH no encontrado${NC}"
    exit 1
fi

# Verificar tenant root
if [[ ! -d "$TENANT_ROOT" ]]; then
    echo -e "${RED}ERROR: $TENANT_ROOT no encontrado${NC}"
    exit 1
fi

# Verificar gcloud auth
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 >/dev/null 2>&1; then
    echo -e "${RED}ERROR: gcloud no autenticado. Ejecuta: gcloud auth login${NC}"
    exit 1
fi

# PASO 1: Iniciar VM si necesario
echo -e "${BLUE}[1/4] Verificando e iniciando VM...${NC}"
if ! start_vm_if_needed; then
    echo -e "${RED}Fallo al iniciar VM${NC}"
    exit 1
fi

# PASO 2: Sincronizar assets
echo -e "${BLUE}[2/4] Sincronizando assets multimedia...${NC}"
sync_assets_to_vm

# PASO 3: Desplegar slots secuencialmente en modo REAL
echo -e "${BLUE}[3/4] Desplegando ${#SLOTS[@]} slots en modo REAL...${NC}"
echo ""

# Array para resultados
declare -A RESULTS

for slot in "${SLOTS[@]}"; do
    echo -e "${YELLOW}>>> Desplegando: $slot${NC}"
    
    if output=$(publish_slot_vm "$slot" 2>&1); then
        # Extraer Post ID del output
        post_id=$(echo "$output" | grep -oE 'Post ID: [a-zA-Z0-9_-]+' | sed 's/Post ID: //' | head -1)
        if [[ -z "$post_id" ]]; then
            post_id=$(echo "$output" | grep -oE '"id": "[^"]+"' | sed 's/"id": "//' | sed 's/"//' | head -1)
        fi
        if [[ -z "$post_id" ]]; then
            post_id="SUCCESS (no ID extracted)"
        fi
        RESULTS["$slot"]="$post_id"
        echo -e "${GREEN}✓ $slot -> $post_id${NC}"
    else
        RESULTS["$slot"]="FAILED"
        echo -e "${RED}✗ $slot -> FAILED${NC}"
        echo "$output"
    fi
    echo ""
    # Pequeña pausa entre slots para no saturar API
    sleep 2
done

# PASO 4: Detener VM
echo -e "${BLUE}[4/4] Deteniendo VM...${NC}"
stop_vm

# ==============================================================================
# TABLA FINAL DE RESULTADOS
# ==============================================================================
echo ""
echo -e "${BLUE}==============================================================${NC}"
echo -e "${BLUE}  RESULTADOS FINALES - 10 Post IDs Confirmados${NC}"
echo -e "${BLUE}==============================================================${NC}"
echo ""
printf "%-45s | %-20s | %-10s\n" "SLOT" "POST ID" "STATUS"
printf "%-45s-+-%-20s-+-%-10s\n" "---------------------------------------------" "--------------------" "----------"

success_count=0
for slot in "${SLOTS[@]}"; do
    post_id="${RESULTS[$slot]}"
    if [[ "$post_id" == "FAILED" ]]; then
        printf "%-45s | %-20s | ${RED}%-10s${NC}\n" "$slot" "$post_id" "FAILED"
    else
        printf "%-45s | %-20s | ${GREEN}%-10s${NC}\n" "$slot" "$post_id" "OK"
        ((success_count++))
    fi
done

echo ""
echo -e "${BLUE}==============================================================${NC}"
echo -e "Total: ${GREEN}$success_count${NC}/${#SLOTS[@]} slots desplegados exitosamente"
echo -e "${BLUE}==============================================================${NC}"

if [[ $success_count -eq ${#SLOTS[@]} ]]; then
    exit 0
else
    exit 1
fi
