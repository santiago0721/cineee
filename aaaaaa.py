import sys

from PyQt5.QtWidgets import QApplication

from interfaz import InicioSesion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = InicioSesion()
    inicio.show()
    sys.exit(app.exec())