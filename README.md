# Oral Cavity Model Paper

Modelling the tumor progression based on lymphatic spread patterns of newly diagnosed oral cavity squamous cell carcinoma patient records.

## Prerequisites

To reproduce the findings in this repository, you will need the following tools installed on your system:

- [uv] for creating isolated virtual environments
- [DVC](https://dvc.org/doc/install) for pipeline management

Please refer to the respective links for installation instructions.

> [!NOTE]
> [uv] is not strictly necessary. But due to its cross-platform lockfile, its integrated Python version management and its insane speed compared to stuff like `venv` or `pip`, we highly recommend it.

[uv]: https://docs.astral.sh/uv/

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/noemibuehrer/oral-cavity-model-paper.git
   cd oral-cavity-model-paper
   ```

2. **Set Up the Virtual Environment**  
   Use `uv` to create and activate a virtual environment:

   ```bash
   uv venv --python 3.10
   source .venv/bin/activate
   ```

3. **Sync the Environment**  
   Synchronize the environment with the `uv.lock` file:

   ```bash
   uv sync
   ```

4. **Initialize DVC**  
   Ensure DVC is initialized and the pipeline is ready:

   ```bash
   dvc pull
   ```

   This will download the necessary data and artifacts from the remote storage.

## Project Organization

```txt
├── LICENSE               <- Open-source MIT license.
├── README.md             <- Detailed information about the setup and experiments in this project.
├── data
│   ├── external          <- Data from lycosystem/lydata repo.
│   └── processed         <- The final, canonical data set for modeling.
│
├── models                <- Drawn samples and computed posteriors or risks.
│   ├── configs           <- YAML files that define models and how to sample their params.
│   ├── histories         <- Bookkeeping of how a MCMC sampling round went.
│   ├── samples           <- The burned-in and thinned chain of MCMC samples as HDF5 files.
│   ├── prevalences       <- Prevalences of different scenarios for each of the MCMC samples as HDF5 files.
│   └── risks             <- Risks of different scenarios for each of the MCMC samples as HDF5 files.
│
├── pyproject.toml        <- Project configuration file with package metadata for
│                            ocmscripts and configuration for tools like ruff.
│
├── uv.lock               <- A cross-platform lockfile of the virtual Python environment created and
|                            updated whenever a command is run via `uv run`.
|
├── dvc.yaml              <- Defines the data, sampling, and inference pipeline.
|
├── dvc.lock              <- A locked record of the state of the defined pipeline using MD5 file hashes.
│
├── reports                <- Generated analysis results.
│   ├── figures            <- Generated graphics and figures to be used in reporting.
│   ├── likelihoods        <- Saved likelihood values to be used in reporting.
│   ├── metrics_unilateral <- Saved metrics for unilateral model comparison.
│   ├── metrics_bilateral  <- Saved metrics for bilateral model comparison.
│   ├── plots              <- Histories of thermodynamic intergration steps.
│   └── risks              <- Saved risks of occult disease to be used in reporting.
│
└── ocmscripts            <- Source code for use in this project.
    ├── __init__.py              <- Makes ocmscripts a Python module.
    ├── config.py                <- Store useful variables and configuration.
    ├── dataset.py               <- Script to concatenate and filter.
    ├── metrics.py               <- Script to calculate metrics for model comparison.
    ├── midline_extension.py     <- Script to calculate ratio of patients with extension.
    ├── model_parameters.py      <- Script to extract model parameters.
    ├── patient_likelihoods.py   <- Script to evaluate likelihoods of patients.
    └── plots                    <- Scripts to create visualizations.
```

## Pipeline

We use [DVC] as a pipeline management and execution tool. Similar to [Make], it defines a directed acyclic graph (DAG) from inputs and outputs of various computational stages. The pipeline:

1. Ingests data from the `data/external/` folder.
2. Uses model/sampling configuration files (e.g., in `models/configs/`) to draw parameter samples.
3. Stores the samples in `models/samples/`.
4. Calculates prevalences and risks and stores them in `models/prevalences` or `models/risks`.
5. Generates figures and plots, saving them to `reports/figures/`.

The pipeline is defined in the `dvc.yaml` file. To execute the pipeline, run:

```bash
dvc repro
```

A successful run produces a `dvc.lock` lockfile, which records the state of the pipeline. This lockfile can also be used to cache runs with different parameters or download selected runs from remote storage.

[DVC]: https://dvc.org
[Make]: https://www.gnu.org/software/make/

## Python Scripts

The individual computational stages within the pipeline are implemented using custom [Python] scripts or lyscripts CLIs. To ensure reproducibility, use the provided `uv.lock` file to create an isolated and OS-independent virtual environment.

[Python]: https://docs.python.org/3.10/

## Reproducing Results

To reproduce the results:

1. Ensure all dependencies are installed and the environment is set up.
2. Pull the required data and artifacts using `dvc pull`.
3. Execute the pipeline using `dvc repro`.

For any issues or questions, please refer to the respective tool documentation or open an issue in this repository.