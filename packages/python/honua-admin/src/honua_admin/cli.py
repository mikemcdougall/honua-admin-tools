"""
Command-line interface for Honua admin operations.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from . import HonuaAdminClient, ServiceConfiguration, BulkImportOptions
from .exceptions import HonuaAdminError

console = Console()


@click.group()
@click.version_option()
def cli():
    """Honua Admin CLI - Python tooling for Honua geospatial platform administration."""
    pass


@cli.group()
def config():
    """Configuration management commands."""
    pass


@config.command()
@click.option('--base-url', required=True, help='Honua API base URL')
@click.option('--api-key', required=True, help='API key for authentication')
@click.option('--config-file', default='~/.honua/config.yaml', help='Config file path')
def init(base_url: str, api_key: str, config_file: str):
    """Initialize CLI configuration."""
    config_path = Path(config_file).expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    config_data = {
        'base_url': base_url,
        'api_key': api_key,
    }

    with open(config_path, 'w') as f:
        yaml.dump(config_data, f, default_flow_style=False)

    console.print(f"✅ Configuration saved to {config_path}")


def load_config(config_file: str = '~/.honua/config.yaml') -> dict:
    """Load configuration from file."""
    config_path = Path(config_file).expanduser()

    if not config_path.exists():
        console.print("❌ Configuration file not found. Run 'honua-admin config init' first.")
        sys.exit(1)

    with open(config_path) as f:
        return yaml.safe_load(f)


@cli.group()
def service():
    """Service management commands."""
    pass


@service.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Preview changes without deploying')
def deploy(config_file: str, dry_run: bool):
    """Deploy a service from configuration file."""

    async def _deploy():
        config = load_config()

        with open(config_file) as f:
            service_config_data = yaml.safe_load(f)

        service_config = ServiceConfiguration(**service_config_data)

        if dry_run:
            console.print("🔍 Dry run mode - would deploy:")
            console.print_json(service_config.model_dump_json(indent=2))
            return

        async with HonuaAdminClient(
            base_url=config['base_url'],
            api_key=config['api_key']
        ) as client:
            try:
                with console.status(f"Deploying service '{service_config.name}'..."):
                    result = await client.create_service(service_config)

                console.print(f"✅ Service deployed successfully!")
                console.print(f"   Service ID: {result.get('id')}")
                console.print(f"   Service URL: {result.get('url')}")

            except HonuaAdminError as e:
                console.print(f"❌ Deployment failed: {e.message}")
                sys.exit(1)

    asyncio.run(_deploy())


@service.command('list')
def list_services():
    """List all services."""

    async def _list():
        config = load_config()

        async with HonuaAdminClient(
            base_url=config['base_url'],
            api_key=config['api_key']
        ) as client:
            try:
                services = await client.list_services()

                if not services:
                    console.print("No services found.")
                    return

                console.print(f"Found {len(services)} service(s):")
                for service in services:
                    console.print(f"  • {service.get('name')} ({service.get('id')})")

            except HonuaAdminError as e:
                console.print(f"❌ Failed to list services: {e.message}")
                sys.exit(1)

    asyncio.run(_list())


@cli.group()
def import_cmd():
    """Data import commands."""
    pass


@import_cmd.command('features')
@click.argument('service_id')
@click.argument('layer_id', type=int)
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', default='geojson', help='Data format (geojson, shapefile, csv)')
@click.option('--batch-size', default=1000, type=int, help='Batch size for imports')
@click.option('--show-progress', is_flag=True, help='Show progress bar')
def import_features(
    service_id: str,
    layer_id: int,
    file_path: str,
    format: str,
    batch_size: int,
    show_progress: bool,
):
    """Import features from file."""

    async def _import():
        config = load_config()

        options = BulkImportOptions(
            service_id=service_id,
            layer_id=layer_id,
            format=format,
            batch_size=batch_size,
        )

        async with HonuaAdminClient(
            base_url=config['base_url'],
            api_key=config['api_key']
        ) as client:
            try:
                if show_progress:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        TimeElapsedColumn(),
                        console=console,
                    ) as progress:
                        task = progress.add_task("Importing features...", total=100)

                        async for import_progress in client.import_features(options, file_path):
                            progress.update(
                                task,
                                completed=import_progress.percentage,
                                description=import_progress.message,
                            )

                        console.print(f"✅ Import completed successfully!")
                else:
                    # Simple import without progress
                    async for import_progress in client.import_features(options, file_path):
                        pass  # Just consume the iterator

                    console.print(f"✅ Import completed successfully!")

            except HonuaAdminError as e:
                console.print(f"❌ Import failed: {e.message}")
                sys.exit(1)

    asyncio.run(_import())


# Add the import command group to the CLI with a different name since 'import' is a keyword
cli.add_command(import_cmd, name='import')


def main():
    """Main CLI entry point."""
    cli()


if __name__ == '__main__':
    main()