"""
Filename: player_cli.py

Usage: player_cli.py

Date: 29/12/20

Description: A CLI for the player.
"""
from consts import PlayerConsts


class Menu:
    def get_board(self):
        board = input(f"Enter your 10X10 board:\nExample:\n{PlayerConsts.EXAMPLE_BOARD}")
        for i in range(PlayerConsts.DIM - 1):
            board += "\n" + input()
        return board

    def get_player_order(self):
        return input("Are you the first/second player? 1/2\n")

    def report_connection(self):
        print("The other player is ready!")

    def get_action(self):
        return input("Choose an action from the menu:\n(1) attempt\n(2) display\n")

    def display_board(self, board):
        for row in board:
            format_row = ""
            for cell in row:
                format_row += cell + " "
            print(format_row)

    def get_index_for_attempt(self):
        coordinates = input("Enter X and Y coordinates: (Ex: 1, 3)\n")
        x_coor, y_coor = coordinates.split(", ")
        return int(x_coor), int(y_coor)

    def display_correct_attempt(self):
        print("Correct!")

    def display_full_ship_hit(self):
        self.display_correct_attempt()
        print("You hit a full battleship!")

    def display_incorrect_attempt(self):
        print("Incorrect!")

    def display_victory_message(self):
        print("You won!")

    def display_error_code(self, code):
        print(f"You received error code {code}!")
