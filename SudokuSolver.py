# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:02:47 2016

@author: John Robison
"""


class chromosome:
    genomes = []
    fitness = 0


def printBoard():
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("\n-----------")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end='')
            print(board[i][j], end='')

        print()


def assessFitness(chromo):
    score = 32
    temp_board = []
    count = 0

    for i in range(9):
        for j in range(9):
            if board[i][j] == '-':
                temp_board[i][j] = chromo.genome[count]
                count += 1

    for i in range(9):
        for j in range(1, 10):
            if temp_board[i].count(j) != 1:
                score -= 1
                break

    cols = []

    for i in range(9):
        cols.append([])
        for j in range(9):
            cols[i].append(temp_board[j][i])

    for i in range(9):
        for j in range(1, 10):
            if cols[i].count(j) != 1:
                score -= 1
                break

    squares = []

    for i in range(3):
        for j in range(3):
            squares.append([])
            for k in range(3):
                for l in range(3):
                    squares[j + 3 * i].append(temp_board[k + 3 * j][l + 3 * i])

    for i in range(9):
        for j in range(1, 10):
            if squares[i].count(j) != 1:
                score -= 1
                break
    
    print(score)
    chromo.fitness = score


board = []
blank_spaces = 0

print("Reading file to get board:\n")
f = open("board.txt", "r")
for i in range(9):
    board.append(list(f.readline().strip()))

for i in range(9):
    for j in range(9):
        if board[i][j] == '-':
            blank_spaces += 1

printBoard()


