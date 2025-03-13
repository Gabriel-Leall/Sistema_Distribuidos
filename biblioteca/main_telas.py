import sys
import pyrebase
import re
from firebase.livros import criar_livro, listar_livros, verificar_livro, atualizar_livro, deletar_livro

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QTableView, QTableWidgetItem
from PyQt5.QtGui import QDesktopServices, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QTableWidget
from PyQt5.QtCore import QByteArray

from interface_grafica.py.login import Ui_Login
from interface_grafica.py.criar_conta import Ui_Criar_Conta
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.add_livro import Ui_Add_Livro
from interface_grafica.py.editar_livro import Ui_Editar_Livro
from interface_grafica.py.excluir_livro import Ui_Excluir_Livro
from interface_grafica.py.listar_livros import Ui_Listar_Livros

from firebase import config_firebase

class Ui_Main(QtWidgets.QWidget):

    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()

        self.tela_login = Ui_Login()
        self.tela_criar_conta = Ui_Criar_Conta()
        self.tela_inicial = Ui_Tela_Inicial()
        self.tela_add_livro = Ui_Add_Livro()
        self.tela_editar_livro = Ui_Editar_Livro()
        self.tela_excluir_livro = Ui_Excluir_Livro()
        self.tela_listar_livros = Ui_Listar_Livros()

        self.tela_login.setupUi(self.stack0)
        self.tela_criar_conta.setupUi(self.stack1)
        self.tela_inicial.setupUi(self.stack2)
        self.tela_add_livro.setupUi(self.stack3)
        self.tela_editar_livro.setupUi(self.stack4)
        self.tela_excluir_livro.setupUi(self.stack5)
        self.tela_listar_livros.setupUi(self.stack6)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)

