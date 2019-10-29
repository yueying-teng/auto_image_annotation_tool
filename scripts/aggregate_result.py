#!/usr/bin/env python

# aggregates the labels from all frames in a video 
# to return the top N most frequent labels and their frequencies
# e.g. python aggregate_result.py /inception/output/mountain_lake.csv


import pandas as pd
import numpy as np
import argparse


def aggregate(csv_path, num):
	df = pd.read_csv(csv_path)

	name = []
	for i in range(df.shape[0]):
	    split = df['label_confidence_pair'].iloc[i].split(';')

	    for pair in split[: -1]:
	        name.append('_'.join(pair.split(':')[0].strip().split(' ')))


	v, c = np.unique(name, return_counts = True)
	p = c/df.shape[0]

	value = v[np.argsort(-c)]
	count = c[np.argsort(-c)]
	# account for video length
	prob = p[np.argsort(-p)]

	# print(np.array((value, count)).T[: num])
	print(np.array((value, prob)).T[: num])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('annotaion', type=str, default='',
                      help='Path to the annotation result')
  parser.add_argument('--n', type=int, default=10,
                      help='Number of top predictions to print.')
  args = parser.parse_args()

  aggregate(args.annotaion, args.n)

