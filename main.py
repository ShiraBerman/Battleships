"""
Filename: main.py

Usage: main.py

Date: 29/12/20

Description:
"""
from battleships_client import BattleshipsClient
from threading import Thread


def main():
    init_client = BattleshipsClient("127.0.0.1")
    listen_client = BattleshipsClient("127.0.0.1")

    init_thread = Thread(target=init_client.send_init_game_message)
    listen_thread = Thread(target=listen_client.wait_for_init)

    listen_thread.start()
    init_thread.start()


if __name__ == '__main__':
    main()
