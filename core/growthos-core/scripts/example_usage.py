#!/usr/bin/env python3
"""Example usage of the new Growth OS with multi-account support."""

import sys
from pathlib import Path

# Add the project root to the path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

from core.models import Piece
from storage.repositories import PieceRepository
from core.enums import EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad, DificultadProduccion, Reutilizable, BloqueadoCanon

def main():
    # Initialize repositories for different accounts
    data_dir = REPO_ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Create repository for account "user123"
    user1_repo = PieceRepository(data_dir / "pieces.csv", account_id="user123")
    
    # Create repository for account "user456"
    user2_repo = PieceRepository(data_dir / "pieces.csv", account_id="user456")
    
    # Create a piece for user123
    user1_piece = Piece(
        ID_Pieza="CNT-0001",
        Titulo="Contenido de Usuario 1",
        Personaje_Principal="Personaje A",
        Personajes_Secundarios="",
        Tipo_Contenido=TipoContenido.REEL,
        Plataforma=Plataforma.INSTAGRAM,
        Objetivo="Contenido para usuario 123",
        Hipotesis_ID="",
        Estado=EstadoPieza.IDEA,
        Prioridad=Prioridad.ALTA,
        Dificultad_Produccion=DificultadProduccion.BAJA,
        Es_Reutilizable=Reutilizable.SÍ,
        Fecha_Ultima_Publicacion=None,
        Fuente="",
        Formato="",
        Categoria=Categoria.HUMOR_MEME,
        Bloqueado_Canon=BloqueadoCanon.NO,
        Estado_Operacion_Normalizado="",
        Estado_Canon_Normalizado="",
        Asset_Ref_Confirmado="",
        Asset_Ref_Candidato="",
        Reconciliacion_Estado=None,
        Reconciliacion_Confianza=None,
        Reconciliacion_Fuente="",
        Reconciliacion_Nota="",
        Registro_Relacionado="",
        Drive_Reference_ID="",
        Meta_Publication_ID="",
        Meta_Permalink="",
        Asset_Set="",
        Asset_Ref="",
        Asset_Filename="",
        Drive_ID="",
        Estado_Canon=None,
        Estado_Produccion=None,
        Estado_Publicacion=None,
        Ultima_Sincronizacion="",
        Motivo_Revision_Normalizado=None,
        Personaje_Principal_Normalizado="",
        Personajes_Secundarios_Normalizados="",
        Rol_Narrativo="",
        Tipo_Humor_Normalizado="",
        Potencial_Etiquetado="",
        Confianza_Taxonomia="",
        Fuente_Taxonomia="",
        Nota_Taxonomia=""
    )
    
    # Create a piece for user456
    user2_piece = Piece(
        ID_Pieza="CNT-0002",
        Titulo="Contenido de Usuario 2",
        Personaje_Principal="Personaje B",
        Personajes_Secundarios="",
        Tipo_Contenido=TipoContenido.CARRUSEL,
        Plataforma=Plataforma.FACEBOOK,
        Objetivo="Contenido para usuario 456",
        Hipotesis_ID="",
        Estado=EstadoPieza.PENDIENTE_PRODUCCION,
        Prioridad=Prioridad.MEDIA,
        Dificultad_Produccion=DificultadProduccion.MEDIA,
        Es_Reutilizable=Reutilizable.NO,
        Fecha_Ultima_Publicacion=None,
        Fuente="",
        Formato="",
        Categoria=Categoria.NARRATIVA,
        Bloqueado_Canon=BloqueadoCanon.NO,
        Estado_Operacion_Normalizado="",
        Estado_Canon_Normalizado="",
        Asset_Ref_Confirmado="",
        Asset_Ref_Candidato="",
        Reconciliacion_Estado=None,
        Reconciliacion_Confianza=None,
        Reconciliacion_Fuente="",
        Reconciliacion_Nota="",
        Registro_Relacionado="",
        Drive_Reference_ID="",
        Meta_Publication_ID="",
        Meta_Permalink="",
        Asset_Set="",
        Asset_Ref="",
        Asset_Filename="",
        Drive_ID="",
        Estado_Canon=None,
        Estado_Produccion=None,
        Estado_Publicacion=None,
        Ultima_Sincronizacion="",
        Motivo_Revision_Normalizado=None,
        Personaje_Principal_Normalizado="",
        Personajes_Secundarios_Normalizados="",
        Rol_Narrativo="",
        Tipo_Humor_Normalizado="",
        Potencial_Etiquetado="",
        Confianza_Taxonomia="",
        Fuente_Taxonomia="",
        Nota_Taxonomia=""
    )
    
    # Save pieces to their respective accounts
    user1_repo.save(user1_piece)
    print(f"Saved piece for user123: {user1_piece.ID_Pieza}")
    
    user2_repo.save(user2_piece)
    print(f"Saved piece for user456: {user2_piece.ID_Pieza}")
    
    # Retrieve all pieces for each account
    user1_pieces = user1_repo.get_all()
    user2_pieces = user2_repo.get_all()
    
    print(f"\nUser123 pieces: {len(user1_pieces)}")
    for piece in user1_pieces:
        print(f"- {piece.ID_Pieza}: {piece.Titulo} ({piece.Estado or 'None'})")
    
    print(f"\nUser456 pieces: {len(user2_pieces)}")
    for piece in user2_pieces:
        print(f"- {piece.ID_Pieza}: {piece.Titulo} ({piece.Estado or 'None'})")
    
    # Show the actual CSV files that were created
    print(f"\nCSV files created:")
    for csv_file in data_dir.glob("pieces_*.csv"):
        print(f"- {csv_file.name}")

if __name__ == "__main__":
    main()
