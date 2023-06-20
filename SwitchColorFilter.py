from CameraClient import CameraClient
import argparse

sDevSN = "FW151A001"  # Camera SN
cameraClient = CameraClient(sDevSN)

# Initialize camera
cameraClient.initializeDevice()

# Get camera device info
cameraClient.getDeviceInfo()

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--filter', type=str, help='Index value', required=True)
args = parser.parse_args()

# Get the filter option from command line argument
filter_option = args.filter

# Call the respective color filter based on the argument
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