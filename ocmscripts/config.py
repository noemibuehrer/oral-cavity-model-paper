from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

def find_project_root(marker: str = "dvc.yaml") -> Path:
    """
    Search upwards from the current file's directory to find the project root.
    """
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / marker).exists():
            return parent
    
    # Fallback: if marker not found, assume the old logic or raise error
    raise RuntimeError(f"Could not find project root containing {marker}")

# Paths
PROJ_ROOT = find_project_root()
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"
CONFIGS_DIR = MODELS_DIR / "configs"
HISTORIES_DIR = MODELS_DIR / "histories"
SAMPLES_DIR = MODELS_DIR / "samples"
PREVALENCES_DIR = MODELS_DIR / "prevalences"
RISKS_DIR = MODELS_DIR / "risks"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    #logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass