# Otimização do custo e da latência entre cinco servidores
# AULA 12 CIAO - AC-4 parte 1 (NSGA-II)

import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize


class DistribuicaoCargaProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=4,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.zeros(4),
            xu=np.ones(4),
        )
        self.custos = np.array([1.2, 2.5, 0.8, 3.0, 1.5])
        self.latencias = np.array([45, 12, 80, 8, 30])

    def _evaluate(self, x, out, *args, **kwargs):
        carga_servidor_5 = max(0.0, 1.0 - np.sum(x))
        cargas = np.append(x, carga_servidor_5)
        custo_total = np.sum(cargas * self.custos)
        latencia_media = np.sum(cargas * self.latencias)
        restricao = np.sum(x) - 1.0
        out["F"] = [custo_total, latencia_media]
        out["G"] = [restricao]


problem = DistribuicaoCargaProblem()

algorithm = NSGA2(
    pop_size=200,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(prob=0.1, eta=20),
    eliminate_duplicates=True,
)

resultado = minimize(
    problem,
    algorithm,
    ("n_gen", 150),
    seed=42,
    verbose=False,
)

if resultado.X is None or resultado.F is None:
    raise RuntimeError("Nenhuma solução viável foi encontrada.")

X = np.atleast_2d(resultado.X)
F = np.atleast_2d(resultado.F)

print("      RESULTADOS DA OTIMIZAÇÃO NSGA-II")
print(f"Soluções não dominadas: {len(F)}")

ordem = np.argsort(F[:, 0])

for posicao, indice in enumerate(ordem[:10], start=1):
    x = X[indice]
    carga_5 = max(0.0, 1.0 - np.sum(x))
    cargas = np.append(x, carga_5)
    percentuais = cargas * 100
    custo, latencia = F[indice]
    print(f"\nSolução {posicao}")
    print(f"Distribuição: {np.round(percentuais, 1)}")
    print(f"Custo: US$ {custo:.2f}/h")
    print(f"Latência: {latencia:.2f} ms")

plt.figure(figsize=(9, 6))
plt.scatter(F[:, 0], F[:, 1], s=35, label="Soluções não dominadas")
plt.xlabel("Custo estimado (US$/h)")
plt.ylabel("Latência média (ms)")
plt.title("NSGA-II - Aproximação da Fronteira de Pareto")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
saida = os.path.join(os.path.dirname(__file__) or ".", "fronteira_pareto.png")
plt.savefig(saida, dpi=110)
plt.close()
print(f"\nGráfico salvo: {saida}")
print(f"Menor custo na fronteira: US$ {F[:, 0].min():.2f}/h | latência {F[np.argmin(F[:, 0]), 1]:.2f} ms")
print(f"Menor latência na fronteira: {F[:, 1].min():.2f} ms | custo US$ {F[np.argmin(F[:, 1]), 0]:.2f}/h")
