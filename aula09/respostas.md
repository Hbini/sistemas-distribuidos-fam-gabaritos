# Gabarito: Aula 09

## Exercício 1
Alteração no `no_p2p.py`: acrescentar `p.add_argument("--host", default="127.0.0.1")` e passar para o construtor, usando `self.endereco = f"{host}:{porta}"`. O IP pode ser obtido com `ipconfig`/`ip a` ou automaticamente:
```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]
```
(o `connect` em UDP não envia nada; só descobre qual interface seria usada). Avaliar o desenho da topologia e a contagem de mensagens (contador incrementado em `_tratar`).

## Exercício 2
O dono responde `BAIXAR` com o conteúdo (usando o enquadramento da Aula 08, Exercício 2). A transferência direta é essencial porque a busca é leve (poucos bytes) mas o arquivo é pesado: se o conteúdo passasse por todos os intermediários, a banda total consumida cresceria com o número de saltos. No BitTorrent, além disso, o arquivo é dividido em pedaços baixados de vários peers ao mesmo tempo.

## Exercício 3
(1) **Eleger um novo sequenciador** quando o atual falhar (detecção por heartbeat + algoritmo de eleição como Bully ou Anel, Aula 12), retomando a numeração a partir do último número confirmado. (2) **Ordem total sem sequenciador central**: algoritmos distribuídos como ISIS (cada membro propõe um número e adota-se o maior) ou ordenação por relógio de Lamport com desempate pelo id do processo. Também é possível usar consenso (Raft/Paxos) para decidir a ordem.

## Exercício 4
Sem repetições, cada salto multiplica por até 4 (na prática, por 3, pois não se devolve a quem enviou; ambas as respostas são aceitáveis se justificadas):
* Fator 4: TTL 1 = 4; TTL 2 = 4 + 16 = 20; TTL 3 = 84; TTL 4 = 340 mensagens.
* Fator 3 após o primeiro salto: 4; 16; 52; 160.
O crescimento é **exponencial** no TTL, por isso a inundação não escala. DHTs como Chord e Kademlia organizam os nós em uma estrutura (anel ou métrica XOR) que permite localizar uma chave em **O(log N)** saltos.
