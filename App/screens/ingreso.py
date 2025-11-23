from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from services.api import login_usuario

class LoginScreen(Screen):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        Window.clearcolor = (0.94, 0.94, 0.94, 1)

    def realizar_login(self, instance=None):

        usuario = self.ids.nombreUsuario.text
        contrasenia = self.ids.contraseniaUsuario.text

        ok, mensaje = login_usuario(usuario, contrasenia)

        if ok:
            self.ids.mensaje.color = (0, 0.6, 0, 1)
            self.manager.current = "menu_principal"
        else:
            self.ids.mensaje.color = (0.8, 0, 0, 1)

        self.ids.mensaje.text = mensaje
