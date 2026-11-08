# Gabarito: Aula 05

## Exercício 1
Ver `servico_pagamentos.py`. No gateway: incluir `"pagamentos": os.environ.get("PAGAMENTOS_URL", "http://localhost:8004")` em `ROTAS`. No compose:
```yaml
  pagamentos:
    build: { context: ., dockerfile: python.Dockerfile }
    command: python servico_pagamentos.py
    environment: { PORTA: "8004" }
```
e `PAGAMENTOS_URL: http://pagamentos:8004` nos serviços pedidos e gateway.

## Exercício 2
Sem compensação, o estoque fica baixado para um pedido que não existe (inconsistência). Como cada serviço tem seu banco, não há transação ACID única. O padrão **Saga** divide a operação em passos locais, cada um com uma **ação compensatória** que desfaz o efeito quando um passo posterior falha (orquestrada pelo serviço de pedidos, ou coreografada por eventos). A consistência obtida é **eventual**. Trechos em `trecho_pedidos_saga_retry.py` e `TrechoEstoqueDevolver.java`.

## Exercício 3
Estratégia: **backoff exponencial** (a espera dobra a cada tentativa; em produção, adiciona-se "jitter" aleatório). Repetir indefinidamente aumenta a carga sobre um serviço que já está com problema (efeito tempestade), prende threads e aumenta a latência para o usuário; por isso combina-se retry com limite de tentativas e **circuit breaker**.

## Exercício 4
| Critério | Monólito | Microsserviços |
|---|---|---|
| Implantação | um pacote só | cada serviço independente |
| Escalabilidade | escala tudo junto | escala só o serviço sobrecarregado |
| Isolamento de falhas | erro pode derrubar tudo | falha fica contida no serviço |
| Consistência | transação ACID local | consistência eventual, Sagas |
| Complexidade operacional | baixa | alta (rede, observabilidade, deploy, containers) |

Para a lanchonete da faculdade (pouco tráfego, equipe pequena), um **monólito bem modularizado** é mais adequado; microsserviços só compensam quando há escala, equipes independentes e necessidade de implantação separada.
