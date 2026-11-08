# Gabarito: Aula 08

## Exercício 1
Trecho para `chat_servidor.py`, dentro do laço de `atender`:
```python
elif linha.startswith("/msg "):
    _, destino, texto = (linha.split(" ", 2) + [""])[:3]
    with trava:
        alvo = next((c for c, n in clientes.items() if n == destino), None)
    if alvo:
        alvo.sendall(f"[privado de {apelido}] {texto}\n".encode("utf-8"))
    else:
        conexao.sendall("*** usuário não encontrado\n".encode("utf-8"))
```
Em Java, a lógica é a mesma, procurando a entrada do mapa `CLIENTES` cujo valor é o apelido.

## Exercício 2
Ver `enquadramento.py`. Ponto-chave: `receber_exato` repete `recv` até completar o tamanho. Atenção: o tamanho é em **bytes**, não em caracteres ("á" ocupa 2 bytes em UTF-8).

## Exercício 3
Ver `servidor_arquivos.py`. A defesa contra path traversal é resolver o caminho absoluto (`resolve()`) e verificar se ele continua dentro da pasta permitida (`is_relative_to`). Filtrar apenas a string ".." não é suficiente (há caminhos absolutos, links simbólicos e codificações alternativas).

## Exercício 4
O socket que faz `listen()` (socket de escuta) só aceita novas conexões; ele nunca troca dados. Cada `accept()` cria um **novo socket conectado**, identificado pela quádrupla (IP e porta do servidor, IP e porta do cliente), usado para conversar com aquele cliente. Assim o servidor atende vários clientes na mesma porta. Em UDP não há conexão: um único socket recebe datagramas de todos os clientes com `recvfrom`, que informa o remetente, e responde com `sendto`.
