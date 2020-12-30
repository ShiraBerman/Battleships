"""
Filename: opponent.py

Usage: opponent.py

Date: 29/12/20

Description: An opponent client for testing.
"""
from battleships_client import BattleshipsClient
from logger import Logger
from player import Player
from player_cli import Menu

DST_HOST = "127.0.0.1"
SRC_PORT = 12346
DST_PORT = 11111


def main():
    console_logger = Logger()
    client = BattleshipsClient(DST_HOST, SRC_PORT, DST_PORT, console_logger)
    init_player = Player(Menu(), client)

    init_player.choose_board()
    init_player.choose_player_order()
    init_player.play()


if __name__ == '__main__':
    main()
