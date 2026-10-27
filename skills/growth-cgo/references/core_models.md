# Core Models Reference - GrowthOS Core Package

Ubicación: `core/growthos-core/core/models.py`

---

## Modelos Principales

### Piece (Pieza de Contenido)
```python
class Piece(BaseModel):
    ID_Pieza: str                    # CNT-0001, FB-0001, HB-001
    Titulo: str = ""
    Personaje_Principal: str = ""    # @char_USM_universe, @char_USM_wilfred, etc.
    Personajes_Secundarios: str = ""
    Tipo_Contenido: Optional[str]    # REEL_MEME_ADAPTADO, REEL_NARRATIVO, etc.
    Plataforma: Optional[str]        # INSTAGRAM, FACEBOOK, MULTI, REELS, STORIES
    Objetivo: str = ""
    Hipotesis_ID: str = ""
    Estado: Optional[str]            # IDEA, EN_PRODUCCION, ASSET_LISTO, PROGRAMADO, PUBLICADO
    Prioridad: Optional[str]         # ALTA, MEDIA, BAJA
    Dificultad_Produccion: Optional[str]  # ALTA, MEDIA, BAJA
    Es_Reutilizable: Optional[str]   # SI, NO
    Fecha_Ultima_Publicacion: Optional[date]
    # ... 40+ campos más (ver models.py)
```

### Publication (Publicación)
```python
class Publication(BaseModel):
    ID_Publicacion: str              # PUB-0001
    ID_Pieza: str                    # CNT-0001
    Tenant_ID: str                   # universe, flexi, etc.
    Plataforma: str                  # INSTAGRAM, FACEBOOK
    Fecha_Publicacion: datetime
    Meta_Publication_ID: str = ""    # ID de Meta Graph API
    Metricas: dict = {}              # clicks, engagement, reach, etc.
    Estado: str = "PUBLICADO"
```

### Experiment (Experimento)
```python
class Experiment(BaseModel):
    ID_Experimento: str              # EXP-001
    Hipotesis_ID: str
    Tenant_ID: str
    Variante_A: dict                 # Config variante A
    Variante_B: dict                 # Config variante B
    Metrica_Primaria: str            # CTR, engagement, conversion
    Estado: str                      # DISENO, EN_CURSO, FINALIZADO
    Resultado: Optional[dict]
```

### Deal (Revenue Lite)
```python
class Deal(BaseModel):
    Deal_ID: str                     # D-0001
    tenant_id: str
    Cliente: str
    Lead_Source: LeadSource          # WHATSAPP, META_ADS, GBP, ORGANIC, REFERRAL
    Linea: FunnelLine                # VENTA_DIRECTA, B2B, CAPACITACION
    Monto_Cotizado: float
    Costo_Produccion: float
    Costo_Adquisicion: float         # CAC
    Etapa: DealStage                 # NUEVO, EN_CONTACTO, COTIZADO, CERRADO_GANADO, CERRADO_PERDIDO
    Fecha_Creacion: datetime
    Fecha_Cierre: Optional[datetime]
    Monto_Final: Optional[float]
```

### CommunityEngagement
```python
class CommunityEngagement(BaseModel):
    ID_Engagement: str
    Tenant_ID: str
    Plataforma: str
    Tipo: str                        # COMMENT, REACTION, SHARE, DM
    Contenido: str
    Sentimiento: str                 # POSITIVE, NEUTRAL, NEGATIVE
    Requiere_Respuesta: bool
    Respondido: bool
    Fecha: datetime
```

### MetricsSnapshot
```python
class MetricsSnapshot(BaseModel):
    ID_Snapshot: str
    Tenant_ID: str
    Fecha: date
    Plataforma: str
    Seguidores: int
    Alcance: int
    Impresiones: int
    Engagement: int
    Clicks: int
    Video_Vistas: int
```

