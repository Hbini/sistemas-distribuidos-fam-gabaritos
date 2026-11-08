# Gabarito: Aula 02

## Exercício 1
Resposta esperada: o speedup cresce até se aproximar do número de núcleos físicos; depois disso estabiliza ou piora, porque os processos extras disputam os mesmos núcleos e o custo de criar processos e juntar resultados (overhead) passa a pesar. A eficiência cai à medida que p aumenta (relacionar com a Lei de Amdahl, que será vista na Aula 04). Aceitar tabelas coerentes com a máquina do aluno.

## Exercício 2
Solução em `coordenador_dinamico.py`. O tempo total cai porque nenhum trabalhador fica ocioso esperando o mais lento: os pedaços do fim do intervalo (mais caros) ficam espalhados. Conceito: balanceamento de carga dinâmico (fila de trabalho / "work stealing" simplificado).

## Exercício 3
Solução em `TrabalhadorJson.java`. Pontos que o aluno deve citar: o protocolo (formato da mensagem e delimitador "\n") é o contrato entre sistemas heterogêneos; a linguagem de cada lado é irrelevante quando o protocolo é respeitado; cuidado com ponto decimal (Locale) e codificação UTF-8.

## Exercício 4
* (a) Caixa eletrônico: **distribuído** (terminal remoto conversa com servidores do banco pela rede; costuma ser cliente/servidor).
* (b) Renderização em GPU: **paralelo** (milhares de núcleos na mesma placa, memória da própria máquina).
* (c) Google Drive: **distribuído** (dados replicados em vários data centers, acesso transparente).
* (d) Supercomputador do clima: **alto desempenho (HPC)**, que é paralelo/distribuído em cluster com rede de baixa latência dedicada.
* (e) Excel no notebook: **centralizado** (tudo em uma máquina; pode usar alguns núcleos, mas não é um sistema distribuído).
