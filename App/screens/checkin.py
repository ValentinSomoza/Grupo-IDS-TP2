from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from baseScreen import BaseScreen
from services.checkinServices import realizarCheckin

class CheckinScreen(BaseScreen):

    def cargarDatosReserva(self, reserva):
        self.reservaActual = reserva
        self._autocompletarCampos()

    def _autocompletarCampos(self):
        app = App.get_running_app()
        if hasattr(self, "ids"):
            self.ids.input_nombre.text = app.nombre or ""
            self.ids.input_apellido.text = app.apellido or ""
            self.ids.input_email.text = app.email or ""
            self.ids.input_telefono.text = app.telefono or ""
            self.ids.input_dni.text = app.dniPasaporte or ""

    def enviarCheckin(self, nombre, apellido, dniPasaporte, email, telefono):
        if not hasattr(self, "reservaActual"):
            self.mostrarPopup("Check-in", "No hay reserva cargada")
            return

        idReserva = self.reservaActual.get('id')
        ok, mensaje = realizarCheckin(idReserva, nombre, apellido, dniPasaporte, email, telefono)

        if ok:
            self.reservaActual['checkin'] = True
            Clock.schedule_once(lambda dt: setattr(App.get_running_app().root, "current", "menu_principal"), 1.5)
        else:
            self.mostrarPopup("Check-in", mensaje)

    def enviarCheckinDesdeKV(self):
        if not hasattr(self, "reservaActual"):
            self.mostrarPopup("Check-in", "No hay reserva cargada")
            return

        if not self.ids.check_aceptar.active:
            self.mostrarPopup("Check-in", "Debes aceptar los términos y condiciones")
            return

        self.enviarCheckin(
            self.ids.input_nombre.text,
            self.ids.input_apellido.text,
            self.ids.input_dni.text,
            self.ids.input_email.text,
            self.ids.input_telefono.text
        )

    def mostrarPopup(self, titulo, mensaje):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=mensaje))
        btn = Button(text="Cerrar", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.8, 0.4))
        btn.bind(on_release=popup.dismiss)
        popup.open()