"""
Gabarito Aula 03, Exercício 2: serviço de nomes com HEARTBEAT.

Novidades em relação ao original:
  * comando VIVO <nome> <host> <porta>: renova o "atestado de vida" da réplica
    (também serve como registro, então REGISTRAR continua funcionando);
  * uma thread "faxineira" remove quem ficou mais de TOLERANCIA segundos sem
    mandar VIVO. Assim o cliente para de tentar réplicas mortas.

Para testar, use replica_com_heartbeat.py (nesta mesma pasta).
"""
import socket
import threading
import time

PORTA = 5000
TOLERANCIA = 6.0
ultimo_sinal: dict[str, dict[str, float]] = {}   # nome -> {"host:porta": instante}
trava = threading.Lock()


def faxineira():
    while True:
        time.sleep(1)
        agora = time.time()
        with trava:
            for nome, enderecos in ultimo_sinal.items():
                for end, t in list(enderecos.items()):
                    if agora - t > TOLERANCIA:
                        del enderecos[end]
                        print(f"[nomes] {end} removido de '{nome}' (sem heartbeat há {agora - t:.0f}s)")


def atender(conexao):
    with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
        for linha in entrada:
            p = linha.split()
            if not p:
                continue
            cmd = p[0].upper()
            if cmd in ("REGISTRAR", "VIVO") and len(p) == 4:
                with trava:
                    ultimo_sinal.setdefault(p[1], {})[f"{p[2]}:{p[3]}"] = time.time()
                resp = "OK"
            elif cmd == "RESOLVER" and len(p) == 2:
                with trava:
                    resp = ",".join(ultimo_sinal.get(p[1], {})) or "VAZIO"
            else:
                resp = "ERRO"
            conexao.sendall((resp + "\n").encode())


def main():
    threading.Thread(target=faxineira, daemon=True).start()
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORTA))
    srv.listen()
    print(f"[nomes+heartbeat] porta {PORTA}, tolerância {TOLERANCIA}s")
    while True:
        c, _ = srv.accept()
        threading.Thread(target=atender, args=(c,), daemon=True).start()


if __name__ == "__main__":
    main()
