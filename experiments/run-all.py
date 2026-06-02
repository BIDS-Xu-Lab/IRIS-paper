import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true', default=False, help='Force re-run of layouts')
parser.add_argument('--reps', type=int, default=5, help='Number of replicates')

args = parser.parse_args()
force = args.force
reps = args.reps

datasets = [
	'scrna-embryo',
	'lit-pd1',
	'lit-adrd',
	'scrna-neuro',
	'meta-gut',
]
layouts = [
	'iris-b0',
	'iris-b.5',
	'iris-b.75',
	'iris-b.9',
	'iris-b.95',
	'iris-b1',
	'umap-md0.1',
	'umap-md0.5',
]

os.makedirs('../outputs', exist_ok=True)

for dataset in datasets:
	for layout in layouts:
		for i in range(reps):
			process = subprocess.Popen(['python', 'run-layout.py', dataset, layout, str(i), 'True' if force else 'False'])
			process.wait()
