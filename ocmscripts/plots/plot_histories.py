from pathlib import Path

from loguru import logger
from lyscripts.plots import BetaPosterior, Histogram, draw
from matplotlib import pyplot as plt
import pandas as pd
import typer

from ocmscripts.config import FIGURES_DIR, HISTORIES_DIR


def history(
    history_file: Path = HISTORIES_DIR / "simple.csv",
    output_path: Path = FIGURES_DIR / "history.png",
) -> None:
    """Plot the sampling history."""
    history = pd.read_csv(history_file)
    logger.info(f"Loaded sampling history from {history_file = }")

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

    axes[0].plot(history.index, history.acor_times)
    axes[0].set_ylabel("Autocorrelation\ntime")

    axes[1].plot(history.index, history.accept_fracs)
    axes[1].set_ylabel("Acceptance\nfraction")

    axes[2].plot(history.index, history.max_log_probs)
    axes[2].set_xlabel("Iteration")
    axes[2].set_ylabel("Max\nlog probability")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    logger.success(f"Saved plot to {output_path = }")

def main():
    """Plot history of sampling."""

    # Input and output directories
    plots_dir = HISTORIES_DIR
    output_dir = FIGURES_DIR / "history_plots"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all CSV files in plots directory
    csv_files = list(plots_dir.glob("*.csv"))
    
    if not csv_files:
        logger.warning(f"No CSV files found in {plots_dir}")
        return
    
    logger.success(f"Found {len(csv_files)} CSV files to process")
    
    # Process each CSV file
    for csv_file in csv_files:        
        history_path = plots_dir / f"{csv_file}"
        output_path = output_dir / f"{csv_file.stem}.pdf"
        
        history(
            history_file=history_path,
            output_path=output_path
        )

if __name__ == "__main__":
    main()