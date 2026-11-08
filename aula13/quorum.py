"""
Gabarito Aula 13, Exercício 2: replicação por QUÓRUM com N=3, W=2, R=2 (W + R > N).
Toda leitura enxerga pelo menos uma réplica que participou da última escrita;
a versão mais alta vence.
"""
N, W, R = 3, 2, 2


class Replica:
    def __init__(self, nome):
        self.nome, self.valor, self.versao, self.acessivel = nome, 100, 0, True


reps = [Replica("R1"), Replica("R2"), Replica("R3")]
versao_global = 0


def escrever(valor):
    global versao_global
    vivas = [r for r in reps if r.acessivel]
    if len(vivas) < W:
        print(f"escrita {valor}: RECUSADA (só {len(vivas)} réplicas, quórum W={W})")
        return
    versao_global += 1
    for r in vivas[:W]:
        r.valor, r.versao = valor, versao_global
    print(f"escrita {valor} (v{versao_global}) gravada em {[r.nome for r in vivas[:W]]}")


def ler(preferidas):
    consultadas = [r for r in reps if r.acessivel and r.nome in preferidas][:R]
    if len(consultadas) < R:
        return "RECUSADA"
    mais_nova = max(consultadas, key=lambda r: r.versao)
    return f"{mais_nova.valor} (v{mais_nova.versao}, consultou {[r.nome for r in consultadas]})"


reps[2].acessivel = False                # partição isola R3
escrever(200)
print("leitura em R1,R2:", ler({"R1", "R2"}))
reps[2].acessivel = True                 # rede volta; R3 ainda está com v0
reps[0].acessivel = False                # agora R1 cai
print("leitura em R2,R3:", ler({"R2", "R3"}), "<- R3 está velha, mas R2 tem a versão nova")
