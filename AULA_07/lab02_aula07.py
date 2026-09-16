# LAB 02 - Algoritmo Genético (Problema da Mochila)
# AULA 07 CIAO - AC2 Parte 2

import numpy as np

np.random.seed(42)

weights = np.array([12, 2, 1, 4, 1])
values = np.array([4, 2, 1, 10, 2])
max_weight = 15

pop_size = 10
num_genes = len(weights)
generations = 10
mutation_rate = 0.1

population = np.random.randint(0, 2, size=(pop_size, num_genes))


def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)
    if total_weight > max_weight:
        return 0
    return total_value


def tournament_selection(pop, fitnesses):
    idx1, idx2 = np.random.choice(len(pop), 2, replace=False)
    if fitnesses[idx1] >= fitnesses[idx2]:
        return pop[idx1].copy()
    return pop[idx2].copy()


def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2


def mutate(ind):
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            ind[i] = 1 - ind[i]
    return ind


for g in range(generations):
    fitnesses = np.array([calculate_fitness(ind) for ind in population])
    new_population = []

    for _ in range(pop_size // 2):
        p1 = tournament_selection(population, fitnesses)
        p2 = tournament_selection(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.extend([mutate(c1), mutate(c2)])

    population = np.array(new_population)

best_idx = np.argmax([calculate_fitness(ind) for ind in population])
best_ind = population[best_idx]
best_fit = calculate_fitness(best_ind)

print("[LAB 02 - SUCESSO]")
print(f"Melhor indivíduo: {best_ind.tolist()} | Fitness: {best_fit}")
print(f"Peso total: {np.sum(best_ind * weights)} | Valor total: {np.sum(best_ind * values)}")
