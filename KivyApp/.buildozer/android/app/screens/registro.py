from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import re

from services.registroServices import registrarUsuario



class RegistroScreen(Screen):

    def validar_campos(self):
        nombre = self.nombre.text.strip()
        apellido = self.apellido.text.strip()
        usuario = self.nombreUsuario.text.strip()
        email = self.email.text.strip()
        telefono = self.telefono.text.strip()
        dni = self.dniPasaporte.text.strip()
        contrasenia = self.contrasenia.text.strip()

        if not all([nombre, apellido, usuario, email, telefono, dni, contrasenia]):
            self.mostrar_mensaje("Todos los campos son obligatorios", error=True)
            return False

        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            self.mostrar_mensaje("El email no es válido", error=True)
            return False

        if not telefono.isdigit():
            self.mostrar_mensaje("El teléfono debe contener solo números", error=True)
            return False
        if not 10 <= len(telefono) <= 15:
            self.mostrar_mensaje("El teléfono debe tener entre 10 y 15 dígitos", error=True)
            return False

        if not dni.isdigit():
            self.mostrar_mensaje("El DNI debe contener solo números", error=True)
            return False
        if not 10 <= len(dni) <= 15:
            self.mostrar_mensaje("El DNI debe tener entre 10 y 15 dígitos", error=True)
            return False

        return True

    def limpiar_campos(self):
        self.nombre.text = ""
        self.apellido.text = ""
        self.nombreUsuario.text = ""
        self.email.text = ""
        self.telefono.text = ""
        self.dniPasaporte.text = ""
        self.contrasenia.text = ""
        self.mensaje.text = ""

    def on_pre_enter(self):
        self.limpiar_campos()

    def mostrar_popup(self, mensaje):
        popup = Popup(
            title="Éxito",
            content=Label(text=mensaje, font_size=18),
            size_hint=(0.7, 0.3),
            auto_dismiss=True
        )
        popup.open()

    def volverLogin(self):
        Clock.schedule_once(self._cambiar_a_login, 1) # 1 es 1 segundo de delay

    def _cambiar_a_login(self, dt):
        self.manager.current = "login"

    def mostrar_mensaje(self, texto, error=False):
        self.mensaje.text = texto
        if error:
            self.mensaje.color = (1, 0, 0, 1)
        else:
            self.mensaje.color = (0, 0.6, 0, 1)

    def enviar_registro(self):

        if not self.validar_campos():
            return

        self.mostrar_mensaje("Registrando usuario...", error=False)

        datos = {
            "nombre": self.nombre.text.strip(),
            "apellido": self.apellido.text.strip(),
            "usuario": self.nombreUsuario.text.strip(),
            "email": self.email.text.strip(),
            "telefono": self.telefono.text.strip(),
            "dni": self.dniPasaporte.text.strip(),
            "contrasenia": self.contrasenia.text.strip()
        }

        exito, respuesta = registrarUsuario(
            datos["nombre"],
            datos["apellido"],
            datos["usuario"],
            datos["email"],
            datos["telefono"],
            datos["dni"],
            datos["contrasenia"]
        )

        if exito:
            self.mostrar_mensaje("Registro exitoso", error=False)
            self.mostrar_popup("Registro completado, ahora inicia sesion")
            self.volverLogin()
        else:
            self.mostrar_mensaje(respuesta, error=True)