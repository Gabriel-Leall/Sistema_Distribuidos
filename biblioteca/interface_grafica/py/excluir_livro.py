# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'excluir_livro.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Excluir_Livro(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(636, 331)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 30, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 150, 541, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_autor_principal = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_autor_principal.setObjectName("lineEdit_autor_principal")
        self.horizontalLayout_2.addWidget(self.lineEdit_autor_principal)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 100, 541, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_titulo_livro = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_titulo_livro.setObjectName("lineEdit_titulo_livro")
        self.horizontalLayout.addWidget(self.lineEdit_titulo_livro)
        self.pushButton_voltar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_voltar.setGeometry(QtCore.QRect(50, 210, 121, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_voltar.setFont(font)
        self.pushButton_voltar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_voltar.setStyleSheet(" border-radius: 8px;\n"
"background-color: rgb(190, 190, 190);")
        self.pushButton_voltar.setObjectName("pushButton_voltar")
        self.pushButton_add_livro = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_livro.setGeometry(QtCore.QRect(430, 210, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_add_livro.setFont(font)
        self.pushButton_add_livro.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_add_livro.setStyleSheet("\n"
"background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
" border-radius: 8px;")
        self.pushButton_add_livro.setObjectName("pushButton_add_livro")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 636, 26))
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
        self.label.setText(_translate("MainWindow", "Excluir Livro"))
        self.label_3.setText(_translate("MainWindow", "Autor principal:"))
        self.label_2.setText(_translate("MainWindow", "Título do livro:"))
        self.pushButton_voltar.setText(_translate("MainWindow", "Voltar"))
        self.pushButton_add_livro.setText(_translate("MainWindow", "Excluir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Excluir_Livro()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
