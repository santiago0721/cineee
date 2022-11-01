from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QAbstractItemView, QInputDialog

from cine import Cine
from excepciones import *


class InicioSesion(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/inicio.ui", self)
        self.registro = Registro()
        self.Admin = Admin()
        self.cine = Cine()
        self.__configurar()
        self.menu_principal = Principal()
        self.registro.principal.append(self.cine)

    def __configurar(self):
        self.Button_registrarse.clicked.connect(self.abrir_ventana_registro)
        self.Button_ingresar.clicked.connect(self.abrir_ventana_principal)
        self.Button_admin.clicked.connect(self.inicio_admin)

    def __limpiar(self):
        self.Txt_usuario.clear()
        self.Txt_clave.clear()

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
            self.__limpiar()

        except ContrasenaInvalida as err:

            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()
            self.Txt_clave.clear()

        else:
            self.menu_principal.exec()
            self.__limpiar()

    def abrir_ventana_registro(self):
        self.registro.exec()

    def inicio_admin(self):
        if self.Txt_clave.text() != "":
            try:
                self.cine.iniciar_sesion_admin(self.Txt_clave.text())
            except ContrasenaInvalida as err:
                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Critical)
                mensaje_ventana.setText(err.mensaje)
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()

            else:
                self.Admin.exec()


