from pathlib import Path

from loguru import logger
from lyscripts.plots import COLORS
from matplotlib import pyplot as plt
import pandas as pd
import typer
import numpy as np
import corner

import emcee
import shared

from ocmscripts.config import FIGURES_DIR, HISTORIES_DIR, SAMPLES_DIR

LABELS = ['b$_1^{i}$', 'b$_2^{i}$', 'b$_3^{i}$', 'b$_4^{i}$', 'b$_5^{i}$',r'b$_1^{c, \epsilon = \text{False}}$', r'b$_2^{c , \epsilon = \text{False}}$', r'b$_3^{c, \epsilon = \text{False}}$', r'b$_4^{c, \epsilon = \text{False}}$', r'b$_5^{c, \epsilon = \text{False}}$', r'$\alpha$', r't$_{2\rightarrow1}$', r't$_{2\rightarrow3}$', r't$_{3\rightarrow4}$', r't$_{3\rightarrow5}$', 'p$_{late}$', r'p$_{\epsilon}$']

def trace_plot(
        samples: np.ndarray,
        output_path: Path = FIGURES_DIR / "mcmc_traceplots.pdf"
) -> None:
    """Plot the MCMC trace plots for all model parameters."""
    nrows, ncols = 6, 3
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=4.0,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows), sharex=True)
    rows, cols = axes.shape

    for i in range(17):
        row, col = divmod(i, cols)
        axis = axes[row, col]
        axis.plot(samples[:, :, i] * 100, color=COLORS['blue'], alpha=0.1)
        axis.set_title(LABELS[i])

        if col == 0:
            axis.set_ylabel('param. estimate [%]')
        else:
            axis.set_ylabel('')

        show_bottom_axis = (row == rows - 1 and col < cols - 1) or (row == rows - 2 and col == cols - 1)
        if show_bottom_axis:
            axis.set_xlabel('steps (thinned)')
            axis.tick_params(labelbottom=True)
        else:
            axis.set_xlabel('')
            axis.tick_params(labelbottom=False)

    fig.delaxes(axes[-1, -1])
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    logger.success(f"Saved trace plots to {output_path=}")

def history(
    history_file: Path = HISTORIES_DIR / "simple.csv",
    output_path: Path = FIGURES_DIR / "history.png",
) -> None:
    """Plot the sampling history."""
    history = pd.read_csv(history_file)
    logger.info(f"Loaded sampling history from {history_file = }")

    nrows, ncols = 1, 2
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=3.0,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/3.0*nrows), sharex=True)
    # rows, cols = axes.shape
    # fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(8,2.5))

    axes[0].plot(history.steps, history.acor_times, label = 'autocorrelation time')
    axes[0].plot(history.steps, history.steps/50,'r--', label = 'trust threshold')
    axes[0].set_ylabel("estimate [steps]")
    axes[0].set_xlabel("steps")
    axes[0].set_title("Estimated autocorrelation time", fontweight='bold')
    axes[0].grid(axis='y')
    axes[0].ticklabel_format(axis='x', style='sci')

    axes[1].plot(history.steps, history.accept_fracs * 100)
    axes[1].set_ylabel("fraction [%]")
    axes[1].set_xlabel("steps")
    axes[1].set_title("Average acceptance fraction of walkers", fontweight='bold')
    axes[1].grid(axis='y')
    axes[1].ticklabel_format(axis='x', style='sci', scilimits=(0,0))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    logger.success(f"Saved plot to {output_path = }")

def main():
    """Plot MCMC diagnostics such as trace plots and corner plots."""

    # Input and output directories
    samples_file =  SAMPLES_DIR / "midline+II_I+III_V.hdf5"
    history_file = HISTORIES_DIR / "midline+II_I+III_V.csv"

    # Read samples
    backend = emcee.backends.HDFBackend(samples_file, name='mcmc', read_only=True)
    samples = backend.get_chain(flat=False, discard=0, thin=1)

    # Trace plot
    trace_plot(samples, FIGURES_DIR / "mcmc_traceplot.pdf")

    # Burn-in history plot
    history(history_file, FIGURES_DIR / "burnin_history.pdf")
    logger.success(f"Saved burn-in plot to {FIGURES_DIR / 'burnin_history.pdf'}")

    # Corner plot
    figure = corner.corner(samples.reshape(-1, 17)*100, titles = LABELS, color = COLORS['blue'], hist_kwargs={'histtype':'bar'}, title_quantiles=[0.025, 0.5, 0.975], show_titles = True, labels = LABELS, label_kwargs={'fontsize': 25}, title_kwargs={'fontsize': 18})
    figure.savefig(FIGURES_DIR / "mcmc_cornerplot.pdf", bbox_inches='tight')
    logger.success(f"Saved corner plot to {FIGURES_DIR / 'mcmc_cornerplot.pdf'}")


if __name__ == "__main__":
    main()
