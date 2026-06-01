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

        differences[path.stem] = result
    
    return differences


def main():
    """Calculate difference in BIC / 2 and log-evidence."""
    unilateral = compute_differences(REPORTS_DIR / "metrics", "metrics_base.json")
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


    # # Input and output directories
    # metrics_dir = REPORTS_DIR / "metrics"
    # output_dir = REPORTS_DIR / "metrics_diff.json"
    # base_path = metrics_dir / "metrics_base.json"

    # json_files = list(metrics_dir.glob("*.json"))

    # # Extract values of base graph
    # base_file = pd.read_json(base_path, typ='series')
    # base_evidence = base_file['evidence']
    # base_bic = base_file['BIC']

    # differences = {}

    # for json_file in json_files:
    #     df = pd.read_json(json_file, typ='series')
    #     diff_evidence = df['evidence'] - base_evidence
    #     diff_BIC = df['BIC'] - base_bic

    #     differences[json_file.stem] = {'evidence': diff_evidence,
    #                                    'BIC': diff_BIC}
    

    # json.dump(differences, open(output_dir, 'w'), indent=4, sort_keys=True)


if __name__ == "__main__":
    main()