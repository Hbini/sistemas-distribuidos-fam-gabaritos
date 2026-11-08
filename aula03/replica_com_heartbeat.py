"""
Gabarito Aula 03, Exercícios 1 e 2: réplica com POT e MOD e envio de heartbeat.
Uso: python replica_com_heartbeat.py 7001
"""
import socket
import sys
import threading
import time

OPERACOES = {
    "SOMA": lambda a, b: a + b,
    "SUB": lambda a, b: a - b,
    "MULT": lambda a, b: a * b,
    "DIV": lambda a, b: a / b,
    "POT": lambda a, b: a ** b,     # Exercício 1: só duas linhas novas
    "MOD": lambda a, b: a % b,
}


def heartbeat(porta):
    while True:
        try:
            with socket.create_connection(("127.0.0.1", 5000), timeout=2) as s:
                s.sendall(f"VIVO calculadora 127.0.0.1 {porta}\n".encode())
                s.recv(10)
        except OSError:
            print("[heartbeat] serviço de nomes indisponível")
        time.sleep(2)


def atender(c, ident):
    with c, c.makefile("r") as f:
        for linha in f:
            p = linha.split()
            try:
                r = f"{OPERACOES[p[0].upper()](float(p[1]), float(p[2]))} (atendido por {ident})"
            except Exception as e:
                r = f"ERRO {type(e).__name__}"
            c.sendall((r + "\n").encode())


def main():
    porta = int(sys.argv[1])
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", porta))
    srv.listen()
    threading.Thread(target=heartbeat, args=(porta,), daemon=True).start()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=atender, args=(c, f"replica-{porta}"), daemon=True).start()


if __name__ == "__main__":
    main()
