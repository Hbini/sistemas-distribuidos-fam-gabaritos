"""
Gabarito Aula 04, Exercício 4: pool com fila LIMITADA (load shedding / backpressure).
Se já existem mais de LIMITE_FILA pedidos aguardando, o servidor responde
OCUPADO na hora, em vez de deixar o cliente esperando indefinidamente.
Uso: python servidor_pool_limitado.py 8000 4
"""
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

TEMPO_SERVICO = 0.2
LIMITE_FILA = 20
pendentes = 0
trava = threading.Lock()


def atender(conexao):
    global pendentes
    with conexao:
        pedido = conexao.recv(1024)
        time.sleep(TEMPO_SERVICO)
        conexao.sendall(b"OK " + pedido.strip() + b"\n")
    with trava:
        pendentes -= 1


def main():
    global pendentes
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    pool = ThreadPoolExecutor(max_workers=threads)
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", porta))
    srv.listen(1024)
    recusados = 0
    while True:
        c, _ = srv.accept()
        with trava:
            cheio = pendentes >= LIMITE_FILA
            if not cheio:
                pendentes += 1
        if cheio:
            recusados += 1
            c.sendall(b"OCUPADO\n")
            c.close()
            print(f"recusados até agora: {recusados}")
        else:
            pool.submit(atender, c)


if __name__ == "__main__":
    main()
