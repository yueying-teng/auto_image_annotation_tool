#!/bin/bash

for folder in /inception/data/video_frames/*; do
	echo "$folder"
	python classify_folder.py "$folder"
done