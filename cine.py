import csv
from typing import Optional

from excepciones import *


class Comestible:
    def __init__(self, nombre: str, cantidad_disponible: int, precio_unitario: float):
        self.nombre: str = nombre
        self.cantidad_disponible: int = cantidad_disponible
        self.precio_unitario: float = precio_unitario

    def unidades_disponibles(self, cantidad: int) -> bool:
        return self.cantidad_disponible >= cantidad

    def __str__(self):
        return f"Producto: {self.nombre}  -  Precio: {self.precio_unitario}  -  C. Disponible: {self.cantidad_disponible}"


class Pelicula:

    def __init__(self, nombre: str, duracion: int, genero: str):
        self.nombre: str = nombre
        self.duracion: int = duracion
        self.genero: str = genero


    def __str__(self):
        return self.nombre


class Sala:

    def __init__(self, hora: str, precio_boleta: float, pelicula: Pelicula):
        self.asientos =  []
        self.hora: str = hora
        self.precio_boleta: float = precio_boleta
        self.pelicula: Pelicula = pelicula

    def __str__(self):
        return f"Nombre: {self.pelicula.nombre}- Genero: {self.pelicula.genero}- Duracion: {self.pelicula.duracion} precio boleto: {self.precio_boleta}"


class Item:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad: int = cantidad
        self.total_item = 0

    def __str__(self):
        return f"NOMBRE = {self.producto}       CANTIDAD = {self.cantidad}"


class Bolsa:
    def __init__(self):
        self.items = []
        self.valor_total = 0

    def agregar_item(self, producto, cantidad):
        item = Item(producto, cantidad)
        self.items.append(item)


class Usuario:
    def __init__(self, cedula: str, nombre: str, clave: str):
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.clave: str = clave
        self.bolsa: Bolsa = Bolsa()

    def agregar_comestible_bolsa(self, comestible: Comestible, cantidad: int):
        self.bolsa.agregar_item(comestible, cantidad)


class Cine:

    def __init__(self):
        self.total_acumulado: float = 0
        self.comestibles: dict[str:Comestible] = {}
        self.usuarios: dict[str: Usuario] = {}
        self.clave_admin = "0721"
        self.usuario_actual: Usuario = Usuario("", "", "")
        #self.cargar_datos_peliculas()
        self.cargar_datos_comestibles()

    def registrar_usuario(self, cedula: str, nombre: str, clave: str):

        if self.buscar_usuario(cedula) is None:
            usuario = Usuario(cedula, nombre, clave)
            self.usuarios[cedula] = usuario

        else:
            raise CuentaExistenteError("esta cuenta ya esta registrada")

    def buscar_usuario(self, cedula: str) -> Optional[Usuario]:
        if cedula in self.usuarios.keys():
            return self.usuarios[cedula]
        else:
            return None

    def iniciar_sesion_usuario(self, cedula: str, clave: str):
        if cedula == "" or clave == "":
            raise EspaciosSinRellenar("debe lllenar todos los datos del ingreso")
        if cedula in self.usuarios.keys():
            usuario = self.usuarios[cedula]
        else:
            raise CuentaNoExistenteError("esta cuenta no esta registrada")
        if usuario.clave == clave:
            self.usuario_actual = usuario

        else:
            raise ContrasenaInvalida("la contraseña no es correcta")

    def iniciar_sesion_admin(self, clave: str) :
        if self.clave_admin != clave:
            raise ContrasenaInvalida("contraseña incorrecta")

    def buscar_comestible(self, nombre: str) -> Optional[Comestible]:
        if nombre in self.comestibles.keys():
            return self.comestibles[nombre]
        else:
            return None

    def agregar_comestibles_bolsa(self, nombre: str, cantidad: int) -> int:

        comestible = self.buscar_comestible(nombre)

        if comestible is not None:
            if comestible.unidades_disponibles(cantidad):

                self.usuario_actual.agregar_comestible_bolsa(comestible, cantidad)
                return 0
            else:
                return 1
        else:
            return 2

    def mostrar_items_bolsa(self):
        return self.usuario_actual.bolsa.items

    def mostrar_comestibles_disponibles(self) -> list:
        lista: list = []
        for objeto in self.comestibles.items():
            lista.append(objeto)
        return lista

    def eliminar_item(self, indice: int) -> bool:
        if (indice > 0) and (indice <= len(self.usuario_actual.bolsa.items)):
            self.usuario_actual.bolsa.items.pop(indice-1)
            return True
        else:
            return False

    """def cargar_datos_peliculas(self):
        with open("datos/peliculas") as file:"""

    def cargar_datos_comestibles(self):
        with open("datos/comestibles") as file:
            datos = csv.reader(file, delimiter="|")
            comestibles = map(lambda data: Comestible(data[0], int(data[1]), float(data[2])), datos)
            self.comestibles = {comestible.nombre: comestible for comestible in comestibles}

