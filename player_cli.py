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
        return input("Choose an action from the menu:\n(1) attempt\n(2) display\n")

    def display_board(self, board):
        print(board)

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
