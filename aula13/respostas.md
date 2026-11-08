# Gabarito: Aula 13

## Exercício 1
Soluções aceitáveis: aumentar a tolerância (mais simples); exigir k heartbeats perdidos seguidos; ou **detector adaptativo** que calcula média e desvio padrão dos intervalos de cada nó e define o timeout como média + 3 desvios (ideia do detector "phi accrual", usado no Cassandra e no Akka). Custo: falhas reais demoram mais para ser detectadas (trade-off entre precisão e velocidade de detecção).

## Exercício 2
Ver `quorum.py`. Com N = 3, W = 2 e R = 2, temos W + R = 4 > 3: todo conjunto de leitura intersecta o conjunto da última escrita, e o número de versão identifica o valor mais novo. O sistema tolera 1 réplica fora do ar para leitura e escrita. É o modelo do Dynamo, Cassandra e etcd/Raft (maioria).

## Exercício 3
| Intervalo | Trabalho perdido (pior caso) | Gravações em 1.000 lotes |
|---|---|---|
| 10 | até 9 lotes | 100 |
| 100 | até 99 lotes | 10 |
| 500 | até 499 lotes | 2 |
Escolha depende do custo relativo: se gravar é barato e o processamento caro, intervalos curtos. Resposta justificada com números deve ser aceita (fórmula de Young para o intervalo ótimo: raiz de 2 x custo do checkpoint x tempo médio entre falhas, como curiosidade).

## Exercício 4
* (a) PIX: **CP** (não pode haver saldo divergente nem pagamento duplicado).
* (b) Curtidas: **AP** (um número levemente desatualizado não causa dano).
* (c) Último assento: **CP** (evitar overbooking; melhor recusar).
* (d) Carrinho da Amazon: **AP** (artigo do Dynamo: sempre aceitar "adicionar ao carrinho" e reconciliar depois).
* (e) DNS: **AP** (caches com TTL; propagação eventual).
