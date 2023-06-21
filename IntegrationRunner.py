import subprocess
import JcSmartDevicePyd
import pandas as pd
import os

# Define the file you want to run
integration_script = "SDKIntegrationScript.py"
csv_file = "test1.csv"
color_map = {"R":"Red", "G":"Green", "B":"Blue"}

# Read the CSV file
df = pd.read_csv(csv_file)

# Create the image filename column
df['image_filename'] = df['grey_level_R'].astype(str) + '_' + df['grey_level_G'].astype(str) + '_' + df['grey_level_B'].astype(str)

# Iterate through each row
for index, row in df.iterrows():
    color_we_focus = color_map[row['Color_we_focus']]
    greylevel_we_fixed_on = row['greylevel_we_fixed_on']
    grey_level_R = row['grey_level_R']
    grey_level_G = row['grey_level_G']
    grey_level_B = row['grey_level_B']
    color_filter = row['color_filter']
    ET = row['ET']

    directory_path = f"{color_we_focus}{greylevel_we_fixed_on}/"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Create the filename
    image_filename = f"{grey_level_R}_{grey_level_G}_{grey_level_B}"

    # Create filename suffix
    suffix = f"_{color_filter}_{ET}"

    # X is red, Y is green, Z is blue, CF3 is clear
    subprocess.call(["python", integration_script, "--index", str(index), "--filter", color_filter,
                     "--exposure", str(ET*1000), "--filename", image_filename, "--filenameSuffix", suffix, "--saved_dir", directory_path])

