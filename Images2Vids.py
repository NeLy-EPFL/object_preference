#IN THIS CODE WE CREATE VIDEOS STARTING FROM IMAGES

from pathlib import Path
from tqdm import tqdm
import subprocess
import os
import sys
import shutil
import numpy as np

# Define input and output paths
data_folder = Path("/home/matthias/Videos/Alice_Samara_cropped2")
output_path = Path(
    "/home/matthias/Videos/Alice_Samara_Videos2/"
)
# Set frames per second for the videos (the same as the original recording)
fps = "29"

# Function to check the integrity of a video using ffprobe
def check_video_integrity(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_format", "-show_streams", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error checking video integrity: {e.stderr.decode('utf-8')}")
        return False

# Function to create a video from images in a given folder
def create_video_from_images(images_folder, output_folder, video_name, fps):
    video_path = output_folder / f"{video_name}.mp4"

    # Only create the video if it doesn't already exist
    if not video_path.exists():
        # Construct the ffmpeg command
        terminal_call = f"/usr/bin/ffmpeg -hwaccel cuda -r {fps} -i {images_folder.as_posix()}/image%d.jpg -pix_fmt yuv420p -c:v libx265 -crf 15 {video_path.as_posix()}"
         # Run the ffmpeg command
        subprocess.run(terminal_call, shell=True)
        return True
    else:
        return False


# -loglevel panic -nostats >  This is to remove the output of the ffmpeg command from the terminal, to add right after the ffmpeg command
# \"scale=-2:-2\"

# Function to search a folder for images and create videos from them
def search_folder_for_images(folder_path, output_folder, fps):
    subdirs = []

    # Recursively find all subdirectories containing jpg images
    for subdir in folder_path.glob("**/*"):
        if subdir.is_dir() and any(
            file.name.endswith(".jpg") for file in subdir.glob("*")
        ):
            subdirs.append(subdir)
    # Progress bar for processing videos        
    with tqdm(total=len(subdirs), desc="Processing videos") as pbar:
        for subdir in subdirs:
            relative_subdir = subdir.relative_to(folder_path)
            video_output_folder = output_folder / relative_subdir
            video_output_folder.mkdir(parents=True, exist_ok=True)
            video_name = relative_subdir.name
            video_path = video_output_folder / f"{video_name}.mp4"
            if video_path.exists():
                if not check_video_integrity(video_path.as_posix()) or os.path.getsize(video_path) < 100 * 1024:
                    print(f"Video {video_name} is corrupted or too small.")
                    print(f"Removing corrupted or small video: {video_path.as_posix()}")
                    video_path.unlink()

            # Create the video if it doesn't exist
            if not video_path.exists():
                create_video_from_images(subdir, video_output_folder, video_name, fps)
            pbar.update(1)

# Iterate over all folders in the data_folder
for folder in data_folder.iterdir():
    if folder.is_dir():
        print(f"Processing folder: {folder.name}")
        output_folder_name = folder.name
        output_folder = output_path / f"{output_folder_name}"
        output_folder.mkdir(parents=True, exist_ok=True)
        processing_output_folder = output_path / f"{output_folder_name}_Processing"

         # Rename output folder to indicate processing
        if not processing_output_folder.exists():
            output_folder.rename(processing_output_folder)

        # Load the fps value from the fps.npy file in the experiment directory
        # fps_file = processing_output_folder / "fps.npy"
        # if fps_file.exists():
        #     fps = np.load(fps_file)
        #     fps = str(fps)
        # else:
        #     print(f"Error: fps.npy file not found in {folder}")
        #     continue
        
        fps = "29"
        
        # Search for images and create videos
        search_folder_for_images(folder, processing_output_folder, fps)
        # Rename the output folder after all videos have been created
        print(f"Processing of {folder.name} complete.")
        new_output_folder_name = f"{output_folder_name}_Videos"
        new_output_folder = output_path / new_output_folder_name
        processing_output_folder.rename(new_output_folder)
        
        # print(f"Processing of {folder.name} complete.")
        # new_output_folder_name = f"{output_folder_name}_Videos"
        # new_output_folder = output_path / new_output_folder_name
        # shutil.move(processing_output_folder.as_posix(), new_output_folder.as_posix())

# subprocess.run(
#     [
#         "/home/matthias/Tracking_Analysis/Ball_Pushing/MazeRecorder/Processing/CheckVideos.sh"
#     ]
# )

# TODO: Add a way to resume an aborted processing in a given folder, by checking already existing videos integrity, skipping them and processing folder not yet done.

# TODO : make the script run as a background process, always checking for non processed videos
