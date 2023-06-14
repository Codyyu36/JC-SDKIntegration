import argparse
import JcSmartDevicePyd
from PGClient import PGClient
from CameraClient import CameraClient
import time

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, help='Index value', required=True)
args = parser.parse_args()

# Read the CSV file into a pandas DataFrame
# df = pd.read_csv('SDKIntegrationConfig.csv')
#
# color_map = {"R":"Red", "G":"Green", "B":"Blue"}
# image_paths = []

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

## Loop through all images

# Set the index value from the command-line argument
index = args.index

clear_exposure_values = [100000, 26500, 5500, 1100, 200]  # in milliseconds
red_filter_exposure_values = [105000, 27000, 6200, 1250, 260]

tNoti = None

# Set camera exposure time, as this is constant
cameraClient.setExposureTime(red_filter_exposure_values[index] * 1000)  # sdk takes in microseconds

# Send image swap request with index
client.send_numbered_image_swap_request(index + 1)
time.sleep(1)

# Get camera to take a picture
cameraClient.takePicture()

# Save the image data of the taken picture
cameraClient.getImageData(index)
