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


def main():
    console_logger = Logger()
    client = BattleshipsClient("127.0.0.1", 12346, 11111, console_logger)
    init_player = Player(Menu(), client)

    init_player.choose_board()
    init_player.choose_player_order()
    init_player.play()


if __name__ == '__main__':
    main()
