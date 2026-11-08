# Gabarito: Aula 12

## Exercício 1
Avaliar a aplicação das três regras: incremento antes de evento/envio; mensagem carrega o relógio; recepção com max + 1. Erro comum: esquecer o "+1" após o max, ou incrementar o relógio do remetente ao receber.

## Exercício 2
Dois eventos são concorrentes quando nenhum vetor é menor ou igual ao outro em todas as posições. Lamport garante apenas "a -> b implica C(a) < C(b)"; a recíproca é falsa, então C(a) < C(b) não distingue "a causou b" de "a e b são concorrentes". O vetor guarda o conhecimento sobre cada processo e permite essa distinção.

## Exercício 3 (com o simulador, contagem aproximada)
* (a) P7 detecta: 1 ELEIÇÃO (para P8), ninguém responde, 6 COORDENADOR: **7 mensagens**. Melhor caso: quem detecta é o maior vivo.
* (b) P1 detecta: cascata de eleições P1, P2, ..., P7; cada uma envia ELEIÇÃO a todos os maiores e recebe OK dos vivos: O(n²), **55 mensagens** no simulador.
* (c) **47 mensagens**; o líder passa a ser P6 (menos processos vivos respondendo OK).
No anel o custo é sempre ~2 voltas (2 x vivos), independente de quem detecta, porém com latência maior (mensagens sequenciais).
Rodar `python eleicao_bully.py 8 7 8`, `python eleicao_bully.py 8 1 8` e `python eleicao_bully.py 8 1 8 7` para conferir os números exatos.

## Exercício 4
Ver `exclusao_centralizada.py`.
| | Centralizado | Ricart e Agrawala |
|---|---|---|
| Mensagens por entrada | 3 | 2(n menos 1) |
| Ponto único de falha | sim (coordenador) | não, mas qualquer falha bloqueia (n pontos de falha) |
| Gargalo | coordenador | não |
| Justiça | FIFO no coordenador | ordem dos carimbos de Lamport |
