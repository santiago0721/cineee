import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

from cine import Cine
from excepciones import *


class InicioSesion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/inicio.ui", self)
        self.registro = Registro()
        self.cine = Cine()
        self.__configurar()
        self.menu_principal = Principal()
        self.registro.principal.append(self.cine)

    def __configurar(self):
        self.Button_registrarse.clicked.connect(self.abrir_ventana_registro)
        self.Button_ingresar.clicked.connect(self.abrir_ventana_principal)

    def abrir_ventana_principal(self):

        try:
            usuario = self.Txt_usuario.text()
            contrasena = self.Txt_clave.text()
            self.cine.iniciar_sesion_usuario(usuario, contrasena)

        except EspaciosSinRellenar as err:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

        except CuentaNoExistenteError as err:

            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

        except ContrasenaInvalida as err:

            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

        else:
            self.menu_principal.exec()

    def abrir_ventana_registro(self):
        self.registro.exec()


class Registro(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Registro.ui", self)
        self.principal = []
        self.__configurar()

    def __configurar(self):
        self.Button_ok.accepted.connect(self.registro_ventana)
        self.Button_ok.rejected.connect(self.cerrar)

    def cerrar(self):
        pass

    def registro_ventana(self):

        try:
            if self.Txt_cedula.text() != "" and self.Txt_nombre.text() != "" and self.Txt_contrasena.text() != "":
                cedula = self.Txt_cedula.text()
                nombre = self.Txt_nombre.text()
                clave = self.Txt_contrasena.text()
                print("se debe mostrar mensaje de cuenta creada")
                self.principal[0].registrar_usuario(cedula, clave, nombre)
            else:
                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Critical)
                mensaje_ventana.setText("debe llenar todos los datos del formulario")
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()

        except CuentaExistenteError as err:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()


class Principal(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/menu_principal.ui", self)
        # self.__configurar()

    def __configurar(self):
        self.Button_reservar_p.clicked.connect("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = InicioSesion()
    inicio.show()
    sys.exit(app.exec())
