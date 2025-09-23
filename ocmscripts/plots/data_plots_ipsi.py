"""Plots showing the LNL involvement observed in the dataset."""

from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Literal

from matplotlib.axes import Axes

import shared
from ocmscripts.config import PROCESSED_DATA_DIR, FIGURES_DIR
from lyscripts.plots import COLORS

dataset_clb_isb = pd.read_csv(PROCESSED_DATA_DIR / "dataset_isb_clb.csv", header=[0, 1, 2])
dataset_ksa = pd.read_csv(PROCESSED_DATA_DIR / "dataset_ksa.csv", header=[0, 1, 2])
dataset = pd.read_csv(PROCESSED_DATA_DIR / "dataset.csv", header=[0, 1, 2])


def main():
    
    # figure comparing ksa and clb/isb
    nrows, ncols = 1, 2
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=1.6,
            width=17,
            constrained_layout=False,
            tight_layout=True,
        )
    )

    #fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharey= True)

    isb_by_t = dataset_clb_isb[[*shared.get_lnl_cols("ipsi"), shared.COL.t_stage]].copy()
    isb_by_t.columns = isb_by_t.columns.droplevel([0,1])

    isb_by_t['t_stage'] = isb_by_t['t_stage'].map(
        {
            0: "T0-2",
            1: "T0-2",
            2: "T0-2",
            3: "T3-4",
            4: "T3-4",
        }
    )
    
    shared.group_and_plot(
        df=isb_by_t,
        column="t_stage",
        axes=axes[0],
        colors = [COLORS["blue"], COLORS["orange"]]
    )

    ksa_by_t = dataset_ksa[[*shared.get_lnl_cols("ipsi"), shared.COL.t_stage]].copy()
    ksa_by_t.columns = ksa_by_t.columns.droplevel([0,1])

    ksa_by_t['t_stage'] = ksa_by_t['t_stage'].map(
        {
            0: "T0-2",
            1: "T0-2",
            2: "T0-2",
            3: "T3-4",
            4: "T3-4",
        }
    )

    shared.group_and_plot(
        df=ksa_by_t,
        column="t_stage",
        axes=axes[1],
        colors = [COLORS["blue"], COLORS["orange"]]
    )

    axes[0].set_title("CLB & ISB", fontweight='bold')
    axes[0].set_ylabel("ipsilateral prevalence [%]")
    axes[1].set_title("KSA", fontweight='bold')
    axes[0].set_yticks(np.arange(0, 45, 5))
    plt.savefig(FIGURES_DIR / "data_ksa_vs_isb_clb_by_tstage.pdf", bbox_inches="tight")


    
if __name__ == "__main__":
    main()