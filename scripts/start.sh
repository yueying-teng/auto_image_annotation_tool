#!/bin/bash

# download the pretrained model
cd /inception/scripts
bash download_inception_model.sh

# extract frames from video 
cd /inception/data
bash extract_frames.sh 


# parse arguments
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --checkpoint)
    CHECKPOINT="$2" # Checkpoint to run inference on
    shift # past argument
    shift # past value 
    ;;
    --labelmap)
    LABELMAP="$2" # Label map that translates from index to mid
    shift # past argument
    shift # past value
    ;;
    --dict)
	DICT="$2" # Path to a dict.csv that translates from mid to a display name.
    shift # past argument
    shift # past value
    ;;
    --image_size)
    IMAGE_SIZE="$2"
    shift # past argument
    shift # past value
    ;;
    --num_classes)    
    NUM_CALSSES="$2"
    shift # past argument
    shift # past value
    ;;
    --num)    
    NUM="$2"  # Number of top predictions to print
    shift # past argument
    shift # past value
    ;;
    --image_folder_path)    
    IMAGE_FOLDER_PATH="$2"  # input image dir
    shift # past argument
    shift # past value
    ;;
esac
done

# make prediction 
cd /inception/scripts
chmod +x make_prediction_forall.sh
make_prediction_forall.sh \
	--checkpoint $CHECKPOINT \
	--labelmap $LABELMAP \
	--dict $DICT \
	--image_size $IMAGE_SIZE \
	--num_classes $NUM_CALSSES \
	--num $NUM \
	--image_folder_path $IMAGE_FOLDER_PATH



