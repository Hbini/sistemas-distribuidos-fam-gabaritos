import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Gabarito Aula 02, Exercício 3: trabalhador Java que fala o protocolo JSON
 * do coordenador Python. Para não depender de bibliotecas externas, o JSON
 * de entrada (bem simples) é lido com expressão regular e a resposta é
 * montada com String.format.
 *
 * Uso: java TrabalhadorJson.java 6003
 * Teste: python coordenador_trabalhadores.py coordenador 127.0.0.1:6001 127.0.0.1:6003
 */
public class TrabalhadorJson {
    static final Pattern CAMPO = Pattern.compile("\"(inicio|fim)\"\\s*:\\s*(\\d+)");

    static boolean ehPrimo(int n) {
        if (n < 2) return false;
        if (n % 2 == 0) return n == 2;
        for (int d = 3; (long) d * d <= n; d += 2) if (n % d == 0) return false;
        return true;
    }

    public static void main(String[] args) throws Exception {
        int porta = Integer.parseInt(args[0]);
        try (ServerSocket servidor = new ServerSocket(porta)) {
            System.out.println("[trabalhador-json:" + porta + "] aguardando...");
            while (true) {
                try (Socket s = servidor.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
                     PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8)) {
                    String linha = in.readLine();
                    int inicio = 0, fim = 0;
                    Matcher m = CAMPO.matcher(linha);
                    while (m.find()) {
                        if (m.group(1).equals("inicio")) inicio = Integer.parseInt(m.group(2));
                        else fim = Integer.parseInt(m.group(2));
                    }
                    long t0 = System.nanoTime();
                    int total = 0;
                    for (int n = inicio; n < fim; n++) if (ehPrimo(n)) total++;
                    double tempo = (System.nanoTime() - t0) / 1e9;
                    String host = InetAddress.getLocalHost().getHostName();
                    // Locale.ROOT garante ponto decimal (JSON não aceita vírgula)
                    out.println(String.format(java.util.Locale.ROOT,
                        "{\"primos\": %d, \"tempo\": %.4f, \"host\": \"%s\"}", total, tempo, host));
                }
            }
        }
    }
}
