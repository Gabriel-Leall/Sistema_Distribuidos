package ProjetoDistribuido;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.*;

public class ServidorMestre {

    private static final String ESCRAVO1_URL = "http://localhost:8001";
    private static final String ESCRAVO2_URL = "http://localhost:8002";

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/processar", new ProcessarHandler());
        server.setExecutor(Executors.newCachedThreadPool());
        System.out.println("Servidor Mestre iniciado na porta 8000");
        server.start();
    }

    static class ProcessarHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
                exchange.sendResponseHeaders(405, -1); // Method Not Allowed
                return;
            }

            String texto = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);

            ExecutorService executor = Executors.newFixedThreadPool(2);
            Future<String> futuroLetras = executor.submit(() -> enviarParaEscravo(ESCRAVO1_URL, "/letras", texto));
            Future<String> futuroNumeros = executor.submit(() -> enviarParaEscravo(ESCRAVO2_URL, "/numeros", texto));

            try {
                String resultadoLetras = futuroLetras.get();
                String resultadoNumeros = futuroNumeros.get();

                String respostaFinal = resultadoLetras + " | " + resultadoNumeros;

                exchange.sendResponseHeaders(200, respostaFinal.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(respostaFinal.getBytes());
                os.close();
            } catch (Exception e) {
                String erro = "Erro ao processar: " + e.getMessage();
                exchange.sendResponseHeaders(500, erro.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(erro.getBytes());
                os.close();
                e.printStackTrace();
            } finally {
                executor.shutdown();
            }
        }

        private String enviarParaEscravo(String baseUrl, String endpoint, String texto) throws IOException {
            // Verifica disponibilidade
            if (!escravoDisponivel(baseUrl + "/status")) {
                return "Escravo em " + baseUrl + " indisponível.";
            }

            // Envia texto
            HttpURLConnection con = (HttpURLConnection) new URL(baseUrl + endpoint).openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "text/plain; charset=utf-8");

            try (OutputStream os = con.getOutputStream()) {
                os.write(texto.getBytes(StandardCharsets.UTF_8));
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            return in.readLine();
        }

        private boolean escravoDisponivel(String statusUrl) {
            try {
                HttpURLConnection con = (HttpURLConnection) new URL(statusUrl).openConnection();
                con.setRequestMethod("GET");
                return con.getResponseCode() == 200;
            } catch (Exception e) {
                return false;
            }
        }
    }
}
