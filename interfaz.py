import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

from cine import Cine
from excepciones import CuentaExistenteError

cine = Cine()
class InicioSesion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/inicio.ui", self)
        self.registro = Registro()
        self.__configurar()


    def __configurar(self):
        self.Button_registrarse.clicked.connect(self.ssss)


    def ssss(self):
        self.respuesta = self.registro.exec()
    def registro_ventana(self):

        if self.respuesta == QDialog.Accepted:
            try:
                self.registro.registrar_usuario()
            except CuentaExistenteError as err:
                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Warning)
                mensaje_ventana.setText(err.mensaje)
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()


class Registro(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Registro.ui", self)
        self.__configurar()



    def __configurar(self):
        self.Button_ok.accepted.connect("no se como conectar")

    def registrar_usuario(self):
        cedula = self.Txt_cedula.text()
        nombre = self.Txt_nombre.text()
        clave = self.Txt_contrasena.text()
        print(("sss"))
        Cine.registrar_usuario(cedula, clave, nombre)

    def accept(self) -> None:
        if self.Txt_cedula.text() != "" and self.Txt_nombre.text() != "" and self.Txt_contrasena.text() != "":
            super(Registro, self).accept()
        else:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText("debe llenar todos los datos del formulario")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = InicioSesion()
    inicio.show()
    sys.exit(app.exec())

