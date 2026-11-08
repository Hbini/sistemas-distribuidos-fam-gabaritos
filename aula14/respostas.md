# Gabarito: Aula 14

## Exercício 1
Sim, A vê a alteração, porque a cada leitura o cliente consulta a versão no servidor (validação a cada acesso). Se a consulta for pulada por 30 s, A pode ler um conteúdo **desatualizado** durante essa janela: a consistência passa a ser fraca/eventual (no NFS isso se chama semântica de "close-to-open" com cache de atributos).

## Exercício 2
No servidor, em `tratar`, operação `escrever`:
```python
atual = arquivos.get(nome, {"versao": 0})
if pedido.get("versao_lida") is not None and pedido["versao_lida"] != atual["versao"]:
    return {"ok": False, "erro": "conflito", "versao_atual": atual["versao"]}
```
No cliente, enviar `versao_lida=cache[nome]["versao"]` e, em caso de conflito, reler o arquivo e pedir ao usuário que refaça a alteração. Mesmo princípio do ETag/If-Match do HTTP e do "rebase" do Git.

## Exercício 3
```python
elif politica == "dois aleatórios":
    a, b = random.sample(nomes, 2)
    s = min((a, b), key=lambda n: livre_em[n] + duracao / VELOCIDADE[n])
```
O makespan fica bem próximo do "menor carga" e muito melhor que o aleatório e o round robin. É usado na prática ("power of two choices", nginx, Envoy) porque consulta só 2 servidores em vez de todos: pouca informação e pouca mensagem, quase o mesmo resultado.

## Exercício 4
O HMAC prova que a mensagem não foi alterada e veio de quem tem a chave, mas uma cópia exata continua válida. Correção: incluir na mensagem assinada um **nonce** (identificador único) e/ou **carimbo de tempo**; o receptor guarda os nonces já vistos e rejeita repetidos e mensagens com horário fora de uma janela (por exemplo, 30 s).
```python
vistos = set()
def aceitar(msg, nonce, instante, tag):
    if nonce in vistos or abs(time.time() - instante) > 30:
        return False
    if not verificar(f"{msg}|{nonce}|{instante}", tag):
        return False
    vistos.add(nonce)
    return True
```
