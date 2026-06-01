import matplotlib.pyplot as plt
import numpy as np
from lymph import types
from lyscripts import utils
from lyscripts.configs import ModelConfig, GraphConfig, DistributionConfig, construct_model, add_distributions
#import config
from typing import Any
import json
import pandas as pd
from ocmscripts import config

def get_model(
    which: str,
    load_samples: bool = True,
) -> types.Model:
    params_path = config.CONFIGS_DIR / "graphs" / f"{which}.ly.yaml"
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
    
    samples_path = config.SAMPLES_DIR / f"{which}.hdf5"
    samples = utils.load_model_samples(samples_path)
    model.set_params(*samples.mean(axis=0))

    return model

def get_samples(which: str) -> np.ndarray:
    samples_path = config.SAMPLES_DIR / f"{which}.hdf5"
    return utils.load_model_samples(samples_path)

def main():
    """Plot figure."""
    model = get_model('midline+II_I+III_V')

    t = np.linspace(0, 10, 11)
    p_midline = {
        "lateralised": (1 - model.midext_prob)**t,
        "extension": 1 - (1 - model.midext_prob)**t,
    }
    dist = {
        "early": model.get_distribution("early").pmf,
        "late": model.get_distribution("late").pmf,
    }

    # calculate probabilities for lateralisation / extension for early and late T-cat.
    prob_early_lat = np.sum(p_midline["lateralised"] * dist["early"])
    prob_early_ext = np.sum(p_midline["extension"] * dist["early"])
    prob_late_lat = np.sum(p_midline["lateralised"] * dist["late"])
    prob_late_ext = np.sum(p_midline["extension"] * dist["late"])

    # extract params from the dataset
    dataset = pd.read_csv(config.PROCESSED_DATA_DIR / "dataset.csv", header = [0, 1, 2])
    early = dataset.loc[dataset['tumor', 'core', 't_stage'] < 3].copy()
    late = dataset.loc[dataset['tumor', 'core', 't_stage'] >= 3].copy()

    # N_early, N_late
    N_early = len(early)
    N_late = len(late)

    # N_ext_early, N_ext_late
    N_ext_early = np.sum(early['tumor', 'core', 'extension'])
    N_ext_late = np.sum(late['tumor', 'core', 'extension'])

    #N_lat_early, N_lat_late
    N_lat_early = np.sum(early['tumor', 'core', 'extension'] == False)
    N_lat_late = np.sum(late['tumor', 'core', 'extension'] == False)

    N_early_info = N_lat_early + N_ext_early
    N_late_info = N_lat_late + N_ext_late

    observed_lat_tot = (N_lat_early + N_lat_late) / (N_early_info + N_late_info)
    observed_ext_tot = (N_ext_early + N_ext_late) / (N_early_info + N_late_info)

    predicted_lat_tot = (prob_early_lat * N_early + prob_late_lat * N_late) / (N_early + N_late)
    predicted_ext_tot = (prob_early_ext * N_early + prob_late_ext * N_late) / (N_early + N_late)
    results = {
        'category': ['early', 'late', 'tot'],
        'total_patients': [N_early, N_late, N_early + N_late],
        'observed_lateralized': [N_lat_early, N_lat_late, N_lat_early + N_lat_late],
        'observed_extended': [N_ext_early, N_ext_late, N_ext_early + N_ext_late],
        'observed_lat_proportion': [N_lat_early/N_early_info, N_lat_late/N_late_info, observed_lat_tot],
        'observed_ext_proportion': [N_ext_early/N_early_info, N_ext_late/N_late_info, observed_ext_tot],
        'predicted_lat_prob': [prob_early_lat, prob_late_lat, predicted_lat_tot],
        'predicted_ext_prob': [prob_early_ext, prob_late_ext, predicted_ext_tot],
    }
    
    # Save to CSV
    results_df = pd.DataFrame(results)
    results_df_transposed = results_df.set_index('category').T
    output_path = config.REPORTS_DIR / "midline_extension_analysis.csv"
    results_df_transposed.to_csv(output_path, index=True)

if __name__ == "__main__":
    main()
