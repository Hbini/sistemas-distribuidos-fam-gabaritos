# Gabarito: Aula 04

## Exercício 1
Com pool de 4 threads e 200 ms por pedido, a capacidade máxima é 4 / 0,2 = **20 pedidos/s**. Até cerca de 4 clientes, a latência fica perto de 200 ms e a vazão cresce linearmente. Depois disso a vazão estabiliza em ~20 pedidos/s (saturação) e a latência cresce linearmente com o número de clientes, porque os pedidos passam a esperar na fila (Lei de Little: L = vazão x tempo no sistema).

## Exercício 2
Com trabalho de CPU em Python, `thread` e `pool` ficam praticamente iguais (ou o modo `thread` piora), porque o **GIL** permite que só uma thread execute bytecode Python por vez; não há paralelismo real de CPU. Em Java as threads rodam de fato em paralelo, então o ganho aparece até o número de núcleos. Solução em Python para CPU: `multiprocessing` ou `ProcessPoolExecutor`.

## Exercício 3
s = 0,2.
* p = 4: 1 / (0,2 + 0,8/4) = 1 / 0,4 = **2,5x** (40 s)
* p = 16: 1 / (0,2 + 0,05) = **4,0x** (25 s)
* p infinito: 1 / 0,2 = **5,0x** (20 s)
* p = 64: 1 / (0,2 + 0,0125) = **4,71x** (21,25 s)

(b) Não compensa: passar de 16 para 64 núcleos reduz só de 25 s para 21,25 s (15%) com 4 vezes mais hardware. Melhor atacar a parte sequencial (por exemplo, otimizar a leitura do banco).

## Exercício 4
Solução em `servidor_pool_limitado.py`. A latência dos pedidos aceitos fica limitada (no máximo cerca de (20/4 + 1) x 200 ms = 1,2 s), enquanto sem limite os últimos clientes esperam vários segundos. A técnica chama-se **load shedding** (descarte de carga), ligada ao conceito de **backpressure** e à ideia de rate limiting.
