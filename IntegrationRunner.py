import subprocess
import JcSmartDevicePyd

# Define the file you want to run
integration_script = "SDKIntegrationScript.py"
color_filter_switch_script = "SwitchColorFilter.py"

clear_filter_exposure_values = [100000, 26500, 5500, 1100, 200]  # in milliseconds
red_filter_exposure_values = [105000, 27000, 6200, 1250, 260]

# Define the number of images we have
num_images = 5

# X is red, Y is green, Z is blue, CF3 is clear
subprocess.call(["python", color_filter_switch_script, "--filter", "CF3"])

for index in range(num_images):
    subprocess.call(["python", integration_script, "--index", str(index),
                     "--exposure", str(clear_filter_exposure_values[index]*1000)])


