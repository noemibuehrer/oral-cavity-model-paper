"""Plots showing the LNL involvement observed in the dataset."""

from lyscripts.plots import COLORS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shared

from ocmscripts.config import FIGURES_DIR, PROCESSED_DATA_DIR

dataset = pd.read_csv(PROCESSED_DATA_DIR / "dataset.csv", header=[0, 1, 2])

def main():
    
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

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharey= True)

    data_by_t = dataset[[*shared.get_lnl_cols("ipsi"), shared.COL.t_stage, shared.COL.inst]].copy()
    data_by_t.columns = data_by_t.columns.droplevel([0,1])

    data_by_t['institution'] = data_by_t['institution'].map(
        {
            "Inselspital Bern": "ISB",
            "Centre Léon Bérard": "CLB",
            "Kantonsspital Aarau": "KSA"
        }
    )

    # Add combined data with "All" institution
    data_combined = data_by_t.copy()
    data_combined['institution'] = "All"
    data_by_t_with_all = pd.concat([data_by_t, data_combined], ignore_index=True)

    # Split by T-stage with the combined data
    data_by_t_early = data_by_t_with_all.loc[data_by_t_with_all['t_stage'] < 3].copy()
    data_by_t_late = data_by_t_with_all.loc[data_by_t_with_all['t_stage'] >= 3].copy()

    data_by_t_early = data_by_t_early.drop(['t_stage'], axis=1)
    data_by_t_late = data_by_t_late.drop(['t_stage'], axis=1)
    
    shared.group_and_plot(
        df = data_by_t_early,
        column="institution",
        axes=axes[0],
        colors=[COLORS["red"], COLORS["green"], COLORS["blue"], [COLORS["orange"]]]
    )

    shared.group_and_plot(
        df = data_by_t_late,
        column="institution",
        axes=axes[1],
        colors=[COLORS["red"], COLORS["green"], COLORS["blue"], [COLORS["orange"]]]
    )

    axes[0].set_title("early T-category (T0-2)", fontweight='bold')
    axes[0].set_ylabel("ipsilateral prevalence [%]")
    axes[1].set_title("advanced T-category (T3-4)", fontweight='bold')
    axes[0].set_yticks(np.arange(0, 45, 5))
    plt.savefig(FIGURES_DIR / "data_ipsi_by_tstage.pdf", bbox_inches="tight")
    
if __name__ == "__main__":
    main()