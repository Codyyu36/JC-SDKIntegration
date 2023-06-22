import pandas as pd
import os
from CameraClient import CameraClient
from PGClient import PGClient

csv_file = "test1.csv"
color_map = {"R":"Red", "G":"Green", "B":"Blue"}

# Read the CSV file
df = pd.read_csv(csv_file)

# Create the image filename column
df['image_filename'] = df['grey_level_R'].astype(str) + '_' + df['grey_level_G'].astype(str) + '_' + df['grey_level_B'].astype(str)

# Create a camera client instance
sDevSN = "FW151A001"  # Camera SN
cameraClient = CameraClient(sDevSN)

# Initialize camera
cameraClient.initializeDevice()

# Create a PG client instance
pg_client = PGClient('127.0.0.1', 9999)

# Connect to the PG
pg_client.connect()

# Send the power switch request to PG
pg_client.send_power_on_request()

# Iterate through each row
for index, row in df.iterrows():
    color_we_focus = color_map[row['Color_we_focus']]
    greylevel_we_fixed_on = row['greylevel_we_fixed_on']
    grey_level_R = row['grey_level_R']
    grey_level_G = row['grey_level_G']
    grey_level_B = row['grey_level_B']
    color_filter = row['color_filter']
    ET = row['ET'] * 1000

    directory_path = f"{color_we_focus}{greylevel_we_fixed_on}/"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Create the filename
    image_filename = f"{grey_level_R}_{grey_level_G}_{grey_level_B}"

    # Create filename suffix
    suffix = f"_{color_filter}_{ET}"

    # Get the filter option from command line argument
    filter_option = color_filter

    # Call the respective color filter based on the argument
    # X is red, Y is green, Z is blue, CF3 is clear
    if filter_option == 'X':
        cameraClient.useRedColorFilter()
    elif filter_option == 'Y':
        cameraClient.useGreenColorFilter()
    elif filter_option == 'Z':
        cameraClient.useBlueColorFilter()
    elif filter_option == 'clear':
        cameraClient.useClearColorFilter()
    else:
        print("Invalid filter option!")

    # Get camera device info
    cameraClient.getDeviceInfo()

    ## Loop through all images

    tNoti = None

    # Set camera exposure time, as this is constant
    cameraClient.setExposureTime(ET)  # sdk takes in microseconds

    # Send image swap request with index
    pg_client.send_image_swap_request(image_filename)

    # Get camera to take a picture
    cameraClient.takePicture()

    # Save the image data of the taken picture
    cameraClient.getImageData(directory_path + image_filename + suffix)
