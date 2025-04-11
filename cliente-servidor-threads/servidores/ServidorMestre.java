package servidores;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.*;

public class ServidorMestre {

    private static final String ESCRAVO1_URL = "http://escravo1:8001";
    private static final String ESCRAVO2_URL = "http://escravo2:8002";

    public static void main(String[] args) throws Exception {
        System.out.println("Iniciando Servidor Mestre...");

        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", 8000), 0);
        server.createContext("/processar", new ProcessarHandler());
        server.setExecutor(Executors.newCachedThreadPool());

        System.out.println("Servidor Mestre iniciado na porta 8000");
        server.start();
    }

    static class ProcessarHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("Requisição recebida em /processar");

            if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
                System.out.println("Método não permitido: " + exchange.getRequestMethod());
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String texto = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            System.out.println("Texto recebido: " + texto);

            ExecutorService executor = Executors.newFixedThreadPool(2);
            Future<String> futuroLetras = executor.submit(() -> {
                System.out.println("Enviando texto para Escravo 1...");
                return enviarParaEscravo(ESCRAVO1_URL, "/letras", texto);
            });

            Future<String> futuroNumeros = executor.submit(() -> {
                System.out.println("Enviando texto para Escravo 2...");
                return enviarParaEscravo(ESCRAVO2_URL, "/numeros", texto);
            });

            try {
                String resultadoLetras = futuroLetras.get();
                String resultadoNumeros = futuroNumeros.get();

                System.out.println("Resposta do Escravo 1: " + resultadoLetras);
                System.out.println("Resposta do Escravo 2: " + resultadoNumeros);

                String respostaFinal = resultadoLetras + " | " + resultadoNumeros;
                System.out.println("Resposta final enviada ao cliente: " + respostaFinal);

                exchange.sendResponseHeaders(200, respostaFinal.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(respostaFinal.getBytes());
                os.close();
            } catch (Exception e) {
                String erro = "Erro ao processar: " + e.getMessage();
                System.out.println(erro);
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
            String statusUrl = baseUrl + "/status";
            if (!escravoDisponivel(statusUrl)) {
                System.out.println("Escravo indisponível em: " + statusUrl);
                return "Escravo em " + baseUrl + " indisponível.";
            }

            System.out.println("Escravo disponível em: " + statusUrl + ". Enviando dados para " + baseUrl + endpoint);
            HttpURLConnection con = (HttpURLConnection) new URL(baseUrl + endpoint).openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "text/plain; charset=utf-8");

            try (OutputStream os = con.getOutputStream()) {
                os.write(texto.getBytes(StandardCharsets.UTF_8));
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String resposta = in.readLine();
            System.out.println("Resposta recebida de " + baseUrl + endpoint + ": " + resposta);
            return resposta;
        }

        private boolean escravoDisponivel(String statusUrl) {
            try {
                HttpURLConnection con = (HttpURLConnection) new URL(statusUrl).openConnection();
                con.setRequestMethod("GET");
                boolean disponivel = con.getResponseCode() == 200;
                System.out.println("Verificando disponibilidade de " + statusUrl + ": " + (disponivel ? "OK" : "FALHOU"));
                return disponivel;
            } catch (Exception e) {
                System.out.println("Erro ao verificar disponibilidade de " + statusUrl + ": " + e.getMessage());
                return false;
            }
        }
    }
}
