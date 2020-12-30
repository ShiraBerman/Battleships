from consts import NetworkConsts, DataIndex


class BattleshipsData:
    def __init__(self, data):
        self.data = data

    def is_data_init_message(self):
        return self.data == NetworkConsts.GAME_INIT_DATA

    def is_indexs_valid(self):
        return (1 <= self.data[DataIndex.X_COOR] <= 10) and (1 <= self.data[DataIndex.Y_COOR] <= 10)

    def is_game_over_message(self):
        return self.data == NetworkConsts.GAME_OVER_DATA

    def is_response_to_attempt_message(self):
        return self.data[DataIndex.IS_HIT_RESPONSE] > 0

    def is_attempt_message(self):
        return self.data[DataIndex.HIT_ATTEMPT] > 0

    def is_data_board_setup_msg(self):
        return self.data == NetworkConsts.BOARD_SETUP_DATA

    def get_status_code(self):
        return self.data[DataIndex.ERROR_CODE]

    def get_response_value(self):
        return self.data[DataIndex.RESPONSE_STATUS]

    def get_indexs(self):
        return self.data[DataIndex.X_COOR], self.data[DataIndex.Y_COOR]
