from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.app import App

from services.ingresoServices import logearUsuario

class LoginScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        Window.clearcolor = (0.94, 0.94, 0.94, 1)

    def realizar_login(self, instance=None):

        usuario = self.ids.nombreUsuario.text
        contrasenia = self.ids.contraseniaUsuario.text

        ok, respuesta = logearUsuario(usuario, contrasenia)

        if ok:
            datosUsuario = respuesta["usuario"]

            app = App.get_running_app()
            app.id_usuario = datosUsuario["id"]
            app.nombre = datosUsuario["nombre"]
            app.apellido = datosUsuario["apellido"]
            app.email = datosUsuario["email"]
            app.telefono = datosUsuario["telefono"]
            app.dniPasaporte = datosUsuario["dniPasaporte"]
            app.nombreUsuario = datosUsuario["nombreUsuario"]

            self.ids.mensaje.color = (0, 0.6, 0, 1)
            self.ids.mensaje.text = respuesta["mensaje"]
            self.manager.current = "menu_principal"

        else:
            self.ids.mensaje.color = (0.8, 0, 0, 1)
            self.ids.mensaje.text = respuesta