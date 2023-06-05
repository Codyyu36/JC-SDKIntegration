from PGClient import Client

# Create a client instance
client = Client('127.0.0.1', 9999)

# Connect to the server
client.connect()

# Send the power on request
client.send_power_on_request()

# Send the power off request
client.send_power_off_request()

# Send image swap request with index
client.send_numbered_image_swap_request(1)