# resultados - aula 12 (AC-4 parte 1 - NSGA-II)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 04/11/2026

Cinco servidores, 100% da carga. Objetivos: custo por hora e latência média, os dois para baixo. Código em `demo_nsga2.py` (NSGA-II, população 200, 150 gerações, seed 42). Gráfico: `fronteira_pareto.png`.

Servidores: 1 (1,20 e 45 ms), 2 (2,50 e 12 ms), 3 (0,80 e 80 ms), 4 (3,00 e 8 ms), 5 (1,50 e 30 ms).

## Saída

```
Soluções não dominadas: 200

Solução 1
Distribuição: [ 0.5  0.  99.5  0.   0. ]
Custo: US$ 0.80/h
Latência: 79.80 ms

Solução 2
Distribuição: [ 0.2  0.  98.7  0.1  0.9]
Custo: US$ 0.81/h
Latência: 79.36 ms

Solução 10
Distribuição: [ 4.6  0.1 90.6  0.   4.7]
Custo: US$ 0.85/h
Latência: 75.98 ms

Menor custo na fronteira: US$ 0.80/h | latência 79.80 ms
Menor latência na fronteira: 9.61 ms | custo US$ 2.80/h
```

A de menor custo ficou em `[0.5, 0, 99.5, 0, 0]`. A de menor latência ficou em `[0, 39.8, 0, 60.2, 0]`.

O extremo teórico de custo é 100% no servidor 3 (US$ 0,80/h e 80 ms). A execução chegou perto: 99,5% nele, US$ 0,80/h e 79,80 ms. O extremo de latência seria 100% no servidor 4 (US$ 3,00/h e 8 ms). A fronteira parou em 9,61 ms e US$ 2,80/h, misturando o servidor 2 (39,8%) com o 4 (60,2%). É aproximação, não a fronteira exata.

## Respostas

1. Menor custo: quase toda a carga no servidor 3 (99,5%), com 0,5% no servidor 1. US$ 0,80/h e 79,80 ms.

2. Menor latência: 60,2% no servidor 4 e 39,8% no servidor 2. 9,61 ms e US$ 2,80/h.

3. A opção barata usa o servidor mais lento. 80 ms pode ser ruim se a prioridade for resposta. O custo baixo não decide sozinho.

4. Cada ponto do gráfico é uma distribuição que nenhuma outra da população bate nos dois objetivos ao mesmo tempo. Eixo x é o custo, eixo y é a latência.

5. O NSGA-II devolve várias soluções porque custo e latência puxam para lados opostos. A empresa escolhe depois, conforme o que pesa mais.

6. A crowding distance mede o quanto uma solução está isolada na fronteira. Quem está num trecho vazio tem mais chance de continuar, para a fronteira não virar um monte de pontos iguais.
