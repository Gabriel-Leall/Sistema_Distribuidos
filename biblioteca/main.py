from PyQt5.QtWidgets import QApplication
from interface_grafica.interface_biblioteca import Biblioteca

if __name__ == "__main__":
    try:
        app = QApplication([])
        janela = Biblioteca()
        janela.show()
        app.exec_()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
