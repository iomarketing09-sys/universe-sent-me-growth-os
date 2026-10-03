# New Growth OS

A fresh implementation of the Growth OS system, built from scratch using the previous project as reference.

## Structure

- `core/` - Core models and enums
- `storage/` - Storage adapters and repositories
- `scripts/` - Utility scripts
- `tests/` - Test suite
- `data/` - Data storage (CSV files)

## Core Components

### Enums (`core/enums.py`)
Defines all enumerated types used throughout the system:
- EstadoPieza: Piece states (Idea, Pendiente de Producción, etc.)
- Plataforma: Social media platforms
- TipoContenido: Content types
- Categoria: Content categories
- Prioridad: Priority levels
- DificultadProduccion: Production difficulty
- Reutilizable: Reusability flag
- BloqueadoCanon: Canon blocking status
- EstadoCanon: Canon state
- EstadoProduccion: Production state
- EstadoPublicacion: Publication state
- MotivoRevision: Revision reasons
- ReconciliacionEstado: Reconciliation state
- ReconciliacionConfianza: Reconciliation confidence

### Models (`core/models.py`)
Pydantic models representing the domain entities:
- Piece: Main content item
- Publication: Publication record
- Experiment: Experiment tracking
- CommunityEngagement: Social media interactions
- MetricsSnapshot: Analytics data
- AssetAlias: Asset management

### Storage (`storage/`)
- `csv_adapter.py`: CSV-based data persistence with enum handling
- `repositories.py`: Repository pattern implementation for each model type with multi-account support

## Multi-Account Support

The system now supports handling multiple accounts separately through account-scoped storage:

### How It Works
Each repository can be initialized with an optional `account_id` parameter. When provided:
- Storage files are automatically named with the account ID suffix (e.g., `pieces_user123.csv`)
- Accounts are completely isolated - each has its own set of CSV files
- No account filtering is needed at the query level since data is physically separated

### Usage Example
```python
from storage.repositories import PieceRepository
from pathlib import Path

# Initialize repositories for different accounts
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Account-specific repositories
user1_repo = PieceRepository(data_dir / "pieces.csv", account_id="user123")
user2_repo = PieceRepository(data_dir / "pieces.csv", account_id="user456")

# Each repository operates on its own separate file:
# user1_repo -> pieces_user123.csv
# user2_repo -> pieces_user456.csv
```

### Benefits
- **Complete isolation**: Accounts don't share or see each other's data
- **Simple backup/migration**: Copy or move account-specific files
- **No query overhead**: No need to filter by account_id in every query
- **Easy scaling**: New accounts automatically get their own storage files

## Usage

See scripts/ for examples of how to use the repositories.

## Development

This is a fresh implementation designed to be simple and maintainable.
It uses CSV files for storage, making it easy to backup and inspect data.

## Notes

This implementation intentionally avoids copying code from the previous version.
Instead, it reimplements the core concepts based on understanding gained from the original project.
