# Soporte Multi‑Cuenta

## Cómo funciona
Cada repositorio puede inicializarse con un parámetro opcional `account_id`. Cuando se proporciona:
- Los archivos de almacenamiento se nombran automáticamente con el sufijo del ID de cuenta (por ejemplo, `pieces_user123.csv`).
- Las cuentas están completamente aisladas: cada una tiene su propio conjunto de archivos CSV.
- No es necesario filtrar por `account_id` a nivel de consulta porque los datos están físicamente separados.

## Beneficios
- **Aislamiento total**: Las cuentas no comparten ni ven los datos de otras.
- **Respaldos y migraciones simples**: Copiar o mover los archivos específicos de una cuenta.
- **Sin sobrecarga de consultas**: No es necesario incluir `account_id` en cada consulta.
- **Escalabilidad fácil**: Nuevas cuentas reciben automáticamente sus propios archivos de almacenamiento.

## Ejemplo de uso
```python
from storage.repositories import PieceRepository
from pathlib import Path

# Inicializar repositorios para diferentes cuentas
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Repositorios específicos por cuenta
user1_repo = PieceRepository(data_dir / "pieces.csv", account_id="user123")
user2_repo = PieceRepository(data_dir / "pieces.csv", account_id="user456")

# Cada repositorio opera en su propio archivo separado:
# user1_repo -> pieces_user123.csv
# user2_repo -> pieces_user456.csv
```
