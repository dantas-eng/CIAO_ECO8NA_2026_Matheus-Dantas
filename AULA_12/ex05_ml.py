# Exercício 5. Erro do modelo x tempo de inferência
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class MLTuningProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 10.0]), xu=np.array([30.0, 200.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        depth, n_trees = x[0], x[1]
        f1_erro = 0.5 / (depth * np.log10(n_trees))
        f2_latencia_ms = (depth * 0.2) + (n_trees * 0.5)
        out["F"] = [f1_erro, f2_latencia_ms]


res5 = minimize(MLTuningProblem(), NSGA2(pop_size=30), termination=("n_gen", 40), seed=7)
F = np.atleast_2d(res5.F)
X = np.atleast_2d(res5.X)
print("[EX 05] soluções:", len(F))
i_erro = int(np.argmin(F[:, 0]))
i_lat = int(np.argmin(F[:, 1]))
print(
    f"  menor erro: profundidade {X[i_erro, 0]:.1f}, árvores {X[i_erro, 1]:.1f} | "
    f"erro {F[i_erro, 0]:.4f} | {F[i_erro, 1]:.2f} ms"
)
print(
    f"  menor latência: profundidade {X[i_lat, 0]:.1f}, árvores {X[i_lat, 1]:.1f} | "
    f"erro {F[i_lat, 0]:.4f} | {F[i_lat, 1]:.2f} ms"
)

plt.figure(figsize=(7, 4))
plt.scatter(F[:, 0], F[:, 1], color="purple", s=45)
plt.title("Exercício 5. Erro x tempo de inferência")
plt.xlabel("Erro do modelo")
plt.ylabel("Tempo de resposta (ms)")
plt.grid(True)
saida = os.path.join(os.path.dirname(__file__) or ".", "ex05_erro_latencia.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
