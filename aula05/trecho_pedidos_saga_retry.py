"""
Gabarito Aula 05, Exercícios 2 e 3: trechos para substituir/acrescentar em
servico_pedidos.py (do_POST), com retry exponencial e compensação (Saga).
"""
import time

PAGAMENTOS_URL = "http://localhost:8004"   # no Docker: http://pagamentos:8004


def chamar_com_retry(chamar, metodo, url, corpo=None, tentativas=3):
    """Exercício 3: backoff exponencial (0,5 s, 1 s, 2 s) só para erro 503."""
    espera = 0.5
    for i in range(tentativas + 1):
        status, resp = chamar(metodo, url, corpo)
        if status != 503 or i == tentativas:
            return status, resp
        time.sleep(espera)
        espera *= 2


# Dentro de do_POST, depois da baixa de estoque (passo 2):
#
#   total = round(produto["preco"] * qtd, 2)
#   status, pag = chamar("POST", f"{PAGAMENTOS_URL}/pagamentos", {"pedido": "novo", "valor": total})
#   if status != 200:
#       # COMPENSAÇÃO: desfaz a etapa anterior, pois não há transação distribuída
#       chamar("POST", f"{ESTOQUE_URL}/estoque/{pid}/devolver", {"quantidade": qtd})
#       return self.responder(402, {"erro": "pagamento recusado", "detalhe": pag})
