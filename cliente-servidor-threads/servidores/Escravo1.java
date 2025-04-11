package servidores;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

public class Escravo1 {

    public static void main(String[] args) throws Exception {
        System.out.println("Iniciando servidor Escravo 1...");

        HttpServer server = HttpServer.create(new InetSocketAddress(8001), 0);
        server.createContext("/letras", new LetrasHandler());
        server.createContext("/status", new StatusHandler());
        server.setExecutor(Executors.newCachedThreadPool());

        System.out.println("Escravo 1 rodando na porta 8001");
        server.start();
    }

    static class LetrasHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("Requisição recebida em /letras");

            if (!"POST".equals(exchange.getRequestMethod())) {
                System.out.println("Método não permitido: " + exchange.getRequestMethod());
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            System.out.println("Lendo texto enviado...");
            String texto = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            System.out.println("Texto recebido: " + texto);

            long count = texto.chars().filter(Character::isLetter).count();
            System.out.println("Quantidade de letras contadas: " + count);

            String resposta = "Letras: " + count;
            exchange.sendResponseHeaders(200, resposta.getBytes().length);
            exchange.getResponseBody().write(resposta.getBytes());
            exchange.getResponseBody().close();
            System.out.println("Resposta enviada ao mestre: " + resposta);
        }
    }

    static class StatusHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("Requisição de status recebida em /status");

            String resposta = "OK";
            exchange.sendResponseHeaders(200, resposta.getBytes().length);
            exchange.getResponseBody().write(resposta.getBytes());
            exchange.getResponseBody().close();

            System.out.println("Status 'OK' enviado");
        }
    }
}
