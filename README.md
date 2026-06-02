# IRIS-paper
Experiments for "IRIS: time-structured manifold projections"

Requirements: iris-learn, matplotlib, seaborn

To run the complete pipeline:

1. Download and unzip data/ from https://doi.org/10.5281/zenodo.20500665
2. Run `python run-all.py --force` from `experiments/` (see reproducibility note below)
2. Run `bash run-metrics-main.sh` from `analysis/`
3. Run `bash run-metrics-beta.sh` from `analysis/`
3. Run all notebooks (`*.ipynb`) in `plotting/`

**Reproducibility note:** layouts created by IRIS and multi-threaded UMAP do not support random seeds. Rerunning the
layouts (step 1) may thus produce slightly different results. However, the findings described in the paper should be
rebust to these variations. Since random states are set for analysis steps that require randomness (e.g. 5-fold
cross-validation), starting from downloaded outputs 