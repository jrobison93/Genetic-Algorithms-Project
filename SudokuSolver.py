# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:02:47 2016

@author: John Robison
"""

from random import randint
from random import random


board = []
blank_spaces = 0
population = []
max_chromes = 20
max_gens = 100000
end_fitness = 27
generation = 0
min_fitness = 0
ave_fitness = 0
max_fitness = 0
total_fitness = 0
mutation_probability = 0.60
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
    for chromo in population[cur_pop]:
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
        population.append([])
        population.append([])
        population[cur_pop].append(chromosome(blank_spaces))
        population[1 if cur_pop == 0 else 0].append(chromosome(blank_spaces))


def performSelection():
    parent1 = 0
    parent2 = 0
    child1 = 0
    child2 = 0

    for i in range(0, len(population[cur_pop]), 2):
        parent1 = selectParent()
        parent2 = selectParent()
        child1 = i
        child2 = i + 1

        performReproduction(parent1, parent2, child1, child2)


def selectParent():
    ret_fitness = 0.0
    fit_marker = random() * total_fitness * 0.25
    chromo = 0

    while True:
        ret_fitness += population[cur_pop][chromo].fitness

        if ret_fitness >= fit_marker:
            return chromo

        chromo += 1
        if chromo == max_chromes:
            chromo = 0


def performReproduction(parent1, parent2, child1, child2):
    cross_point = randint(1, blank_spaces)
    next_pop = 1 if cur_pop == 0 else 0

    for i in range(cross_point):
        population[next_pop][child1].genomes[i] = mutate(
            population[cur_pop][parent1].genomes[i])
        population[next_pop][child2].genomes[i] = mutate(
            population[cur_pop][parent2].genomes[i])

    for i in range(cross_point, blank_spaces):
        population[next_pop][child1].genomes[i] = mutate(
            population[cur_pop][parent2].genomes[i])
        population[next_pop][child2].genomes[i] = mutate(
            population[cur_pop][parent1].genomes[i])


def mutate(gene):
    prob = random()

    if prob > mutation_probability:
        gene = randint(1, 9)
    return gene

print("Reading file to get board:\n")
f = open("board.txt", "r")
for i in range(9):
    board.append(list(f.readline().strip()))

for i in range(9):
    for j in range(9):
        if board[i][j] == '-':
            blank_spaces += 1

printBoard(board)

initPopulation()
fitnessCheck()

while generation < max_gens:
    cur_crossovers = cur_mutations = 0

    performSelection()

    cur_pop = 1 if cur_pop == 0 else 0

    fitnessCheck()

    if generation % 1000 == 0:
        print("Generation " + str(generation))
        print("\tmax_fitness = " + str(max_fitness))
        print("\tmin_fitness = " + str(min_fitness))
        print("\tave_fitness = " + str(ave_fitness) + "\n")

    generation += 1

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
