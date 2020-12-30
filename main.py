"""
Filename: main.py

Usage: main.py

Date: 29/12/20

Description:
"""
from battleships_client import BattleshipsClient
from logger import Logger
from player import Player
from player_cli import Menu


def main():
    console_logger = Logger()
    client = BattleshipsClient("127.0.0.1", 11111, 12346, console_logger)
    waiting_player = Player(Menu(), client)

    waiting_player.choose_board()
    waiting_player.choose_player_order()
    waiting_player.play()


if __name__ == '__main__':
    main()
