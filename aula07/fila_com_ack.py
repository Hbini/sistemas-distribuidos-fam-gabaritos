"""
Gabarito Aula 07, Exercício 2: fila com ACK e reentrega por timeout (at-least-once).

Protocolo: PUT <fila> <msg> -> OK | GET <fila> -> MSG <id> <msg> ou VAZIA | ACK <id> -> OK
    python fila_com_ack.py broker
    python fila_com_ack.py produtor cozinha 5
    python fila_com_ack.py consumidor cozinha Chef-A
    python fila_com_ack.py consumidor-falho cozinha Chef-B   (pega e "trava", sem ACK)
"""
import collections
import itertools
import socket
import sys
import threading
import time

PORTA = 9401
PRAZO = 5.0
filas = collections.defaultdict(collections.deque)
em_processamento = {}                  # id -> (fila, msg, instante do GET)
ids = itertools.count(1)
trava = threading.Lock()


def vigia():
    while True:
        time.sleep(1)
        agora = time.time()
        with trava:
            for i, (fila, msg, t) in list(em_processamento.items()):
                if agora - t > PRAZO:
                    del em_processamento[i]
                    filas[fila].appendleft((i, msg))
                    print(f"[broker] sem ACK para {i} ({msg}); voltou para a fila")


def atender(c):
    with c, c.makefile("r") as f:
        for linha in f:
            p = linha.rstrip("\n").split(" ", 2)
            with trava:
                if p[0] == "PUT":
                    filas[p[1]].append((next(ids), p[2]))
                    r = "OK"
                elif p[0] == "GET":
                    if filas[p[1]]:
                        i, msg = filas[p[1]].popleft()
                        em_processamento[i] = (p[1], msg, time.time())
                        r = f"MSG {i} {msg}"
                    else:
                        r = "VAZIA"
                elif p[0] == "ACK":
                    em_processamento.pop(int(p[1]), None)
                    r = "OK"
                else:
                    r = "ERRO"
            c.sendall((r + "\n").encode())


def broker():
    threading.Thread(target=vigia, daemon=True).start()
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORTA))
    srv.listen()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=atender, args=(c,), daemon=True).start()


def cliente(modo, fila, arg):
    with socket.create_connection(("127.0.0.1", PORTA)) as s, s.makefile("r") as r:
        if modo == "produtor":
            for i in range(1, int(arg) + 1):
                s.sendall(f"PUT {fila} pedido-{i}\n".encode())
                r.readline()
            return
        while True:
            s.sendall(f"GET {fila}\n".encode())
            resp = r.readline().strip()
            if resp == "VAZIA":
                time.sleep(0.5)
                continue
            _, i, msg = resp.split(" ", 2)
            print(f"[{arg}] processando {msg}")
            if modo == "consumidor-falho":
                print(f"[{arg}] travei! (não vou mandar ACK)")
                time.sleep(3600)
            time.sleep(1)
            s.sendall(f"ACK {i}\n".encode())
            r.readline()


if __name__ == "__main__":
    broker() if sys.argv[1] == "broker" else cliente(sys.argv[1], sys.argv[2], sys.argv[3])
