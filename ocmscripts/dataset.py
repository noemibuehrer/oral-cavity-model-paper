
from pathlib import Path

from loguru import logger
from lydata import C
from lydata.accessor import LyDataFrame
import pandas as pd
import typer

app = typer.Typer()

from ocmscripts.config import PROCESSED_DATA_DIR


def compile_icd_codes(list: list[int]) -> list[str]:
    """Compile a list of ICD codes from the given subsites"""
    icd_codes = []
    for i in list:
        base = f"C{i:02d}"
        icd_codes += [base] + [f"{base}.{j}" for j in range(10)]
    return icd_codes


@app.command()
def main(
    input_paths: list[Path],
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv"
):
    """Combine multiple datasets and filter for oral cavity subsites."""
    full_dataset: LyDataFrame = pd.DataFrame()
    for input_path in input_paths:
        dataset = pd.read_csv(input_path, header=[0, 1, 2])
        dataset = dataset.convert_dtypes()
        full_dataset = pd.concat([full_dataset, dataset], ignore_index=True)

        logger.info(f"Loaded dataset from {input_path = }")
    
    enhanced_dataset = full_dataset.ly.enhance()

    is_oral_cavity = C("subsite").isin(compile_icd_codes([2, 3, 4, 6]))
    filtered_dataset = enhanced_dataset.ly.query(query=is_oral_cavity)
    logger.info(f"Remaining {filtered_dataset.shape = }")

    filtered_dataset.to_csv(output_path, index=False)
    logger.info(f"Saved dataset to {output_path = }")


if __name__ == "__main__":
    app()
                                       

