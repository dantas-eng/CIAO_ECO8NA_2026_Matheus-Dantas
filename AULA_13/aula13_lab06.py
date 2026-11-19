# Exercício 6. Escala hospitalar: inteiros, restrição e MCDM
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.mcdm.pseudo_weights import PseudoWeights
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize


class EscalaHospitalarProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([2, 4]),
            xu=np.array([20, 40]),
            vtype=int,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        medicos, enfermeiros = int(x[0]), int(x[1])
        f1_custo = (medicos * 1200.0) + (enfermeiros * 450.0)
        f2_espera = (180.0 / medicos) + (240.0 / enfermeiros)
        g1 = f2_espera - 25.0
        out["F"] = [f1_custo, f2_espera]
        out["G"] = [g1]


algorithm = NSGA2(
    pop_size=40,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True,
)

res6 = minimize(EscalaHospitalarProblem(), algorithm, termination=("n_gen", 50), seed=42)
opt = res6.opt
F = np.atleast_2d(opt.get("F"))
X = np.atleast_2d(opt.get("X"))
G = np.atleast_2d(opt.get("G"))
ok = G[:, 0] <= 1e-6
F, X = F[ok], X[ok]

pesos = np.array([0.40, 0.60])
indice = PseudoWeights(pesos).do(F)
escolha_x = X[indice]
escolha_f = F[indice]

print(f"[LAB 06] viaveis: {len(F)}")
print(
    f"Escala recomendada (40% custo, 60% espera): "
    f"{int(escolha_x[0])} medicos, {int(escolha_x[1])} enfermeiros"
)
print(f"Custo: R$ {escolha_f[0]:.2f} | Espera: {escolha_f[1]:.2f} min")
print(f"Respeita espera <= 25: {escolha_f[1] <= 25.0}")
