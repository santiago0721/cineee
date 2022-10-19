import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog

from cine import Cine


class InicioSesion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/inicio.ui", self)
        self.Cine = Cine()
        self.registro = Registro()
        self.__configurar()


    def __configurar(self):
        self.Button_registrarse.clicked.connect(self.registro_ventana)

    def registro_ventana(self):
        respuesta = self.registro.exec()
        if respuesta == QDialog.Accepted:
            self.registro.registrar_usuario()



class Registro(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Registro.ui", self)
        self.__configurar()



    def __configurar(self):
        self.Button_ok.clicked.connect(self.registrar_usuario)


    def registrar_usuario(self):

        cedula = self.Txt_cedula.text()
        nombre = self.Txt_nombre.text()
        clave = self.Txt_contrasena.text()
        self.Cine.registrar_usuario(cedula, clave, nombre)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = InicioSesion()
    inicio.show()
    sys.exit(app.exec())

