"""
Gabarito Aula 08, Exercício 3: servidor de arquivos com proteção contra path traversal.
Usa o enquadramento do exercício 2.
    python servidor_arquivos.py servidor
    python servidor_arquivos.py cliente exemplo.txt
"""
import pathlib
import socket
import sys

from enquadramento import enviar_mensagem, receber_mensagem

PORTA = 9701
PASTA = pathlib.Path("compartilhada").resolve()


def servidor():
    PASTA.mkdir(exist_ok=True)
    (PASTA / "exemplo.txt").write_text("Conteúdo de exemplo da Aula 08\n", encoding="utf-8")
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORTA))
    srv.listen()
    while True:
        c, _ = srv.accept()
        with c:
            comando, _, nome = receber_mensagem(c).partition(" ")
            alvo = (PASTA / nome).resolve()
            # O caminho final PRECISA continuar dentro da pasta compartilhada
            if comando != "BAIXAR" or not alvo.is_relative_to(PASTA):
                enviar_mensagem(c, "ERRO acesso negado")
            elif not alvo.is_file():
                enviar_mensagem(c, "ERRO arquivo não encontrado")
            else:
                enviar_mensagem(c, "OK " + alvo.read_text(encoding="utf-8"))


def cliente(nome):
    with socket.create_connection(("127.0.0.1", PORTA)) as s:
        enviar_mensagem(s, f"BAIXAR {nome}")
        print(receber_mensagem(s))


if __name__ == "__main__":
    servidor() if sys.argv[1] == "servidor" else cliente(sys.argv[2])
