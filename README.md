# IRIS-paper
Experiments for "IRIS: time-structured manifold projections"

Requirements: iris-learn, matplotlib, seaborn

To run the complete pipeline:

1. Download and unzip data/ from https://doi.org/10.5281/zenodo.20500665
2. Run `python run-all.py --force` from `experiments/` (see reproducibility note below)
3. Run `bash run-metrics-main.sh` from `analysis/`
4. Run `bash run-metrics-beta.sh` from `analysis/`
5. Run all notebooks (`*.ipynb`) in `plotting/`

**Reproducibility note:** Neither IRIS nor multi-threaded UMAP support random seeds. This means rerunning the
experiments (step 2) will produce layouts that look different, especially in terms of high-level organization,
and may also produce slightly different quantitaive results. However, the overall findings described in the paper
should be robust to these variations. Since random states are set for analysis steps that require stochasticity
(e.g. 5-fold cross-validation), starting from downloaded outputs (steps 3-5) should exactly reproduce the results
represented in figures.

IRIS can be installed from PyPI, e.g. `pip install iris-learn`. If you are looking for IRIS source code (for
development or editable installation), see https://github.com/BIDS-Xu-Lab/IRIS.
