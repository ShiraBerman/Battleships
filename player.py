"""
Filename: player.py

Usage: player.py

Date: 29/12/20

Description:
"""
from threading import Thread
from socket import error

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
SHIP_CELL = "o"
EMPTY_CELL = "-"
DEAD_SHIP_CELL = "X"


class Player:
    def __init__(self, menu, client):
        self.menu = menu
        self.client = client
        self.board = []
        self.order = SECOND_PLAYER
        self.is_current_turn = False
        self.is_game_over = False
        self.data = []

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

        victory_thread = Thread(target=self.is_game_over_data_received)
        victory_thread.start()

        data_thread = Thread(target=self.receive_messages)
        data_thread.start()

        while not self.is_game_over:
            self.execute_action()
        self.client.send_game_over_message()

    def execute_action(self):
        actions = {"attempt": self.send_attempt, "display": self.display_current_board}
        if self.is_current_turn:
            action = self.menu.get_action()
            actions[action]()

    def send_attempt(self):
        x_coor, y_coor = self.menu.get_index_for_attempt()
        self.client.send_attempt_message(x_coor, y_coor)

    def display_current_board(self):
        self.menu.display_board(self.board)

    def incorrect_attempt(self):
        self.is_current_turn = False
        self.menu.display_incorrect_attempt()

    def correct_attempt(self):
        self.menu.display_correct_attempt()

    def correct_attempt_full_ship(self):
        self.menu.display_full_ship_hit()

    def update_game_over_status(self):
        for row in self.board:
            for cell in row:
                if cell == SHIP_CELL:
                    self.is_game_over = False
                    return
        self.is_game_over = True

    def send_response_to_attempt(self, data):
        x_coor, y_coor = self.client.get_indexs(data)
        cell_value = self.board[y_coor - 1][x_coor - 1]
        if cell_value == EMPTY_CELL:
            self.client.send_response_to_attempt(0)
            self.is_current_turn = True
        elif (cell_value == SHIP_CELL) or (cell_value == DEAD_SHIP_CELL):
            self.client.send_response_to_attempt(1)
            self.board[y_coor - 1][x_coor - 1] = DEAD_SHIP_CELL
            self.update_game_over_status()

    def is_game_over_data_received(self):
        while not self.is_game_over:
            for data in self.data:
                if self.client.is_game_over_message(data):
                    self.menu.display_victory_message()
                    self.is_game_over = True

    def receive_messages(self):
        while not self.is_game_over:
            try:
                data = self.client.receive_message()
                self.data.append(data)
                self.received_data_handler(data)
            except error:
                pass

    def received_data_handler(self, data):
        if self.is_current_turn:
            if self.client.is_response_to_attempt_message(data):
                response_actions = [self.incorrect_attempt, self.correct_attempt, self.correct_attempt_full_ship]
                response_actions[self.client.get_response_value(data)]()
        else:
            if self.client.is_attempt_message(data):
                self.send_response_to_attempt(data)
