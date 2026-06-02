The scripts here compute metrics on layouts.

- `run-metrics-main.sh`: compute KNN and SVR for layouts in Figures 1(c), A3, and A6.
- `run-metrics-beta.sh`: compute KNN and ENT for Figure A4.

The scripts require that layouts are in `../data/outputs/`; these can be downloaded or produced by scripts in `../experiments/`.
Metric files will be stored in `../data/metrics/`.