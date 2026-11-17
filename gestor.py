# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de gestión del sistema

from datetime import datetime
from pathlib import Path

from modelos import Cliente, Sala, Equipo, Asesoria, Reserva

from excepciones import (
    ErrorSistema,
    DatosInvalidosError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    ServicioNoEncontradoError,
    ReservaNoEncontradaError,
    RegistroError
)


# Clase administradora del sistema
class GestorSistema:

    def __init__(self):

        # Almacenamiento temporal sin base de datos
        self.clientes = []
        self.servicios = []
        self.reservas = []

        # Archivo para registrar eventos y errores
        self.archivo_log = Path(__file__).parent / "eventos.log"

    # Registrar eventos del sistema
    def registrar_evento(self, mensaje, nivel="INFO"):

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(f"[{fecha}] [{nivel}] {mensaje}\n")

        except OSError as error:
            raise RegistroError(
                "No fue posible escribir en el archivo de eventos."
            ) from error

    # Control centralizado de las operaciones
    def ejecutar_operacion(self, funcion, *args, **kwargs):

        try:
            resultado = funcion(*args, **kwargs)

        except ErrorSistema as error:
            self.registrar_evento(str(error), "ERROR")
            raise

        except Exception as error:
            mensaje = "Error inesperado durante la operación."
            self.registrar_evento(
                f"{mensaje} Tipo: {type(error).__name__}", "ERROR"
            )
            raise ErrorSistema(mensaje) from error

        else:
            self.registrar_evento(
                f"Operación exitosa: {funcion.__name__}"
            )
            return resultado

        finally:
            print(f"Operación finalizada: {funcion.__name__}")

    # Registrar un nuevo cliente
    def registrar_cliente(self, documento, nombre, correo, telefono):

        cliente = Cliente(documento, nombre, correo, telefono)

        if any(c.documento == cliente.documento for c in self.clientes):
            raise ClienteDuplicadoError(
                "El cliente ya se encuentra registrado."
            )

        self.clientes.append(cliente)

        return cliente

    # Buscar un cliente por su documento
    def buscar_cliente(self, documento):

        for cliente in self.clientes:

            if cliente.documento == str(documento).strip():
                return cliente

        raise ClienteNoEncontradoError("Cliente no encontrado.")

    # Registrar un nuevo servicio
    def registrar_servicio(self, tipo, nombre, tarifa):

        tipos = {
            "salas": Sala,
            "equipos": Equipo,
            "asesorias": Asesoria
        }

        if tipo not in tipos:
            raise DatosInvalidosError("Tipo de servicio inválido.")

        identificador = f"S{len(self.servicios) + 1:03d}"

        servicio = tipos[tipo](identificador, nombre, tarifa)

        self.servicios.append(servicio)

        return servicio

    # Buscar un servicio por su identificador
    def buscar_servicio(self, identificador):

        for servicio in self.servicios:

            if servicio.identificador == identificador:
                return servicio

        raise ServicioNoEncontradoError("Servicio no encontrado.")

    # Crear una nueva reserva
    def crear_reserva(self, documento, servicio_id,
                      duracion, impuesto=0, descuento=0):

        cliente = self.buscar_cliente(documento)
        servicio = self.buscar_servicio(servicio_id)

        identificador = f"R{len(self.reservas) + 1:03d}"

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion,
            impuesto,
            descuento
        )

        self.reservas.append(reserva)

        return reserva

    # Buscar una reserva
    def buscar_reserva(self, identificador):

        for reserva in self.reservas:

            if reserva.identificador == identificador:
                return reserva

        raise ReservaNoEncontradaError("Reserva no encontrada.")

    # Confirmar una reserva
    def confirmar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        reserva.confirmar()

        return reserva

    # Cancelar una reserva
    def cancelar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        reserva.cancelar()

        return reserva

    # Procesar una reserva
    def procesar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        return reserva.procesar()

    # Consultar el historial de eventos
    def leer_eventos(self):

        try:
            with open(self.archivo_log, "r", encoding="utf-8") as archivo:
                return archivo.read()

        except FileNotFoundError:
            return ""

        except OSError as error:
            raise RegistroError(
                "No fue posible consultar los eventos."
            ) from error
