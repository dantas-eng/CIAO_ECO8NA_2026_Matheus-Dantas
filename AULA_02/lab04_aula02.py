import random

random.seed(42)

produtos = ['Arroz', 'Feijao', 'Leite', 'Cafe', 'Macarrao', 'Oleo', 'Acucar', 'Biscoito']
precos = [22, 8, 5, 15, 4, 9, 4, 6]
utilidade = [8, 7, 6, 9, 5, 6, 4, 5]
orcamento = 50
n = len(produtos)

for tentativa in range(1, 4):
    combinacao = [random.randint(0, 1) for _ in range(n)]

    custo_total = sum(precos[i] for i in range(n) if combinacao[i] == 1)
    util_total = sum(utilidade[i] for i in range(n) if combinacao[i] == 1)
    valida = custo_total <= orcamento

    print('Combinacao (0=nao compra, 1=compra):', tuple(combinacao))
    print('Custo total: R$', custo_total)
    print('Utilidade total:', util_total)
    print('Respeita orcamento?', valida)
    print('Itens escolhidos:')
    for i in range(n):
        if combinacao[i] == 1:
            print(' -', produtos[i], '| preco:', precos[i], '| utilidade:', utilidade[i])
    print()
