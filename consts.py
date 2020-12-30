
class PlayerConsts:
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
    FIRST_PLAYER = "1"
    SECOND_PLAYER = "2"
    OTHER_BOARD = "? ? ? ? ? ? ? ? ? ?\n" + \
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
    SEPARATOR = " "


class NetworkConsts:
    DATA_SIZE = 9
    GAME_INIT_DATA = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"
    BOARD_SETUP_DATA = b"\x00\x01\x00\x00\x00\x00\x00\x00\x00"
    GAME_OVER_DATA = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00"
    INCORRECT_ATTEMPT = 0
    CORRECT_ATTEMPT = 1
    FULL_BATTLESHIP = 2
    BYTE_SIZE = 1
    BIG_ENDIAN = "big"
    HOST = "0.0.0.0"


class Error:
    NO_ERROR = 0
    INVALID_DATA = 1
    INDEX_OUT_OF_RANGE = 2
    INVALID_RESPONSE_STATUS = 3
    UNEXPECTED_START_MSG = 4
    UNEXPECTED_BOARD_MSG = 5
    WRONG_TURN = 6
    UNEXPECTED_RESPONSE_MSG = 7


class HitStatus:
    NO_HIT = 0
    HIT = 1
    FULL_SHIP = 2


class DataIndex:
    GAME_INIT = 0
    BOARD_SETUP = 1
    HIT_ATTEMPT = 2
    X_COOR = 3
    Y_COOR = 4
    IS_HIT_RESPONSE = 5
    RESPONSE_STATUS = 6
    END_GAME = 7
    ERROR_CODE = 8
