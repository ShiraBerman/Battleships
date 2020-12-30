"""
Filename: player.py

Usage: player.py

Date: 29/12/20

Description:
"""
from threading import Thread
from socket import error
from consts import PlayerConsts
from data import BattleshipsData
from time import sleep


class Player:
    def __init__(self, menu, client):
        self.menu = menu
        self.client = client
        self.board = []
        self.order = PlayerConsts.SECOND_PLAYER
        self.is_current_turn = False
        self.is_game_over = False
        self.data = []

    def format_board(self, board: str):
        self.board = board.splitlines()
        for i in range(PlayerConsts.DIM):
            self.board[i] = self.board[i].split(PlayerConsts.SEPARATOR)

    def choose_board(self):
        self.format_board(self.menu.get_board())

    def choose_player_order(self):
        self.order = self.menu.get_player_order()

    def config_first_player(self):
        self.client.send_init_game_message()
        self.client.wait_for_init()
        self.client.send_board_setup_message()
        self.client.wait_for_board_setup()
        self.is_current_turn = True

    def config_second_player(self):
        self.client.wait_for_init()
        self.client.send_init_game_message()
        self.client.wait_for_board_setup()
        self.client.send_board_setup_message()

    def play(self):
        if self.order == PlayerConsts.SECOND_PLAYER:
            self.config_second_player()
        else:
            self.config_first_player()
        self.menu.report_connection()

        victory_thread = Thread(target=self.is_game_over_data_received)
        victory_thread.start()

        data_thread = Thread(target=self.receive_messages)
        data_thread.start()

        while not self.is_game_over:
            sleep(1)
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
                if cell == PlayerConsts.SHIP_CELL:
                    self.is_game_over = False
                    return
        self.is_game_over = True

    def send_response_to_attempt(self, data: BattleshipsData):
        x_coor, y_coor = data.get_indexs()
        cell_value = self.board[y_coor - 1][x_coor - 1]
        if cell_value == PlayerConsts.EMPTY_CELL:
            self.client.send_response_to_attempt(0)
            self.is_current_turn = True
        elif (cell_value == PlayerConsts.SHIP_CELL) or (cell_value == PlayerConsts.DEAD_SHIP_CELL):
            self.client.send_response_to_attempt(1)
            self.board[y_coor - 1][x_coor - 1] = PlayerConsts.DEAD_SHIP_CELL
            self.update_game_over_status()

    def is_game_over_data_received(self):
        while not self.is_game_over:
            for data in self.data:
                if data.is_game_over_message():
                    self.menu.display_victory_message()
                    self.is_game_over = True

    def receive_messages(self):
        while not self.is_game_over:
            try:
                data = BattleshipsData(self.client.receive_message())
                self.data.append(data)
                self.received_data_handler(data)
            except error:
                pass

    def received_data_handler(self, data: BattleshipsData):
        if data.get_status_code() > 0:
            self.menu.display_error_code(data.get_status_code())
        elif self.is_current_turn:
            if data.is_response_to_attempt_message():
                response_actions = [self.incorrect_attempt, self.correct_attempt, self.correct_attempt_full_ship]
                response_actions[data.get_response_value()]()
        else:
            if data.is_attempt_message():
                if not data.is_indexs_valid():
                    self.client.send_error_message(2)
                else:
                    self.send_response_to_attempt(data)
