import subprocess
import JcSmartDevicePyd
import pandas as pd

# Define the file you want to run
integration_script = "SDKIntegrationScript.py"
color_filter_switch_script = "SwitchColorFilter.py"
csv_file = "test1.csv"

# Read the CSV file
df = pd.read_csv(csv_file)

# Iterate through each row
for index, row in df.iterrows():
    color_we_focus = row['Color_we_focus']
    greylevel_we_fixed_on = row['greylevel_we_fixed_on']
    grey_level_R = row['grey_level_R']
    grey_level_G = row['grey_level_G']
    grey_level_B = row['grey_level_B']
    color_filter = row['color_filter']
    ET = row['ET']
    index_value = row['index']

    # Create the string with format "R_G_B"
    image_filename = f"{grey_level_R}_{grey_level_G}_{grey_level_B}"

    # X is red, Y is green, Z is blue, CF3 is clear
    subprocess.call(["python", color_filter_switch_script, "--filter", color_filter])

    subprocess.call(["python", integration_script, "--index", str(index),
                     "--exposure", str(ET*1000), "--filename", image_filename])