### AssetAlias
```python
class AssetAlias(BaseModel):
    Asset_ID: str
    Tenant_ID: str
    Filename: str
    Aliases: List[str]               # Nombres alternativos
    Tags: List[str]
    Confirmado: bool
```

---

## Enums Clave

```python
# Estado de pieza
class EstadoPieza(str, Enum):
    IDEA = "IDEA"
    EN_PRODUCCION = "EN_PRODUCCION"
    ASSET_LISTO = "ASSET_LISTO"
    PROGRAMADO = "PROGRAMADO"
    PUBLICADO = "PUBLICADO"
    ARCHIVADO = "ARCHIVADO"

# Plataformas
class Plataforma(str, Enum):
    INSTAGRAM = "INSTAGRAM"
    FACEBOOK = "FACEBOOK"
    MULTI = "MULTI"
    REELS = "REELS"
    STORIES = "STORIES"
    WHATSAPP = "WHATSAPP"
    TIKTOK = "TIKTOK"
    YOUTUBE = "YOUTUBE"

# Tipo de contenido
class TipoContenido(str, Enum):
    REEL_MEME_ADAPTADO = "REEL_MEME_ADAPTADO"
    REEL_NARRATIVO = "REEL_NARRATIVO"
    REEL_EDUCATIVO = "REEL_EDUCATIVO"
    CARRUSEL_PRODUCTO = "CARRUSEL_PRODUCTO"
    STORY_SECUENCIAL = "STORY_SECUENCIAL"
    IMAGE_STATIC = "IMAGE_STATIC"

# Lead Source (Revenue)
class LeadSource(str, Enum):
    WHATSAPP = "whatsapp"
    META_ADS = "meta_ads"
    GBP = "gbp"
    ORGANIC = "organic"
    REFERRAL = "referral"

# Deal Stage
class DealStage(str, Enum):
    NUEVO = "nuevo"
    EN_CONTACTO = "en_contacto"
    COTIZADO = "cotizado"
    CERRADO_GANADO = "cerrado_ganado"
    CERRADO_PERDIDO = "cerrado_perdido"

# Funnel Line
class FunnelLine(str, Enum):
    VENTA_DIRECTA = "venta_directa"
    B2B = "b2b"
    CAPACITACION = "capacitacion"
    OTRO = "otro"
```

---

## Repositories (Storage Layer)

Ubicación: `core/growthos-core/storage/repositories.py`

| Repository | Modelo | Métodos Clave |
|------------|--------|---------------|
| `PieceRepository` | Piece | `read_all()`, `save()`, `get_all()` |
| `PublicationRepository` | Publication | `read_all()`, `save()` |
| `ExperimentRepository` | Experiment | `read_all()`, `save()` |
| `DealRepository` | Deal | `read_all()`, `save()`, `get_all()` |
| `CommunityEngagementRepository` | CommunityEngagement | `read_all()`, `save()` |
| `MetricsSnapshotRepository` | MetricsSnapshot | `read_all()`, `save()` |
| `AssetAliasRepository` | AssetAlias | `read_all()`, `save()` |

**Patrón**: Todos usan `CSVAdapter` con aislamiento por `account_id` (tenant).

---

## Uso Básico

```python
from growthos.core.models import Piece, Deal
from growthos.storage.repositories import PieceRepository, DealRepository
from pathlib import Path

# Pieces
piece_repo = PieceRepository(Path("data/pieces.csv"), account_id="universe")
pieces = piece_repo.read_all()
new_piece = Piece(ID_Pieza="CNT-9999", Titulo="Test", ...)
piece_repo.save(new_piece)

# Deals (Revenue Lite)
deal_repo = DealRepository(Path("tenants/flexi/data/deals_flexi.csv"), account_id="flexi")
deal = Deal(Deal_ID="D-0001", tenant_id="flexi", ...)
deal_repo.save(deal)
report = deal_repo.get_all()  # Para reportes
```

---

*Actualizado: 15 Octubre 2026*
