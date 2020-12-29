"""
Filename: battleships_client.py

Usage: battleships_client.py

Date: 29/12/20

Description: Communication with other BattleshipsClients.
"""
from socket import socket, AF_INET

PORT = 12346
DATA_SIZE = 9
GAME_INIT_DATA = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"
BOARD_SETUP_DATA = b"\x00\x01\x00\x00\x00\x00\x00\x00\x00"
INCORRECT_ATTEMPT = 0
CORRECT_ATTEMPT = 1
FULL_BATTLESHIP = 2
BYTE_SIZE = 1
BIG_ENDIAN = "big"
HOST = "0.0.0.0"


class BattleshipsClient:
    def __init__(self, host, src_port, dst_port, logger):
        self.dst_host = host
        self.src_port = src_port
        self.dst_port = dst_port
        self.logger = logger
        self.socket = None

    def is_data_init_message(self, data):
        return data == GAME_INIT_DATA

    def wait_for_init(self):
        with socket(AF_INET) as ip_socket:
            ip_socket.bind((HOST, self.src_port))
            ip_socket.listen(1)
            conn_socket, address = ip_socket.accept()
            self.socket = conn_socket
            self.logger.log(f"Connected by: {address}")
            while True:
                data = conn_socket.recv(DATA_SIZE)
                if self.is_data_init_message(data):
                    self.logger.log(f"Data is init message: {data}")
                    break

    def wait_for_board_setup(self):
        data = None
        while data != BOARD_SETUP_DATA:
            data = self.receive_message()
        return data

    def send_init_game_message(self):
        self.socket = socket(AF_INET)
        self.socket.connect((self.dst_host, self.dst_port))
        self.socket.sendall(GAME_INIT_DATA)

    def receive_message(self):
        while True:
            data = self.socket.recv(DATA_SIZE)
            if data:
                self.logger.log(f"data: {data}")
                return data

    def send_board_setup_message(self):
        self.socket.sendall(BOARD_SETUP_DATA)

    def send_attempt_message(self, x_coor: int, y_coor: int):
        self.socket.sendall(b"\x00\x00\x01" + x_coor.to_bytes(BYTE_SIZE, BIG_ENDIAN)
                            + y_coor.to_bytes(BYTE_SIZE, BIG_ENDIAN)
                            + b"\x00\x00\x00\x00")

    def send_response_to_attempt(self, status: int):
        self.socket.sendall(b"\x00\x00\x00\x00\x00" + status.to_bytes(BYTE_SIZE, BIG_ENDIAN) + b"\x00\x00")
