import sys
import pyrebase
import re
from firebase.livros import criar_livro, listar_livros, atualizar_livro, deletar_livro
from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


from interface_grafica.py.login import Ui_Login
from interface_grafica.py.criar_conta import Ui_Criar_Conta
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.tela_inicial import Ui_Tela_Inicial
from interface_grafica.py.add_livro import Ui_Add_Livro
from interface_grafica.py.editar_livro import Ui_Editar_Livro
import interface_grafica.estilos as estilos

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

        self.tela_login = Ui_Login()
        self.tela_criar_conta = Ui_Criar_Conta()
        self.tela_inicial = Ui_Tela_Inicial()
        self.tela_add_livro = Ui_Add_Livro()
        self.tela_editar_livro = Ui_Editar_Livro()

        self.tela_login.setupUi(self.stack0)
        self.tela_criar_conta.setupUi(self.stack1)
        self.tela_inicial.setupUi(self.stack2)
        self.tela_add_livro.setupUi(self.stack3)
        self.tela_editar_livro.setupUi(self.stack4)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)

class Main(Ui_Main, QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        
        self.modelo_tabela = QStandardItemModel()
        self.modelo_tabela.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano", "ID"])
        
        self.tela_inicial.tableView.setModel(self.modelo_tabela)
        
        self.tela_inicial.pushButton_busca.setEnabled(False)
        
        self.tela_inicial.lineEdit_pesquisar.textChanged.connect(self.verificar_campo_busca)
        
        # Aplicar estilos aos componentes da interface
        self.aplicar_estilos_componentes()

        # Botões da tela de login
        self.tela_login.pushButton_criar_conta.clicked.connect(self.abrir_tela_criar_conta)
        self.tela_login.pushButton_entrar.clicked.connect(self.entrar_sistema)
        self.tela_login.pushButton_voltar.clicked.connect(self.sair)

        # Botões da tela de criar conta
        self.tela_criar_conta.pushButton_criar_conta.clicked.connect(self.criar_conta)
        self.tela_criar_conta.pushButton.clicked.connect(self.abrir_tela_login)

        # Botões da tela inicial
        self.tela_inicial.pushButton_add_livro.clicked.connect(self.abrir_tela_add_livro)
        self.tela_inicial.pushButton_voltar.clicked.connect(self.abrir_tela_login)
        self.tela_inicial.pushButton_busca.clicked.connect(self.buscar_livro)

        # Botões da tela adicionar livro
        self.tela_add_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_add_livro.pushButton_add_livro.clicked.connect(self.adicionar_livro)

        # Botões da tela editar livro
        self.tela_editar_livro.pushButton_voltar.clicked.connect(self.abrir_tela_inicial)
        self.tela_editar_livro.pushButton_add_livro.clicked.connect(self.editar_livro)

    def aplicar_estilos_componentes(self):
        self.stack0.setStyleSheet(estilos.estilo_janela_principal)
        self.stack1.setStyleSheet(estilos.estilo_janela_principal)
        self.stack2.setStyleSheet(estilos.estilo_janela_principal)
        self.stack3.setStyleSheet(estilos.estilo_janela_principal)
        self.stack4.setStyleSheet(estilos.estilo_janela_principal)
        
        # Aplicando estilo preto sólido à tela de login
        self.stack0.setStyleSheet(estilos.estilo_tela_login)
        
        # Estilo específico para a tela inicial - ajustando todos os elementos
        self.stack2.setStyleSheet(estilos.estilo_tela_inicial)
        
        # Ajustando o conteúdo da scroll area
        if self.tela_inicial.scrollAreaWidgetContents:
            self.tela_inicial.scrollAreaWidgetContents.setStyleSheet(estilos.estilo_scroll_content)
        
        # Botões da tela de login e criar conta
        self.tela_login.pushButton_entrar.setStyleSheet(estilos.estilo_botoes_login)
        self.tela_login.pushButton_criar_conta.setStyleSheet(estilos.estilo_botoes_login)
        self.tela_login.pushButton_voltar.setStyleSheet(estilos.estilo_botoes_voltar)
        self.tela_criar_conta.pushButton_criar_conta.setStyleSheet(estilos.estilo_botoes_adicionar)
        self.tela_criar_conta.pushButton.setStyleSheet(estilos.estilo_botoes_voltar)
        
        # Botões da tela inicial
        self.tela_inicial.pushButton_add_livro.setStyleSheet(estilos.estilo_botoes_adicionar)
        self.tela_inicial.pushButton_voltar.setStyleSheet(estilos.estilo_botoes_voltar)
        self.tela_inicial.pushButton_busca.setStyleSheet(estilos.estilo_botoes_login)
        
        # Estilo da tabela
        self.tela_inicial.tableView.setAlternatingRowColors(True)
        self.tela_inicial.tableView.horizontalHeader().setStyleSheet(estilos.estilo_cabecalho_tabela)
        self.tela_inicial.tableView.setStyleSheet(estilos.estilo_tabela)
        self.tela_inicial.tableView.verticalScrollBar().setStyleSheet(estilos.estilo_scrollbar)
        
        # Botões das telas de adicionar e editar
        self.tela_add_livro.pushButton_add_livro.setStyleSheet(estilos.estilo_botoes_adicionar)
        self.tela_add_livro.pushButton_voltar.setStyleSheet(estilos.estilo_botoes_voltar)
        self.tela_editar_livro.pushButton_add_livro.setStyleSheet(estilos.estilo_botoes_adicionar)
        self.tela_editar_livro.pushButton_voltar.setStyleSheet(estilos.estilo_botoes_voltar)
        
        # Login - campos com bordas azuis
        self.tela_login.lineEdit_email.setStyleSheet(estilos.estilo_campo_login)
        self.tela_login.lineEdit__senha.setStyleSheet(estilos.estilo_campo_login)
        
        # Criar conta
        self.tela_criar_conta.lineEdit_email.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_criar_conta.lineEdit_senha.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_criar_conta.lineEdit_conf_senha.setStyleSheet(estilos.estilo_campo_texto)
        
        # Busca
        self.tela_inicial.lineEdit_pesquisar.setStyleSheet(estilos.estilo_campo_texto)
        
        # Campos de adicionar livro
        self.tela_add_livro.lineEdit_titulo_livro.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_add_livro.lineEdit_autor_principal.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_add_livro.lineEdit_quantidade_paginas.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_add_livro.lineEdit_ano_publicacao.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_add_livro.lineEdit_id_livro.setStyleSheet(estilos.estilo_campo_texto)
        
        # Campos de editar livro
        self.tela_editar_livro.lineEdit_titulo_livro.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_editar_livro.lineEdit_autor_principal.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_editar_livro.lineEdit_quantidade_paginas.setStyleSheet(estilos.estilo_campo_texto)
        self.tela_editar_livro.lineEdit_ano_publicacao.setStyleSheet(estilos.estilo_campo_texto)

    def verificar_campo_busca(self):
        texto = self.tela_inicial.lineEdit_pesquisar.text().strip()
        self.tela_inicial.pushButton_busca.setEnabled(bool(texto) and texto.isdigit())

    def limpar_valor(self, valor):
        if isinstance(valor, list) and len(valor) > 0:
            return valor[0]
        valor_str = str(valor)
        if valor_str.startswith('[') and valor_str.endswith(']'):
            valor_str = valor_str[1:-1]  
            valor_str = valor_str.replace("'", "").replace('"', '')  
        return valor_str

    def mostrar_livro_na_tela(self, livro):
        try:
            layout = self.tela_inicial.scrollAreaWidgetContents.layout()
            self.limpar_scroll_area()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(self.tela_inicial.scrollAreaWidgetContents)
                self.tela_inicial.scrollAreaWidgetContents.setLayout(layout)

            if layout:
                for i in reversed(range(layout.count())):
                    widget = layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()  

            id = self.limpar_valor(livro.get('id', 'Desconhecido'))
            titulo = self.limpar_valor(livro.get('titulo', 'Desconhecido'))
            autor = self.limpar_valor(livro.get('autor', 'Desconhecido'))
            paginas = self.limpar_valor(livro.get('paginas', 'Desconhecido'))
            ano = self.limpar_valor(livro.get('ano', 'Desconhecido'))

            frame_info = QtWidgets.QFrame()
            frame_info.setStyleSheet(estilos.estilo_frame_info_livro)
            frame_layout = QtWidgets.QVBoxLayout(frame_info)

            label_titulo = QtWidgets.QLabel(f"Título: {titulo}")
            label_autor = QtWidgets.QLabel(f"Autor: {autor}")
            label_paginas = QtWidgets.QLabel(f"Páginas: {paginas}")
            label_ano = QtWidgets.QLabel(f"Ano: {ano}")

            label_titulo.setStyleSheet(estilos.estilo_label_info)
            label_autor.setStyleSheet(estilos.estilo_label_info)
            label_paginas.setStyleSheet(estilos.estilo_label_info)
            label_ano.setStyleSheet(estilos.estilo_label_info)

            info_layout = QtWidgets.QHBoxLayout()
            info_layout.addWidget(label_titulo)
            info_layout.addWidget(label_autor)
            info_layout.addWidget(label_paginas)
            info_layout.addWidget(label_ano)

            frame_layout.addLayout(info_layout)

            buttons_layout = QtWidgets.QHBoxLayout()  

            button_editar = QtWidgets.QPushButton("Editar")
            button_editar.setStyleSheet(estilos.estilo_botoes_editar)
            button_editar.clicked.connect(lambda: self.editar_livro(livro.get('id')))
            buttons_layout.addWidget(button_editar)

            button_excluir = QtWidgets.QPushButton("Excluir")
            button_excluir.setStyleSheet(estilos.estilo_botoes_excluir)
            button_excluir.clicked.connect(lambda: self.excluir_livro(livro.get('id')))
            buttons_layout.addWidget(button_excluir)

            frame_layout.addLayout(buttons_layout)
            layout.addWidget(frame_info)

            # Garantindo que o scrollAreaWidgetContents tenha o estilo correto
            self.tela_inicial.scrollAreaWidgetContents.setStyleSheet(estilos.estilo_scroll_content)

        except Exception as e:
            print(f"Erro ao exibir livro na tela: {e}")

    def editar_livro(self, id_livro):
        self.abrir_tela_editar_livro(id_livro)

        livro = self.buscar_livro_por_id(id_livro)
        if not livro:
            QMessageBox.warning(self, "Erro", "Livro não encontrado.")
            return

        self.id_livro_atual = id_livro

        
        titulo = self.limpar_valor(livro.get('titulo', ''))
        autor = self.limpar_valor(livro.get('autor', ''))
        paginas = self.limpar_valor(livro.get('paginas', ''))
        ano = self.limpar_valor(livro.get('ano', ''))

        self.tela_editar_livro.lineEdit_titulo_livro.setText(titulo)
        self.tela_editar_livro.lineEdit_autor_principal.setText(autor)
        self.tela_editar_livro.lineEdit_quantidade_paginas.setText(paginas)
        self.tela_editar_livro.lineEdit_ano_publicacao.setText(ano)

        try:
            self.tela_editar_livro.pushButton_add_livro.clicked.disconnect()
        except TypeError:
            pass  

        self.tela_editar_livro.pushButton_add_livro.clicked.connect(self.salvar_edicao_livro)

    def salvar_edicao_livro(self):
       
        if not hasattr(self, 'id_livro_atual'):
            QMessageBox.warning(self, "Erro", "Nenhum livro foi selecionado para edição.")
            return

        titulo_final = self.tela_editar_livro.lineEdit_titulo_livro.text().strip()
        autor_final = self.tela_editar_livro.lineEdit_autor_principal.text().strip()
        paginas_final = self.tela_editar_livro.lineEdit_quantidade_paginas.text().strip()
        ano_final = self.tela_editar_livro.lineEdit_ano_publicacao.text().strip()

        if not titulo_final or not autor_final or not paginas_final or not ano_final:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        
        if not paginas_final.isdigit() or int(paginas_final) <= 0:
            QMessageBox.warning(self, "Erro", "O número de páginas deve ser um número inteiro positivo.")
            return

        
        if not ano_final.isdigit():
            QMessageBox.warning(self, "Erro", "O ano de publicação deve conter apenas números.")
            return

        ano_int = int(ano_final)
        from datetime import datetime
        ano_atual = datetime.now().year

        if ano_int < 1000 or ano_int > ano_atual:
            QMessageBox.warning(self, "Erro", f"O ano de publicação deve estar entre 1000 e {ano_atual}.")
            return

        try:
            
            atualizar_livro(
                self.id_livro_atual, 
                self.limpar_valor(titulo_final), 
                self.limpar_valor(autor_final), 
                self.limpar_valor(paginas_final), 
                self.limpar_valor(ano_final),                
            )
            QMessageBox.information(self, "Sucesso", f"Livro '{titulo_final}' atualizado com sucesso!")

            self.abrir_tela_inicial()
        except Exception as e:
            self.mostrar_erro(f"Erro ao editar livro: {e}")

    def abrir_tela_editar_livro(self, id_livro):
        self.QtStack.setCurrentIndex(4)  

    def abrir_tela_inicial(self):
        self.QtStack.setCurrentIndex(2)  
        
        # Aplicando estilo para garantir que a tela tenha fundo preto
        self.stack2.setStyleSheet(estilos.estilo_tela_inicial)
        
        # Garantindo que o scrollAreaWidgetContents também tenha o estilo correto
        if self.tela_inicial.scrollAreaWidgetContents:
            self.tela_inicial.scrollAreaWidgetContents.setStyleSheet(estilos.estilo_scroll_content)
        
        self.tela_inicial.lineEdit_pesquisar.setText("")  
        self.tela_inicial.pushButton_busca.setEnabled(False)

        self.limpar_scroll_area()
        self.listar_livros_na_tela()

    def limpar_scroll_area(self):
        try:
            scroll_area_widget = self.tela_inicial.scrollAreaWidgetContents

            for widget in scroll_area_widget.findChildren(QtWidgets.QWidget):
                widget.deleteLater()

            novo_layout = QtWidgets.QVBoxLayout(scroll_area_widget)
            scroll_area_widget.setLayout(novo_layout)  

            scroll_area_widget.setStyleSheet(estilos.estilo_scroll_content)
            
            scroll_area_widget.update()

        except Exception as e:
            print(f"Erro ao limpar a scrollArea: {e}")


    def buscar_livro_por_id(self, id_livro):
        try:
            livro_ref = config_firebase.db.collection("livros").document(id_livro).get()
            
            if livro_ref.exists:
                livro = livro_ref.to_dict()
                print(f"Livro encontrado: {livro}")
                return livro
            else:
                print("Livro não encontrado")
                return None
        except Exception as e:
            print(f"Erro ao buscar livro: {e}")
            return None

    def buscar_livro(self):
        id_livro = self.tela_inicial.lineEdit_pesquisar.text().strip()

        # Garante que a área de exibição de resultados tenha o estilo correto antes da busca
        self.tela_inicial.scrollArea.setStyleSheet(estilos.estilo_scroll_area_busca)
        self.tela_inicial.scrollAreaWidgetContents.setStyleSheet(estilos.estilo_scroll_content)

        livro = self.buscar_livro_por_id(id_livro)

        if livro:
            self.mostrar_livro_na_tela(livro)  
        else:
            QMessageBox.warning(self, "Erro", "Livro não encontrado.")
            
        # Garante que a área mantenha o estilo mesmo após a exibição do resultado
        self.tela_inicial.scrollAreaWidgetContents.setStyleSheet(estilos.estilo_scroll_content)

    def abrir_tela_login(self):
        self.QtStack.setCurrentIndex(0)
        self.tela_login.lineEdit_email.clear()
        self.tela_login.lineEdit__senha.clear()
        
        # Garante que a tela de login tenha o fundo preto
        self.stack0.setStyleSheet(estilos.estilo_tela_login)
        
        # Reaplica os estilos aos campos de entrada
        self.tela_login.lineEdit_email.setStyleSheet(estilos.estilo_campo_login)
        self.tela_login.lineEdit__senha.setStyleSheet(estilos.estilo_campo_login)

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
        self.tela_criar_conta.lineEdit_email.clear()
        self.tela_criar_conta.lineEdit_senha.clear()
        self.tela_criar_conta.lineEdit_conf_senha.clear()

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
        
        if len(senha) < 6 or len(conf_senha) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres.")
            return

        if senha != conf_senha:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            return

        try:
            user = config_firebase.auth.create_user_with_email_and_password(email, senha)
            print("Conta criada com sucesso!")
            QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
            self.abrir_tela_login()
        except Exception as e:
            # Verifica se o erro é de email já existente
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                QMessageBox.warning(self, "Erro", "Este email já está cadastrado. Use outro email ou faça login.")
            else:
                print(f"Erro ao criar usuário: {e}")
                QMessageBox.warning(self, "Erro", "Erro ao criar conta. Verifique os dados.")

    def adicionar_livro(self):
       
        titulo = self.tela_add_livro.lineEdit_titulo_livro.text().strip()
        autor = self.tela_add_livro.lineEdit_autor_principal.text().strip()
        paginas = self.tela_add_livro.lineEdit_quantidade_paginas.text().strip()
        ano = self.tela_add_livro.lineEdit_ano_publicacao.text().strip()
        id = self.tela_add_livro.lineEdit_id_livro.text().strip()

        
        if not all([titulo, autor, paginas, ano, id]):
            self.mostrar_erro('Todos os campos devem ser preenchidos.')
            return

        if not id.isdigit():
            self.mostrar_erro('O ID do livro deve ser um número.')
            return

       
        if self.buscar_livro_por_id(id):
            self.mostrar_erro(f"Já existe um livro com o ID {id}. Escolha outro ID.")
            return

        if not paginas.isdigit():
            self.mostrar_erro('O número de páginas deve ser um valor numérico.')
            return

        ano_atual = datetime.now().year
        if not (ano.isdigit() and len(ano) == 4 and 0 < int(ano) <= ano_atual):
            self.mostrar_erro(f'O ano de publicação deve ser válido.')
            return

        try:
            
            criar_livro(titulo, autor, paginas, ano, id)
            QMessageBox.information(self, "Sucesso", f"Livro '{titulo}' adicionado com sucesso!")

            
            self.tela_add_livro.lineEdit_titulo_livro.clear()
            self.tela_add_livro.lineEdit_autor_principal.clear()
            self.tela_add_livro.lineEdit_quantidade_paginas.clear()
            self.tela_add_livro.lineEdit_ano_publicacao.clear()
            self.tela_add_livro.lineEdit_id_livro.clear()

            
            self.abrir_tela_inicial()

        except Exception as e:
            self.mostrar_erro(f"Erro ao adicionar livro: {e}")


    def listar_livros_na_tela(self):
        try:
            print("Listando livros...")
            livros = list(listar_livros())  

            livros = livros[:30]
            
            self.modelo_tabela.setRowCount(0)
            
            self.modelo_tabela.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano", "ID"])
            
            for livro in livros:
                livro_dict = livro.to_dict()

                titulo = str(self.limpar_valor(livro_dict.get('titulo', '')))
                autor = str(self.limpar_valor(livro_dict.get('autor', '')))
                paginas = str(self.limpar_valor(livro_dict.get('paginas', '')))
                ano = str(self.limpar_valor(livro_dict.get('ano', '')))
                id_livro = str(self.limpar_valor(livro_dict.get('id', '')))

                titulo_item = QStandardItem(titulo)
                autor_item = QStandardItem(autor)
                paginas_item = QStandardItem(paginas)
                ano_item = QStandardItem(ano)
                id_item = QStandardItem(id_livro)

                
                titulo_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                autor_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                paginas_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                ano_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

                self.modelo_tabela.appendRow([titulo_item, autor_item, paginas_item, ano_item, id_item])

            print("Livros listados com sucesso.")
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
            self.mostrar_erro(f"Erro ao listar livros: {e}")
        

    def abrir_tela_add_livro(self):
        self.QtStack.setCurrentIndex(3)
        self.tela_add_livro.lineEdit_titulo_livro.clear()
        self.tela_add_livro.lineEdit_autor_principal.clear()
        self.tela_add_livro.lineEdit_quantidade_paginas.clear()
        self.tela_add_livro.lineEdit_ano_publicacao.clear()
        self.tela_add_livro.lineEdit_id_livro.clear()  

    def excluir_livro(self, id):

        if not id:
            self.mostrar_erro('Faltou informar o ID do livro.')
            return
            
        confirmacao = QMessageBox.question(self, 'Confirmação', 
                                         f"Tem certeza que deseja excluir o livro:'\nID: {id}",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmacao == QMessageBox.No:
            return
            
        try:
            deletar_livro(id)
            QMessageBox.information(self, "Sucesso", f"Livro do autor (ID: {id}) excluído com sucesso!")
            self.limpar_scroll_area()
            self.tela_inicial.lineEdit_pesquisar.clear()
            
            
            
            self.listar_livros_na_tela()

        except Exception as e:
            self.mostrar_erro(f"Erro ao excluir livro: {e}")

    def mostrar_erro(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setWindowTitle("Erro")
        msg.exec_()

    def sair(self):
        QtWidgets.QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())


        