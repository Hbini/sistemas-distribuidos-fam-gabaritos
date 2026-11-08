import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

/**
 * Gabarito Aula 11, Exercício 2: RMI com CALLBACK (servidor chama o cliente).
 *   java RMICallback.java servidor
 *   java RMICallback.java cliente Ana
 */
public class RMICallback {
    public static void main(String[] args) throws Exception {
        if (args[0].equals("servidor")) {
            Registry r = LocateRegistry.createRegistry(1099);
            r.rebind("Cozinha", new CozinhaImpl());
            System.out.println("Cozinha publicada");
        } else {
            Cozinha cozinha = (Cozinha) LocateRegistry.getRegistry("127.0.0.1", 1099).lookup("Cozinha");
            NotificadorImpl meuNotificador = new NotificadorImpl(args[1]);   // objeto remoto DO CLIENTE
            System.out.println(cozinha.fazerPedido(args[1], "pastel", meuNotificador));
            System.out.println("Pedido feito. Vou esperar o aviso sem ficar perguntando...");
            Thread.sleep(5000);
            UnicastRemoteObject.unexportObject(meuNotificador, true);
        }
    }
}

interface Notificador extends Remote {
    void pedidoPronto(String msg) throws RemoteException;
}

interface Cozinha extends Remote {
    String fazerPedido(String cliente, String item, Notificador n) throws RemoteException;
}

class NotificadorImpl extends UnicastRemoteObject implements Notificador {
    final String nome;
    NotificadorImpl(String nome) throws RemoteException { this.nome = nome; }
    public void pedidoPronto(String msg) { System.out.println("[callback para " + nome + "] " + msg); }
}

class CozinhaImpl extends UnicastRemoteObject implements Cozinha {
    CozinhaImpl() throws RemoteException { }
    public String fazerPedido(String cliente, String item, Notificador n) {
        new Thread(() -> {
            try {
                Thread.sleep(3000);
                n.pedidoPronto("Seu " + item + " está pronto, " + cliente + "!");   // chamada remota ao cliente
            } catch (Exception e) { System.out.println("cliente inalcançável: " + e); }
        }).start();
        return "Pedido de " + item + " recebido";
    }
}
