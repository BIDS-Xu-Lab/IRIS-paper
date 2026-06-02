from datetime import time
import os

import numpy as np
import joblib
import pandas as pd
from pickle import load, dump
from sys import argv
from scipy.special import rel_entr

name = argv[1]
layouts = argv[2].split(',')
metrics = argv[3].split(',')

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy.stats import entropy

kf = KFold(n_splits=5, shuffle=True, random_state=42)

data2lbl = {
	'scrna-embryo': 'author_major_cell_cluster',
	'lit-pd1': 'topic',
	'lit-adrd': 'L1_clusters',
	'scrna-neuro': 'cell_type',
	'meta-gut': 'study',
}

metric2name = {
	'knn': 'KNN',
	'svr': 'SVR',
	'ent': 'ENT',
}

layout2name = {
	'iris-b0': 'IRIS-B0',
	'iris-b.5': 'IRIS-B0.5',
	'iris-b.75': 'IRIS-B0.75',	
	'iris-b.9': 'IRIS-B0.9',
	'iris-b.95': 'IRIS-B0.95',
	'iris-b1': 'IRIS-B1',	
	'umap-md0.1': 'UMAP-MD0.1',
	'umap-md0.5': 'UMAP-MD0.5',
}

reps = 5

n_samples_svr = 10000
rng = np.random.default_rng(42)

zeta = 0.1
bins = 100
p=np.array([(2.*zeta/bins + (((x+1.)/bins)**2-(x/bins)**2)*(1-zeta))/(1.+zeta) for x in range(bins)])

df = pd.DataFrame(columns=['dataset', 'layout', 'rep'] + [metric2name[metric] for metric in metrics] + ['runtime'])

def layout_file(dataset, layout, rep):
	return f'../data/outputs/{dataset}.{layout}.r{rep}.npy'

def get_labels(dataset):
	with open(f'../data/inputs/{dataset}.meta.tsv', 'rb') as f:
		df = pd.read_csv(f, sep='\t')
	return df[data2lbl[dataset]].values

def add_metric(df, dataset, layout, rep, values, time):
	df.loc[len(df)] = [dataset, layout2name[layout], rep] + values + [time]

for dataset in data2lbl.keys():
	print(f'Processing dataset {dataset}')
	for layout in layouts:
		print(f' Processing layout {layout}')
		for rep in range(reps):
			print(f'  Rep {rep}')
			file = layout_file(dataset, layout, rep)
			lay = np.load(open(file, 'rb'))
			t = np.load(f'../data/inputs/{dataset}.time.npy').astype(dtype=np.float32)
			lbl = get_labels(dataset)
			vals = []
			for metric in metrics:
				if metric == 'knn':
					val = cross_val_score(KNeighborsClassifier(n_neighbors=5), lay, lbl, cv=kf, scoring='accuracy').mean()
				elif metric == 'svr':
					chosen_indices = rng.choice(lay.shape[0], size=np.min([n_samples_svr, lay.shape[0]]), replace=False)
					val = cross_val_score(Pipeline([('scaler', StandardScaler()), ('svr', SVR(kernel='poly', degree=2))]), lay[chosen_indices], t.ravel()[chosen_indices], cv=kf, scoring='r2').mean()
				elif metric == 'ent':
					val = entropy(np.histogram2d(lay[:,0], lay[:,1], bins=100)[0].flatten())
				else:
					assert False, f'Unknown metric {metric}'

				vals.append(val)
			with open(f'../data/outputs/{dataset}.{layout}.r{rep}.npy.time.txt', 'rb') as f:
				time = float(f.read().decode())
			add_metric(df, dataset, layout, rep, vals, time)

os.makedirs('../data/metrics', exist_ok=True)

df.dropna().to_csv(f'../data/metrics/metrics.{name}.csv', index=False)
