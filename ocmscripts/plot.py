from pathlib import Path

from loguru import logger
from lyscripts.plots import BetaPosterior, Histogram, draw
from matplotlib import pyplot as plt
import pandas as pd
import typer

from ocmscripts.config import FIGURES_DIR, HISTORIES_DIR, PREVALENCES_DIR, SAMPLES_DIR

app = typer.Typer()


@app.command()
def history(
    history_file: Path = HISTORIES_DIR / "simple.csv",
    output_path: Path = FIGURES_DIR / "history.png",
) -> None:
    """Plot the sampling history."""
    history = pd.read_csv(history_file)
    logger.info(f"Loaded sampling history from {history_file = }")

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

    axes[0].plot(history.index, history.acor_times)
    axes[0].set_ylabel("Autocorrelation time")

    axes[1].plot(history.index, history.accept_fracs)
    axes[1].set_ylabel("Acceptance fraction")

    axes[2].plot(history.index, history.max_log_probs)
    axes[2].set_xlabel("Iteration")
    axes[2].set_ylabel("Max log probability")

    plt.savefig(output_path, bbox_inches="tight")
    logger.success(f"Saved plot to {output_path = }")


@app.command()
def prevalences(
    samples_file: Path = SAMPLES_DIR / "base_integration.hdf5",
    prevalences_file: Path = PREVALENCES_DIR / "base_integration.hdf5",
    output_path: Path = FIGURES_DIR / "base_prevalences.png",
) -> None:
    """Plot the overall prevalence estimates."""
    fig, axes = plt.subplots(nrows=1, ncols=1)
    content = []
    content.append(
        Histogram.from_hdf5(
            filename = prevalences_file,
            dataname = "001",
        )
    )
    content.append(
        BetaPosterior.from_hdf5(
            filename = prevalences_file,
            dataname = "001"
        )
    )
    draw(
        axes = axes,
        contents = content,
    )
    plt.savefig(output_path, bbox_inches="tight")
    



if __name__ == "__main__":
    app()