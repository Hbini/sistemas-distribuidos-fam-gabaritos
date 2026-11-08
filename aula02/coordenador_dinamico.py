"""
Gabarito Aula 02, Exercício 2: distribuição DINÂMICA de tarefas (work queue).

Em vez de dividir o intervalo em N pedaços fixos (um por trabalhador), o
coordenador cria muitos pedaços pequenos e os coloca numa fila. Cada thread
"despachante" pega o próximo pedaço livre e envia ao seu trabalhador assim que
ele termina o anterior. Trabalhadores rápidos acabam fazendo mais pedaços.

Usa os trabalhadores originais (coordenador_trabalhadores.py trabalhador PORTA).
Uso: python coordenador_dinamico.py 127.0.0.1:6001 127.0.0.1:6002
"""
import json
import queue
import socket
import sys
import threading
import time


def enviar_json(s, obj):
    s.sendall((json.dumps(obj) + "\n").encode())


def receber_json(s):
    dados = b""
    while not dados.endswith(b"\n"):
        parte = s.recv(4096)
        if not parte:
            raise ConnectionError("conexão encerrada")
        dados += parte
    return json.loads(dados)


def main(enderecos, limite=2_000_000, pedacos=20):
    fila = queue.Queue()
    tamanho = limite // pedacos
    for i in range(pedacos):
        fila.put((i * tamanho, limite if i == pedacos - 1 else (i + 1) * tamanho))

    total = 0
    contagem = {e: 0 for e in enderecos}
    trava = threading.Lock()

    def despachante(endereco):
        nonlocal total
        host, porta = endereco.split(":")
        while True:
            try:
                inicio, fim = fila.get_nowait()
            except queue.Empty:
                return
            with socket.create_connection((host, int(porta))) as s:
                enviar_json(s, {"inicio": inicio, "fim": fim})
                r = receber_json(s)
            with trava:
                total += r["primos"]
                contagem[endereco] += 1

    t0 = time.perf_counter()
    ths = [threading.Thread(target=despachante, args=(e,)) for e in enderecos]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    print(f"Total de primos: {total} em {time.perf_counter() - t0:.2f}s")
    for e, c in contagem.items():
        print(f"  {e} processou {c} pedaços")


if __name__ == "__main__":
    main(sys.argv[1:])
