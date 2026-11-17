"""Command line entry point: g11 demo and g11 train."""

from pathlib import Path

import torch
import typer
import yaml

from g11.app import DemoApp
from model.train import Trainer

cli = typer.Typer()


@cli.callback()
def _root():
    """SignVoice: LSM sign recognition converted to speech."""


@cli.command()
def demo():
    """Launch the one-page Gradio demo (offline)."""
    root = Path(__file__).resolve().parent.parent.parent
    DemoApp(root / "glossary" / "LSM.yaml").launch(server_name="127.0.0.1")


def _run_training(data):
    """Build the Trainer from the YAML config and run every LOSO fold."""
    torch.manual_seed(int(data["seed"]))
    trainer = Trainer(
        Path(data["clips"]),
        Path(data["out"]),
        [str(gloss) for gloss in data["glosses"]],
        epochs=int(data["epochs"]),
        lr=float(data["learning_rate"]),
        device=data["device"],
        seed=int(data["seed"]),
    )
    return trainer.run()


@cli.command()
def train(config: Path = Path("config/es_MX.yaml")):
    """Train the sign model per LOSO fold with a pre-registered config."""
    data = yaml.safe_load(config.read_text())
    out = _run_training(data)
    for signer, metrics in out.items():
        if signer == "latency_ms":
            print(f"latency_ms: {metrics:.3f}")
        else:
            print(f"signer {signer}: top1={metrics['top1']:.3f} f1_macro={metrics['f1_macro']:.3f}")


def run():
    """Run the CLI (entry point g11)."""
    cli()


if __name__ == "__main__":
    run()
