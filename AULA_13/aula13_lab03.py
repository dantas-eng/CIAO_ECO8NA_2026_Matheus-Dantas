# Exercício 3. Exploração (eta baixo) contra explotação (eta alto)
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize


class BenchmarkTradeoffProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([0.1, 0.1]), xu=np.array([10.0, 10.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0] ** 2 + x[1]
        f2 = (10.0 / x[0]) + (5.0 / x[1])
        out["F"] = [f1, f2]


problem = BenchmarkTradeoffProblem()

alg_exploracao = NSGA2(
    pop_size=30,
    crossover=SBX(prob=0.9, eta=5),
    mutation=PM(prob=0.5, eta=5),
)
alg_explotacao = NSGA2(
    pop_size=30,
    crossover=SBX(prob=0.9, eta=30),
    mutation=PM(prob=0.05, eta=30),
)

res_a = minimize(problem, alg_exploracao, ("n_gen", 20), seed=42)
res_b = minimize(problem, alg_explotacao, ("n_gen", 20), seed=42)
Fa = np.atleast_2d(res_a.F)
Fb = np.atleast_2d(res_b.F)
print(f"[LAB 03] A: {len(Fa)} pontos | f1 {Fa[:, 0].min():.2f}-{Fa[:, 0].max():.2f}")
print(f"[LAB 03] B: {len(Fb)} pontos | f1 {Fb[:, 0].min():.2f}-{Fb[:, 0].max():.2f}")

plt.figure(figsize=(8, 5))
plt.scatter(Fa[:, 0], Fa[:, 1], color="orange", label="Config A: eta=5", alpha=0.8, s=60)
plt.scatter(Fb[:, 0], Fb[:, 1], color="navy", marker="x", label="Config B: eta=30", s=60)
plt.title("Exercicio 3 - SBX/PM em 20 geracoes")
plt.xlabel("Objetivo 1")
plt.ylabel("Objetivo 2")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
saida = os.path.join(os.path.dirname(__file__) or ".", "lab03_operadores.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("grafico:", saida)
