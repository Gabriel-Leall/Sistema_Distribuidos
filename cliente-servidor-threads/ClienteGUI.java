package ProjetoDistribuido;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;

public class ClienteGUI extends JFrame {

    private JTextArea inputArea;
    private JTextArea outputArea;
    private JButton enviarBtn;

    public ClienteGUI() {
        setTitle("Cliente - Sistema Distribuído");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null); // centraliza

        inputArea = new JTextArea(5, 40);
        outputArea = new JTextArea(10, 40);
        outputArea.setEditable(false);

        enviarBtn = new JButton("Enviar");
        enviarBtn.setPreferredSize(new Dimension(100, 30)); // botão menor
        enviarBtn.addActionListener(this::enviarTexto);

        // Layout principal
        JPanel painel = new JPanel();
        painel.setLayout(new BorderLayout(10, 10));

        JPanel topo = new JPanel(new BorderLayout());
        topo.setBorder(BorderFactory.createTitledBorder("Digite o texto"));
        topo.add(new JScrollPane(inputArea), BorderLayout.CENTER);

        JPanel centro = new JPanel(new FlowLayout(FlowLayout.CENTER));
        centro.add(enviarBtn);

        JPanel fundo = new JPanel(new BorderLayout());
        fundo.setBorder(BorderFactory.createTitledBorder("Resposta do servidor"));
        fundo.add(new JScrollPane(outputArea), BorderLayout.CENTER);

        painel.add(topo, BorderLayout.NORTH);
        painel.add(centro, BorderLayout.CENTER);
        painel.add(fundo, BorderLayout.SOUTH);

        add(painel);
        setVisible(true);
    }

    private void enviarTexto(ActionEvent e) {
        String texto = inputArea.getText().trim();
        if (texto.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Digite um texto antes de enviar.");
            return;
        }

        try {
            // Salva no arquivo entrada.txt
            Path caminho = Path.of("entrada.txt");
            Files.writeString(caminho, texto);
            outputArea.setText("Texto salvo em entrada.txt\n");

            // Envia para o servidor
            URI uri = URI.create("http://localhost:8000/processar");
            URL url = uri.toURL();
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "text/plain; charset=utf-8");

            try (OutputStream os = con.getOutputStream()) {
                os.write(texto.getBytes());
            }

            int status = con.getResponseCode();
            outputArea.append("Código HTTP: " + status + "\n");

            // Lê a resposta
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String linha;
            while ((linha = in.readLine()) != null) {
                outputArea.append("Resposta: " + linha + "\n");
            }
            in.close();

        } catch (Exception ex) {
            outputArea.append("Erro ao enviar: " + ex.getMessage() + "\n");
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ClienteGUI::new);
    }
}
