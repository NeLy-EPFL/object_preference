import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import re 


#REMEMBER TO CALL THE FOLDER WITH IMAGES AS EXPERIMENT1, EXPERIMENT2 ETC (start from 1!!)

#functions to rename all the images in order that they have a progressive number
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


arenas = 9 #starts from zero so it's ok to have 9 here
experiments = 6 #remember experiment starts from 1 so if we have 5, this value has to be 6!!

for experiment in range(1,experiments): 
    print (f'processing experiment: {experiment}')  

    # create a folder to save the cutted mazes for the experiment
    experiment_dir= f"/home/matthias/Videos/Alice_Samara_cropped2/mazes_experiment{experiment}" #CHANGE PATH HERE FOR THE FOLDER WHERE YOU WANT TO SAVE THE MAZES

    # If the directory exists, delete it
    if os.path.exists(experiment_dir):
        shutil.rmtree(experiment_dir)
    #create directory
    os.makedirs(experiment_dir)
    
    #process the images
    start_image = 0
    
    # get filenames in the folder
    
    filenames = os.listdir(f"/home/matthias/Videos/Alice_Samara_experiments/experiment{experiment}") #CHANGE PATH HERE (where the original images are stored)
    
    # Find the image with the highest number
    highest_image = 0
    for filename in filenames:
        match = re.match(r'image(\d+).jpg', filename)
        if match:
            image_number = int(match.group(1))
            if image_number > highest_image:
                highest_image = image_number
    

    masks_dict = {}
    bounding_box_dict = {}

    for image in range(start_image, highest_image+1):
        print (f'processing image: {image}')
    # Load the image
        img = cv2.imread(f"/home/matthias/Videos/Alice_Samara_experiments/experiment{experiment}/image{image}.jpg") ##CHANGE PATH HERE 
        
        if img is None:
            print(f"Image {image} not found, skipping.")
            continue

    # Check if the current image is one of the ones you want to display
        '''if image in [39,50,44,46]:
            fig, ax = plt.subplots()
            plt.axis("off")
            im = ax.imshow(img, cmap="gray", vmin=0, vmax = 255)
            plt.title(f"experiment{experiment}, image{image}")
            plt.show()'''

        # Convert to grayscale if not already
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Enter the arenas coordinates
        X1 = 0
        X2 = 710
        X3 = 1450
        X4 = 2200
        X5 = 2980
        X6 = 3690

        Y1 = 0
        Y2 = 725
        Y3 = 1140
        Y4 = 1860
        Y5 = 2350
        Y6 = 3200

        # Make tuples containing the 9 combinations of coordinates required to get the arenas
        regions_of_interest = [
            (X1, Y1, X2, Y2),
            (X3, Y1, X4, Y2),
            (X5, Y1, X6, Y2),
            (X1, Y3, X2, Y4),
            (X3, Y3, X4, Y4),
            (X5, Y3, X6, Y4),
            (X1, Y5, X2, Y6),
            (X3, Y5, X4, Y6),
            (X5, Y5, X6, Y6),
        ]

        # Create a 3x3 grid of subplots to display each crop

        '''fig, axs = plt.subplots(3, 3, figsize=(20, 20))
        
        for arena_number in range(arenas): #andranno da zero a 8
            
            axs[arena_number // 3, arena_number % 3].axis("off")
            axs[arena_number // 3, arena_number % 3].imshow(
                img[
                    regions_of_interest[arena_number][1] : regions_of_interest[arena_number][3],
                    regions_of_interest[arena_number][0] : regions_of_interest[arena_number][2],
                ],
                cmap="gray",
                vmin=0,
                vmax=255,
            )

        # Remove the axis of each subplot and draw them closer together
        for ax in axs.flat:
            ax.axis("off")
        plt.subplots_adjust(wspace=0, hspace=0)'''

        # Dictionary to store the images, useful for the plot
        arena_images = {}

        for arena_number in range(arenas): 
            print (f'processing arena: {arena_number}')
            
            # create a folder for the experiment
            arena_dir= f"{experiment_dir}/arena{arena_number}" 
            #create directory
            os.makedirs(arena_dir, exist_ok=True)

            #useful when you plot
            arena_name = f"experiment{experiment}_image{image}_Arena{arena_number}"

            # Crop the image
            arena= img[
                regions_of_interest[arena_number][1] : regions_of_interest[arena_number][3],
                regions_of_interest[arena_number][0] : regions_of_interest[arena_number][2],
            ]

        # Store the image in the dictionary, useful for the plot
            arena_images[arena_name] = arena



    #Check if the current image is one of the ones you want to display
            '''if arena_name in ["experiment1_image39_Arena2", "experiment1_image50_Arena2", "experiment1_image44_Arena3", "experiment1_image46_Arena3"]:
                fig, ax = plt.subplots()
                plt.axis("off")
                im = ax.imshow(arena, cmap="gray", vmin=0, vmax = 255)
                plt.title(arena_name)
                plt.show()'''

            
            if image == 0:
                #LOOP TO DO IT WITH EACH single maze 
                # Dictionary to store the images
                maze_images = {}
                masks = []
                bounding_box = []

                #threshold definition to understand what to crop 
                _, binary = cv2.threshold(arena,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                #closing to remove black dots inside our kernel
                # Define the kernel for erosion
                kernel = np.ones((30, 30), np.uint8)  # Adjust kernel size as needed

                # Apply erosion
                closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

                # Apply connected components to label connected regions (so to extract the shape we are interested in) and get statistics
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closing)
                
                #we want to order mazes based on the x coordinate instead of the y coordinate
                centroids_T = np.transpose(centroids[1:]) #the second line [1] will be the x coordinate of mazes and remove background
                x_val_mazes = centroids_T[0] #select only first line (x coordinates)
                index_x_val_mazes_sorted =  np.argsort(x_val_mazes) + 1 #add one because you removed background (first element) 
                        #returns the INDEX of the sorted x coordinates of the mazes 
                        #eg [1,2,0] --> at index 1 of X_val_mazes there is coordinate of 1st maze, at index 2 the second ecc ecc
                        #remove background label (corresponding to the element zero)
                #index_x_val_mazes_sorted = np.delete(index_x_val_mazes_sorted_bg,2) #remove background label 

                # Iterate through each labeled component 
                for maze in index_x_val_mazes_sorted: #starts from zero
                    #maze number will be the index of the index_x_val_mazes_sorted so the number of the maze we are processing
                    #(at index zero there will be the index of the maze 0), while the value maze will contain 
                    #the index of the mazes x coordinate contained in the x_val_mazes

                    # Get statistics for the component
                    left, top, width, height, area = stats[maze]
                    centroid_x, centroid_y = centroids[maze]

                    # Create a mask for this specific component
                    component_mask = np.uint8(labels == maze) * 255 
                    
                    masks.append(component_mask)
                    bounding_box.append([top, height, left, width])
                    
                masks_dict[f"Arena{arena_number}"]={}
                masks_dict[f"Arena{arena_number}"]["masks"] = masks
                masks_dict[f"Arena{arena_number}"]["bounding_box"] = bounding_box
                
            sel_masks = masks_dict[f"Arena{arena_number}"]["masks"]
            sel_bb = masks_dict[f"Arena{arena_number}"]["bounding_box"]
            
            for maze_number, (component_mask, stat) in enumerate(zip(sel_masks, sel_bb)):
                print (f'processing maze: {maze_number}')
                #create subfolder of experiment, one for each maze
                maze_dir = f"{arena_dir}/maze{maze_number}"
                # Create the directory
                os.makedirs(maze_dir, exist_ok=True)
                    
                maze_name = f"{arena_name}_maze{maze_number}"
                print(maze_name)
                top = stat[0]
                heigth = stat[1]
                left = stat[2]
                width = stat[3]
                
                # Use bitwise AND operation to extract the shape
                shape = cv2.bitwise_and(arena, arena, mask=component_mask)

                shape_crop = shape[top:top+height, left:left+width]
                
                #maze_images[maze_name] = shape_crop
                
                # Rotate the image
                if maze_number == 1:
                    shape_crop = cv2.rotate(shape_crop, cv2.ROTATE_180)
                    
                #check that the image has a even number of pixels (height and width) and make it even in case it hasn't
                height, width = shape_crop.shape[:2]

                # Check if the dimensions are even
                if height % 2 != 0 or width % 2 != 0:
                    
                    # If not, subtract 1 from the dimensions to make them even
                    shape_crop = cv2.resize(shape_crop, (width - (width % 2), height - (height % 2)))
                    

    # Check if the current image is one of the ones you want to display
                '''if maze_name in ["experiment1_image39_Arena2_maze1", "experiment1_image39_Arena2_maze2", "experiment1_image50_Arena2_maze1", "experiment1_image50_Arena2_maze2", "experiment1_image44_Arena3_maze1", "experiment1_image44_Arena3_maze2", "experiment1_image46_Arena3_maze1", "experiment1_image46_Arena3_maze2"]:
                    fig, ax = plt.subplots()
                    plt.axis("off")
                    im = ax.imshow(shape_crop, cmap="gray", vmin=0, vmax = 255)
                    plt.title(maze_name)
                    plt.show()'''

                # Save the image 
                cv2.imwrite(f"{maze_dir}/{maze_name}.jpg", shape_crop)
                
    # Call the function with the path to your input folder
    rename_files_in_folders(f"{experiment_dir}") 
#/home/matthias/Videos/Alice_Samara_cropped/mazes_experiment1_Cropped_Checked          
                

    #extra code, jsut in case.
        #     # Save or process the extracted shape
        #     cv2.imwrite(f'shape_{label}.jpg', shape)  
        #     # Print statistics
        #     print(f"Component {label}:")
        #     print(f"  Area: {area}")
        #     print(f"  Bounding Box: ({left}, {top}, {width}, {height})")
        #     print(f"  Centroid: ({centroid_x}, {centroid_y})")
        # # Show the result
        # cv2.imshow('Result', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()         