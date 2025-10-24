from collections import namedtuple
from typing import Any, Literal

import json
import h5py
import ast

from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from lyscripts.configs import ScenarioConfig, DiagnosisConfig, InvolvementConfig

GOLDEN_RATIO = 1.61803398875
CM_TO_INCH = 0.393701

def turn_axis_off(axes):
    """Turn off axis."""
    axes.set_xticks([])
    axes.set_yticks([])

def get_fontsizes(base: int = 8, offset: int = 2) -> dict[str, int]:
    """Get fontsizes that can be used to update the matplotlib rcParams.

    This is essentially taken from the tueplots package v0.0.14.
    """
    return {
        "font.size": base,
        "axes.labelsize": base,
        "legend.fontsize": base - offset,
        "xtick.labelsize": base - offset,
        "ytick.labelsize": base - offset,
        "axes.titlesize": base,
    }


def get_figsizes(
    nrows: int = 1,
    ncols: int = 1,
    aspect_ratio: float = GOLDEN_RATIO,
    width: float = 17.0,
    pad: float = 0.005,
    unit: Literal["cm", "in"] = "cm",
    constrained_layout: bool = True,
    tight_layout: bool = True,
    individual: bool = False,
) -> dict[str, Any]:
    """Get figure sizes that can be used to update the matplotlib rcParams.

    This is heavily inspired by the tueplots package v0.0.14.
    """
    if unit == "cm":
        width *= CM_TO_INCH
        pad *= CM_TO_INCH

    subplot_width = width / ncols
    height = subplot_width / aspect_ratio

    if not individual:
        height *= nrows

    return {
        "figure.figsize": (width, height),
        "figure.constrained_layout.use": constrained_layout,
        "figure.autolayout": tight_layout,
        "savefig.bbox": "tight",
        "savefig.pad_inches": pad,
    }

Columns = namedtuple(
    "Columns", [
        "inst",
        "age",
        "nd",
        "t_stage",
        "n_stage",
        "midext",
        "ipsi_III",
    ])

COL = Columns(
    inst=("patient", "core", "institution"),
    age=("patient", "core", "age"),
    nd=("patient", "core", "neck_dissection"),
    t_stage=("tumor", "core", "t_stage"),
    n_stage=("patient", "core", "n_stage"),
    midext=("tumor", "core", "extension"),
    ipsi_III=("max_llh", "ipsi", "III"),
)

CONTRA_LNLS = [
    ("max_llh", "contra", "I"),
    ("max_llh", "contra", "II"),
    ("max_llh", "contra", "III"),
    ("max_llh", "contra", "IV"),
    ("max_llh", "contra", "V"),
]

IPSI_LNLS = [
    ("max_llh", "ipsi", "I"),
    ("max_llh", "ipsi", "II"),
    ("max_llh", "ipsi", "III"),
    ("max_llh", "ipsi", "IV"),
    ("max_llh", "ipsi", "V"),
]

def get_lnl_cols(
        side: Literal["ipsi", "contra"],
        lnls: list[str] | None = None,
) -> list[tuple[str, str, str]]:
    if lnls is None:
        lnls = ["I", "II", "III", "IV", "V"]
    return [("max_llh", side, lnl) for lnl in lnls]

def group_and_plot(
    df: pd.DataFrame,
    column: str,
    axes: Axes,
    colors: list[str],
) -> None:
    """Group `df` by `column` and plot the result."""
    grouped = df.groupby(by=column)
    counts = grouped.count().T
    aggregated = 100 * grouped.mean().T
    # Create edges with natural margins (0.9 to 0.1 instead of 1.0 to 0.0)
    edges = np.linspace(0.9, 0.1, len(grouped) + 1)
    positions = edges[1:] + ((edges[0] - edges[1]) / 2)

    for i, ((label, series), (_, count)) in enumerate(
        zip(aggregated.items(), counts.items())
    ):
        series.plot(
            ax=axes,
            kind="bar",
            label=f"{label} ({count.iloc[0]})",
            color=colors[i],
            position=positions[i],
            rot=0,
            zorder=2 - i * 0.1,
        )

    axes.legend()
    axes.grid(visible=True, axis="y")

def get_scenario(scenario_dict: dict[Any]) -> ScenarioConfig:
    """Create a ScenarioConfig from dictionary of the HDF5 file attributes."""
    scenario_dict['diagnosis'] = DiagnosisConfig.model_validate(ast.literal_eval(scenario_dict['diagnosis']))
    if 'involvement' in scenario_dict:
        scenario_dict['involvement'] = InvolvementConfig.model_validate(ast.literal_eval(scenario_dict.get('involvement')))
    else:
        scenario_dict['involvement'] = InvolvementConfig()
    
    if isinstance(scenario_dict['midext'], str):
        scenario_dict['midext'] = ast.literal_eval(scenario_dict['midext'])
    scenario_config = ScenarioConfig.model_validate(scenario_dict)
    return(scenario_config)

def dict_key(d):
    return json.dumps(d, sort_keys=True)

def get_label(scenario: ScenarioConfig) -> str:
    """Get the label for the scenario."""
    t_stage_map = {"early": "early", "late": "late"}
    midext_map = {False: "lateral", True: "mid-ext"}

    label = get_diag_label(scenario.diagnosis)
    m = scenario.midext
    t = scenario.t_stages[0]
    return f"{t_stage_map[t]}; {midext_map[m]}, {label}"

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
