from kivy.app import App
from kivy.uix.screenmanager import Screen
from baseScreen import BaseScreen

class MiCuentaScreen(BaseScreen):

    def on_pre_enter(self):
        app = App.get_running_app()

        self.ids.lbl_nombre.text = app.nombre or "Dato no disponible"
        self.ids.lbl_apellido.text = app.apellido or "Dato no disponible"
        self.ids.lbl_email.text = app.email or "Dato no disponible"
        self.ids.lbl_telefono.text = app.telefono or "Dato no disponible"
        self.ids.lbl_dni.text = app.dniPasaporte or "Dato no disponible"
        self.ids.lbl_usuario.text = app.nombreUsuario or "Dato no disponible"
        self.ids.lbl_fecha_creacion.text = app.fechaCreacion or "Dato no disponible"

    def volver(self):
        self.go_to_screen("menu_principal", "slide")