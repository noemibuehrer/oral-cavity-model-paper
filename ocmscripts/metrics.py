from pathlib import Path

from loguru import logger
from lyscripts.plots import BetaPosterior, Histogram, draw
from matplotlib import pyplot as plt
import pandas as pd
import typer
import json 
from ocmscripts.config import FIGURES_DIR, HISTORIES_DIR, REPORTS_DIR

def compute_differences(
        metrics_dir: Path, base_name: str
) -> dict[str, dict[str, float]]:
    base = pd.read_json(metrics_dir / base_name, typ="series")
    base_bic = base["BIC"]
    base_has_evidence = "evidence" in base
    base_has_llh = "max_llh" in base

    differences: dict[str, dict[str, float]] = {}

    for path in sorted(metrics_dir.glob("*.json")):
        if path.name == base_name:
            continue

        current = pd.read_json(path, typ="series")
        result = {
            "BIC": float(current["BIC"] - base_bic),
        }

        if base_has_evidence and "evidence" in current:
            result["evidence"] = float(current["evidence"] - base["evidence"])

        if base_has_llh and "max_llh" in current:
            result["max_llh"] = float(current["max_llh"] - base["max_llh"])

        differences[path.stem] = result
    
    return differences


def main():
    """Calculate difference in BIC / 2 and log-evidence."""
    unilateral = compute_differences(REPORTS_DIR / "metrics_unilateral", "metrics_base.json")
    bilateral = compute_differences(
        REPORTS_DIR / "metrics_bilateral",
        "metrics_midline_base_bic.json",
    )

    output = {
        "unilateral": unilateral,
        "bilateral": bilateral,    
    }

    with open(REPORTS_DIR / "metrics_diff.json", "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()