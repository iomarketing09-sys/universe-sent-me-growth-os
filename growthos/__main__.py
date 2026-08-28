"""GrowthOS CLI entrypoint."""

import sys
from pathlib import Path

import typer
from rich.console import Console

from growthos.config import settings
from growthos.storage.database import init_db
from growthos.storage.csv_adapter import CSVAdapter
from growthos.storage.repositories import (
    PieceRepository,
    PublicationRepository,
    ExperimentRepository,
    CommunityRepository,
    MetricsSnapshotRepository,
    AssetAliasRepository,
)
from growthos.core.models import (
    Piece,
    Publication,
    Experiment,
    CommunityEngagement,
    MetricsSnapshot,
    AssetAlias,
)

app = typer.Typer(
    name="growthos",
    help="Growth OS - Operational CLI for Universe Sent Me content pipeline",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()


# =========================================================================
# Database Commands
# =========================================================================

@app.command("db")
def db_init(
    force: bool = typer.Option(False, "--force", "-f", help="Force reinitialize"),
):
    """Initialize SQLite database and run migrations."""
    if force:
        db_path = settings.sqlite_path
        if db_path.exists():
            console.print(f"[yellow]Removing existing database: {db_path}[/yellow]")
            db_path.unlink()

    console.print(f"[green]Initializing database at {settings.sqlite_path}[/green]")
    init_db()
    console.print("[green]Database initialized successfully[/green]")


# =========================================================================
# Import/Export Commands
# =========================================================================

@app.command("import-csv")
def import_csv(
    source: Path = typer.Argument(..., help="Path to CSV file"),
    entity: str = typer.Option("pieces", "--entity", "-e", help="Entity type to import"),
):
    """Import CSV file into SQLite database."""
    if not settings.USE_SQLITE:
        console.print("[yellow]USE_SQLITE is False - import skipped (set USE_SQLITE=true in .env)[/yellow]")
        raise typer.Exit(1)

    if not source.exists():
        console.print(f"[red]File not found: {source}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Importing {entity} from {source}[/green]")

    repo_map = {
        "pieces": (PieceRepository, Piece),
        "publications": (PublicationRepository, Publication),
        "experiments": (ExperimentRepository, Experiment),
        "community": (CommunityRepository, CommunityEngagement),
        "metrics": (MetricsSnapshotRepository, MetricsSnapshot),
        "aliases": (AssetAliasRepository, AssetAlias),
    }

    if entity not in repo_map:
        console.print(f"[red]Unknown entity: {entity}. Valid: {list(repo_map.keys())}[/red]")
        raise typer.Exit(1)

    repo_class, model = repo_map[entity]
    repo = repo_class()
    models = CSVAdapter.import_csv(model, source)

    for model in models:
        repo.save(model)

    console.print(f"[green]Imported {len(models)} {entity}[/green]")


@app.command("export-csv")
def export_csv(
    entity: str = typer.Argument(..., help="Entity type to export"),
    output: Path = typer.Option(..., "--output", "-o", help="Output CSV path"),
):
    """Export entity from SQLite to CSV."""
    if not settings.USE_SQLITE:
        console.print("[yellow]USE_SQLITE is False - export skipped (set USE_SQLITE=true in .env)[/yellow]")
        raise typer.Exit(1)

    repo_map = {
        "pieces": (PieceRepository, Piece),
        "publications": (PublicationRepository, Publication),
        "experiments": (ExperimentRepository, Experiment),
        "community": (CommunityRepository, CommunityEngagement),
        "metrics": (MetricsSnapshotRepository, MetricsSnapshot),
        "aliases": (AssetAliasRepository, AssetAlias),
    }

    if entity not in repo_map:
        console.print(f"[red]Unknown entity: {entity}. Valid: {list(repo_map.keys())}[/red]")
        raise typer.Exit(1)

    repo_class, model = repo_map[entity]
    repo = repo_class()
    models = repo.get_all()

    CSVAdapter.export_piece_csv(models, output) if entity == "pieces" else CSVAdapter.export_csv(models, output, model)
    console.print(f"[green]Exported {len(models)} {entity} to {output}[/green]")


# =========================================================================
# Validate Commands
# =========================================================================

@app.command("validate-csv")
def validate_csv(
    source: Path = typer.Argument(..., help="Path to original CSV"),
    exported: Path = typer.Argument(..., help="Path to exported CSV"),
):
    """Compare two CSV files for semantic equivalence."""
    console.print(f"[green]Comparing {source} vs {exported}[/green]")

    result = CSVAdapter.compare_semantic(source, exported)

    if result["match"]:
        console.print("[green]✓ Semantic match![/green]")
    else:
        console.print("[red]✗ Semantic mismatch[/red]")
        console.print(f"  Original rows: {result['original_rows']}")
        console.print(f"  Exported rows: {result['exported_rows']}")
        if result["id_mismatch"]:
            console.print(f"  ID mismatches: {result['id_mismatch']}")
        if result["field_mismatches"]:
            for field, mismatches in result["field_mismatches"].items():
                console.print(f"  {field}: {len(mismatches)} mismatches")
                for m in mismatches[:5]:
                    console.print(f"    Row {m['row']}: '{m['original']}' vs '{m['exported']}'")
        if result["errors"]:
            for err in result["errors"]:
                console.print(f"  Error: {err}")

    raise typer.Exit(0 if result["match"] else 1)


# =========================================================================
# Canon Check (placeholder for Phase 2)
# =========================================================================

@app.command("canon")
def canon_check(
    piece_id: str = typer.Argument(..., help="Piece ID to check (CNT-####)"),
):
    """Check canon status for a piece (placeholder)."""
    console.print(f"[yellow]Canon check for {piece_id} - not implemented yet (Phase 2)[/yellow]")


# =========================================================================
# Main
# =========================================================================

def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
