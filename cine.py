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
        return f"Producto: {self.nombre} - Precio: {self.precio_unitario} "


class Pelicula:

    def __init__(self, nombre: str, duracion: str, genero: str):

        self.salas: [Pelicula] = []
        self.nombre: str = nombre
        self.duracion: str = duracion
        self.genero: str = genero


    def __str__(self):
        return f"Nombre: {self.nombre} ----- Duracion: {self.duracion} ----- Genero: {self.genero}"


    def crear_sala(self,hora, precio_boleta):
        sala = Sala(hora, precio_boleta, self)
        self.salas.append(sala)




class Sala:

    def __init__(self, hora: str, precio_boleta: float, pelicula: Pelicula):
        self.cantidad_disponible = 20
        self.hora: str = hora
        self.precio_unitario: float = precio_boleta
        self.pelicula: Pelicula = pelicula

    def __str__(self):
        return f"Nombre: {self.pelicula.nombre}- Genero: {self.pelicula.genero}- Duracion: {self.pelicula.duracion} precio boleto: {self.precio_unitario}"


class Item:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad: int = cantidad
        self.total_item = 0



    def __str__(self):
        return f"NOMBRE = {self.producto}      CANTIDAD = {self.cantidad}"


class Bolsa:
    def __init__(self):
        self.items = []
        self.valor_total = 0

    def agregar_item(self, producto, cantidad):
        item = Item(producto, cantidad)
        self.items.append(item)
        return item

    def total(self):
        total = 0
        for objeto in self.items:
            total += objeto.cantidad * objeto.producto.precio_unitario
        return total

    def eliminar(self, indice):
        self.items.pop(indice)

    def descontar_items_bolsa(self):
        for item in self.items:
            item.producto.cantidad_disponible -= item.cantidad

    def vaciar_bolsa(self):
        self.items.clear()

class Usuario:
    def __init__(self, cedula: str, nombre: str, clave: str):
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.clave: str = clave
        self.bolsa: Bolsa = Bolsa()

    def agregar_comestible_bolsa(self, comestible: Comestible, cantidad: int):
        self.bolsa.agregar_item(comestible, cantidad)

    def agregar_sala_bolsa(self, sala, cantidad):
        self.bolsa.agregar_item(sala, cantidad)
    def total(self):
        return self.bolsa.total()

    def eliminar_item_bolsa(self, indice):
        self.bolsa.eliminar(indice)

    def items_bolsa(self):
        self.bolsa.descontar_items_bolsa()

    def vaciar_bolsa(self):
        self.bolsa.vaciar_bolsa()




