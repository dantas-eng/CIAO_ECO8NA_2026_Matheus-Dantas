# LAB 04 - ACO: Feromônio, Evaporação e Atratividade
# AULA 07 CIAO - AC2 Parte 2

import numpy as np

latency_matrix = np.array([
    [0, 5, 2, 9],
    [5, 0, 3, 1],
    [2, 3, 0, 7],
    [9, 1, 7, 0],
])

num_nodes = len(latency_matrix)
pheromone = np.ones((num_nodes, num_nodes))
rho = 0.25


def update_pheromone(pheromone_matrix, paths, costs, rho):
    pheromone_matrix = pheromone_matrix * (1 - rho)

    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            pheromone_matrix[u][v] += 1.0 / cost

    return pheromone_matrix


mock_paths = [[0, 2, 1, 3], [0, 1, 3]]
mock_costs = [6.0, 6.0]

updated_pheromone = update_pheromone(pheromone, mock_paths, mock_costs, rho)
print("[LAB 04 - SUCESSO] Matriz de Feromônio Atualizada:")
print(updated_pheromone)
