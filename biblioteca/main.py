from PyQt5.QtWidgets import QApplication
from interface_grafica.interface_biblioteca import Biblioteca

if __name__ == "__main__":
        app = QApplication([])
        janela = Biblioteca()
        janela.show()
        app.exec_()