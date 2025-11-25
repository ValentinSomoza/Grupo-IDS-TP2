from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime

from baseScreen import BaseScreen
from services.reservaServices import enviarReserva

from screens.datePicker import SimpleDatePicker
from kivy.app import App

class ReservaScreen(BaseScreen):

    mensaje = StringProperty("")

    def on_pre_enter(self):
        from kivy.app import App
        app = App.get_running_app()

        self.mensaje = ""

        campos = [
            "ti_in_adultos", "ti_in_ninios", "ti_in_noches",
            "ti_in_tipo", "ti_in_fecha_in", "ti_in_fecha_out"
        ]

        for campo in campos:
            input_widget = self.ids.get(campo)
            if input_widget:
                input_widget.text = ""

        self.ids.ti_in_nombre.text = app.nombre or ""
        self.ids.ti_in_apellido.text = app.apellido or ""
        self.ids.ti_in_dni.text = app.dniPasaporte or ""
        self.ids.ti_in_telefono.text = app.telefono or ""
        self.ids.ti_in_email.text = app.email or ""

    def abrir_fecha_entrada(self):
        SimpleDatePicker(callback=self._set_fecha_entrada).open()

    def abrir_fecha_salida(self):
        SimpleDatePicker(callback=self._set_fecha_salida).open()

    def _set_fecha_entrada(self, fecha):
        self.ids.ti_in_fecha_in.text = fecha

    def _set_fecha_salida(self, fecha):
        self.ids.ti_in_fecha_out.text = fecha

    def enviar_reserva(self):
        app = App.get_running_app()

        datos = {
            "nombre": self.ids.ti_in_nombre.text.strip(),
            "apellido": self.ids.ti_in_apellido.text.strip(),
            "dniPasaporte": self.ids.ti_in_dni.text.strip(),
            "telefono": self.ids.ti_in_telefono.text.strip(),
            "email": self.ids.ti_in_email.text.strip(),
            "noches": self.ids.ti_in_noches.text.strip(),
            "adultos": self.ids.ti_in_adultos.text.strip(),
            "ninios": self.ids.ti_in_ninios.text.strip(),
            "tipoHabitacion": self.ids.ti_in_tipo.text.strip(),
            "fechaEntrada": self.ids.ti_in_fecha_in.text.strip(),
            "fechaSalida": self.ids.ti_in_fecha_out.text.strip(),
            "id_usuario": app.id_usuario
        }

        campos_obligatorios = [
            "nombre", "apellido", "dniPasaporte", "telefono", "email",
            "noches", "adultos", "tipoHabitacion", "fechaEntrada", "fechaSalida"
        ]

        for campo in campos_obligatorios:
            if not datos[campo]:
                self.mensaje = f"[color=ff0000]Error: El campo '{campo}' es obligatorio[/color]"
                return

        if datos["ninios"] == "":
            datos["ninios"] = "0"

        try:
            if int(datos["ninios"]) < 0:
                self.mensaje = "[color=ff0000]Error: Niños no puede ser menor que 0[/color]"
                return
        except ValueError:
            self.mensaje = "[color=ff0000]Error: Niños debe ser un número[/color]"
            return

        self.mensaje = "Enviando reserva..."
        Clock.schedule_once(lambda dt: self._procesar_envio(datos), 0)

    def _procesar_envio(self, datos):
        respuesta = enviarReserva(datos)

        if "error" in respuesta:
            self.mensaje = f"[color=ff0000]{respuesta['error']}[/color]"
            return

        self.mensaje = "[color=00aa00]¡Reserva realizada con éxito![/color]"

        Clock.schedule_once(lambda dt: self.go_to_screen("menu_principal", "slide"), 1.5)
