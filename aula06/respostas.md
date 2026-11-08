# Gabarito: Aula 06

## Exercício 1
Novo formato: `"!I20sHBd"` (B = 1 byte sem sinal). Tamanho: 4 + 20 + 2 + 1 + 8 = **35 bytes** (com '!' não há preenchimento/alinhamento). Java: `in.readUnsignedByte()` entre `readUnsignedShort()` e `readDouble()`. Se só o servidor for atualizado, o cliente lê os bytes deslocados: a quantidade sai certa, mas o preço é montado com o byte da mesa no início, resultando em valor absurdo, e sobra 1 byte. Conclusão: o formato binário é um **contrato rígido**; mudanças exigem versionamento do protocolo.

## Exercício 2
Solução em `udp_confiavel.py`. Com perda de 30% na ida e 30% na volta, a chance de uma tentativa falhar é 1 menos 0,7 x 0,7 = 0,51; com 5 tentativas a chance de perder a mensagem é 0,51^5, cerca de 3,5%, então chegam em média ~48 de 50. Quem faz isso por você é o **TCP** (números de sequência, ACK, timeout e retransmissão), e protocolos como o **QUIC** (base do HTTP/3) fazem isso sobre UDP.

## Exercício 3
Valores aproximados: JSON ~70 bytes por pedido (~70 KB para 1.000) contra 34 bytes em struct (34 KB): economia de cerca de **50%**. Vantagens do JSON: legível por humanos (fácil depurar), autodescritivo (nomes dos campos), flexível (campos opcionais e novos sem quebrar clientes), suportado nativamente por praticamente todas as linguagens e navegadores.

## Exercício 4
* (a) Telefone: síncrona e transiente.
* (b) WhatsApp: assíncrona e persistente (servidor guarda até o destinatário conectar).
* (c) API REST: síncrona e transiente.
* (d) E-mail: assíncrona e persistente.
* (e) Vídeo ao vivo via UDP: assíncrona e transiente (pacote perdido não é recuperado).
