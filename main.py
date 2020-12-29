"""
Filename: main.py

Usage: main.py

Date: 29/12/20

Description:
"""
from battleships_client import BattleshipsClient
from logger import Logger


def main():
    console_logger = Logger()
    listen_client = BattleshipsClient("127.0.0.1", 11111, 12345, console_logger)
    listen_client.wait_for_init()
    listen_client.send_init_game_message()
    data = listen_client.receive_message()
    listen_client.send_response_to_attempt(2)


if __name__ == '__main__':
    main()
