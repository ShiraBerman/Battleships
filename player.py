"""
Filename: player.py

Usage: player.py

Date: 29/12/20

Description:
"""
FIRST_PLAYER = "1"
SECOND_PLAYER = "2"
OTHER_BOARD =   "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n" + \
                "? ? ? ? ? ? ? ? ? ?\n"


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
            self.is_current_turn = True
        self.menu.report_connection()
        while not self.is_game_over:
            self.execute_action()

    def execute_action(self):
        actions = {"attempt": self.send_attempt, "display": self.display_current_board}
        if self.is_current_turn:
            action = self.menu.get_action()
            actions[action]()
        else:
            data = self.client.receive_message()
            self.client.send_response_to_attempt(0)

    def send_attempt(self):
        x_coor, y_coor = self.menu.get_index_for_attempt()
        self.client.send_attempt_message(x_coor, y_coor)
        self.get_attempt_response()

    def get_attempt_response(self):
        response_actions = [self.incorrect_attempt, self.correct_attempt, self.correct_attempt_full_ship]
        data = self.client.receive_message()
        response_actions[self.client.get_response_value(data)]()

    def display_current_board(self):
        self.menu.display_board(self.board)

    def incorrect_attempt(self):
        self.is_current_turn = False
        self.menu.display_incorrect_attempt()

    def correct_attempt(self):
        self.menu.display_correct_attempt()

    def correct_attempt_full_ship(self):
        self.menu.display_full_ship_hit()

    def send_response_to_attempt(self):
        x_coor, y_coor = self.client.get_indexs()
        cell_value = self.board[y_coor][x_coor]
