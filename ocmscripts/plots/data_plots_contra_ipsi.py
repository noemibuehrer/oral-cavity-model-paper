"""Plots showing the LNL involvement observed in the dataset."""

from lyscripts.plots import COLORS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shared

from ocmscripts.config import FIGURES_DIR, PROCESSED_DATA_DIR

dataset = pd.read_csv(PROCESSED_DATA_DIR / "dataset.csv", header=[0, 1, 2])


# contralateral involvement by T-category and Midline extension
def main():
    
    # figure comparing ksa and clb/isb
    nrows, ncols = 1, 1
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=1.7,
            width=12,
            constrained_layout=False,
            tight_layout=True,
        )
    )

    #fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharey = True, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/1.6*nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharey= True)
    
    lateral = dataset[dataset[shared.COL.midext] == 0]
    lateral_n0 = lateral[lateral['max_llh', 'ipsi'].sum(axis=1) == 0] 
    lateral_1 = lateral[lateral[shared.IPSI_LNLS].sum(axis=1) == 1]
    lateral_2 = lateral[lateral[shared.IPSI_LNLS].sum(axis=1) >= 2]

    midext = dataset[dataset[shared.COL.midext] == 1]
    midext_1 = midext[midext[shared.IPSI_LNLS].sum(axis=1) == 1]
    midext_0 = midext[midext['max_llh', 'ipsi'].sum(axis=1) == 0]
    
    mlateral_n0 = lateral_n0[shared.CONTRA_LNLS]['max_llh', 'contra'].mean(axis=0)
    mlateral_1 = lateral_1[shared.CONTRA_LNLS]['max_llh', 'contra'].mean(axis=0)
    mlateral_2 = lateral_2[shared.CONTRA_LNLS]['max_llh', 'contra'].mean(axis=0)
    mmidext_1 = midext_1[shared.CONTRA_LNLS]['max_llh', 'contra'].mean(axis=0)
    mmidext_0 = midext_0[shared.CONTRA_LNLS]['max_llh', 'contra'].mean(axis=0)
    
    pos = np.arange(len(mlateral_n0))
    axes.bar(
        x=pos-3 * 0.6/12,
        height=100 * mlateral_n0,
        color=COLORS["green"],
        label=f'lateralised; ipsi N0 ({len(lateral_n0)})',
        width=0.6,
        zorder = 5,
    )
    axes.bar(
        x=pos - 0.6/12,
        height=100 * mlateral_1,
        color=COLORS["blue"],
        label=f'lateralised; 1 ipsi LNL ({len(lateral_1)})',
        width=0.6,
        zorder = 4,

    )
    axes.bar(
        x=pos+0.6/12,
        height=100 * mlateral_2,
        color=COLORS["orange"],
        label=f'lateralised; ≥ 2 ipsi LNL ({len(lateral_2)})',
        width=0.6,
        zorder = 3,

    )
    axes.bar(
        x=pos+3 * 0.6/12,
        height=100 * mmidext_1,
        color=COLORS["red"],
        label=f'mid.ext.; 1 ipsi LNL ({len(midext_1)})',
        width=0.6,
        zorder = 2,
    )
    # axes.bar(
    #     x=pos+5 * 0.6/12,
    #     height=100 * mmidext_0,
    #     color=COLORS["green"],
    #     label=f'mid.ext.; ipsi N0({len(midext_0)})',
    #     width=0.6,
    #     zorder = 2,
    # )
    axes.grid(visible=True, axis='y', zorder=1)
    axes.set_ylabel("contralateral prevalence [%]")
    axes.legend()
    axes.set_xticks(pos, labels=['I', 'II', 'III', 'IV', 'V'])
    plt.savefig(FIGURES_DIR / "contra_by_inv_midext.pdf", bbox_inches="tight")


    
if __name__ == "__main__":
    main()