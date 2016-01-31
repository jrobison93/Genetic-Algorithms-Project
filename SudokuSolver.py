# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:02:47 2016

@author: John Robison
"""


class chromosome:
    genomes = []


def printBoard():
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("\n-----------")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end='')
            print(board[i][j], end='')

        print()

board = []
print("Reading file to get board:\n")
f = open("board.txt", "r")
for i in range(9):
    board.append(list(f.readline().strip()))

printBoard()
