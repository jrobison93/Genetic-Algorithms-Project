# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:02:47 2016

@author: John Robison
"""

from random import randint
from random import random
from copy import deepcopy


board = []
blank_spaces = 0
population = []
max_chromes = 21
max_gens = 100000000
end_fitness = 1323
generation = 0
min_fitness = 0
ave_fitness = 0
max_fitness = 0
total_fitness = 0
staleness_factor = 10
staleness_count = 0
previous_max = 0
mutation_probability = 0.95
mutation_change = 0.0025
cur_pop = 0
output = open("output.txt", "w")


# A class that will store Chromosome information such as genomes and fitness
class chromosome:

    def __init__(self, size):
        self.genomes = []
        self.fitness = 0
        for i in range(size):
            self.genomes.append(randint(1, 9))

# Helper function which prints a Sudoku board to the console
def printBoard(given):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("---+---+---")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end='')
            print(given[i][j], end='')

        print()


# Helper function which prints a chromosome as a Sudoku board to the console
def printChromoBoard(chromo):
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

    printBoard(temp_board)


# Determines the fitness of each chromosome in the current population
# Maintains statistics on the populations and stores them to a file
def fitnessCheck():
    global ave_fitness
    ave_fitness = 0
    global max_fitness
    max_fitness = 0
    global min_fitness
    min_fitness = 1323
    global total_fitness
    total_fitness = 0
    for chromo in population[cur_pop]:
        assessFitness(chromo)
        total_fitness += chromo.fitness
        max_fitness = max(max_fitness, chromo.fitness)
        min_fitness = min(min_fitness, chromo.fitness)
    ave_fitness = total_fitness / len(population[cur_pop])

    output.write(str(generation) + ", " + str(min_fitness) + ", " +
                 str(max_fitness) + ", " + str(ave_fitness) + "\n")


# Determines the fitness for an individual chromosome
#
# The fitness is determined by the unique number of values in each row,
# column, and square as well as the consistency of each row, column, and square
def assessFitness(chromo):
    score = 0
    temp_board = []
    count = 0

    for i in range(9):
        temp_board.append([])
        for j in range(9):
            if board[i][j] == '-':
                temp_board[i].append(chromo.genomes[count])
                count += 1
            else:
                temp_board[i].append(int(board[i][j]))

    for i in range(9):
        score += len(set(temp_board[i]))
        consistent = True
        for j in range(1, 10):
            if temp_board[i].count(j) != 1:
                score -= 2 ** temp_board[i].count(j)
                consistent = False
                break
        if consistent:
            score += 40

    cols = []

    for i in range(9):
        cols.append([])
        for j in range(9):
            cols[i].append(temp_board[j][i])

    for i in range(9):
        score += len(set(cols[i]))
        consistent = True
        for j in range(1, 10):
            if cols[i].count(j) != 1:
                score -= 2 ** cols[i].count(j)
                consistent = False
                break
        if consistent:
            score += 40

    squares = []

    for i in range(3):
        for j in range(3):
            squares.append([])
            for k in range(3):
                for l in range(3):
                    squares[j + 3 * i].append(temp_board[k + 3 * j][l + 3 * i])

    for i in range(9):
        score += len(set(squares[i]))
        consistent = True
        for j in range(1, 10):
            if squares[i].count(j) != 1:
                score -= 2 ** squares[i].count(j)
                consistent = False
                break
        if consistent:
            score += 40

    chromo.fitness = score


# Creates the starting population
def initPopulation():
    for i in range(max_chromes):
        population.append([])
        population.append([])
        population[cur_pop].append(chromosome(blank_spaces))
        population[1 if cur_pop == 0 else 0].append(chromosome(blank_spaces))


# Selects the parents and children of the next generation, then creates that
# generation
#
# Maintains the chromosome with the max_fitness between populations
def performSelection():
    parent1 = 0
    parent2 = 0
    child1 = 0
    child2 = 0

    population[cur_pop].sort(key=lambda x: x.fitness, reverse=True)
    next_pop = 1 if cur_pop == 0 else 0

    for i in range(0, len(population[cur_pop]) - 3, 2):
        parent1 = selectParent()
        parent2 = selectParent()
        child1 = i
        child2 = i + 1

        performReproduction(parent1, parent2, child1, child2)

    performReproduction(0, 0, len(population[cur_pop]) - 3,
                        len(population[cur_pop]) - 2)
    population[next_pop][len(population[cur_pop]) - 1] = deepcopy(
        population[cur_pop][0])

# Determines which chromosome should be the parent of a child for the next
# generation. This is done through a roulette-wheel process
def selectParent():
    ret_fitness = 0.0
    fit_marker = random() * total_fitness
    chromo = randint(0, max_chromes - 1)

    while True:
        ret_fitness += population[cur_pop][chromo].fitness

        if ret_fitness >= fit_marker:
            return chromo

        chromo += 1
        if chromo == max_chromes:
            chromo = 0


# When a mommy and a daddy love each other very much, they get split into
# three random parts, mutated, and then Frankensteined back together to
# create their children.
def performReproduction(parent1, parent2, child1, child2):
    cross_point1 = randint(1, len(population[cur_pop][parent1].genomes))
    cross_point2 = randint(cross_point1,
                           len(population[cur_pop][parent1].genomes))
    next_pop = 1 if cur_pop == 0 else 0

    for i in range(0, cross_point1):
        population[next_pop][child1].genomes[i] = mutate(
            population[cur_pop][parent1].genomes[i])
        population[next_pop][child2].genomes[i] = mutate(
            population[cur_pop][parent2].genomes[i])

    for i in range(cross_point1, cross_point2):
        population[next_pop][child1].genomes[i] = mutate(
            population[cur_pop][parent1].genomes[i])
        population[next_pop][child2].genomes[i] = mutate(
            population[cur_pop][parent2].genomes[i])

    for i in range(cross_point2, blank_spaces):
        population[next_pop][child1].genomes[i] = mutate(
            population[cur_pop][parent2].genomes[i])
        population[next_pop][child2].genomes[i] = mutate(
            population[cur_pop][parent1].genomes[i])


# Randomly changes the value of a genome
def mutate(gene):
    prob = random()

    if prob > mutation_probability:
        gene = randint(1, 9)
    return gene

print("Reading file to get board:\n")
f = open("board.txt", "r")
for i in range(9):
    board.append(list(f.readline().strip()))
f.close()

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

        if previous_max == max_fitness:
            if staleness_count >= staleness_factor:
                staleness_count = 0
                mutation_probability -= mutation_change
            else:
                staleness_count += 1
        else:
            staleness_count = 0

        previous_max = max_fitness
        printChromoBoard(population[1 if cur_pop == 0 else 0][0])

    generation += 1

    if generation > (max_gens * 0.25):
        if ave_fitness / max_fitness > 0.98:
            print("Converged")
            break

    if max_fitness >= end_fitness:
        print("Solution found")
        break

for chromo in population[cur_pop]:
    if chromo.fitness == max_fitness:
        print("The derived solution to this board is: ")
        printChromoBoard(chromo)
        break

output.close()
