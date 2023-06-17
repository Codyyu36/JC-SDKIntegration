import subprocess
import cv2

# Define the file you want to run
integration_script = "SDKIntegrationScript.py"
color_filter_switch_script = "SwitchColorFilter.py"

# Define the number of images we have
num_images = 5

subprocess.call(["python", color_filter_switch_script, "--filter", "CF3"])

for index in range(num_images):
    subprocess.call(["python", integration_script, "--index", str(index)])
