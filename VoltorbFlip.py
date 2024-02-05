import random

def create_board():
    board = []
    for row in range(0,5):
        board.append([])
        for col in range(0,5):
            board[row].append(random.randint(0,3))
    return board

def get_totals(board):
    totals = [[],[]]
    for row in range(0,5):
        rowTotal = sum(board[row])
        totals[1].append(rowTotal)
    for col in range(0,5):
        colTotal = 0
        for row in range(0,5):
            colTotal += board[row][col]
        totals[0].append(colTotal)
    return totals

def get_voltorbs(board):
    voltorbs = [[],[]]
    for row in range(0,5):
        rowTotal = board[row].count(0)
        voltorbs[1].append(rowTotal)
    for col in range(0,5):
        colTotal = 0
        for row in range(0,5):
            if board[row][col] == 0:
                colTotal += 1
        voltorbs[0].append(colTotal)
    return voltorbs
