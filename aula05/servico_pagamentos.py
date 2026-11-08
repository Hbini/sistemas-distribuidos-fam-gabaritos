"""
Gabarito Aula 05, Exercício 1: microsserviço de pagamentos (porta 8004).
Aprova até R$ 100,00; acima disso responde 402 (Payment Required).
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = int(os.environ.get("PORTA", 8004))
LIMITE = 100.0
pagamentos = []


class Pagamentos(BaseHTTPRequestHandler):
    def responder(self, status, corpo):
        d = json.dumps(corpo, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(d)))
        self.end_headers()
        self.wfile.write(d)

    def do_GET(self):
        self.responder(200, {"status": "ok"} if self.path == "/saude" else pagamentos)

    def do_POST(self):
        corpo = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        valor = float(corpo.get("valor", 0))
        if valor > LIMITE:
            return self.responder(402, {"aprovado": False, "motivo": "valor acima do limite"})
        pagamentos.append(corpo)
        self.responder(200, {"aprovado": True, "transacao": len(pagamentos)})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORTA), Pagamentos).serve_forever()
