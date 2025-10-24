import h5py
import matplotlib.pyplot as plt
import numpy as np
import shared
import ast
import json

from lyscripts.plots import COLORS, Histogram, draw
from lyscripts.configs import ScenarioConfig, DiagnosisConfig, InvolvementConfig

from ocmscripts.config import FIGURES_DIR, RISKS_DIR, REPORTS_DIR

def main():
    """Plot figure."""
    nrows, ncols = 3, 1
    plt.rcParams.update(shared.get_fontsizes())
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            width=17/2,
            aspect_ratio=2.5,
        )
    )

    not_plot = ["late; mid-ext, ipsi: I,II,III,IV; contra: N0"]

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True)

    contents = {"III": [], "IV": [], "V": []}
    mean_lists = {"III": [], "IV": [], "V": []}
    mean_risks = {"I": {}, "II": {}, "III": {}, "IV": {}, "V": {}}
    counter = {"III": 0, "IV": 0, "V": 0}
    colors = [COLORS["green"], COLORS["blue"], COLORS["orange"], COLORS["red"], "#6821ab"]

    output_path = FIGURES_DIR / "risks_ipsi.pdf"

    with h5py.File(RISKS_DIR / "midline_risks_ipsi.hdf5", "r") as h5file:
        for dset in h5file.values():
            scenario = shared.get_scenario(dict(dset.attrs))
            label = shared.get_label(scenario)
            for_subplot = list(scenario.involvement.ipsi.keys()).pop()
            mean_risks[for_subplot].update({label: [dset[:].mean(), dset[:].std()]})
            try: 
                mean_lists[for_subplot].append(dset[:].mean())
            except KeyError:
                continue
    
    with open(REPORTS_DIR / "risks/mean_risks_ipsi.json", mode="w", encoding="utf-8") as risks_file:
        json.dump(mean_risks, risks_file)

    indices = {}
    for lnl, means in mean_lists.items():
        indices[lnl] = np.argsort(np.argsort(means))
    
    with h5py.File(RISKS_DIR / "midline_risks_ipsi.hdf5", "r") as h5file:
        for dset in h5file.values():
            scenario = shared.get_scenario(dict(dset.attrs))
            label = shared.get_label(scenario)
            if label in not_plot:
                continue
            for_subplot = list(scenario.involvement.ipsi.keys()).pop()
            try: 
                c = counter[for_subplot]
            except KeyError:
                continue
            counter[for_subplot] += 1
            contents[for_subplot].append(
                Histogram(
                    raw_values=dset[:],
                    kwargs={
                        "label": shared.get_label(scenario),
                        "color": colors[indices[for_subplot][c]],
                    },
                )
            )
    
    index = np.argsort(mean_lists['III'])
    backup = contents['III'].copy()
    contents['III'] = [backup[i] for i in index]

    for ax, (lnl, content) in zip(axes, contents.items()):
        draw(ax, content, xlims=(0,10), hist_kwargs={"bins": 60})
        ax.set_ylabel(f"Ipsi LNL {lnl}", fontweight = "bold")
        ax.set_yticks([])
        ax.legend()
    axes[2].set_ylim(0, 1.0)
    plt.savefig(output_path)

if __name__ == "__main__":
    main()