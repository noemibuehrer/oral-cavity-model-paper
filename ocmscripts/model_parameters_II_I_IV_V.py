from lymph import types
from lyscripts import utils
from lyscripts.configs import ModelConfig, GraphConfig, DistributionConfig, construct_model, add_distributions
import config
from typing import Any
import numpy as np
import json

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

def get_model_variables(which: str) -> dict[str, Any]:
    """Get the variables from the models"""
    model = get_model(which)
    samples = get_samples(which)
    names = model.get_named_params()

    means, stds = samples.mean(axis=0), samples.std(axis=0)

    variables = {}
    for name, mean, std in zip(names, means, stds):
        variables[name] = f"{mean*100:.2f}, {std*100:.2f}"
    
    return variables

def main():
    vars = get_model_variables('midline+II_I+IV_V')
    save_path = config.REPORTS_DIR / 'midline+II_I+IV_V_params.json'
    with open(save_path, "w") as file:
        json.dump(vars, file, indent=2)



if __name__ == "__main__":
    main()
    

