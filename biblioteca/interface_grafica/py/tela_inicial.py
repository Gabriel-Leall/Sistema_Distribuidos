# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_inicial.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tela_Inicial(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(917, 675)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(20, 90, 851, 191))
        self.tableView.setObjectName("tableView")
        self.pushButton_add_livro = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_livro.setGeometry(QtCore.QRect(720, 20, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_add_livro.setFont(font)
        self.pushButton_add_livro.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_add_livro.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);\n"
" border-radius: 8px;")
        self.pushButton_add_livro.setObjectName("pushButton_add_livro")
        self.pushButton_voltar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_voltar.setGeometry(QtCore.QRect(30, 580, 111, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_voltar.setFont(font)
        self.pushButton_voltar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_voltar.setStyleSheet(" border-radius: 8px;\n"
"background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_voltar.setObjectName("pushButton_voltar")
        self.lineEdit_pesquisar = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_pesquisar.setGeometry(QtCore.QRect(490, 300, 261, 31))
        self.lineEdit_pesquisar.setObjectName("lineEdit_pesquisar")
        self.pushButton_busca = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_busca.setGeometry(QtCore.QRect(770, 300, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_busca.setFont(font)
        self.pushButton_busca.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_busca.setStyleSheet("background-color: rgb(0, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
" border-radius: 8px;")
        self.pushButton_busca.setObjectName("pushButton_busca")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 350, 851, 201))
        self.scrollArea.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 849, 199))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 300, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_add_livro.setText(_translate("MainWindow", "Adicionar livro"))
        self.pushButton_voltar.setText(_translate("MainWindow", "Sair do sistema"))
        self.lineEdit_pesquisar.setPlaceholderText(_translate("MainWindow", "Digite o ID do livro..."))
        self.pushButton_busca.setText(_translate("MainWindow", "Buscar"))
        self.label.setText(_translate("MainWindow", " Livros cadastrados"))
        self.label_2.setText(_translate("MainWindow", "Buscar livro"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Tela_Inicial()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
