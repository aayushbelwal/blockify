from PIL import Image
import numpy as np
import os
import json
import time
import concurrent.futures


# Load textures inside directory
def loadTextures(name):
    img = Image.open(os.path.join(dir_name, name))
    textures[name.split('.')[0]] = img


# Return RGBA color code of an image as: "{name}: [R, G, B, A]"
def getColorCode(name):
    img_processed = textures[name].resize((1, 1), Image.LANCZOS).convert("RGBA")
    return f"\"{name}\": {np.array(img_processed)[0][0].tolist()}"


# Load and save the RGBA color codes of textures in a ".json" file
def blocksToRGBA():
    global textures
    textures = {}

    # Create a new empty file
    try:
        file_path = f"{dir_name}.json"
        mapping_file = open(file_path, 'x')
    except FileExistsError:
        input(f"\n[!] Warning -- \"{dir_name}.json\" already exists. \nPress Enter to overwrite it: ")
    
    start = time.perf_counter()

    # Load textures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(loadTextures, texture_list)

    # Saving RGBA color code to file
    with open(file_path, 'w') as file:
        file.write("{\n")

        # Process each texture and save its RGBA color code in file
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(getColorCode, textures.keys()))
            
            for i, result in enumerate(results):
                if i < len(results) - 1:
                    file.write(f"\t{result},\n")
                else:
                    file.write(f"\t{result}\n")

        file.write("}")
    
    end = time.perf_counter()
    print(f"\n[i] Conversion Finished in {round((end - start), 2)} second(s). \nRGBA color codes of textures are stored in \"{file_path}\".")


# Validate directory
def validateDir():
    global texture_list
    
    try:
        # Get list of all ".png" files inside direcory
        texture_list = [x for x in os.listdir(dir_name) if x.endswith(".png")]
    except FileNotFoundError:
        print(f"\n[!] Error -- Directory \"{dir_name}\" not found. \nPlease Try Again.")
        getDirName()
        return
    else:
        # Check if texture_list is empty
        if len(texture_list) == 0:
            print(f"\n[!] Error -- No textures found. \nPlease check if all the textures placed DIRECTLY inside \"{dir_name}\" directory (not in subfolders) and have \".png\" extension.")
            getDirName()
            return
        
        print(f"\n[i] Found {len(texture_list)} textures inside \"{dir_name}\" directory.")
        blocksToRGBA()


# Get directory name from User
def getDirName():
    global dir_name
    dir_name = input("\nEnter directory name which contain Minecraft textures and press Enter: ")  
    
    if dir_name == '':
        getDirName()
    else:
        validateDir()


if __name__ == "__main__":
   getDirName()
