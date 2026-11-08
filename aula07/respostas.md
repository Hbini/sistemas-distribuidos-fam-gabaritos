# Gabarito: Aula 07

## Exercício 1
Ver `broker_pubsub_curinga.py`: a única mudança relevante é a função `casa(padrao, topico)`, usada em `publicar`. Sistemas reais: RabbitMQ (topic exchange com `*` e `#`) e MQTT (`+` e `#`).

## Exercício 2
Ver `fila_com_ack.py`. Garantia obtida: **at-least-once** (pelo menos uma vez). Se o consumidor processar e travar antes do ACK, a mensagem será reentregue e processada duas vezes; por isso o processamento deve ser **idempotente** (ou usar deduplicação por id). Exactly-once exige mecanismos adicionais (transações ou deduplicação no consumidor).

## Exercício 3
Ver `ConsumidorFila.java`. Os pedidos são divididos entre o Chef Python e o Chef Java, comprovando que a fila desacopla a linguagem dos participantes.

## Exercício 4
* (a) **Pub/sub**: um evento para muitos interessados (Firebase Cloud Messaging funciona assim).
* (b) **Fila**: cada e-mail deve ser enviado uma única vez; os 5 servidores competem pelas mensagens e a carga se equilibra.
* (c) **Cliente/servidor** síncrono (request/response): o cliente precisa da resposta na hora e consistente.
* (d) **Memória compartilhada** com sincronização (trava ou variável atômica): mesma máquina, baixa latência.
