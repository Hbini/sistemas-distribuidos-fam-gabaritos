# Gabarito: Aula 03

## Exercício 1
Python: 2 linhas no dicionário `OPERACOES` (ver `replica_com_heartbeat.py`). Java: 2 entradas no `Map.of(...)`:
```java
"POT", (a, b) -> Math.pow(a, b),
"MOD", (a, b) -> a % b
```
O cliente não muda, pois envia a operação como texto. Isso caracteriza um **sistema aberto/flexível**: interfaces publicadas e extensão sem reescrever o restante.

## Exercício 2
Solução em `servico_nomes_heartbeat.py` + `replica_com_heartbeat.py`. Conceitos: detecção de falhas por heartbeat e timeout; trade-off da tolerância (muito curta gera falsos positivos; muito longa deixa réplicas mortas na lista por mais tempo).

## Exercício 3
Disponibilidade observada: depende do experimento; com failover deve ficar próxima de 100% enquanto houver ao menos uma réplica viva.
Teórica com 3 réplicas de 95%: 1 menos (0,05)^3 = 1 menos 0,000125 = **99,9875%**. Com 1 réplica: 95%; com 2: 99,75%.

## Exercício 4
Exemplos aceitáveis: acesso (abrir arquivo do OneDrive no Explorer como se fosse local); localização (URL www.google.com não revela o servidor); migração (VM do provedor de nuvem movida sem o usuário perceber); relocação (chamada de celular que troca de antena em movimento); replicação (CDN da Netflix); concorrência (Google Docs com várias pessoas editando); falha (WhatsApp reenviando mensagem quando a rede volta). Avaliar a coerência da justificativa.
