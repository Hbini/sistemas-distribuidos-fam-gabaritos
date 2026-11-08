"""
Gabarito Aula 11, Exercício 1: servidor XML-RPC com pedidos e atendimento concorrente.
SimpleXMLRPCServer é ITERATIVO (um pedido por vez). Para atender em paralelo,
misturamos a classe com socketserver.ThreadingMixIn, e aí a lista de pedidos
precisa de trava.
"""
import threading
import time
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer


class ServidorConcorrente(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True


pedidos = []
trava = threading.Lock()


def fazer_pedido(cliente, itens):
    time.sleep(2)                       # simula preparo; com 2 clientes dá para ver a concorrência
    with trava:
        pedidos.append({"cliente": cliente, "itens": itens})
        return len(pedidos)


def listar_pedidos():
    with trava:
        return list(pedidos)


srv = ServidorConcorrente(("0.0.0.0", 9800), allow_none=True, logRequests=False)
srv.register_function(fazer_pedido)
srv.register_function(listar_pedidos)
print("RPC concorrente na porta 9800")
srv.serve_forever()
