import subprocess
import cv2

# Define the file you want to run
file_to_run = "SDKIntegrationScript.py"

# Define the number of times to run the file
num_times = 5

for index in range(num_times):
    subprocess.call(["python", file_to_run, "--index", str(index)])
