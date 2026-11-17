# SOFTWARE FJ - Pink Edition
# UNAD - Programación 213023
# Estudiante: Laura del Carmen Pirachican Forero
# Módulo de interfaz gráfica

import customtkinter as ctk

from temas import obtener_tema, FUENTE
from idiomas import traducir
from gestor import GestorSistema
from excepciones import ErrorSistema

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

               # Conectar la interfaz con el gestor del sistema
        self.sistema = GestorSistema()

        # Listas compartidas con el gestor
        self.clientes = self.sistema.clientes
        self.servicios = self.sistema.servicios
        self.reservas = self.sistema.reservas

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
        elif self.pagina == "clientes":
            self.mostrar_clientes(principal)

        elif self.pagina == "servicios":
            self.mostrar_servicios(principal)

        elif self.pagina == "reservas":
            self.mostrar_reservas(principal)

        elif self.pagina == "eventos":
            self.mostrar_eventos(principal)
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

    # Módulo de gestión de clientes
    def mostrar_clientes(self, padre):

        contenido = ctk.CTkScrollableFrame(
            padre,
            fg_color="transparent"
        )
        contenido.pack(fill="both", expand=True, pady=15)

        formulario = ctk.CTkFrame(
            contenido,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        formulario.pack(fill="x", pady=10)

        titulo = (
            "Registrar nuevo cliente"
            if self.idioma == "es"
            else "Register new customer"
        )

        ctk.CTkLabel(
            formulario,
            text=titulo,
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        campos = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        campos.pack(fill="x", padx=20)

        campos.grid_columnconfigure(0, weight=1)
        campos.grid_columnconfigure(1, weight=1)

        entradas = {}

        for i, clave in enumerate(
            ["documento", "nombre", "correo", "telefono"]
        ):

            bloque = ctk.CTkFrame(
                campos,
                fg_color="transparent"
            )
            bloque.grid(
                row=i // 2,
                column=i % 2,
                sticky="ew",
                padx=8,
                pady=10
            )

            ctk.CTkLabel(
                bloque,
                text=self.t(clave),
                font=(FUENTE, 13),
                text_color=self.c["secundario"]
            ).pack(anchor="w")

            entrada = ctk.CTkEntry(
                bloque,
                height=38,
                corner_radius=10,
                fg_color=self.c["fondo"],
                border_color=self.c["borde"],
                text_color=self.c["texto"],
                font=(FUENTE, 14)
            )
            entrada.pack(fill="x", pady=5)

            entradas[clave] = entrada

        # Mensaje de confirmación o error
        mensaje = ctk.CTkLabel(
            formulario,
            text="",
            font=(FUENTE, 13),
            wraplength=450
        )
        mensaje.pack(pady=5)

        # Función para registrar al cliente
        def registrar_cliente():

            try:
                self.sistema.ejecutar_operacion(
                    self.sistema.registrar_cliente,
                    entradas["documento"].get(),
                    entradas["nombre"].get(),
                    entradas["correo"].get(),
                    entradas["telefono"].get()
                )

            except ErrorSistema as error:

                texto = str(error)

                if self.idioma == "en":

                    errores = {
                        "El identificador es obligatorio.":
                            "Identification is required.",
                        "Todos los campos son obligatorios.":
                            "All fields are required.",
                        "Documento de identidad inválido.":
                            "Invalid identification number.",
                        "Nombre inválido.":
                            "Invalid name.",
                        "Correo electrónico inválido.":
                            "Invalid email address.",
                        "Número de teléfono inválido.":
                            "Invalid phone number.",
                        "El cliente ya se encuentra registrado.":
                            "The customer is already registered."
                    }

                    texto = errores.get(
                        texto, "Unable to complete the operation."
                    )

                mensaje.configure(
                    text=texto,
                    text_color=self.c["error"]
                )

            else:

                for entrada in entradas.values():
                    entrada.delete(0, "end")

                actualizar_clientes()

                mensaje.configure(
                    text=self.t("exito"),
                    text_color=self.c["exito"]
                )

        ctk.CTkButton(
            formulario,
            text="+ " + self.t("registrar"),
            height=42,
            corner_radius=12,
            fg_color=self.c["principal"],
            hover_color=self.c["hover"],
            font=(FUENTE, 15, "bold"),
            command=registrar_cliente
        ).pack(fill="x", padx=25, pady=(5, 25))

        # Panel de clientes registrados
        listado = ctk.CTkFrame(
            contenido,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        listado.pack(fill="x", pady=15)

        ctk.CTkLabel(
            listado,
            text=(
                "Clientes registrados"
                if self.idioma == "es"
                else "Registered customers"
            ),
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        tabla = ctk.CTkFrame(
            listado,
            fg_color="transparent"
        )
        tabla.pack(fill="x", padx=20, pady=(0, 20))

        # Actualizar la lista de clientes
        def actualizar_clientes():

            for elemento in tabla.winfo_children():
                elemento.destroy()

            if not self.clientes:

                ctk.CTkLabel(
                    tabla,
                    text=(
                        "No hay clientes registrados"
                        if self.idioma == "es"
                        else "No registered customers"
                    ),
                    text_color=self.c["secundario"]
                ).pack(pady=20)

            for cliente in self.clientes:

                tarjeta = ctk.CTkFrame(
                    tabla,
                    fg_color=self.c["fondo"],
                    corner_radius=12
                )
                tarjeta.pack(fill="x", pady=5)

                ctk.CTkLabel(
                    tarjeta,
                    text=cliente.nombre,
                    font=(FUENTE, 17, "bold"),
                    text_color=self.c["principal"]
                ).pack(anchor="w", padx=15, pady=(10, 5))

                ctk.CTkLabel(
                    tarjeta,
                    text=(
                        f"{self.t('documento')}: {cliente.documento}\n"
                        f"{self.t('correo')}: {cliente.correo}\n"
                        f"{self.t('telefono')}: {cliente.telefono}"
                    ),
                    justify="left",
                    text_color=self.c["texto"],
                    font=(FUENTE, 13)
                ).pack(anchor="w", padx=15, pady=(0, 10))

        actualizar_clientes()


    # Módulo de gestión de servicios
    def mostrar_servicios(self, padre):

        contenido = ctk.CTkScrollableFrame(
            padre,
            fg_color="transparent"
        )
        contenido.pack(fill="both", expand=True, pady=15)

        formulario = ctk.CTkFrame(
            contenido,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        formulario.pack(fill="x", pady=10)

        ctk.CTkLabel(
            formulario,
            text=(
                "Registrar nuevo servicio"
                if self.idioma == "es"
                else "Register new service"
            ),
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        # Tipos de servicios disponibles
        tipos = {
            self.t("salas"): "salas",
            self.t("equipos"): "equipos",
            self.t("asesorias"): "asesorias"
        }

        ctk.CTkLabel(
            formulario,
            text=(
                "Tipo de servicio"
                if self.idioma == "es"
                else "Service type"
            ),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25)

        tipo = ctk.CTkOptionMenu(
            formulario,
            values=list(tipos.keys()),
            fg_color=self.c["principal"],
            button_color=self.c["hover"],
            height=38
        )
        tipo.pack(fill="x", padx=25, pady=8)

        # Campos del formulario
        ctk.CTkLabel(
            formulario,
            text=(
                "Nombre del servicio"
                if self.idioma == "es"
                else "Service name"
            ),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25)

        nombre = ctk.CTkEntry(
            formulario,
            height=38,
            corner_radius=10,
            fg_color=self.c["fondo"],
            border_color=self.c["borde"],
            text_color=self.c["texto"]
        )
        nombre.pack(fill="x", padx=25, pady=8)

        ctk.CTkLabel(
            formulario,
            text=(
                "Tarifa por hora (COP)"
                if self.idioma == "es"
                else "Hourly rate (COP)"
            ),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25)

        tarifa = ctk.CTkEntry(
            formulario,
            height=38,
            corner_radius=10,
            fg_color=self.c["fondo"],
            border_color=self.c["borde"],
            text_color=self.c["texto"]
        )
        tarifa.pack(fill="x", padx=25, pady=8)

        mensaje = ctk.CTkLabel(
            formulario,
            text="",
            wraplength=450
        )
        mensaje.pack(pady=5)

        # Registrar un servicio
        def registrar():

            try:
                self.sistema.ejecutar_operacion(
                    self.sistema.registrar_servicio,
                    tipos[tipo.get()],
                    nombre.get(),
                    tarifa.get()
                )

            except ErrorSistema as error:

                errores = {
                    "Tarifa inválida.":
                        "Invalid hourly rate.",
                    "La tarifa debe ser positiva y finita.":
                        "The hourly rate must be positive and finite.",
                    "El nombre del servicio es obligatorio.":
                        "Service name is required."
                }

                texto = str(error)

                if self.idioma == "en":
                    texto = errores.get(
                        texto, "Unable to register the service."
                    )

                mensaje.configure(
                    text=texto,
                    text_color=self.c["error"]
                )

            else:
                nombre.delete(0, "end")
                tarifa.delete(0, "end")

                actualizar_servicios()

                mensaje.configure(
                    text=self.t("exito"),
                    text_color=self.c["exito"]
                )

        ctk.CTkButton(
            formulario,
            text="+ " + self.t("registrar"),
            height=42,
            corner_radius=12,
            font=(FUENTE, 15, "bold"),
            fg_color=self.c["principal"],
            hover_color=self.c["hover"],
            command=registrar
        ).pack(fill="x", padx=25, pady=20)

        # Catálogo de servicios registrados
        listado = ctk.CTkFrame(
            contenido,
            corner_radius=18,
            fg_color=self.c["tarjeta"]
        )
        listado.pack(fill="x", pady=15)

        ctk.CTkLabel(
            listado,
            text=(
                "Servicios registrados"
                if self.idioma == "es"
                else "Registered services"
            ),
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        tabla = ctk.CTkFrame(
            listado,
            fg_color="transparent"
        )
        tabla.pack(fill="x", padx=20, pady=10)

        def actualizar_servicios():

            for elemento in tabla.winfo_children():
                elemento.destroy()

            if not self.servicios:

                ctk.CTkLabel(
                    tabla,
                    text=(
                        "No hay servicios registrados"
                        if self.idioma == "es"
                        else "No registered services"
                    ),
                    text_color=self.c["secundario"]
                ).pack(pady=20)

            for servicio in self.servicios:

                tarjeta = ctk.CTkFrame(
                    tabla,
                    fg_color=self.c["fondo"],
                    corner_radius=12
                )
                tarjeta.pack(fill="x", pady=6)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"{servicio.identificador} | {servicio.nombre}",
                    font=(FUENTE, 17, "bold"),
                    text_color=self.c["principal"]
                ).pack(anchor="w", padx=15, pady=10)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"$ {servicio.tarifa:,.2f} COP / h",
                    font=(FUENTE, 15),
                    text_color=self.c["texto"]
                ).pack(anchor="w", padx=15)

                def cambiar_estado(s=servicio):

                    try:
                        self.sistema.ejecutar_operacion(
                            s.cambiar_disponibilidad,
                            not s.disponible
                        )

                    except ErrorSistema as error:
                        mensaje.configure(
                            text=(
                                str(error)
                                if self.idioma == "es"
                                else "Unable to change availability."
                            ),
                            text_color=self.c["error"]
                        )

                    finally:
                        actualizar_servicios()

                ctk.CTkButton(
                    tarjeta,
                    text=(
                        "Disponible" if servicio.disponible
                        else "No disponible"
                    ) if self.idioma == "es" else (
                        "Available" if servicio.disponible
                        else "Unavailable"
                    ),
                    fg_color=(
                        self.c["exito"] if servicio.disponible
                        else self.c["error"]
                    ),
                    hover_color=self.c["hover"],
                    corner_radius=10,
                    command=cambiar_estado
                ).pack(anchor="w", padx=15, pady=12)

        actualizar_servicios()



    # Módulo de gestión de reservas
    def mostrar_reservas(self, padre):

        es = self.idioma == "es"

        contenido = ctk.CTkScrollableFrame(
            padre,
            fg_color="transparent"
        )
        contenido.pack(fill="both", expand=True, pady=15)

        formulario = ctk.CTkFrame(
            contenido,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        formulario.pack(fill="x", pady=10)

        ctk.CTkLabel(
            formulario,
            text="Crear nueva reserva" if es else "Create new booking",
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        # Obtener los clientes y servicios registrados
        clientes = {
            f"{c.documento} | {c.nombre}": c.documento
            for c in self.clientes
        }

        servicios = {
            f"{s.identificador} | {s.nombre}": s.identificador
            for s in self.servicios if s.disponible
        }

        # Selector de clientes
        ctk.CTkLabel(
            formulario,
            text="Seleccionar cliente" if es else "Select customer",
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25)

        cliente = ctk.CTkOptionMenu(
            formulario,
            values=list(clientes) or [
                "Sin clientes" if es else "No customers"
            ],
            fg_color=self.c["principal"],
            button_color=self.c["hover"],
            height=38
        )
        cliente.pack(fill="x", padx=25, pady=8)

        # Selector de servicios
        ctk.CTkLabel(
            formulario,
            text="Seleccionar servicio" if es else "Select service",
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25)

        servicio = ctk.CTkOptionMenu(
            formulario,
            values=list(servicios) or [
                "Sin servicios disponibles" if es
                else "No available services"
            ],
            fg_color=self.c["principal"],
            button_color=self.c["hover"],
            height=38
        )
        servicio.pack(fill="x", padx=25, pady=8)

        # Campos para calcular el costo
        campos = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        campos.pack(fill="x", padx=20, pady=10)

        entradas = {}

        for i, clave in enumerate(
            ["duracion", "impuesto", "descuento"]
        ):

            campos.grid_columnconfigure(i, weight=1)

            bloque = ctk.CTkFrame(
                campos,
                fg_color="transparent"
            )
            bloque.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=5
            )

            etiqueta = self.t(clave)

            if clave != "duracion":
                etiqueta += " (%)"

            ctk.CTkLabel(
                bloque,
                text=etiqueta,
                text_color=self.c["texto"]
            ).pack(anchor="w")

            entrada = ctk.CTkEntry(
                bloque,
                height=38,
                corner_radius=10,
                fg_color=self.c["fondo"],
                border_color=self.c["borde"],
                text_color=self.c["texto"]
            )
            entrada.pack(fill="x", pady=5)

            entrada.insert(0, "1" if clave == "duracion" else "0")

            entradas[clave] = entrada

        # Panel de cotización
        total = ctk.CTkLabel(
            formulario,
            text="$ 0.00 COP",
            font=(FUENTE, 34, "bold"),
            text_color=self.c["principal"]
        )
        total.pack(pady=15)

        mensaje = ctk.CTkLabel(
            formulario,
            text="",
            wraplength=450
        )
        mensaje.pack(pady=5)

        def mostrar_error(error):

            mensaje.configure(
                text=str(error) if es else (
                    "Unable to complete the operation: "
                    + type(error).__name__
                ),
                text_color=self.c["error"]
            )

        # Calcular el valor de la reserva
        def calcular():

            try:
                seleccionado = self.sistema.ejecutar_operacion(
                    self.sistema.buscar_servicio,
                    servicios.get(servicio.get(), "")
                )

                costo = self.sistema.ejecutar_operacion(
                    seleccionado.calcular_costo,
                    entradas["duracion"].get(),
                    entradas["impuesto"].get(),
                    entradas["descuento"].get()
                )

            except ErrorSistema as error:
                total.configure(text="$ 0.00 COP")
                mostrar_error(error)

            else:
                total.configure(text=f"$ {costo:,.2f} COP")

                mensaje.configure(
                    text=self.t("exito"),
                    text_color=self.c["exito"]
                )

        # Crear la reserva
        def crear():

            try:
                reserva = self.sistema.ejecutar_operacion(
                    self.sistema.crear_reserva,
                    clientes.get(cliente.get(), ""),
                    servicios.get(servicio.get(), ""),
                    entradas["duracion"].get(),
                    entradas["impuesto"].get(),
                    entradas["descuento"].get()
                )

            except ErrorSistema as error:
                mostrar_error(error)

            else:
                total.configure(
                    text=f"$ {reserva.costo:,.2f} COP"
                )

                actualizar_reservas()

                mensaje.configure(
                    text=self.t("exito"),
                    text_color=self.c["exito"]
                )

        botones = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        botones.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(
            botones,
            text="Calcular costo" if es else "Calculate cost",
            height=42,
            corner_radius=12,
            fg_color=self.c["principal"],
            hover_color=self.c["hover"],
            command=calcular
        ).pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(
            botones,
            text="Crear reserva" if es else "Create booking",
            height=42,
            corner_radius=12,
            fg_color=self.c["exito"],
            hover_color=self.c["hover"],
            command=crear
        ).pack(side="left", expand=True, fill="x", padx=5)

        # Listado de reservas
        listado = ctk.CTkFrame(
            contenido,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        listado.pack(fill="x", pady=15)

        ctk.CTkLabel(
            listado,
            text="Reservas registradas" if es else "Registered bookings",
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        tabla = ctk.CTkFrame(
            listado,
            fg_color="transparent"
        )
        tabla.pack(fill="x", padx=20, pady=10)

        # Ejecutar cambios de estado
        def cambiar_estado(funcion, identificador):

            try:
                self.sistema.ejecutar_operacion(
                    funcion,
                    identificador
                )

            except ErrorSistema as error:
                mostrar_error(error)

            else:
                actualizar_reservas()

                mensaje.configure(
                    text=self.t("exito"),
                    text_color=self.c["exito"]
                )

        def actualizar_reservas():

            for elemento in tabla.winfo_children():
                elemento.destroy()

            if not self.reservas:

                ctk.CTkLabel(
                    tabla,
                    text="No hay reservas" if es else "No bookings",
                    text_color=self.c["secundario"]
                ).pack(pady=20)

            for reserva in self.reservas:

                tarjeta = ctk.CTkFrame(
                    tabla,
                    fg_color=self.c["fondo"],
                    corner_radius=12
                )
                tarjeta.pack(fill="x", pady=8)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"{reserva.identificador} | {reserva.servicio.nombre}",
                    font=(FUENTE, 18, "bold"),
                    text_color=self.c["principal"]
                ).pack(anchor="w", padx=15, pady=10)

                ctk.CTkLabel(
                    tarjeta,
                    text=(
                        f"{reserva.cliente.nombre}\n"
                        f"{reserva.duracion:g} h\n"
                        f"$ {reserva.costo:,.2f} COP\n"
                        f"{self.t(reserva.estado)}"
                    ),
                    justify="left",
                    text_color=self.c["texto"],
                    font=(FUENTE, 14)
                ).pack(anchor="w", padx=15)

                acciones = ctk.CTkFrame(
                    tarjeta,
                    fg_color="transparent"
                )
                acciones.pack(fill="x", padx=10, pady=15)

                operaciones = [
                    (
                        "confirmar",
                        self.sistema.confirmar_reserva,
                        self.c["exito"]
                    ),
                    (
                        "cancelar",
                        self.sistema.cancelar_reserva,
                        self.c["error"]
                    ),
                    (
                        "procesar",
                        self.sistema.procesar_reserva,
                        self.c["principal"]
                    )
                ]

                for clave, funcion, color in operaciones:

                    ctk.CTkButton(
                        acciones,
                        text=self.t(clave),
                        width=95,
                        fg_color=color,
                        hover_color=self.c["hover"],
                        corner_radius=8,
                        command=lambda f=funcion, r=reserva.identificador:
                            cambiar_estado(f, r)
                    ).pack(side="left", padx=5)

        actualizar_reservas()


    # Módulo de registro de eventos y errores
    def mostrar_eventos(self, padre):

        es = self.idioma == "es"

        panel = ctk.CTkFrame(
            padre,
            fg_color=self.c["tarjeta"],
            corner_radius=18
        )
        panel.pack(fill="both", expand=True, pady=20)

        ctk.CTkLabel(
            panel,
            text=(
                "Historial de operaciones del sistema"
                if es else "System activity history"
            ),
            font=(FUENTE, 20, "bold"),
            text_color=self.c["texto"]
        ).pack(anchor="w", padx=25, pady=20)

        ctk.CTkLabel(
            panel,
            text=(
                "Consulta las operaciones exitosas y los errores registrados."
                if es else "View successful operations and recorded errors."
            ),
            font=(FUENTE, 13),
            text_color=self.c["secundario"],
            wraplength=500
        ).pack(anchor="w", padx=25, pady=5)

        # Indicadores de actividad
        indicadores = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        indicadores.pack(fill="x", padx=20, pady=15)

        contadores = {}

        for clave, titulo, color in [
            (
                "total",
                "Total de eventos" if es else "Total events",
                self.c["principal"]
            ),
            (
                "info",
                "Operaciones exitosas" if es else "Successful operations",
                self.c["exito"]
            ),
            (
                "error",
                "Errores registrados" if es else "Recorded errors",
                self.c["error"]
            )
        ]:

            tarjeta = ctk.CTkFrame(
                indicadores,
                fg_color=self.c["fondo"],
                corner_radius=12
            )
            tarjeta.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            contador = ctk.CTkLabel(
                tarjeta,
                text="0",
                font=(FUENTE, 30, "bold"),
                text_color=color
            )
            contador.pack(pady=(15, 0))

            ctk.CTkLabel(
                tarjeta,
                text=titulo,
                font=(FUENTE, 12),
                text_color=self.c["texto"]
            ).pack(pady=(0, 15))

            contadores[clave] = contador

        # Visor del archivo log
        visor = ctk.CTkTextbox(
            panel,
            corner_radius=12,
            fg_color=self.c["fondo"],
            text_color=self.c["texto"],
            border_width=1,
            border_color=self.c["borde"],
            font=("Consolas", 12),
            wrap="word"
        )
        visor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        visor.tag_config(
            "info",
            foreground=self.c["exito"]
        )

        visor.tag_config(
            "error",
            foreground=self.c["error"]
        )

        # Actualizar el historial de eventos
        def actualizar_eventos():

            visor.configure(state="normal")
            visor.delete("1.0", "end")

            try:
                historial = self.sistema.leer_eventos()

                lineas = [
                    linea for linea in historial.splitlines()
                    if linea.strip()
                ]

                exitos = sum(
                    "[INFO]" in linea for linea in lineas
                )

                errores = sum(
                    "[ERROR]" in linea for linea in lineas
                )

                contadores["total"].configure(text=str(len(lineas)))
                contadores["info"].configure(text=str(exitos))
                contadores["error"].configure(text=str(errores))

                if not lineas:
                    visor.insert(
                        "end",
                        "No hay eventos registrados."
                        if es else "No recorded events."
                    )

                for linea in lineas:

                    etiqueta = (
                        "error" if "[ERROR]" in linea
                        else "info"
                    )

                    visor.insert(
                        "end",
                        linea + "\n",
                        etiqueta
                    )

            except ErrorSistema as error:
                visor.insert(
                    "end",
                    str(error) if es else "Unable to read event logs.",
                    "error"
                )

            finally:
                visor.configure(state="disabled")

        # Botón para actualizar el historial
        ctk.CTkButton(
            panel,
            text="Actualizar historial" if es else "Refresh history",
            font=(FUENTE, 14, "bold"),
            height=42,
            corner_radius=12,
            fg_color=self.c["principal"],
            hover_color=self.c["hover"],
            command=actualizar_eventos
        ).pack(fill="x", padx=25, pady=20)

        actualizar_eventos()
