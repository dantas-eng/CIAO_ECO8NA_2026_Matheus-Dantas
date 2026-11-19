# Exercício 2. Cluster Kubernetes com réplicas e nós inteiros
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize


class KubernetesClusterProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([2, 1]),
            xu=np.array([40, 12]),
            vtype=int,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        replicas, nodes = int(x[0]), int(x[1])
        f1_tempo = (600.0 / replicas) + (200.0 / nodes)
        f2_custo = (replicas * 12.0) + (nodes * 85.0)
        out["F"] = [f1_tempo, f2_custo]


algorithm = NSGA2(
    pop_size=25,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True,
)

res = minimize(KubernetesClusterProblem(), algorithm, termination=("n_gen", 35), seed=10)
X = np.atleast_2d(res.X)
F = np.atleast_2d(res.F)
print(f"[LAB 02] solucoes: {len(F)} | inteiras: {np.all(np.isclose(X, np.round(X)))}")
i_tempo = int(np.argmin(F[:, 0]))
i_custo = int(np.argmin(F[:, 1]))
print(
    f"menor tempo: {int(X[i_tempo, 0])} replicas, {int(X[i_tempo, 1])} nodes | "
    f"{F[i_tempo, 0]:.2f} ms | USD {F[i_tempo, 1]:.2f}"
)
print(
    f"menor custo: {int(X[i_custo, 0])} replicas, {int(X[i_custo, 1])} nodes | "
    f"{F[i_custo, 0]:.2f} ms | USD {F[i_custo, 1]:.2f}"
)
