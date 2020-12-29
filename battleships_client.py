"""
Filename: battleships_client.py

Usage: battleships_client.py

Date: 29/12/20

Description: Communication with other BattleshipsClients.
"""
from socket import socket, AF_INET

PORT = 12346


class BattleshipsClient:
    def __init__(self, host):
        self.host = host

    def is_data_init_message(self, data):
        return data == b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"

    def wait_for_init(self):
        with socket(AF_INET) as ip_socket:
            ip_socket.bind((self.host, PORT))
            ip_socket.listen(1)
            conn_socket, address = ip_socket.accept()
            with conn_socket:
                print(f"Connected by: {address}")
                while True:
                    data = conn_socket.recv(9)
                    # print(f"Received data: {data}")
                    if self.is_data_init_message(data):
                        print(f"Data is init message: {data}")
                        break

    def send_init_game_message(self):
        with socket(AF_INET) as ip_socket:
            ip_socket.connect((self.host, PORT))
            ip_socket.sendall(b"\x01\x00\x00\x00\x00\x00\x00\x00\x00")
