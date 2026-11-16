"""Command line entry point: g11 demo."""

from pathlib import Path

import typer

from g11.app import DemoApp

cli = typer.Typer()


@cli.callback()
def _root():
    """SignVoice: LSM sign recognition converted to speech."""


@cli.command()
def demo():
    """Launch the one-page Gradio demo (offline)."""
    root = Path(__file__).resolve().parent.parent.parent
    DemoApp(root / "glossary" / "LSM.yaml").launch(server_name="127.0.0.1")


def run():
    """Run the CLI (entry point g11)."""
    cli()


if __name__ == "__main__":
    run()
