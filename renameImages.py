import os
import shutil
import re

def rename_files(images_folder):
    # Get a list of all jpg files in the images folder
    images = [f for f in os.listdir(images_folder) if f.endswith('.jpg')]

    # Extract the number from each filename and use it for sorting
    images.sort(key=lambda f: int(re.search(r'image(\d+)_', f).group(1)))

    # Rename files in the folder with continuous numbering
    for i, image in enumerate(images, start=1):
        src = os.path.join(images_folder, image)
        dst = os.path.join(images_folder, f'image{i}.jpg')
        shutil.move(src, dst)

def rename_files_in_folders(input_folder):
    # Walk through all directories in the input folder
    for root, dirs, files in os.walk(input_folder):
        # If the directory contains any jpg files, rename the files
        if any(f.endswith('.jpg') for f in files):
            print(f'Renaming files in folder: {root}')
            rename_files(root)

# Call the function with the path to your input folder
rename_files_in_folders("/home/matthias/Videos/Alice_Samara_cropped/mazes_experiment1_Cropped_Checked")