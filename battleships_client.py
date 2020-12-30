"""
Filename: battleships_client.py

Usage: battleships_client.py

Date: 29/12/20

Description: Communication with other BattleshipsClients.
"""
from socket import socket, AF_INET
from consts import NetworkConsts
from data import BattleshipsData


class BattleshipsClient:
    def __init__(self, dst_host, src_port, dst_port, logger):
        self.dst_host = dst_host
        self.src_port = src_port
        self.dst_port = dst_port
        self.logger = logger
        self.socket = None

    def wait_for_init(self):
        with socket(AF_INET) as ip_socket:
            ip_socket.bind((NetworkConsts.HOST, self.src_port))
            ip_socket.listen(1)
            conn_socket, address = ip_socket.accept()
            self.socket = conn_socket
            while True:
                data = BattleshipsData(conn_socket.recv(NetworkConsts.DATA_SIZE))
                if data.is_data_init_message():
                    break

    def wait_for_board_setup(self):
        data = None
        while data != NetworkConsts.BOARD_SETUP_DATA:
            data = self.receive_message()
        return data

    def receive_message(self):
        while True:
            data = self.socket.recv(NetworkConsts.DATA_SIZE)
            if data:
                return data

    def send_init_game_message(self):
        self.socket = socket(AF_INET)
        self.socket.connect((self.dst_host, self.dst_port))
        self.socket.sendall(NetworkConsts.GAME_INIT_DATA)

    def send_board_setup_message(self):
        self.socket.sendall(NetworkConsts.BOARD_SETUP_DATA)

    def send_attempt_message(self, x_coor: int, y_coor: int):
        self.socket.sendall(b"\x00\x00\x01" + x_coor.to_bytes(NetworkConsts.BYTE_SIZE, NetworkConsts.BIG_ENDIAN)
                            + y_coor.to_bytes(NetworkConsts.BYTE_SIZE, NetworkConsts.BIG_ENDIAN)
                            + b"\x00\x00\x00\x00")

    def send_response_to_attempt(self, status: int):
        self.socket.sendall(b"\x00\x00\x00\x00\x00\x01"
                            + status.to_bytes(NetworkConsts.BYTE_SIZE, NetworkConsts.BIG_ENDIAN)
                            + b"\x00\x00")

    def send_game_over_message(self):
        self.socket.sendall(NetworkConsts.GAME_OVER_DATA)

    def send_error_message(self, error_code):
        self.socket.sendall(b"\x00\x00\x00\x00\x00\x00\x00\x00"
                            + error_code.to_bytes(NetworkConsts.BYTE_SIZE, NetworkConsts.BIG_ENDIAN))
