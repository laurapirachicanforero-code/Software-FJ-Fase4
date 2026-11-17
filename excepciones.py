# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de excepciones personalizadas


# Clase base para los errores del sistema
class ErrorSistema(Exception):
    pass


# Error cuando se ingresan datos incorrectos
class DatosInvalidosError(ErrorSistema):
    pass


# Error cuando faltan datos obligatorios
class CampoVacioError(ErrorSistema):
    pass


# Error cuando un cliente ya está registrado
class ClienteDuplicadoError(ErrorSistema):
    pass


# Error cuando un cliente no existe
class ClienteNoEncontradoError(ErrorSistema):
    pass


# Error cuando un servicio no existe
class ServicioNoEncontradoError(ErrorSistema):
    pass


# Error cuando un servicio no está disponible
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Error cuando una reserva no es válida
class ReservaInvalidaError(ErrorSistema):
    pass


# Error cuando una reserva no existe
class ReservaNoEncontradaError(ErrorSistema):
    pass


# Error cuando una operación no está permitida
class OperacionNoPermitidaError(ErrorSistema):
    pass


# Error durante el cálculo de costos
class CalculoError(ErrorSistema):
    pass


# Error al registrar eventos en archivos
class RegistroError(ErrorSistema):
    pass
