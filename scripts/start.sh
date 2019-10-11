#!/bin/bash

# download the pretrained model
cd /inception/scripts
bash download_inception_model.sh

# extract frames from video 
cd /inception/data
bash extract_frames.sh 

# make prediction 
cd /inception/scripts
bash make_prediction_forall.sh