# Exercício 5. Uma recomendação na fronteira (PseudoWeights)
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.mcdm.pseudo_weights import PseudoWeights
from pymoo.optimize import minimize


class CloudDatabaseProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=np.array([4.0, 100.0]), xu=np.array([128.0, 5000.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        ram, iops = x[0], x[1]
        f1_custo_hora = (ram * 0.45) + (iops * 0.008)
        f2_tempo_query = (200.0 / ram) + (15000.0 / iops)
        out["F"] = [f1_custo_hora, f2_tempo_query]


res5 = minimize(CloudDatabaseProblem(), NSGA2(pop_size=40), ("n_gen", 50), seed=42)
F = np.atleast_2d(res5.F)
X = np.atleast_2d(res5.X)

pesos = np.array([0.30, 0.70])
indice_escolhido = PseudoWeights(pesos).do(F)
melhor_x = X[indice_escolhido]
melhor_f = F[indice_escolhido]

print("Decisao Recomendada (Pesos 30% Custo / 70% Performance):")
print(f"-> Configuracao: {melhor_x[0]:.1f} GB RAM | {melhor_x[1]:.0f} IOPS")
print(f"-> Resultado:    US$ {melhor_f[0]:.2f}/h | Tempo de Query: {melhor_f[1]:.2f} ms")

plt.figure(figsize=(8, 5))
plt.scatter(F[:, 0], F[:, 1], color="lightgray", edgecolor="gray", label="Outras solucoes")
plt.scatter(melhor_f[0], melhor_f[1], color="red", s=150, marker="*", label="Escolhida (MCDM)")
plt.title("Exercicio 5 - Selecao na fronteira")
plt.xlabel("Custo por hora (US$)")
plt.ylabel("Tempo de query (ms)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
saida = os.path.join(os.path.dirname(__file__) or ".", "lab05_mcdm.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("grafico:", saida)
