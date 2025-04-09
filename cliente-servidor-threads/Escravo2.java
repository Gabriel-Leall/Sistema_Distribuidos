package ProjetoDistribuido;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

public class Escravo2 {

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8002), 0);
        server.createContext("/numeros", new NumerosHandler());
        server.createContext("/status", new StatusHandler());
        server.setExecutor(Executors.newCachedThreadPool());
        System.out.println("Escravo 2 rodando na porta 8002");
        server.start();
    }

    static class NumerosHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            String texto = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            long count = texto.chars().filter(Character::isDigit).count();

            String resposta = "Números: " + count;
            exchange.sendResponseHeaders(200, resposta.getBytes().length);
            exchange.getResponseBody().write(resposta.getBytes());
            exchange.getResponseBody().close();
        }
    }

    static class StatusHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String resposta = "OK";
            exchange.sendResponseHeaders(200, resposta.getBytes().length);
            exchange.getResponseBody().write(resposta.getBytes());
            exchange.getResponseBody().close();
        }
    }
}
