// Gabarito Aula 05, Exercício 2: acrescentar em ServicoEstoque.tratar(), antes do último "else":
//
//  } else if (metodo.equals("POST") && partes.length == 3 && partes[2].equals("devolver")) {
//      String corpo = new String(troca.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
//      Matcher m = QTD.matcher(corpo);
//      int qtd = m.find() ? Integer.parseInt(m.group(1)) : 1;
//      int novo = ESTOQUE.merge(id, qtd, Integer::sum);   // soma atômica
//      responder(troca, 200, "{\"produto_id\": " + id + ", \"restante\": " + novo + "}");
//
// Arquivo de exemplo apenas (não compila sozinho).
