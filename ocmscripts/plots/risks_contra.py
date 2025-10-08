import h5py
import matplotlib.pyplot as plt
import numpy as np
import shared
import ast
import json

from lyscripts.plots import COLORS, Histogram, draw
from lyscripts.configs import ScenarioConfig, DiagnosisConfig, InvolvementConfig

from ocmscripts.config import FIGURES_DIR, RISKS_DIR, REPORTS_DIR

def get_scenario(scenario_dict: dict[str]) -> ScenarioConfig:
    """Create a ScenarioConfig from dictionary of the HDF5 file attributes."""
    scenario_dict['diagnosis'] = DiagnosisConfig.model_validate(ast.literal_eval(scenario_dict['diagnosis']))
    scenario_dict['involvement'] = InvolvementConfig.model_validate(ast.literal_eval(scenario_dict['involvement']))
    scenario_config = ScenarioConfig.model_validate(scenario_dict)
    return(scenario_config)

def get_diag_label(diagnosis: DiagnosisConfig) -> str:
    """Get the diagnosis label."""
    label = ""

    ipsi_positive = [
        lnl for lnl, status in diagnosis.ipsi.get("CT", {}).items() if status
    ]
    if len(ipsi_positive) > 0:
        label += "ipsi: " + ",".join(ipsi_positive)
    else:
        label += "ipsi: N0"
    if "FNA" in diagnosis.ipsi:
        label += " (FNA+)"
    

    contra_positive = [
        lnl
        for lnl, status in diagnosis.contra.get("CT", {}).items()
        if status
    ]
    if len(contra_positive) > 0:
        label += "; contra: " + ",".join(contra_positive)
    else:
        label += "; contra: N0"
    if "FNA" in diagnosis.contra:
        label += " (FNA+)"

    return label


def get_label(scenario: ScenarioConfig) -> str:
    """Get the label for the scenario."""
    t_stage_map = {"early": "early", "late": "late"}
    midext_map = {False: "lateral", True: "mid-ext"}

    label = get_diag_label(scenario.diagnosis)
    m = scenario.midext
    t = scenario.t_stages[0]
    return f"{t_stage_map[t]}; {midext_map[m]}, {label}"


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

    contents = {"I": [], "II": [], 'III': []}
    mean_lists = {"I": [], "II": [], "III": []}
    mean_risks = {"I": {}, "II": {}, "III": {}, "IV": {}, 'V': {}}
    counter = {"I": 0, "II": 0, 'III': 0}
    colors = [COLORS["green"], COLORS["blue"], COLORS["orange"], COLORS["red"], "#6821ab"]

    output_path = FIGURES_DIR / "risks_contra.pdf"

    with h5py.File(RISKS_DIR / "midline_risks_contra.hdf5", "r") as h5file:
        for dset in h5file.values():
            scenario = get_scenario(dict(dset.attrs))
            label = get_label(scenario)
            for_subplot = list(scenario.involvement.contra.keys()).pop()
            mean_risks[for_subplot].update({label: [dset[:].mean(), dset[:].std()]})
            try: 
                mean_lists[for_subplot].append(dset[:].mean())

            except KeyError:
                continue
    
    with open(REPORTS_DIR / "risks/mean_risks_contra.json", mode="w", encoding="utf-8") as risks_file:
        json.dump(mean_risks, risks_file)


    indices = {}
    for lnl, means in mean_lists.items():
        indices[lnl] = np.argsort(np.argsort(means))
    
    with h5py.File(RISKS_DIR / "midline_risks_contra.hdf5", "r") as h5file:
        for dset in h5file.values():
            scenario = get_scenario(dict(dset.attrs))
            label = get_label(scenario)
            if label in not_plot:
                continue
            for_subplot = list(scenario.involvement.contra.keys()).pop()
            try: 
                c = counter[for_subplot]
            except KeyError:
                continue
            counter[for_subplot] += 1
            contents[for_subplot].append(
                Histogram(
                    raw_values=dset[:],
                    kwargs={
                        "label": get_label(scenario),
                        "color": colors[indices[for_subplot][c]],
                    },
                )
            )

    for lnl in indices.keys():
        index = indices[lnl]
        backup = contents[lnl].copy()
        contents[lnl] = [backup[i] for i in np.argsort(mean_lists[lnl])]

    for ax, (lnl, content) in zip(axes, contents.items()):
        draw(ax, content, xlims=(0,10), hist_kwargs={"bins": 60})
        ax.set_ylabel(f"Contra LNL {lnl}", fontweight = "bold")
        ax.set_yticks([])
        ax.legend()
    #axes[2].set_ylim(0, 1.0)
    plt.savefig(output_path)

if __name__ == "__main__":
    main()