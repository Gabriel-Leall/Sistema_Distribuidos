from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QMessageBox
from firebase.livros import criar_livro, listar_livros

class Biblioteca(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Biblioteca')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.titulo_input = QLineEdit(self)
        self.titulo_input.setPlaceholderText('Título do Livro')
        layout.addWidget(self.titulo_input)

        self.autor_input = QLineEdit(self)
        self.autor_input.setPlaceholderText('Autor do Livro')
        layout.addWidget(self.autor_input)

        self.paginas_input = QLineEdit(self)
        self.paginas_input.setPlaceholderText('Quantidade de Páginas do Livro')
        layout.addWidget(self.paginas_input)

        self.ano_input = QLineEdit(self)
        self.ano_input.setPlaceholderText('Ano de Publicação do Livro')
        layout.addWidget(self.ano_input)

        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText('ID do Livro')
        layout.addWidget(self.id_input)

        self.criar_livro_button = QPushButton('Criar Livro', self)
        self.criar_livro_button.clicked.connect(self.criar_livro)
        layout.addWidget(self.criar_livro_button)

        self.listar_livros_button = QPushButton('Listar Livros', self)
        self.listar_livros_button.clicked.connect(self.listar_livros)
        layout.addWidget(self.listar_livros_button)

        self.listar_livros = QTextEdit(self)
        self.listar_livros.setReadOnly(True) #INFO: Apenas para ler os livros, sem poder editar.
        layout.addWidget(self.listar_livros)

        self.setLayout(layout)

    def criar_livro(self):
        titulo = self.titulo_input.text()
        autor = self.autor_input.text()
        paginas = self.paginas_input.text()
        ano = self.ano_input.text()
        id = self.id_input.text()

        if not titulo:
            self.mostrar_erro('Faltou informar o título.')
            return
        if not autor:
            self.mostrar_erro('Faltou informar o autor.')
            return
        if not paginas:
            self.mostrar_erro('Faltou informar as páginas.')
            return
        if not ano:
            self.mostrar_erro('Faltou informar o ano.')
            return
        if not id:
            self.mostrar_erro('Faltou informar o id.')
            return

        criar_livro(titulo, autor, paginas, ano, id)

        #INFO: Limpa os campos.
        self.titulo_input.clear()
        self.autor_input.clear()
        self.paginas_input.clear()
        self.ano_input.clear()
        self.id_input.clear()

    def listar_livros(self):
        try:
            print("Listando livros...")
            livros = listar_livros()
            self.listar_livros.clear()
            for livro in livros:
                livro_dict = livro.to_dict()
                self.listar_livros.append(f"Titulo: {livro_dict['titulo']} - Autor: {livro_dict[r'autor']} -  Ano: ({livro_dict['ano']}) - Paginas: {livro_dict['paginas']} - Id: {livro_dict['id']}")
            print("Livrors listados com sucesso.")
        except Exception as e:
            print(f"Erro ao listar livros: {e}")

    def mostrar_erro(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setWindowTitle("Erro")
        msg.exec_()