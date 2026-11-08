import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Gabarito Aula 07, Exercício 3: consumidor Java da fila_mensagens.py (porta 9400).
 * Uso: java ConsumidorFila.java cozinha Chef-Java
 */
public class ConsumidorFila {
    public static void main(String[] args) throws Exception {
        String fila = args[0], nome = args[1];
        try (Socket s = new Socket("127.0.0.1", 9400);
             PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
            while (true) {
                out.println("GET " + fila);
                String r = in.readLine();
                if (r == null) break;
                if (r.equals("VAZIA")) { Thread.sleep(500); continue; }
                System.out.println("[" + nome + "] preparando " + r.substring(4) + "...");
                Thread.sleep(1000);
            }
        }
    }
}
