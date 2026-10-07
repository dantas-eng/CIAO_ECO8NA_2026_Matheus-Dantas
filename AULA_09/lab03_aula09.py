"""
Lab 03 - Aula 09 (AC-3 Sprint 1): sistema de inferencia fuzzy DO ZERO (so NumPy + Matplotlib)
Problema: risco de evasao de um aluno a partir de FREQUENCIA (%) e DESEMPENHO (nota 0-10).
Saida: risco de evasao (0-100 %).
Execucao: python lab03_aula09.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1) Universos de discurso (com unidade) ----------
U = {
    "frequencia": np.linspace(0, 100, 1001),   # % de presenca
    "desempenho": np.linspace(0, 10, 1001),    # nota media 0-10
    "risco": np.linspace(0, 100, 1001),        # % de risco de evasao
}


def tri(x, a, b, c):
    """Triangular: sobe a->b, desce b->c."""
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)


def trap(x, a, b, c, d):
    """Trapezoidal: sobe a->b, platô b->c, desce c->d (a==b ou c==d vira 'ombro')."""
    up = (x >= b).astype(float) if a == b else np.clip((x - a) / (b - a), 0, 1)
    down = (x <= c).astype(float) if c == d else np.clip((d - x) / (d - c), 0, 1)
    return np.minimum(up, down)


# ---------- 2) Termos linguisticos e funcoes de pertinencia ----------
x_f, x_d, x_r = U["frequencia"], U["desempenho"], U["risco"]
MF = {
    "frequencia": {"baixa": trap(x_f, 0, 0, 55, 75), "media": tri(x_f, 60, 75, 90), "alta": trap(x_f, 80, 90, 100, 100)},
    "desempenho": {"baixo": trap(x_d, 0, 0, 3, 5), "medio": tri(x_d, 3, 5.5, 8), "alto": trap(x_d, 6, 8, 10, 10)},
    "risco": {"baixo": trap(x_r, 0, 0, 15, 35), "medio": tri(x_r, 25, 50, 75), "alto": trap(x_r, 65, 85, 100, 100)},
}


def mu(var, termo, valor):
    """Fuzzificacao: grau de pertinencia de um valor crisp em um termo."""
    return float(np.interp(valor, U[var], MF[var][termo]))


# ---------- 3) Base de regras (E = min, OU = max) ----------
# cada regra: (descricao, funcao(f, d) -> forca de disparo, termo de saida)
REGRAS = [
    ("R1 SE freq baixa E desemp baixo ENTAO risco alto", lambda f, d: min(f["baixa"], d["baixo"]), "alto"),
    ("R2 SE freq baixa E desemp medio ENTAO risco alto", lambda f, d: min(f["baixa"], d["medio"]), "alto"),
    ("R3 SE freq baixa E desemp alto  ENTAO risco medio", lambda f, d: min(f["baixa"], d["alto"]), "medio"),
    ("R4 SE freq media E desemp baixo ENTAO risco alto", lambda f, d: min(f["media"], d["baixo"]), "alto"),
    ("R5 SE freq media E desemp medio ENTAO risco medio", lambda f, d: min(f["media"], d["medio"]), "medio"),
    ("R6 SE freq media E desemp alto  ENTAO risco baixo", lambda f, d: min(f["media"], d["alto"]), "baixo"),
    ("R7 SE freq alta  E desemp baixo ENTAO risco medio", lambda f, d: min(f["alta"], d["baixo"]), "medio"),
    ("R8 SE freq alta  E (desemp medio OU desemp alto) ENTAO risco baixo",
     lambda f, d: min(f["alta"], max(d["medio"], d["alto"])), "baixo"),
]


def inferir(freq, nota):
    f = {t: mu("frequencia", t, freq) for t in MF["frequencia"]}
    d = {t: mu("desempenho", t, nota) for t in MF["desempenho"]}
    agregado = np.zeros_like(x_r)
    for nome, regra, saida in REGRAS:
        forca = regra(f, d)
        agregado = np.maximum(agregado, np.minimum(forca, MF["risco"][saida]))  # implicacao (corte) + agregacao (max)
    if agregado.sum() == 0:
        raise ValueError(f"nenhuma regra disparou para ({freq}, {nota})")
    risco = float((x_r * agregado).sum() / agregado.sum())                      # centroide
    return risco


def faixa(r):
    return "baixo" if r < 33 else ("medio" if r < 66 else "alto")


# ---------- 4) Testes (entrada -> saida do sistema x resposta esperada) ----------
CASOS = [  # (frequencia %, nota, faixa esperada, descricao)
    (95, 9.0, "baixo", "aluno assiduo e com notas altas"),
    (50, 2.0, "alto", "faltoso e com notas baixas"),
    (75, 5.5, "medio", "no limite de presenca e nota mediana"),
    (92, 3.0, "medio", "assiduo, mas com notas baixas"),
]

if __name__ == "__main__":
    print(f"{'freq':>5} {'nota':>5} | {'risco':>6} | {'obtido':<6} | {'esperado':<8} | resultado")
    ok = 0
    for fr, nt, esp, desc in CASOS:
        r = inferir(fr, nt)
        passou = faixa(r) == esp
        ok += passou
        print(f"{fr:>5} {nt:>5} | {r:6.2f} | {faixa(r):<6} | {esp:<8} | {'OK' if passou else 'FALHOU'}  ({desc})")
    print(f"\n{ok}/{len(CASOS)} casos dentro do esperado")

    # ---------- graficos ----------
    fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
    for a, (var, tit) in zip(ax, [("frequencia", "Frequencia (%)"), ("desempenho", "Desempenho (nota 0-10)"), ("risco", "Risco de evasao (%)")]):
        for nome, m in MF[var].items():
            a.plot(U[var], m, lw=2, label=nome)
        a.set_title(tit); a.set_ylabel("pertinencia"); a.legend(); a.grid(alpha=.3)
    plt.tight_layout(); plt.savefig("lab03_funcoes_pertinencia.png", dpi=110)
    print("\nGrafico salvo: lab03_funcoes_pertinencia.png")
