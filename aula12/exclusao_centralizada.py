"""
Gabarito Aula 12, Exercício 4: exclusão mútua CENTRALIZADA (simulação com threads).
3 mensagens por entrada (PEDIR, CONCEDIDO, LIBERAR). Simples e justo (FIFO),
mas o coordenador é ponto único de falha e gargalo.
"""
import queue
import threading
import time

pedidos = queue.Queue()                    # caixa de entrada do coordenador
mensagens = 0


def coordenador():
    global mensagens
    ocupado, fila = False, []
    while True:
        tipo, pid, resposta = pedidos.get()
        mensagens += 1
        if tipo == "PEDIR":
            if ocupado:
                fila.append(resposta)
                print(f"   coordenador: P{pid} vai para a fila")
            else:
                ocupado = True
                resposta.put("CONCEDIDO"); mensagens += 1
        else:  # LIBERAR
            if fila:
                fila.pop(0).put("CONCEDIDO"); mensagens += 1
            else:
                ocupado = False


def processo(pid):
    minha_caixa = queue.Queue()
    pedidos.put(("PEDIR", pid, minha_caixa))
    minha_caixa.get()
    print(f">>> P{pid} na seção crítica")
    time.sleep(0.2)
    print(f"<<< P{pid} saiu")
    pedidos.put(("LIBERAR", pid, None))


threading.Thread(target=coordenador, daemon=True).start()
ts = [threading.Thread(target=processo, args=(i,)) for i in range(3)]
for t in ts:
    t.start()
for t in ts:
    t.join()
time.sleep(0.1)
print(f"Mensagens: {mensagens} (3 por entrada)")
