import sys
import pyrebase
import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QByteArray

from interface_grafica.py.login import Ui_Login
from interface_grafica.py.criar_conta import Ui_Criar_Conta
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.add_livro import Ui_Add_Livro
from interface_grafica.py.editar_livro import Ui_Editar_Livro
from interface_grafica.py.excluir_livro import Ui_Excluir_Livro

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

        self.tela_login = Ui_Login()
        self.tela_criar_conta = Ui_Criar_Conta()
        self.tela_inicial = Ui_Tela_Inicial()
        self.tela_add_livro = Ui_Add_Livro()
        self.tela_editar_livro = Ui_Editar_Livro()
        self.tela_excluir_livro = Ui_Excluir_Livro()

        self.tela_login.setupUi(self.stack0)
        self.tela_criar_conta.setupUi(self.stack1)
        self.tela_inicial.setupUi(self.stack2)
        self.tela_add_livro.setupUi(self.stack3)
        self.tela_editar_livro.setupUi(self.stack4)
        self.tela_excluir_livro.setupUi(self.stack5)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)

class Main(Ui_Main, QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

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

        # Botões da tela adicionar livro
        self.tela_add_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)

        # Botões da tela editar livro
        self.tela_editar_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)

        # Botões da tela excluir livro
        self.tela_excluir_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)


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


        
    def abrir_tela_inicial(self):
        self.QtStack.setCurrentIndex(2)
        self.tela_inicial.lineEdit_pesquisar.setText("")

    def abrir_tela_add_livro(self):
        self.QtStack.setCurrentIndex(3)

    def abrir_tela_editar_livro(self):
        self.QtStack.setCurrentIndex(4)

    def abrir_tela_excluir_livro(self):
        self.QtStack.setCurrentIndex(5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())


        