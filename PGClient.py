import socket

class PGClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(10)

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("Connection successful!")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running and the IP/port are correct.")
        except socket.timeout:
            print("Connection timed out. Check your network settings.")
        except Exception as e:
            print("An error occurred:", str(e))

    def send_initialization_request(self):
        request_data = {
            'STX': 0x02,
            'Command': 'IC',
            'CmdType': 'C',
            'Acknowledge': '',
            'Reserve': '',
            'ETX': 0x03
        }

        request_bytes = bytes([request_data['STX']]) + \
                        request_data['Command'].encode('ascii') + \
                        request_data['CmdType'].encode('ascii') + \
                        request_data['Acknowledge'].encode('ascii') + \
                        request_data['Reserve'].encode('ascii') + \
                        bytes([request_data['ETX']])
        request_bytes =  bytes.fromhex('02 2C 49 43 2C 43 2C 2C 03')
        print("initialization request: {}".format(request_bytes))
        self.client_socket.sendall(request_bytes)
        response = self.client_socket.recv(1024)
        print(response)

    def send_power_on_request(self):
        #         b'\x02SP,C,,,1,1,1,1\x03'

        request_data = {
            'STX': 0x02,
            'Command': 'SP,',
            'CmdType': 'C,',
            'Acknowledge': ',',
            'Reserve': ',',
            'RackNo': "1,",
            'PgNo': "1,",
            'ChannelNo': "1,",
            'Operation Code': "1",
            'ETX': 0x03
        }

        request_bytes = bytes([request_data['STX']]) + \
                        request_data['Command'].encode() + \
                        request_data['CmdType'].encode() + \
                        request_data['Acknowledge'].encode() + \
                        request_data['Reserve'].encode() + \
                        request_data['RackNo'].encode() + \
                        request_data['PgNo'].encode() + \
                        request_data['ChannelNo'].encode() + \
                        request_data['Operation Code'].encode() + \
                        bytes([request_data['ETX']])

        #         request_bytes = bytes.fromhex('02 53 50 2C 43 2C 2C 2C 31 2C 31 2C 31 2C 31 03')
        print("power on request: {}".format(request_bytes))
        self.client_socket.sendall(request_bytes)
        response = self.client_socket.recv(1024)
        print(response)

    def send_power_off_request(self):
        request_data = {
            'STX': 0x02,
            'Command': 'SP,',
            'CmdType': 'C,',
            'Acknowledge': ',',
            'Reserve': ',',
            'RackNo': "1,",
            'PgNo': "1,",
            'ChannelNo': "1,",
            'Operation Code': "0",
            'ETX': 0x03
        }

        request_bytes = bytes([request_data['STX']]) + \
                        request_data['Command'].encode() + \
                        request_data['CmdType'].encode() + \
                        request_data['Acknowledge'].encode() + \
                        request_data['Reserve'].encode() + \
                        request_data['RackNo'].encode() + \
                        request_data['PgNo'].encode() + \
                        request_data['ChannelNo'].encode() + \
                        request_data['Operation Code'].encode() + \
                        bytes([request_data['ETX']])

        print("power off request: {}".format(request_bytes))
        self.client_socket.sendall(request_bytes)
        response = self.client_socket.recv(1024)
        print(response)

    def send_image_swap_request(self, image_path):
        request_data = {
            'STX': 0x02,
            'Command': 'NP,',
            'CmdType': 'C,',
            'Acknowledge': ',',
            'Reserve': ',',
            'RackNo': "1,",
            'PgNo': "1,",
            'ChannelNo': "1,",
            'PatternName': image_path,
            'ETX': 0x03
        }

        request_bytes = bytes([request_data['STX']]) + \
                        request_data['Command'].encode('ascii') + \
                        request_data['CmdType'].encode('ascii') + \
                        request_data['Acknowledge'].encode('ascii') + \
                        request_data['Reserve'].encode('ascii') + \
                        request_data['RackNo'].encode() + \
                        request_data['PgNo'].encode() + \
                        request_data['ChannelNo'].encode() + \
                        request_data['PatternName'].encode('ascii') + \
                        bytes([request_data['ETX']])

        print("power image_swap request: {}".format(request_bytes))
        self.client_socket.sendall(request_bytes)
        response = self.client_socket.recv(1024)
        print(response)

    def send_numbered_image_swap_request(self, image_number):
        request_data = {
            'STX': 0x02,
            'Command': 'CP,',
            'CmdType': 'C,',
            'Acknowledge': ',',
            'Reserve': ',',
            'RackNo': "1,",
            'PgNo': "1,",
            'ChannelNo': "1,",
            'PatternIndex': str(image_number),
            'ETX': 0x03
        }

        request_bytes = bytes([request_data['STX']]) + \
                        request_data['Command'].encode('ascii') + \
                        request_data['CmdType'].encode('ascii') + \
                        request_data['Acknowledge'].encode('ascii') + \
                        request_data['Reserve'].encode('ascii') + \
                        request_data['RackNo'].encode() + \
                        request_data['PgNo'].encode() + \
                        request_data['ChannelNo'].encode() + \
                        request_data['PatternIndex'].encode('ascii') + \
                        bytes([request_data['ETX']])

        print("power image_swap request: {}".format(request_bytes))
        self.client_socket.sendall(request_bytes)
        response = self.client_socket.recv(1024)
        print(response)

    def close(self):
        self.client_socket.close()