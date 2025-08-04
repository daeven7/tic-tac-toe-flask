import numpy as np

def board_to_array(board):
    board_array = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                board_array[i][j] = -1
            elif board[i][j] == 'O':
                board_array[i][j] = 1
            elif board[i][j] == '' or board[i][j] is None:
                board_array[i][j] = 0
            else:
                raise ValueError(f"Invalid board value: {board[i][j]}")
    return board_array

def array_to_board(board_array):
    board = []
    for i in range(3):
        row = []
        for j in range(3):
            if board_array[i][j] == -1:
                row.append('X')
            elif board_array[i][j] == 1:
                row.append('O')
            else:
                row.append('')
        board.append(row)
    return board 