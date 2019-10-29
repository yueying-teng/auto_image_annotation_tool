#!/bin/bash

mkdir ./video_frames/
cd ./video

for file in *; do
	echo "$file"
	filename="${file%.*}"
	mkdir -p ../video_frames/"$filename"

	ffmpeg -i "$file" -vf fps=1 ../video_frames/"$filename"/"$filename"%3d.jpg

done