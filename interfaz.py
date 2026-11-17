# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de interfaz gráfica

import customtkinter as ctk

from temas import obtener_tema, FUENTE
from idiomas import traducir


# Clase principal de la aplicación
class SoftwareFJ(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.title("Software FJ - Pink Edition")
        self.geometry("1200x750")
        self.minsize(900, 600)

        # Preferencias iniciales
        self.idioma = "es"
        self.oscuro = False
        self.pagina = "inicio"

        # Listas internas del sistema
        self.clientes = []
        self.servicios = []
        self.reservas = []

        self.construir_interfaz()

    # Obtener la traducción
    def t(self, clave):
        return traducir(clave, self.idioma)

    # Cambiar el tema visual
    def cambiar_tema(self):
        self.oscuro = not self.oscuro
        self.construir_interfaz()

    # Cambiar el idioma
    def cambiar_idioma(self, opcion):
        self.idioma = "es" if opcion == "Español" else "en"
        self.construir_interfaz()

    # Navegar entre los módulos
    def navegar(self, pagina):
        self.pagina = pagina
        self.construir_interfaz()

    # Construir la interfaz principal
    def construir_interfaz(self):

        for elemento in self.winfo_children():
            elemento.destroy()

        ctk.set_appearance_mode(
            "dark" if self.oscuro else "light"
        )

        self.c = obtener_tema(self.oscuro)
        self.configure(fg_color=self.c["fondo"])

        # Menú lateral
        lateral = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=self.c["lateral"]
        )
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral,
            text="SOFTWARE FJ",
            font=(FUENTE, 27, "bold"),
            text_color=self.c["principal"]
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            lateral,
            text="P I N K  E D I T I O N",
            font=(FUENTE, 11),
            text_color=self.c["secundario"]
        ).pack()

        # Opciones de navegación
        opciones = [
            ("inicio", "⌂"),
            ("clientes", "♙"),
            ("servicios", "◇"),
            ("reservas", "▦"),
            ("eventos", "☷"),
            ("configuracion", "⚙")
        ]

        for clave, simbolo in opciones:

            seleccionado = self.pagina == clave

            ctk.CTkButton(
                lateral,
                text=f"{simbolo}   {self.t(clave)}",
                font=(FUENTE, 14),
                height=45,
                corner_radius=12,
                anchor="w",
                fg_color=(
                    self.c["seleccion"]
                    if seleccionado else "transparent"
                ),
                hover_color=self.c["seleccion"],
                text_color=self.c["texto"],
                command=lambda p=clave: self.navegar(p)
            ).pack(fill="x", padx=15, pady=6)

        # Botón para cerrar la aplicación
        ctk.CTkButton(
            lateral,
            text=self.t("salir"),
            fg_color=self.c["principal"],
            hover_color=self.c["hover"],
            corner_radius=12,
            height=40,
            command=self.destroy
        ).pack(side="bottom", fill="x", padx=20, pady=25)

        # Área principal
        principal = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        principal.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # Encabezado superior
        encabezado = ctk.CTkFrame(
            principal,
            fg_color="transparent"
        )
        encabezado.pack(fill="x", pady=(0, 25))

        # Selector de idioma
        selector = ctk.CTkOptionMenu(
            encabezado,
            values=["Español", "English"],
            command=self.cambiar_idioma,
            fg_color=self.c["principal"],
            button_color=self.c["hover"],
            button_hover_color=self.c["principal"],
            text_color="#FFFFFF",
            width=125
        )
        selector.set(
            "Español" if self.idioma == "es" else "English"
        )
        selector.pack(side="right", padx=5)

        # Selector de tema
        ctk.CTkButton(
            encabezado,
            text="☀" if self.oscuro else "☾",
            font=(FUENTE, 22),
            width=45,
            height=35,
            fg_color=self.c["tarjeta"],
            hover_color=self.c["seleccion"],
            text_color=self.c["principal"],
            command=self.cambiar_tema
        ).pack(side="right", padx=5)

        # Título del módulo seleccionado
        ctk.CTkLabel(
            principal,
            text=self.t(
                "panel" if self.pagina == "inicio"
                else self.pagina
            ),
            font=(FUENTE, 28, "bold"),
            text_color=self.c["texto"],
            anchor="w"
        ).pack(fill="x")

        # Mostrar el módulo correspondiente
        if self.pagina == "inicio":
            self.mostrar_inicio(principal)

        elif self.pagina == "configuracion":
            self.mostrar_configuracion(principal)

        else:
            ctk.CTkLabel(
                principal,
                text=self.t("desarrollo"),
                font=(FUENTE, 18),
                text_color=self.c["secundario"]
            ).pack(pady=70)

        # Estado del sistema
        ctk.CTkLabel(
            principal,
            text="●  " + self.t("operativo"),
            font=(FUENTE, 12),
            text_color=self.c["exito"]
        ).pack(side="bottom", anchor="w")

    # Panel de administración
    def mostrar_inicio(self, padre):

        ctk.CTkLabel(
            padre,
            text=self.t("bienvenida"),
            font=(FUENTE, 15),
            text_color=self.c["secundario"]
        ).pack(anchor="w", pady=(5, 25))

        indicadores = ctk.CTkFrame(
            padre,
            fg_color="transparent"
        )
        indicadores.pack(fill="x")

        datos = [
            ("clientes", len(self.clientes)),
            ("servicios", len(self.servicios)),
            ("reservas", len(self.reservas))
        ]

        for clave, cantidad in datos:

            tarjeta = ctk.CTkFrame(
                indicadores,
                fg_color=self.c["tarjeta"],
                corner_radius=18,
                height=130
            )
            tarjeta.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            ctk.CTkLabel(
                tarjeta,
                text=str(cantidad),
                font=(FUENTE, 42, "bold"),
                text_color=self.c["principal"]
            ).pack(pady=(20, 0))

            ctk.CTkLabel(
                tarjeta,
                text=self.t(clave),
                font=(FUENTE, 15),
                text_color=self.c["texto"]
            ).pack(pady=(0, 20))

        # Catálogo de tipos de servicios
        catalogo = ctk.CTkFrame(
            padre,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        catalogo.pack(fill="x", pady=30)

        titulo = (
            "Tipos de servicios"
            if self.idioma == "es"
            else "Service categories"
        )

        ctk.CTkLabel(
            catalogo,
            text=titulo,
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        for servicio in ["salas", "equipos", "asesorias"]:

            ctk.CTkLabel(
                catalogo,
                text="◇   " + self.t(servicio),
                font=(FUENTE, 16),
                text_color=self.c["principal"]
            ).pack(anchor="w", padx=30, pady=12)

    # Panel de configuración
    def mostrar_configuracion(self, padre):

        ctk.CTkLabel(
            padre,
            text=self.t("tema"),
            font=(FUENTE, 18),
            text_color=self.c["texto"]
        ).pack(anchor="w", pady=20)

        interruptor = ctk.CTkSwitch(
            padre,
            text=self.t("oscuro"),
            progress_color=self.c["principal"],
            text_color=self.c["texto"],
            command=self.cambiar_tema
        )

        if self.oscuro:
            interruptor.select()

        interruptor.pack(anchor="w", pady=10)

        ctk.CTkLabel(
            padre,
            text=self.t("idioma"),
            font=(FUENTE, 18),
            text_color=self.c["texto"]
        ).pack(anchor="w", pady=20)

        selector = ctk.CTkSegmentedButton(
            padre,
            values=["Español", "English"],
            selected_color=self.c["principal"],
            selected_hover_color=self.c["hover"],
            command=self.cambiar_idioma
        )
        selector.set(
            "Español" if self.idioma == "es" else "English"
        )
        selector.pack(anchor="w")
