"""
Gabarito Aula 08, Exercício 2: mensagens com prefixo de tamanho (length-prefix framing).
    python enquadramento.py servidor
    python enquadramento.py cliente
"""
import socket
import struct
import sys

PORTA = 9700


def enviar_mensagem(sock, texto: str) -> None:
    dados = texto.encode("utf-8")
    sock.sendall(struct.pack("!I", len(dados)) + dados)     # 4 bytes de tamanho + conteúdo


def receber_exato(sock, n: int) -> bytes:
    """Lê exatamente n bytes, juntando quantos recv forem necessários."""
    partes = []
    while n > 0:
        bloco = sock.recv(min(n, 65536))
        if not bloco:
            raise ConnectionError("conexão fechada no meio da mensagem")
        partes.append(bloco)
        n -= len(bloco)
    return b"".join(partes)


def receber_mensagem(sock) -> str:
    (tamanho,) = struct.unpack("!I", receber_exato(sock, 4))
    return receber_exato(sock, tamanho).decode("utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["servidor"]:
        srv = socket.socket()
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", PORTA))
        srv.listen()
        c, _ = srv.accept()
        with c:
            msg = receber_mensagem(c)
            print(f"recebi {len(msg)} caracteres; começo: {msg[:20]!r}")
            enviar_mensagem(c, f"OK, recebi {len(msg)} caracteres")
    else:
        with socket.create_connection(("127.0.0.1", PORTA)) as s:
            enviar_mensagem(s, "á" * 100_000)               # 200.000 bytes em UTF-8
            print(receber_mensagem(s))
