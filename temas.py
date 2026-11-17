# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de configuración visual

# Paleta de colores para el tema claro
TEMA_CLARO = {
    "fondo": "#FFF5F9",
    "lateral": "#F9E1ED",
    "tarjeta": "#FFFFFF",
    "principal": "#CE488C",
    "hover": "#B53676",
    "texto": "#552640",
    "secundario": "#916D83",
    "borde": "#EFDBe7",
    "seleccion": "#EFBED7",
    "exito": "#36A77C",
    "error": "#D94F65",
    "alerta": "#E5A93D"
}

# Paleta de colores para el tema oscuro
TEMA_OSCURO = {
    "fondo": "#18131E",
    "lateral": "#261C2C",
    "tarjeta": "#302536",
    "principal": "#EF80B4",
    "hover": "#D6639A",
    "texto": "#FAEAF3",
    "secundario": "#BFA9BD",
    "borde": "#49354D",
    "seleccion": "#553047",
    "exito": "#65D6A4",
    "error": "#FF758F",
    "alerta": "#F4C46B"
}

# Configuración de la tipografía
FUENTE = "Segoe UI"

# Función para seleccionar la paleta de colores
def obtener_tema(oscuro=False):
    return TEMA_OSCURO if oscuro else TEMA_CLARO
