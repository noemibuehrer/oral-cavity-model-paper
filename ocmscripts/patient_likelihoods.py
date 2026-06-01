import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from loguru import logger

from lymph import types, matrix
from lyscripts import utils
from lyscripts.configs import ModelConfig, GraphConfig, DistributionConfig, construct_model, add_distributions
import ocmscripts.config
from typing import Any
import numpy as np
import json

import pandas as pd

def get_model(
    which: str,
    load_samples: bool = True,
) -> types.Model:
    params_path = ocmscripts.config.CONFIGS_DIR / "graphs" / f"{which}.ly.yaml"
    params = utils.load_yaml_params(params_path)
    model_config = ModelConfig(**params['model'])
    graph_config = GraphConfig(**params['graph'])
    distributions = {}
    for key, item in params['distributions'].items():
        dist_config = DistributionConfig(**item)
        distributions[key] = dist_config

    model = construct_model(model_config, graph_config)
    model = add_distributions(model, distributions)

    if not load_samples:
        return model
    
    samples_path = ocmscripts.config.SAMPLES_DIR / f"{which}_bic.hdf5"
    samples = utils.load_model_samples(samples_path)
    model.set_params(*samples.mean(axis=0))

    return model

def main():
    # Setup output directory
    output_dir = Path(ocmscripts.config.REPORTS_DIR) / "likelihoods"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load models
    model_IV_V = get_model('midline+II_I+IV_V')
    model_IV_V.set_modality('max_llh', sens=1, spec=1)

    # load model with III -> V connection
    model_III_V = get_model('midline+II_I+III_V')
    model_III_V.set_modality('max_llh', sens=1, spec=1)

    # Load patient data
    data = pd.read_csv(ocmscripts.config.PROCESSED_DATA_DIR / 'dataset.csv', header=[0, 1, 2])
    model_IV_V.load_patient_data(data)
    model_III_V.load_patient_data(data)

    # Calculate likelihoods
    patient_llh_III_V = model_III_V.patient_likelihoods()
    patient_llh_IV_V = model_IV_V.patient_likelihoods()
    
    llh_diff = np.log(patient_llh_III_V) - np.log(patient_llh_IV_V)

    # Add to dataframe
    data['patient', 'core', 'llh_diff'] = llh_diff
    data['patient', 'core', 'llh_III_V'] = np.log(patient_llh_III_V)
    data['patient', 'core', 'llh_IV_V'] = np.log(patient_llh_IV_V)

    # Define LNL columns
    IPSI_LNL = [('max_llh', 'ipsi', 'I'), ('max_llh', 'ipsi', 'II'), ('max_llh', 'ipsi', 'III'), ('max_llh', 'ipsi', 'IV'), ('max_llh', 'ipsi', 'V')]
    CONTRA_LNL = [('max_llh', 'contra', 'I'), ('max_llh', 'contra', 'II'), ('max_llh', 'contra', 'III'), ('max_llh', 'contra', 'IV'), ('max_llh', 'contra', 'V')]

    # Analyze likelihoods
    threshold = -2
    low_llh_data = data[[('patient', 'core', 'id'), *IPSI_LNL, *CONTRA_LNL, ('patient', 'core', 'llh_III_V'), ('patient', 'core', 'llh_IV_V'), ('patient', 'core', 'llh_diff')]][llh_diff < threshold]
    high_llh_data = data[[('patient', 'core', 'id'), *IPSI_LNL, *CONTRA_LNL, ('patient', 'core', 'llh_III_V'), ('patient', 'core', 'llh_IV_V'), ('patient', 'core', 'llh_diff')]][llh_diff >= threshold]

    low_llh_sum = low_llh_data.sum()
    high_llh_sum = high_llh_data.sum()

    # Prepare results dictionary
    results = {
        "summary": {
            "low_llh_diff_count": len(low_llh_data),
            "high_llh_diff_count": len(high_llh_data),
            "threshold": threshold,
        },
        "low_llh_diff": {
            "llh_III_V": float(low_llh_sum['patient', 'core', 'llh_III_V']),
            "llh_IV_V": float(low_llh_sum['patient', 'core', 'llh_IV_V']),
            "llh_diff": float(low_llh_sum['patient', 'core', 'llh_diff']),
        },
        "high_llh_diff": {
            "llh_III_V": float(high_llh_sum['patient', 'core', 'llh_III_V']),
            "llh_IV_V": float(high_llh_sum['patient', 'core', 'llh_IV_V']),
            "llh_diff": float(high_llh_sum['patient', 'core', 'llh_diff']),
        },
    }

    # Save plot
    plt.figure()
    plt.hist(llh_diff, range=(-6.5, 2.5), bins=18, histtype='bar', edgecolor='black')
    plt.grid(axis='y')
    plt.xlabel('Log likelihood difference (III→V vs IV→V)')
    plt.ylabel('Number of patients')
    plot_path = output_dir / "patient_likelihoods.pdf"
    plt.savefig(plot_path, bbox_inches='tight')
    logger.success(f"Saved plot to {plot_path}")

    # Save results to JSON
    json_path = output_dir / "patient_likelihoods.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.success(f"Saved results to {json_path}")

if __name__ == "__main__":
    main()