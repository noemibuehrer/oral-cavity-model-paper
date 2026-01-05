"""Plots showing the LNL involvement observed in the dataset."""

from lyscripts.plots import COLORS
import matplotlib.pyplot as plt
import pandas as pd
import shared

from ocmscripts.config import FIGURES_DIR, PROCESSED_DATA_DIR

dataset = pd.read_csv(PROCESSED_DATA_DIR / "dataset.csv", header=[0, 1, 2])


# contralateral involvement by T-category and Midline extension
def main():
    
    # figure comparing ksa and clb/isb
    nrows, ncols = 1, 2
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=1.3,
            width=17,
            constrained_layout=False,
            tight_layout=True,
        )
    )

    #fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharey= True)
    
    contra_by_t = dataset[[*shared.get_lnl_cols("contra"), shared.COL.t_stage]].copy()
    contra_by_t.columns = contra_by_t.columns.droplevel([0,1])

    contra_by_t['t_stage'] = contra_by_t['t_stage'].map(
        {
            0: "T1-2",
            1: "T1-2",
            2: "T1-2",
            3: "T3-4",
            4: "T3-4",
        }
    )

    contra_by_ext = dataset[[*shared.get_lnl_cols("contra"), shared.COL.midext]].copy()
    contra_by_ext.columns = contra_by_ext.columns.droplevel([0,1])
    contra_by_ext['extension'] = contra_by_ext['extension'].map(
        {
            0: False,
            1: True,
        }
    )
    
    shared.group_and_plot(
        df=contra_by_t,
        column="t_stage",
        axes=axes[0],
        colors = [COLORS["blue"], COLORS["orange"]]
    )

    shared.group_and_plot(
        df=contra_by_ext,
        column="extension",
        axes=axes[1],
        colors = [COLORS["green"], COLORS["red"]]
    )


    axes[0].set_title("T-category", fontweight='bold')
    axes[1].set_title("Midline extension", fontweight='bold')
    axes[0].set_ylabel("contralateral prevalence [%]")


    plt.savefig(FIGURES_DIR / "contra_by_t_and_midext.pdf", bbox_inches="tight")


    
if __name__ == "__main__":
    main()