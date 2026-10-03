#!/usr/bin/env python3
"""
Instagram Publisher - Lógica reutilizable de publicación en Instagram
Usado por ig_scheduler.py multi-tenant
"""

import os
import base64
import requests
import time
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class IgPublisher:
    """Publicador de Instagram - encapsula todo el flujo de publicación"""
    
    def __init__(self, page_token: str, ig_id: str, imgbb_key: str, asset_root: Path):
        self.page_token = page_token
        self.ig_id = ig_id
        self.imgbb_key = imgbb_key
        self.asset_root = asset_root
    
    def find_asset(self, filename: str) -> Optional[Path]:
        # Use os.walk with followlinks=True to handle symlinks
        import os
        for root, dirs, files in os.walk(self.asset_root, followlinks=True):
            if filename in files:
                return Path(root) / filename
        return None

    # Old rglob method (kept for reference)
    def _find_asset_rglob(self, filename: str) -> Optional[Path]:
        """Busca archivo de asset"""
        matches = list(self.asset_root.rglob(filename))
        if not matches:
            return None
        if len(matches) > 1:
            logger.warning(f"Múltiples coincidencias para {filename}: {[str(m) for m in matches]}")
        return matches[0]
    
    def upload_to_imgbb(self, file_path: Path) -> str:
        """Sube imagen a imgbb y retorna URL pública"""
        logger.info(f"Subiendo a imgbb: {file_path.name}")
        with open(file_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        
        r = requests.post(
            'https://api.imgbb.com/1/upload',
            data={'key': self.imgbb_key, 'image': img_data},
            timeout=60
        ).json()
        
        if not r.get('success'):
            raise RuntimeError(f"Error imgbb: {r}")
        
        url = r['data']['url']
        logger.info(f"✅ imgbb: {url}")
        return url
    
    def create_media_container(self, image_url: str, caption: str) -> str:
        """Crea container de media en Instagram. Retorna creation_id."""
        url = f'https://graph.facebook.com/v19.0/{self.ig_id}/media'
        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.page_token,
        }
        r = requests.post(url, data=payload, timeout=60).json()
        
        if 'id' not in r:
            raise RuntimeError(f"Error creando media container: {r}")
        
        creation_id = r['id']
        logger.info(f"Container creado: {creation_id}")
        return creation_id
    
    def wait_for_container_ready(self, creation_id: str, max_wait: int = 60) -> bool:
        """Espera a que el container esté listo (status: Finished)"""
        url = f'https://graph.facebook.com/v19.0/{creation_id}?fields=id,status&access_token={self.page_token}'
        
        for i in range(max_wait // 5):
            time.sleep(5)
            r = requests.get(url, timeout=30).json()
            status = r.get('status', '')
            logger.info(f"Container status: {status}")
            if 'Finished' in status or 'ready' in status.lower():
                return True
            if 'error' in r or 'failed' in status.lower():
                raise RuntimeError(f"Container falló: {r}")
        
        raise TimeoutError(f"Container no listo después de {max_wait}s")
    
    def publish_media_container(self, creation_id: str) -> str:
        """Publica el container inmediatamente. Retorna post_id."""
        url = f'https://graph.facebook.com/v19.0/{self.ig_id}/media_publish'
        r = requests.post(url, data={'creation_id': creation_id, 'access_token': self.page_token}, timeout=60).json()
        
        if 'id' not in r:
            raise RuntimeError(f"Error publicando: {r}")
        
        post_id = r['id']
        logger.info(f"✅ Publicado en Instagram: {post_id}")
        return post_id
    
    def publish(self, media_filename: str, caption: str) -> str:
        """Flujo completo de publicación. Retorna post_id."""
        # 1. Encontrar asset
        asset_file = self.find_asset(media_filename)
        if not asset_file:
            raise FileNotFoundError(f"Asset no encontrado: {media_filename}")
        
        # 2. Subir a imgbb
        image_url = self.upload_to_imgbb(asset_file)
        
        # 3. Crear container
        creation_id = self.create_media_container(image_url, caption)
        
        # 4. Esperar ready
        self.wait_for_container_ready(creation_id)
        
        # 5. Publicar
        post_id = self.publish_media_container(creation_id)
        
        return post_id


def load_tenant_credentials(tenant_id: str) -> dict:
    """Carga credenciales desde tenants/<tenant_id>/.env"""
    from pathlib import Path
    
    env_path = Path(f'tenants/{tenant_id}/.env')
    if not env_path.exists():
        raise FileNotFoundError(f"No existe .env para tenant: {tenant_id}")
    
    creds = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                creds[k.strip()] = v.strip()
    
    required = ['FB_PAGE_ID', 'META_ACCESS_TOKEN', 'IMGBB_API_KEY']
    for r in required:
        if not creds.get(r):
            raise ValueError(f"Falta {r} en {env_path}")
    
    return creds


def get_meta_tokens(access_token: str, page_id: str) -> Tuple[str, str]:
    """Obtiene page_token e IG Business ID"""
    url = f'https://graph.facebook.com/v19.0/{page_id}?fields=access_token,instagram_business_account&access_token={access_token}'
    r = requests.get(url, timeout=30).json()
    page_token = r.get('access_token')
    ig_id = r.get('instagram_business_account', {}).get('id')
    
    if not page_token or not ig_id:
        raise ValueError(f"No se pudieron obtener tokens: {r}")
    
    return page_token, ig_id


def create_ig_publisher_for_tenant(tenant_id: str) -> IgPublisher:
    """Factory: crea IgPublisher configurado para un tenant"""
    creds = load_tenant_credentials(tenant_id)
    page_token, ig_id = get_meta_tokens(creds['META_ACCESS_TOKEN'], creds['FB_PAGE_ID'])
    asset_root = Path(f'tenants/{tenant_id}/assets')
    
    return IgPublisher(
        page_token=page_token,
        ig_id=ig_id,
        imgbb_key=creds['IMGBB_API_KEY'],
        asset_root=asset_root
    )
