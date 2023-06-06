import JcSmartDevicePyd
import pandas as pd
from PGClient import PGClient
from CameraClient import CameraClient
import time

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('SDKIntegrationConfig.csv')

color_map = {"R":"Red", "G":"Green", "B":"Blue"}
image_paths = []

# Create a PG client instance
client = PGClient('127.0.0.1', 9999)

# Connect to the PG
client.connect()

# Send the power switch request to PG
client.send_power_on_request()

sDevSN = "FW151A001"  # Camera SN

# Create a camera client instance
cameraClient = CameraClient(sDevSN)

# Initialize camera
cameraClient.initializeDevice()

# Get camera device info
cameraClient.getDeviceInfo()

# Set camera exposure time, as this is constant
cameraClient.setExposureTime(5500)

## Loop through all images

# Iterate over each row in the DataFrame
# PG doesn't yet support switching with name, so we are switching with index for now

# for index, row in df.iterrows():
#     # Retrieve values from each column
#     color_we_focus = color_map[row['Color_we_focus']]
#     greylevel_we_fixed_on = row['greylevel_we_fixed_on']
#     grey_level_R = row['grey_level_R']
#     grey_level_G = row['grey_level_G']
#     grey_level_B = row['grey_level_B']
#     aperture = row['aperture']
#     ET = row['ET']
#
#     image_path = f"{color_we_focus}{greylevel_we_fixed_on}/{grey_level_R}_{grey_level_G}_{grey_level_B}.bmp"
#     client.send_image_swap_request(image_path)
#
#     time.sleep(0.5)  # Wait for 0.5 seconds
#
#     #now we send aperture and ET settings to the camera, and have it take a picture
#     #first we check if we can find the device
#     JcSmartDevicePyd.eREP_INIT_DEVICE_OPERATE()
#     vecDevList = JcSmartDevicePyd.SI_PyGetDeviceList()
#
#     nDevCnt = len(vecDevList)
#     if nDevCnt < 1:
#         print('No device find.')
#         break

#Loop through all images
for index in range(20):

    # Send image swap request with index
    client.send_numbered_image_swap_request(index)
    time.sleep(1)

    # Get camera to take a picture
    cameraClient.takePicture()

    # Save the image data of the taken picture
    cameraClient.getImageData()



