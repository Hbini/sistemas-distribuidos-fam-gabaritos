"""
Gabarito Aula 07, Exercício 1: broker pub/sub com curinga no final do tópico.
Só muda a função publicar(): verifica se o padrão assinado "casa" com o tópico.
"""
import socket
import threading

PORTA = 9300
assinantes = {}
trava = threading.Lock()


def casa(padrao: str, topico: str) -> bool:
    if padrao.endswith("*"):
        return topico.startswith(padrao[:-1])     # "cardapio.*" casa com "cardapio.almoco"
    return padrao == topico


def publicar(topico, mensagem):
    linha = f"MSG {topico} {mensagem}\n".encode()
    n = 0
    with trava:
        for padrao, conexoes in assinantes.items():
            if casa(padrao, topico):
                for c in list(conexoes):
                    try:
                        c.sendall(linha)
                        n += 1
                    except OSError:
                        conexoes.remove(c)
    return n


def atender(c):
    for linha in c.makefile("r", encoding="utf-8"):
        p = linha.rstrip("\n").split(" ", 2)
        if p[0] == "SUB":
            with trava:
                assinantes.setdefault(p[1], []).append(c)
        elif p[0] == "PUB" and len(p) == 3:
            c.sendall(f"OK {publicar(p[1], p[2])}\n".encode())


srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", PORTA))
srv.listen()
while True:
    conexao, _ = srv.accept()
    threading.Thread(target=atender, args=(conexao,), daemon=True).start()
