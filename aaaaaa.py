import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QWidget

from cine import Cine
from excepciones import CuentaExistenteError

class InicioSesion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/inicio.ui", self)
        self.registro = Registro()
        self.cine = Cine()
        self.__configurar()
        self.registro.principal.append(self.cine)



    def __configurar(self):
        self.Button_registrarse.clicked.connect(self.abrir_ventana_registro)


    def abrir_ventana_registro(self):
        self.respuesta = self.registro.exec()



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
                print(("sss"))
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




class IngresarPrincipal(QWidget):
    def __init__(self):
        QWidget.__init__(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    inicio = InicioSesion()
    inicio.show()
    sys.exit(app.exec())