class Cine:

    def __init__(self):
        self.total_acumulado: float = 0
        self.comestibles: dict[str:Comestible] = {}
        self.usuarios: dict[str: Usuario] = {}
        self.peliculas: dict[str: Pelicula] = {}
        self.clave_admin = "0721"
        self.usuario_actual: Usuario = Usuario("", "", "")
        self.cargar_datos_peliculas()
        self.cargar_datos_comestibles()
        self.cargar_datos_usuarios()
        self.cargar_datos_salas()

    def registrar_usuario(self, cedula: str, nombre: str, clave: str):

        if self.buscar_usuario(cedula) is None:
            usuario = Usuario(cedula, nombre, clave)
            self.usuarios[cedula] = usuario
            self.agregar_usuario_archivo(cedula, nombre, clave)

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

    def iniciar_sesion_admin(self, clave: str):
        if self.clave_admin != clave:
            raise ContrasenaInvalida("contraseña incorrecta")


    def agregar_comestibles_bolsa(self, comestible, cantidad: int):
        if comestible.cantidad_disponible >= cantidad:
            return self.usuario_actual.agregar_comestible_bolsa(comestible, cantidad)
        else:
            raise CantidadNoDisponible("no se puede agregar esta cantidad del producto solo "
                                       f"hay {comestible.cantidad_disponible} unidades disponibles")
    def agregar_sala_bolsa(self, sala, cantidad: int):
        if sala.cantidad_disponible >= cantidad:
            return self.usuario_actual.agregar_sala_bolsa(sala, cantidad)
        else:
            raise CantidadNoDisponible("no se puede agregar esta cantidad del producto solo "
                                       f"hay {sala.cantidad_disponible} unidades disponibles")

    def mostrar_items_bolsa(self):
        return self.usuario_actual.bolsa.items


    def eliminar_item(self, indice: int):
        self.usuario_actual.eliminar_item_bolsa(indice)

    def comprar_bolsa(self):
        total= self.calucular_total()
        self.usuario_actual.vaciar_bolsa()
        return total

    def calucular_total(self):
        total = self.usuario_actual.total()
        return total


    def cargar_datos_peliculas(self):
        with open("datos/peliculas", encoding="utf8") as file:
            datos = csv.reader(file, delimiter="|")
            peliculas = map(lambda data: Pelicula(data[0], data[1], data[2]), datos)
            self.peliculas = {pelicula.nombre: pelicula for pelicula in peliculas}
    def cargar_datos_comestibles(self):
        with open("datos/comestibles", encoding="utf8") as file:
            datos = csv.reader(file, delimiter="|")
            comestibles = map(lambda data: Comestible(data[0], int(data[1]), float(data[2])), datos)
            self.comestibles = {comestible.nombre: comestible for comestible in comestibles}

    def guardar_nuevo_comestible(self,nombre:str,cantidad_disponible:int, precio_unitario:float):
        with open ("datos/comestibles", encoding="utf8", mode="a") as file:
            file.write(f"\n{nombre}|{cantidad_disponible}|{precio_unitario}")

    def guardar_nueva_pelicula(self, nombre: str, duracion: str, genero: str):
        with open ("datos/peliculas", encoding="utf8", mode="a") as file:
            file.write(f"\n{nombre}|{duracion}|{genero}")
    def agregar_nuevo_comestible(self,nombre:str,cantidad_disponible:str, precio_unitario:str):
        if nombre == "" or cantidad_disponible == "" or precio_unitario == "":
            raise EspaciosSinRellenar("debe lllenar todos los datos")

        else:
            self.guardar_nuevo_comestible(nombre, int(cantidad_disponible), float(precio_unitario))

    def agregar_nueva_pelicula(self,nombre:str,duracion:str, genero:str):
        if nombre == "" or duracion == "" or genero == "":
            raise EspaciosSinRellenar("debe lllenar todos los datos")

        else:
            self.guardar_nueva_pelicula(nombre, duracion, genero)

    def cargar_datos_usuarios(self):
        with open("datos/usuarios", encoding="utf8") as file:
            datos = csv.reader(file, delimiter="|")
            usuarios = map(lambda data: Usuario(data[0], data[1], data[2]), datos)
            self.usuarios = {usuario.clave: usuario for usuario in usuarios}

    def cargar_datos_salas(self):
        with open("datos/salas", encoding="utf8") as file:
            for linea in file:
                info = linea.split("|")
                self.peliculas[info[2]].salas.append(Sala(info[0], float(info[1]), self.peliculas[info[2]]))

    def agregar_usuario_archivo(self, cedula: str, nombre: str, clave: str):
        with open ("datos/usuarios", encoding="utf8", mode="a") as file:
            file.write(f"\n{cedula}|{nombre}|{clave}")

    def agregar_sala_archivo(self,hora, precio_boleta, pelicula:Pelicula):
        with open ("datos/salas", encoding="utf8", mode="a") as file:
            file.write(f"\n{hora}|{precio_boleta}|{pelicula.nombre}|{pelicula.duracion}|{pelicula.genero}")

    def crear_sala(self, hora, precio_boleta, pelicula:Pelicula):
        if hora == "" or precio_boleta == "":
            raise EspaciosSinRellenar("debe llenar todos los espacios")

        else:
            pelicula.crear_sala(hora, precio_boleta)
            self.agregar_sala_archivo(hora, precio_boleta, pelicula)

    def descuento(self, total):
        if total >= 150000:
            return 15, total * 0.85
        else:
            return 10, total * 0.9
    def mensaje_descuento(self, total):
        if total >= 90000:
            cantidad, valor = self.descuento(total)
            return f""" 
            el valor total de la compra es de {total} 
            se realizo un descuento de {cantidad} %
            el valor a pagar es {valor}"""
        else:
            return f"el valor a pagar es {total}"

    def descontar_unidades(self):
        self.usuario_actual.items_bolsa()


    def vaciar_bolsa(self):
        self.usuario_actual.vaciar_bolsa()
    def comestible_mas_caro(self):
        comestibles = list(self.comestibles.values())
        mas_caro = comestibles[0]
        for comestible in comestibles:
            if mas_caro.precio_unitario < comestible.precio_unitario:
                mas_caro = comestible
        return mas_caro

    def comestible_mas_barato(self):
        comestibles = list(self.comestibles.values())
        mas_barato = comestibles[0]
        for comestible in comestibles:
            if mas_barato.precio_unitario > comestible.precio_unitario:
                mas_barato = comestible
        return mas_barato

    def lista_salas(self):
        lista = []
        peliculas = list(self.peliculas.values())
        for pelicula in peliculas:
            for peli in pelicula.salas:
                lista.append(peli)
        return lista

    def sala_mas_cara(self):
        lista = self.lista_salas()
        mas_cara = lista[0]
        for sala in lista:
            if mas_cara.precio_unitario < sala.precio_unitario:
                mas_cara = sala

        return mas_cara

    def sala_mas_barata(self):
        lista = self.lista_salas()
        mas_barata = lista[0]
        for sala in lista:
            if mas_barata.precio_unitario > sala.precio_unitario:
                mas_barata = sala

        return mas_barata


    def estadisticas(self):

        comestible_mas_caro = self.comestible_mas_caro()
        comestible_mas_barato = self.comestible_mas_barato()
        sala_mas_cara = self.sala_mas_cara()
        sala_mas_barata = self.sala_mas_barata()
        return (comestible_mas_caro.nombre, comestible_mas_caro.precio_unitario),\
               (comestible_mas_caro.nombre, comestible_mas_barato.precio_unitario),\
               (sala_mas_cara.pelicula.nombre, sala_mas_cara.precio_unitario),\
               (sala_mas_barata.pelicula.nombre, sala_mas_barata.precio_unitario)













