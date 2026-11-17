# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de programación orientada a objetos

from abc import ABC, abstractmethod
import re

from excepciones import (
    DatosInvalidosError,
    CampoVacioError
)


# Clase abstracta general del sistema
class Entidad(ABC):

    def __init__(self, identificador):
        if not str(identificador).strip():
            raise CampoVacioError("El identificador es obligatorio.")

        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass


# Clase Cliente que hereda de Entidad
class Cliente(Entidad):

    def __init__(self, documento, nombre, correo, telefono):

        super().__init__(documento)

        # Validar los datos antes de almacenarlos
        if not all(str(dato).strip() for dato in
                   (documento, nombre, correo, telefono)):
            raise CampoVacioError("Todos los campos son obligatorios.")

        if not re.fullmatch(r"[0-9]{5,15}", str(documento).strip()):
            raise DatosInvalidosError("Documento de identidad inválido.")

        if len(nombre.strip()) < 3 or not all(
            letra.isalpha() or letra.isspace()
            for letra in nombre.strip()
        ):
            raise DatosInvalidosError("Nombre inválido.")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo.strip()):
            raise DatosInvalidosError("Correo electrónico inválido.")

        if not re.fullmatch(r"[0-9]{7,15}", str(telefono).strip()):
            raise DatosInvalidosError("Número de teléfono inválido.")

        # Encapsulación de datos personales
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = str(telefono).strip()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.identificador

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Sobrescritura del método abstracto
    def describir(self):
        return f"{self.nombre} - {self.documento}"


# Importar excepciones adicionales
from excepciones import (
    ServicioNoDisponibleError,
    CalculoError
)
import math


# Clase abstracta para los servicios
class Servicio(Entidad):

    def __init__(self, identificador, nombre, tarifa):

        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise CampoVacioError("El nombre del servicio es obligatorio.")

        try:
            tarifa = float(tarifa)
        except (ValueError, TypeError) as error:
            raise DatosInvalidosError("Tarifa inválida.") from error

        if not math.isfinite(tarifa) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser positiva y finita.")

        self._nombre = nombre.strip()
        self._tarifa = tarifa
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("Estado de disponibilidad inválido.")

        self._disponible = estado

    # Validar los parámetros del servicio
    @abstractmethod
    def validar_parametros(self, duracion):
        if not self.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no está disponible."
            )

        try:
            horas = float(duracion)
        except (ValueError, TypeError) as error:
            raise DatosInvalidosError("Duración inválida.") from error

        if not math.isfinite(horas) or horas <= 0:
            raise DatosInvalidosError("La duración debe ser positiva y finita.")

        return horas

    # Método abstracto para calcular costos
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    # Cálculo con parámetros opcionales
    def calcular_total(self, subtotal, impuesto=0, descuento=0):

        try:
            impuesto = float(impuesto)
            descuento = float(descuento)

            if not 0 <= impuesto <= 100:
                raise ValueError("Impuesto fuera del rango permitido.")

            if not 0 <= descuento <= 100:
                raise ValueError("Descuento fuera del rango permitido.")

            base = subtotal * (1 - descuento / 100)
            total = base * (1 + impuesto / 100)

            if not math.isfinite(total) or total < 0:
                raise ValueError("Resultado del cálculo inválido.")

            return round(total, 2)

        except (ValueError, TypeError, OverflowError) as error:
            raise CalculoError("Error al calcular el costo.") from error


# Servicio especializado: reserva de salas
class Sala(Servicio):

    def validar_parametros(self, duracion):

        horas = super().validar_parametros(duracion)

        if horas > 12:
            raise DatosInvalidosError(
                "Una sala puede reservarse hasta 12 horas."
            )

        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        horas = self.validar_parametros(duracion)
        subtotal = self.tarifa * horas

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        return f"Sala: {self.nombre}"


# Servicio especializado: alquiler de equipos
class Equipo(Servicio):

    def validar_parametros(self, duracion):

        horas = super().validar_parametros(duracion)

        if horas > 72:
            raise DatosInvalidosError(
                "El alquiler no puede superar las 72 horas."
            )

        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        horas = self.validar_parametros(duracion)
        subtotal = self.tarifa * horas

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        return f"Equipo: {self.nombre}"


# Servicio especializado: asesoría profesional
class Asesoria(Servicio):

    def validar_parametros(self, duracion):

        horas = super().validar_parametros(duracion)

        if horas > 8:
            raise DatosInvalidosError(
                "La asesoría no puede superar las 8 horas."
            )

        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        horas = self.validar_parametros(duracion)
        subtotal = self.tarifa * horas

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        return f"Asesoría: {self.nombre}"


# Excepciones para la gestión de reservas
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


# Clase encargada de gestionar las reservas
class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio,
                 duracion, impuesto=0, descuento=0):

        super().__init__(identificador)

        # Validar el cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Cliente inválido.")

        # Validar el servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Servicio inválido.")

        # Almacenar los datos de la reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__estado = "pendiente"

        # Validar duración y calcular el costo
        self.__duracion = servicio.validar_parametros(duracion)
        self.__costo = servicio.calcular_costo(
            self.__duracion, impuesto, descuento
        )

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # Confirmar una reserva pendiente
    def confirmar(self):

        if self.estado != "pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no está disponible."
            )

        self.__estado = "confirmada"

    # Cancelar una reserva
    def cancelar(self):

        if self.estado not in ("pendiente", "confirmada"):
            raise OperacionNoPermitidaError(
                "La reserva no se puede cancelar."
            )

        self.__estado = "cancelada"

    # Procesar una reserva confirmada
    def procesar(self):

        if self.estado != "confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada."
            )

        self.__estado = "procesada"

        return self.costo

    # Describir la reserva
    def describir(self):

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} h | "
            f"Estado: {self.estado}"
        )
