import argparse
import JcSmartDevicePyd
from PGClient import PGClient
from CameraClient import CameraClient
import time

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, help='Index value', required=True)
parser.add_argument('--exposure', type=int, help='Exposure time', required=True)
parser.add_argument('--filename', type=str, help='Image file name', required=True)
args = parser.parse_args()

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

# Set camera distance
cameraClient.setDistance(104)

# Get camera device info
cameraClient.getDeviceInfo()

## Loop through all images

tNoti = None

# Set camera exposure time, as this is constant
cameraClient.setExposureTime(args.exposure)  # sdk takes in microseconds

# Send image swap request with index
client.send_numbered_image_swap_request(args.index)
time.sleep(1)

# Get camera to take a picture
cameraClient.takePicture()

# Save the image data of the taken picture
cameraClient.getImageData(args.filename)
