# Gabarito: Aula 11

## Exercício 1
Ver `rpc_servidor_pedidos.py`. O `SimpleXMLRPCServer` padrão é **iterativo**: com `fazer_pedido` levando 2 s, dois clientes simultâneos terminam em ~2 s e ~4 s. Verificação: medir o tempo de cada cliente ou imprimir `threading.current_thread().name` no servidor. Com `ThreadingMixIn`, ambos terminam em ~2 s, e a lista compartilhada passa a exigir `Lock`.

## Exercício 2
Ver `RMICallback.java`. O cliente passa a ser também servidor (exporta `NotificadorImpl`). Paradigma: **callback / comunicação por eventos (notificação assíncrona)**, que inverte o fluxo: em vez de o cliente perguntar repetidamente (polling), o servidor avisa quando o evento ocorre. Observação para rede real: o firewall do cliente precisa aceitar a conexão de volta.

## Exercício 3
Com `durable=True` na fila e `delivery_mode` persistente nas mensagens, o RabbitMQ grava em disco e os 10 pedidos **sobrevivem** ao reinício. Sem essas opções, fila e mensagens ficam só em memória e **se perdem**. Conceito: comunicação **persistente** (Aula 06) oferecida pelo MOM; custo: menor desempenho por causa da escrita em disco.

## Exercício 4
| | RPC | RMI | REST | MOM |
|---|---|---|---|---|
| Acoplamento temporal | alto (os dois ativos) | alto | alto | baixo (fila guarda) |
| Acoplamento de linguagem | depende (XML/JSON-RPC, gRPC: baixo) | alto (só Java) | baixo (HTTP + JSON) | baixo (AMQP, clientes em várias linguagens) |
| Modelo | síncrono | síncrono | síncrono (request/response) | assíncrono |
| Caso de uso | microsserviços internos de alto desempenho (gRPC) | sistemas legados 100% Java | APIs públicas, web e mobile | processamento de pedidos, e-mails, integração entre sistemas |
