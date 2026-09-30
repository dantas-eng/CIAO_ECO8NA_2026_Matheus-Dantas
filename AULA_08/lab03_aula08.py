# LAB 03 - ACO para topologia de rede (árvore geradora)
# AULA 08 CIAO - fechamento AC-2

import numpy as np

np.random.seed(42)

N = 10
NUM_ANTS = 25
ITERATIONS = 80
ALPHA = 1.0
BETA = 2.5
RHO = 0.2
Q = 1.0

D = np.array(
    [
        [0, 12, 9, 15, 20, 18, 25, 22, 30, 28],
        [12, 0, 8, 11, 14, 16, 19, 24, 21, 26],
        [9, 8, 0, 7, 13, 10, 17, 15, 18, 20],
        [15, 11, 7, 0, 6, 9, 12, 14, 16, 19],
        [20, 14, 13, 6, 0, 5, 8, 11, 13, 15],
        [18, 16, 10, 9, 5, 0, 7, 10, 12, 14],
        [25, 19, 17, 12, 8, 7, 0, 4, 9, 11],
        [22, 24, 15, 14, 11, 10, 4, 0, 6, 8],
        [30, 21, 18, 16, 13, 12, 9, 6, 0, 5],
        [28, 26, 20, 19, 15, 14, 11, 8, 5, 0],
    ],
    dtype=float,
)

CRITICAL_PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]


def edges_to_adj(edges):
    adj = np.zeros((N, N), dtype=int)
    for i, j in edges:
        adj[i, j] = 1
        adj[j, i] = 1
    return adj


def build_adj_list(edges):
    graph = [[] for _ in range(N)]
    for i, j in edges:
        w = D[i, j]
        graph[i].append((j, w))
        graph[j].append((i, w))
    return graph


def path_latency(graph, src, dst):
    if src == dst:
        return 0.0
    visited = {src}
    queue = [(src, 0.0)]
    while queue:
        node, cost = queue.pop(0)
        for nxt, w in graph[node]:
            if nxt in visited:
                continue
            if nxt == dst:
                return cost + w
            visited.add(nxt)
            queue.append((nxt, cost + w))
    return float("inf")


def total_critical_latency(edges):
    graph = build_adj_list(edges)
    return sum(path_latency(graph, i, j) for i, j in CRITICAL_PAIRS)


def random_spanning_tree():
    in_tree = {0}
    edges = []
    while len(in_tree) < N:
        outside = [n for n in range(N) if n not in in_tree]
        i = np.random.choice(list(in_tree))
        j = np.random.choice(outside)
        edges.append((min(i, j), max(i, j)))
        in_tree.add(j)
    return edges


def construct_ant_solution(pheromone):
    start = np.random.randint(0, N)
    in_tree = {start}
    edges = []
    while len(in_tree) < N:
        candidates = []
        for i in in_tree:
            for j in range(N):
                if j in in_tree or i == j:
                    continue
                tau = pheromone[i, j] ** ALPHA
                eta = (1.0 / D[i, j]) ** BETA
                candidates.append((i, j, tau * eta))
        total = sum(c[2] for c in candidates)
        r = np.random.rand() * total
        acc = 0.0
        chosen = candidates[-1]
        for cand in candidates:
            acc += cand[2]
            if acc >= r:
                chosen = cand
                break
        i, j, _ = chosen
        edges.append((min(i, j), max(i, j)))
        in_tree.add(j)
    return edges


def is_valid_tree(edges):
    if len(edges) != N - 1:
        return False
    adj = edges_to_adj(edges)
    seen = {0}
    queue = [0]
    while queue:
        u = queue.pop()
        for v in range(N):
            if adj[u, v] and v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == N


def run_aco():
    pheromone = np.ones((N, N), dtype=float)
    np.fill_diagonal(pheromone, 0.0)
    best_edges = None
    best_cost = float("inf")

    for _ in range(ITERATIONS):
        iteration_solutions = []
        for _ in range(NUM_ANTS):
            edges = construct_ant_solution(pheromone)
            if not is_valid_tree(edges):
                continue
            cost = total_critical_latency(edges)
            iteration_solutions.append((edges, cost))

        if not iteration_solutions:
            continue

        iteration_solutions.sort(key=lambda x: x[1])
        best_iter_edges, best_iter_cost = iteration_solutions[0]

        if best_iter_cost < best_cost:
            best_cost = best_iter_cost
            best_edges = best_iter_edges

        pheromone *= 1.0 - RHO
        deposit = Q / best_iter_cost
        for i, j in best_iter_edges:
            pheromone[i, j] += deposit
            pheromone[j, i] += deposit

    return best_edges, best_cost


print("[LAB 03 - ACO topologia de rede]")
best_edges, aco_cost = run_aco()
adj_final = edges_to_adj(best_edges)

print("\nMatriz de adjacência final (10x10):")
print(adj_final)

random_costs = [total_critical_latency(random_spanning_tree()) for _ in range(30)]
random_mean = float(np.mean(random_costs))
gain_pct = (random_mean - aco_cost) / random_mean * 100.0

print(f"\nLatência acumulada (pares críticos) — ACO: {aco_cost:.2f}")
print(f"Latência média topologia aleatória (30 amostras): {random_mean:.2f}")
print(f"Ganho percentual do ACO: {gain_pct:.2f}%")
print(f"Árvore válida: {is_valid_tree(best_edges)}")
