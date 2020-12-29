"""
Filename: player.py

Usage: player.py

Date: 29/12/20

Description:
"""
FIRST_PLAYER = "1"
SECOND_PLAYER = "2"


class Player:
    def __init__(self, menu, client):
        self.menu = menu
        self.client = client
        self.board = []
        self.order = SECOND_PLAYER
        self.is_current_turn = False
        self.is_game_over = False

    def format_board(self, board: str):
        self.board = board.splitlines()
        for i in range(10):
            self.board[i] = self.board[i].split(" ")

    def choose_board(self):
        self.format_board(self.menu.get_board())

    def choose_player_order(self):
        self.order = self.menu.get_player_order()

    def play(self):
        if self.order == SECOND_PLAYER:
            self.client.wait_for_init()
            self.client.send_init_game_message()
            self.client.wait_for_board_setup()
            self.client.send_board_setup_message()
        else:
            self.client.send_init_game_message()
            self.client.wait_for_init()
            self.client.send_board_setup_message()
            self.client.wait_for_board_setup()
        self.menu.report_connection()
        while not self.is_game_over:
            self.execute_action()

    def execute_action(self):
        if self.is_current_turn:
            action = self.menu.get_action()
        else:
            data = self.client.receive_message()
