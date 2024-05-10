#!/bin/bash

# activate the right conda environment
#source activate sleap

# Set input and output paths
datafolder="/home/matthias/Videos/Alice_Samara_Videos2"
model_path_fly="/home/matthias/Alice_Samara_labelling/models/240508_163938.multi_instance.n=100/"

# Print out the values of datafolder and model_path
echo "datafolder: $datafolder"
echo "model_path_fly: $model_path_fly"

# Find all subdirectories in datafolder
subdirs=$(find $datafolder -type d)

# For each subdirectory, check if .slp and .h5 files already exist
for subdir in $subdirs; do
# Only process directories that have been pre-processed or fully processed
    #if [[ $subdir == *_Checked* ]]; then # || [[ $subdir == *_Tracked* ]] has been removed for efficiency


    slp_file_fly=$(find $subdir -maxdepth 1 -type f -name "*_tracked_fly.slp")
    h5_file_fly=$(find $subdir -maxdepth 1 -type f -name "*_tracked_fly.h5")
    
    # Find all videos in this folder
    videos=$(find $subdir -maxdepth 1 -type f -name "*.mp4" -print)
    
    # For each video, use sleap-track terminal command with existing model to track ball positions
    for video in $videos; do
        video_name=$(basename $video .mp4)
        output_folder=$(dirname $video)
        output_file_fly="${output_folder}/${video_name}_tracked_fly.slp"
        
        # If .slp and .h5 files for fly do not exist, track fly
        if [ -z "$slp_file_fly" ] && [ -z "$h5_file_fly" ]; then
            sleap-track $video --model $model_path_fly --output $output_file_fly
            sleap-convert "$output_file_fly" --format analysis
        fi
    done
    #fi
done

# Set path to python script
#python_script="/home/matthias/Videos/Tracked_example"

# Run python script
#python $python_script