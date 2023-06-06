from PGClient import PGClient
import time

# Create a client instance
client = PGClient('127.0.0.1', 9999)

# Connect to the server
client.connect()

# Send the power on request
client.send_power_on_request()

# Send the power off request
# client.send_power_off_request()

# Send image swap request with index
for index in range(20):

    client.send_numbered_image_swap_request(index)
    time.sleep(1)