# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de pruebas de funcionamiento

from gestor import GestorSistema
from excepciones import *


# Crear una instancia del sistema
sistema = GestorSistema()

# Contadores de pruebas
aprobadas = 0
fallidas = 0


# Función para ejecutar y evaluar cada prueba
def probar(nombre, funcion, *args, error_esperado=None):

    global aprobadas, fallidas

    print("\n" + "-" * 60)
    print(nombre)

    try:
        resultado = sistema.ejecutar_operacion(funcion, *args)

        if error_esperado is not None:
            fallidas += 1
            print("FALLIDA: se esperaba una excepción.")
        else:
            aprobadas += 1
            print("APROBADA: operación exitosa.")

        return resultado

    except ErrorSistema as error:

        if error_esperado and isinstance(error, error_esperado):
            aprobadas += 1
            print("APROBADA: error controlado.")
        else:
            fallidas += 1
            print("FALLIDA: error no esperado.")

        print("Mensaje:", error)


print("=" * 60)
print("SOFTWARE FJ - PINK EDITION")
print("PRUEBAS DE FUNCIONAMIENTO")
print("=" * 60)


# PRUEBA 1: Registro válido de cliente
probar(
    "01. Registrar cliente válido",
    sistema.registrar_cliente,
    "10000001", "Ana Martinez",
    "ana@example.com", "3000000001"
)

# PRUEBA 2: Documento inválido
probar(
    "02. Documento inválido",
    sistema.registrar_cliente,
    "ABC", "Maria Lopez",
    "maria@example.com", "3000000002",
    error_esperado=DatosInvalidosError
)

# PRUEBA 3: Correo inválido
probar(
    "03. Correo inválido",
    sistema.registrar_cliente,
    "10000003", "Maria Lopez",
    "correo_invalido", "3000000003",
    error_esperado=DatosInvalidosError
)

# PRUEBA 4: Cliente duplicado
probar(
    "04. Cliente duplicado",
    sistema.registrar_cliente,
    "10000001", "Ana Martinez",
    "ana@example.com", "3000000001",
    error_esperado=ClienteDuplicadoError
)

# PRUEBA 5: Campos vacíos
probar(
    "05. Campos obligatorios vacíos",
    sistema.registrar_cliente,
    "10000004", "", "", "",
    error_esperado=CampoVacioError
)

# PRUEBA 6: Crear servicio de sala
probar(
    "06. Registrar sala",
    sistema.registrar_servicio,
    "salas", "Sala ejecutiva", 50000
)

# PRUEBA 7: Crear servicio de equipos
probar(
    "07. Registrar equipo",
    sistema.registrar_servicio,
    "equipos", "Proyector", 35000
)

# PRUEBA 8: Crear servicio de asesoría
probar(
    "08. Registrar asesoría",
    sistema.registrar_servicio,
    "asesorias", "Consultoría técnica", 80000
)

# PRUEBA 9: Tarifa negativa
probar(
    "09. Tarifa negativa",
    sistema.registrar_servicio,
    "salas", "Sala de reuniones", -50000,
    error_esperado=DatosInvalidosError
)

# PRUEBA 10: Tipo de servicio inválido
probar(
    "10. Tipo de servicio inexistente",
    sistema.registrar_servicio,
    "transporte", "Servicio incorrecto", 50000,
    error_esperado=DatosInvalidosError
)

# PRUEBA 11: Reserva válida
probar(
    "11. Crear reserva válida",
    sistema.crear_reserva,
    "10000001", "S001", 3, 19, 10
)

# PRUEBA 12: Duración negativa
probar(
    "12. Reserva con duración negativa",
    sistema.crear_reserva,
    "10000001", "S001", -3,
    error_esperado=DatosInvalidosError
)

# PRUEBA 13: Cliente inexistente
probar(
    "13. Reserva con cliente inexistente",
    sistema.crear_reserva,
    "99999999", "S001", 2,
    error_esperado=ClienteNoEncontradoError
)

# PRUEBA 14: Servicio inexistente
probar(
    "14. Reserva con servicio inexistente",
    sistema.crear_reserva,
    "10000001", "S999", 2,
    error_esperado=ServicioNoEncontradoError
)

# PRUEBA 15: Confirmar reserva
probar(
    "15. Confirmar reserva",
    sistema.confirmar_reserva,
    "R001"
)

# PRUEBA 16: Procesar reserva
probar(
    "16. Procesar reserva confirmada",
    sistema.procesar_reserva,
    "R001"
)

# PRUEBA 17: Operación no permitida
probar(
    "17. Cancelar reserva procesada",
    sistema.cancelar_reserva,
    "R001",
    error_esperado=OperacionNoPermitidaError
)

# PRUEBA 18: Descuento inválido
probar(
    "18. Descuento superior al 100%",
    sistema.crear_reserva,
    "10000001", "S002", 2, 19, 150,
    error_esperado=CalculoError
)


# Mostrar resultados finales
print("\n" + "=" * 60)
print("RESULTADOS DE LAS PRUEBAS")
print("=" * 60)

print("Pruebas ejecutadas:", aprobadas + fallidas)
print("Pruebas aprobadas:", aprobadas)
print("Pruebas fallidas:", fallidas)

print("\nClientes registrados:", len(sistema.clientes))
print("Servicios registrados:", len(sistema.servicios))
print("Reservas registradas:", len(sistema.reservas))

print("\nArchivo de eventos:", sistema.archivo_log)
print("=" * 60)
