"""
Filename: player_cli.py

Usage: player_cli.py

Date: 29/12/20

Description:
"""

DIM = 10
EXAMPLE_BOARD = "- - - - - - - o o o\n" + \
                "o - - - - - - - - -\n" + \
                "o - - - - o - - - -\n" + \
                "o - - - - o - - - -\n" + \
                "o - - - - - - - - -\n" + \
                "- - - - - o o o o o\n" + \
                "o - - - - - - - - -\n" + \
                "o - - - - - - - - -\n" + \
                "o - - - - o - - - -\n" + \
                "- - - - - o - - - -\n"


class Menu:
    def get_board(self):
        board = input(f"Enter your 10X10 board:\nExample:\n{EXAMPLE_BOARD}")
        for i in range(DIM - 1):
            board += "\n" + input()
        return board

    def get_player_order(self):
        return input("Are you the first/second player? 1/2\n")

    def report_connection(self):
        print("The other player is ready!")

    def get_action(self):
        print("Choose an action from the menu:\nattempt\ndisplay")
