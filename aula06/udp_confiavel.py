"""
Gabarito Aula 06, Exercício 2: confiabilidade implementada pela aplicação sobre UDP
(stop-and-wait com número de sequência, timeout e retransmissão).

    python udp_confiavel.py servidor
    python udp_confiavel.py cliente
"""
import random
import socket
import sys

PORTA = 9201
PERDA = 0.30


def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", PORTA))
    vistos = set()
    while True:
        dados, origem = s.recvfrom(1024)
        seq, _, texto = dados.decode().partition("|")
        if random.random() < PERDA:
            continue                      # perda simulada na ida
        if seq in vistos:
            print(f"duplicata {seq} ignorada (só reenviando ACK)")
        else:
            vistos.add(seq)
            print(f"processei {seq}: {texto}")
        if random.random() < PERDA:
            continue                      # perda simulada na volta (do ACK)
        s.sendto(f"ACK|{seq}".encode(), origem)


def cliente():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.3)
    entregues = tentativas_total = 0
    for seq in range(50):
        for tentativa in range(1, 6):
            tentativas_total += 1
            s.sendto(f"{seq}|mensagem {seq}".encode(), ("127.0.0.1", PORTA))
            try:
                resp, _ = s.recvfrom(1024)
                if resp.decode() == f"ACK|{seq}":
                    entregues += 1
                    break
            except socket.timeout:
                pass
    print(f"Entregues: {entregues}/50 com {tentativas_total} envios no total")


if __name__ == "__main__":
    servidor() if sys.argv[1:] == ["servidor"] else cliente()