class Registro(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Registro.ui", self)
        self.principal = []
        self.__configurar()

    def __configurar(self):
        self.Button_ok.accepted.connect(self.registro_ventana)
        self.Button_ok.rejected.connect(self.cerrar)

    def __limpiar(self):
        self.Txt_cedula.clear()
        self.Txt_nombre.clear()
        self.Txt_contrasena.clear()

    def cerrar(self):
        pass

    def registro_ventana(self):

        try:
            if self.Txt_cedula.text() != "" and self.Txt_nombre.text() != "" and self.Txt_contrasena.text() != "":
                cedula = self.Txt_cedula.text()
                nombre = self.Txt_nombre.text()
                clave = self.Txt_contrasena.text()
                self.principal[0].registrar_usuario(cedula, clave, nombre)
                self.__limpiar()

                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle(":)")
                mensaje_ventana.setText("registro exitoso")
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()
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
            self.__limpiar()




class Admin(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/admin.ui", self)
        self.cine = Cine()
        self.__configurar()
        self.__cargar_datos()

    def __configurar(self):
        self.Button_Cargar_comestible.clicked.connect(self.nuevo_comestible)

        self.Button_Cargar_pelicula.clicked.connect(self.nueva_pelicula)

        self.listView_.setModel(QStandardItemModel())

        self.Button_Crear_sala.clicked.connect(self.crear_sala)


    def nueva_pelicula(self):
        nombre = self.Txt_Nombre_pelicula_2.text()
        duracion = self.Txt_duracion.text()
        genero = self.Txt_Genero.text()
        try:
            self.cine.agregar_nueva_pelicula(nombre, duracion, genero)
        except EspaciosSinRellenar as err:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()
        else:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle(":)")
            mensaje_ventana.setText("pelicula creada ")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

    def nuevo_comestible(self):
        nombre = self.Txt_Nombre_comestible.text()
        cantidad_disponible = self.Txt_Cantidad_disponible.text()
        precio_unitario = self.Txt_Precio_unitario.text()
        try:
            self.cine.agregar_nuevo_comestible(nombre, cantidad_disponible, precio_unitario)
        except EspaciosSinRellenar as err:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()
        except ValueError:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText("ingrese datos numericos de tipo entero en el campo de cantidad disponible "
                                    "y datos numericos de cualquier tipo en el ultimo campo")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

        else:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle(":)")
            mensaje_ventana.setText("comestible creado ")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()




    def __cargar_datos(self):
        peliculas = list(self.cine.peliculas.values())
        for pelicula in peliculas:
            item = QStandardItem(str(pelicula))
            item.pelicula = pelicula
            item.setEditable(False)
            self.listView_.model().appendRow(item)

    def crear_sala(self):
        try:
            modelo = self.listView_.model()
            valor = modelo.itemFromIndex(self.listView_.selectedIndexes()[0])
            hora = self.Txt_hora.text()
            precio_boleta = float(self.Txt_Precio_boleta.text())
            self.cine.crear_sala(hora, precio_boleta, valor.pelicula)

        except EspaciosSinRellenar as err:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText(err.mensaje)
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()
        except IndexError:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText("debe seleccionar una pelicula")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

        except ValueError:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Critical)
            mensaje_ventana.setText("debe ingresar un valor numerico en : Precio boleta")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()


        else:
            self.Txt_hora.clear()
            self.Txt_Precio_boleta.clear()
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle(":)")
            mensaje_ventana.setText("sala creada")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()






class Principal(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.cine = Cine()
        uic.loadUi("gui/menu_principal.ui", self)
        self.__configurar()
        self.__cargar_datos()

    def __configurar(self):
        self.Button_agregar_comestible_p.clicked.connect(self.agregra_comestible_a_bolsa)
        self.Button_eliminar_bolsa_p.clicked.connect(self.eliminar_item)
        self.Button_ver_estadisticas_p.clicked.connect(self.estadisticas)
        self.Button_comprar_bolsa_p.clicked.connect(self.abrir_comprar_bolsa)
        self.Button_reservar_p.clicked.connect(self.reservar)
        self.listView_comestibles.setModel(QStandardItemModel())

        self.listView_peliculas.setModel(QStandardItemModel())

        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(["NOMBRE", "CANT", "TOTAl"])
        self.tableView.setModel(table_model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 70)
        self.tableView.setColumnWidth(2, 80)

    def agregra_comestible_a_bolsa(self):
        cantidad, ok = QInputDialog.getInt(self, "Agregar comestible a bolsa", "Cantidad", 1)

        if ok:
            try:

                modelo = self.listView_comestibles.model()
                valor = modelo.itemFromIndex(self.listView_comestibles.selectedIndexes()[0])
                objeto = self.cine.agregar_comestibles_bolsa(valor.comestible, cantidad)

            except IndexError:

                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Warning)
                mensaje_ventana.setText("debe seleccionar un comestible")
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()

            except CantidadNoDisponible as err:

                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Warning)
                mensaje_ventana.setText(err.mensaje)

                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()


            else:
                total = "${:,.2f}".format(valor.comestible.precio_unitario * cantidad)
                celda_1 = QStandardItem(valor.comestible.nombre)
                celda_2 = QStandardItem(str(cantidad))
                celda_3 = QStandardItem(total)
                celda_1.item = objeto

                model = self.tableView.model()
                model.appendRow([celda_1, celda_2, celda_3])
                self.total_bolsa()

    def reservar(self):
        cantidad, ok = QInputDialog.getInt(self, "Agregar funcion a bolsa", "Cantidad", 1)

        if ok:
            try:

                modelo = self.listView_peliculas.model()
                valor = modelo.itemFromIndex(self.listView_peliculas.selectedIndexes()[0])
                objeto = self.cine.agregar_sala_bolsa(valor.sala, cantidad)

            except IndexError:

                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Warning)
                mensaje_ventana.setText("debe seleccionar un comestible")
                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()

            except CantidadNoDisponible as err:

                mensaje_ventana = QMessageBox(self)
                mensaje_ventana.setWindowTitle("Error")
                mensaje_ventana.setIcon(QMessageBox.Warning)
                mensaje_ventana.setText(err.mensaje)

                mensaje_ventana.setStandardButtons(QMessageBox.Ok)
                mensaje_ventana.exec()


            else:
                total = "${:,.2f}".format(valor.sala.precio_unitario * cantidad)
                celda_1 = QStandardItem(valor.sala.pelicula.nombre)
                celda_2 = QStandardItem(str(cantidad))
                celda_3 = QStandardItem(total)
                celda_1.item = objeto

                model = self.tableView.model()
                model.appendRow([celda_1, celda_2, celda_3])
                self.total_bolsa()


    def eliminar_item(self):
        try:
            selection_model = self.tableView.selectionModel()
            modelo = self.tableView.model()
            row_index = selection_model.selectedIndexes()[0].row()
            self.cine.eliminar_item(row_index)
            modelo.removeRow(row_index)
            self.total_bolsa()
        except IndexError:
            mensaje_ventana = QMessageBox(self)
            mensaje_ventana.setWindowTitle("Error")
            mensaje_ventana.setIcon(QMessageBox.Warning)
            mensaje_ventana.setText("debe seleccionar un item")
            mensaje_ventana.setStandardButtons(QMessageBox.Ok)
            mensaje_ventana.exec()

    def total_bolsa(self):
        total = self.cine.calucular_total()
        self.lineEdit.setText("${:,.2f}".format(total))

    def __cargar_datos(self):
        comestibles = list(self.cine.comestibles.values())
        for comestible in comestibles:
            item = QStandardItem(str(comestible))
            item.comestible = comestible
            item.setEditable(False)
            self.listView_comestibles.model().appendRow(item)

        peliculas = list(self.cine.peliculas.values())
        for pelicula in peliculas:
            for sala in pelicula.salas:
                objeto = QStandardItem(str(sala))
                objeto.sala = sala
                objeto.setEditable(False)
                self.listView_peliculas.model().appendRow(objeto)

    def vaciar_bolsa(self):

        selection_model = self.tableView.selectionModel()
        modelo = self.tableView.model()
        for indice in self.cine.usuario_actual.bolsa.items:
            modelo.removeRow(0)

    def abrir_comprar_bolsa(self):
        self.vaciar_bolsa()
        total = self.cine.calucular_total()
        mensaje = self.cine.mensaje_descuento(total)
        mensaje_ventana = QMessageBox(self)
        mensaje_ventana.setWindowTitle("COMPRA")
        mensaje_ventana.setText(mensaje)
        mensaje_ventana.setStandardButtons(QMessageBox.Ok)
        mensaje_ventana.exec()
        self.cine.descontar_unidades()


    def estadisticas(self):
        mensaje = self.cine.estadisticas()
        mensaje_ventana = QMessageBox(self)
        mensaje_ventana.setWindowTitle("Estadisticas")
        mensaje_ventana.setText(f"""
        comestible mas caro = {mensaje[0][0]} su precio es {mensaje[0][1]}
        comestible mas barato = {mensaje[1][0]} su precio es {mensaje[1][1]}       

""")
        mensaje_ventana.setStandardButtons(QMessageBox.Ok)
        mensaje_ventana.exec()
        self.cine.descontar_unidades()









