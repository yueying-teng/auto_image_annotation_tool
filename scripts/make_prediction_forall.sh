#!/bin/bash

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
    NUM_CLASSES="$2"
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

for folder in "$IMAGE_FOLDER_PATH"*; do
	echo "$folder"
	python classify_folder.py "$folder" \
		--checkpoint $CHECKPOINT \
		--labelmap $LABELMAP \
		--dict $DICT \
		--image_size $IMAGE_SIZE \
		--num_classes $NUM_CLASSES \
		--n $NUM 

done