class Main(Ui_Main, QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        
        
        self.modelo_tabela = QStandardItemModel()
        self.modelo_tabela.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano", "ID"])
        
        # Configurações da tabela na tela inicial
        self.tela_inicial.tableView.setModel(self.modelo_tabela)
        # Não precisamos configurar estilo aqui, pois foi movido para tela_inicial.py
        
        # Mesmas configurações para a tabela na tela de listar livros
        self.tela_listar_livros.tableView.setModel(self.modelo_tabela)
        # Não precisamos configurar estilo aqui, pois foi movido para listar_livros.py
        
        # Botões da tela de login
        self.tela_login.pushButton_criar_conta.clicked.connect(self.abrir_tela_criar_conta)
        self.tela_login.pushButton_entrar.clicked.connect(self.entrar_sistema)

        # Botões da tela de criar conta
        self.tela_criar_conta.pushButton_criar_conta.clicked.connect(self.criar_conta)
        self.tela_criar_conta.pushButton.clicked.connect(self.abrir_tela_login)

        # Botões da tela inicial
        self.tela_inicial.pushButton_add_livro.clicked.connect(self.abrir_tela_add_livro)
        self.tela_inicial.pushButton_editar_livro.clicked.connect(self.abrir_tela_editar_livro)
        self.tela_inicial.pushButton_excluir_livro.clicked.connect(self.abrir_tela_excluir_livro)
        self.tela_inicial.pushButton_voltar.clicked.connect(self.abrir_tela_login)
        self.tela_inicial.pushButton_busca.clicked.connect(self.listar_livros_na_tela)
        self.tela_inicial.pushButton_listar_livro.clicked.connect(self.listar_livros_na_tela)

        # Botões da tela adicionar livro
        self.tela_add_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_add_livro.pushButton_add_livro.clicked.connect(self.adicionar_livro)

        # Botões da tela editar livro
        self.tela_editar_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_editar_livro.pushButton_add_livro.clicked.connect(self.editar_livro)

        # Botões da tela excluir livro
        self.tela_excluir_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_excluir_livro.pushButton_add_livro.clicked.connect(self.excluir_livro)
        
        # Botões da tela listar livros
        self.tela_listar_livros.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_listar_livros.pushButton_listar.clicked.connect(self.listar_livros_na_tela)

    def abrir_tela_login(self):
        self.QtStack.setCurrentIndex(0)
            
    def entrar_sistema(self):
    
        email = self.tela_login.lineEdit_email.text()
        senha = self.tela_login.lineEdit__senha.text()

        if not email or not senha:
            print("Campos vazios detectados")  
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos")
            return
        
        try:
            print(f"{email}, {senha}")  
            user = config_firebase.auth.sign_in_with_email_and_password(email, senha)
            
            print("Sucesso ao entrar no sistema")
            self.abrir_tela_inicial()
        except:
            QMessageBox.warning(self, "Erro", "Email ou senha incorretos. Tente novamente.")


    def email_valido(self, email):
        padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(padrao, email) is not None

    def abrir_tela_criar_conta(self):
        self.QtStack.setCurrentIndex(1)

    def criar_conta(self):
        email = self.tela_criar_conta.lineEdit_email.text()
        senha = self.tela_criar_conta.lineEdit_senha.text()
        conf_senha = self.tela_criar_conta.lineEdit_conf_senha.text()

        if not email or not senha or not conf_senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if not self.email_valido(email):
            QMessageBox.warning(self, "Erro", "Email inválido. Use um formato correto.")
            return

        if senha != conf_senha:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            return

        try:
            user = config_firebase.auth.create_user_with_email_and_password(email, senha)
            print("Conta criada com sucesso!")
            QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
            self.abrir_tela_login()
        except:
            print("Erro ao criar usuário")
            QMessageBox.warning(self, "Erro", "Erro ao criar conta. Verifique os dados.")

    def adicionar_livro(self):
        titulo = self.tela_add_livro.lineEdit_titulo_livro.text()
        autor = self.tela_add_livro.lineEdit_autor_principal.text()
        paginas = self.tela_add_livro.lineEdit_quantidade_paginas.text()
        ano = self.tela_add_livro.lineEdit_ano_publicacao.text()
        id = self.tela_add_livro.lineEdit_id_livro.text()

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
            self.mostrar_erro('Faltou informar o ID.')
            return

        try:
            criar_livro(titulo, autor, paginas, ano, id)
            QMessageBox.information(self, "Sucesso", f"Livro '{titulo}' adicionado com sucesso!")
            
            # Limpa os campos após adicionar
            self.tela_add_livro.lineEdit_titulo_livro.clear()
            self.tela_add_livro.lineEdit_autor_principal.clear()
            self.tela_add_livro.lineEdit_quantidade_paginas.clear()
            self.tela_add_livro.lineEdit_ano_publicacao.clear()
            self.tela_add_livro.lineEdit_id_livro.clear()

        except Exception as e:
            self.mostrar_erro(f"Erro ao adicionar livro: {e}")


    def listar_livros_na_tela(self):
        try:
            print("Listando livros...")
            livros = listar_livros()
            
            # Limpa a tabela antes de preencher
            self.modelo_tabela.setRowCount(0)
            
            # Define os cabeçalhos da tabela
            self.modelo_tabela.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano", "ID"])
            
            # Adiciona cada livro como uma linha na tabela
            for livro in livros:
                livro_dict = livro.to_dict()
                
                # Criando itens com formatação aprimorada
                titulo_item = QStandardItem(livro_dict.get('titulo', ''))
                autor_item = QStandardItem(livro_dict.get('autor', ''))
                paginas_item = QStandardItem(str(livro_dict.get('paginas', '')))
                ano_item = QStandardItem(str(livro_dict.get('ano', '')))
                id_item = QStandardItem(livro_dict.get('id', ''))
                
                # Configurando alinhamento
                titulo_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                autor_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                paginas_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                ano_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                
                # Adicionando número de sequência à linha (opcional)
                row = self.modelo_tabela.rowCount()
                sequence_item = QStandardItem(str(row + 1))
                sequence_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                
                # Inserindo itens na linha
                self.modelo_tabela.appendRow([titulo_item, autor_item, paginas_item, ano_item, id_item])
                
            # Não precisamos mais ajustar as colunas automaticamente, pois já configuramos isso no __init__
            
            # Exibe mensagem de sucesso se estiver na tela inicial
            tela_atual = self.QtStack.currentIndex()
            if tela_atual == 2:  # Tela inicial
                QMessageBox.information(self, "Sucesso", "Livros listados com sucesso!")
            
            print("Livros listados com sucesso.")
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
            self.mostrar_erro(f"Erro ao listar livros: {e}")
        
    def abrir_tela_inicial(self):
        self.QtStack.setCurrentIndex(2)
        self.tela_inicial.lineEdit_pesquisar.setText("")
        
        # Chama o método de ajuste da tabela que está definido em tela_inicial.py
        try:
            self.tela_inicial.ajustar_tabela(self)
        except Exception as e:
            print(f"Erro ao ajustar tabela da tela inicial: {e}")

    def abrir_tela_add_livro(self):
        self.QtStack.setCurrentIndex(3)

    def abrir_tela_editar_livro(self):           
        self.QtStack.setCurrentIndex(4)

    def abrir_tela_excluir_livro(self):
        self.QtStack.setCurrentIndex(5)
        
    def abrir_tela_listar_livros(self):
        self.QtStack.setCurrentIndex(6)
        self.listar_livros_na_tela()  
        
        try:
            self.tela_listar_livros.ajustar_tabela(self)
        except Exception as e:
            print(f"Erro ao ajustar tabela da tela listar livros: {e}")

    def editar_livro(self):
        titulo = self.tela_editar_livro.lineEdit_titulo_livro.text()
        autor = self.tela_editar_livro.lineEdit_autor_principal.text()
        paginas = self.tela_editar_livro.lineEdit_quantidade_paginas.text()
        ano = self.tela_editar_livro.lineEdit_ano_publicacao.text()
        id = self.tela_editar_livro.lineEdit_id_livro.text()

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
            self.mostrar_erro('Faltou informar o ID.')
            return
            

        try:
            atualizar_livro(id, titulo, autor, paginas, ano, id)
            QMessageBox.information(self, "Sucesso", f"Livro '{titulo}' atualizado com sucesso!")
            
            self.tela_editar_livro.lineEdit_titulo_livro.clear()
            self.tela_editar_livro.lineEdit_autor_principal.clear()
            self.tela_editar_livro.lineEdit_quantidade_paginas.clear()
            self.tela_editar_livro.lineEdit_ano_publicacao.clear()
            self.tela_editar_livro.lineEdit_id.clear()
            
            self.abrir_tela_inicial()
        except Exception as e:
            self.mostrar_erro(f"Erro ao editar livro: {e}")

    def excluir_livro(self):
        titulo = self.tela_excluir_livro.lineEdit_titulo_livro.text()
        id = self.tela_excluir_livro.lineEdit_id.text()

        if not id:
            self.mostrar_erro('Faltou informar o ID.')
            return
            
        titulo = self.tela_excluir_livro.lineEdit_titulo_livro.text()
        
        # Confirmação de exclusão
        confirmacao = QMessageBox.question(self, 'Confirmação', 
                                         f"Tem certeza que deseja excluir o livro '{titulo}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmacao == QMessageBox.No:
            return
            
        try:
            # Usa a função de deletar livro importada do módulo firebase.livros
            deletar_livro(id)
            QMessageBox.information(self, "Sucesso", f"Livro '{titulo}' excluído com sucesso!")
            
            # Limpa os campos após excluir
            self.tela_excluir_livro.lineEdit_titulo_livro.clear()
            self.tela_excluir_livro.lineEdit_id.clear()
            

        except Exception as e:
            self.mostrar_erro(f"Erro ao excluir livro: {e}")

    def mostrar_erro(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setWindowTitle("Erro")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())


        