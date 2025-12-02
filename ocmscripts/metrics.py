from pathlib import Path

from loguru import logger
from lyscripts.plots import BetaPosterior, Histogram, draw
from matplotlib import pyplot as plt
import pandas as pd
import typer
import json 
from ocmscripts.config import FIGURES_DIR, HISTORIES_DIR, REPORTS_DIR

def main():
    """Calculate difference in BIC / 2 and log-evidence."""

    # Input and output directories
    metrics_dir = REPORTS_DIR / "metrics"
    output_dir = REPORTS_DIR / "metrics_diff.json"
    base_path = metrics_dir / "metrics_base.json"

    json_files = list(metrics_dir.glob("*.json"))

    # Extract values of base graph
    base_file = pd.read_json(base_path, typ='series')
    base_evidence = base_file['evidence']
    base_bic = base_file['BIC']

    differences = {}

    for json_file in json_files:
        df = pd.read_json(json_file, typ='series')
        diff_evidence = df['evidence'] - base_evidence
        diff_BIC = df['BIC'] - base_bic

        differences[json_file.stem] = {'evidence': diff_evidence,
                                       'BIC': diff_BIC}
    

    json.dump(differences, open(output_dir, 'w'), indent=4, sort_keys=True)


if __name__ == "__main__":
    main()