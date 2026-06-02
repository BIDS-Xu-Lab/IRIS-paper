from sys import argv

dataset = argv[1]
layout = argv[2]
replicate = int(argv[3])
force = len(argv) > 4 and argv[4] == 'True'

import os
if not force and os.path.exists(f'../data/outputs/{dataset}.{layout}.r{replicate}.npy'):
	print(f'=============== Skipping {dataset} with {layout}, replicate {replicate} ===============')
	exit()

import numpy as np
import joblib
import pandas as pd

from IRIS import fit_transform
from umap import UMAP

def layout_iris(X, t, beta=0.95):
	return fit_transform(X, time=t, alpha=1, beta=beta, zeta=0.1, n_trees=32, n_iterations=int(X.shape[0]/100), gamma=128, n_neighbors=32, n_propagations=3, n_threads=10)

def layout_umap(X, min_dist=0.1):
	return UMAP(n_components=2, init='random', min_dist=min_dist, verbose=True, n_jobs=10).fit_transform(X)

print(f'=============== Processing {dataset} with {layout}, replicate {replicate} ===============')
t = np.load(f'../data/inputs/{dataset}.time.npy').astype(dtype=np.float32)
X = np.load(f'../data/inputs/{dataset}.emb.npy')

start_time = pd.Timestamp.now()

if layout.startswith('iris'):
	lay = layout_iris(X, t, beta=float(layout[6:]))
elif layout.startswith('umap-md'):
	lay = layout_umap(X, min_dist=float(layout[7:]))

end_time = pd.Timestamp.now()
elapsed_time = (end_time - start_time).total_seconds()

np.save(f'../data/outputs/{dataset}.{layout}.r{replicate}.npy', lay)
with open(f'../data/outputs/{dataset}.{layout}.r{replicate}.npy.time.txt', 'wb') as f:
	f.write(str(elapsed_time).encode())
