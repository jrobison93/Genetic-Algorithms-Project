# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:02:47 2016

@author: John Robison
"""

from random import randint


board = []
blank_spaces = 0
population = []
max_chromes = 20
max_gens = 10000
end_fitness = 27
generation = 0
min_fitness = 0
ave_fitness = 0
max_fitness = 0
cur_pop = 0
output = open("output.txt", "w")


class chromosome:

    def __init__(self, size):
        self.genomes = []
        self.fitness = 0
        for i in range(size):
            self.genomes.append(randint(1, 9))


def printBoard(given):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("\n-----------")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end='')
            print(given[i][j], end='')

        print()


def fitnessCheck():
    ave_fitness = 0
    max_fitness = 0
    min_fitness = 27
    total_fitness = 0
    for chromo in population:
        assessFitness(chromo)
        total_fitness += chromo.fitness
        max_fitness = max(max_fitness, chromo.fitness)
        min_fitness = min(min_fitness, chromo.fitness)
    ave_fitness = total_fitness / len(population)

    output.write(str(generation) + ", " + str(min_fitness) + ", " +
                 str(max_fitness) + ", " + str(ave_fitness) + "\n")


def assessFitness(chromo):
    score = 27
    temp_board = []
    count = 0

    for i in range(9):
        temp_board.append([])
        for j in range(9):
            if board[i][j] == '-':
                temp_board[i].append(chromo.genomes[count])
                count += 1
            else:
                temp_board[i].append(board[i][j])

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

    chromo.fitness = score


def initPopulation():
    for i in range(max_chromes):
        population[cur_pop].append(chromosome(size=blank_spaces))


print("Reading file to get board:\n")
f = open("board.txt", "r")
for i in range(9):
    board.append(list(f.readline().strip()))

for i in range(9):
    for j in range(9):
        if board[i][j] == '-':
            blank_spaces += 1


def performSelection():
    parent1 = 0
    parent2 = 0
    child1 = 0 
    child2 = 0    

    for i in len(population[cur_pop]):
        child1 = i
        child2 = i + 1
        
        parent1 = selectParent()
        parent2 = selectParent()
        
        performReproduction(parent1, parent2, child1, child2)


printBoard(board)

initPopulation()
fitnessCheck()

while generation < max_gens:
    cur_crossovers = cur_mutations = 0

    performSelection()

    cur_pop = 1 if cur_pop == 0 else 0

    fitnessCheck()

    if generation % 100 == 0:
        print("\tGeneration " + str(generation))
        print("\tmax_fitness = " + str(max_fitness))
        print("\tmin_fitness = " + str(min_fitness))
        print("\tave_fitness = " + str(ave_fitness) + "\n")

    if generation > (max_gens * 0.25):
        if ave_fitness / max_fitness > 0.98:
            print("Converged")
            break

    if max_fitness == end_fitness:
        print("Solution found")
        break

for chromo in population[cur_pop]:
    if chromo.fitness == max_fitness:
        print("The derived solution to this board is: ")
        printChromoBoard(chromo)
