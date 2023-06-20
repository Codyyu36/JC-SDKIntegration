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
parser.add_argument('--saved_dir', type=str, help='Image saved directory', required=True)
parser.add_argument('--filenameSuffix', type=str, help='Color filter and exposure time', required=True)
args = parser.parse_args()

# Create a PG client instance
pg_client = PGClient('127.0.0.1', 9999)

# Connect to the PG
pg_client.connect()

# Send the power switch request to PG
pg_client.send_power_on_request()

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
pg_client.send_image_swap_request(args.filename+".a1")
time.sleep(1)

# Get camera to take a picture
cameraClient.takePicture()

# Save the image data of the taken picture
cameraClient.getImageData(args.saved_dir+args.filename+args.filenameSuffix)
