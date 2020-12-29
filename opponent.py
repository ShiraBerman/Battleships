"""
Filename: opponent.py

Usage: opponent.py

Date: 29/12/20

Description: An opponent client for testing.
"""
from battleships_client import BattleshipsClient
from logger import Logger


def main():
    console_logger = Logger()
    init_client = BattleshipsClient("127.0.0.1", 12345, 11111, console_logger)
    init_client.send_init_game_message()
    init_client.wait_for_init()
    init_client.send_attempt_message(1, 1)
    data = init_client.receive_message()


if __name__ == '__main__':
    main()
