import kivy
kivy.require("2.3.1")
kivy.config.Config.set('graphics', 'dpi', '120')

from kivymd.app import MDApp
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition

#from dotenv import load_dotenv

from screens.ingreso import LoginScreen
from screens.menuPrincipal import MenuPrincipalScreen
from screens.misReservas import MisReservasScreen
from screens.detalleReserva import DetalleReservaScreen
from screens.checkin import CheckinScreen
from screens.registro import RegistroScreen
from screens.miCuenta import MiCuentaScreen
from screens.reserva import ReservaScreen

Builder.load_file("kv/ingreso.kv")
Builder.load_file("kv/menuPrincipal.kv")
Builder.load_file("kv/misReservas.kv")
Builder.load_file("kv/detalleReserva.kv")
Builder.load_file("kv/checkin.kv")
Builder.load_file("kv/registro.kv")
Builder.load_file("kv/miCuenta.kv")
Builder.load_file("kv/reserva.kv")
Builder.load_file("kv/datePicker.kv")


class HotelBrunoApp(MDApp):

    id_usuario = None
    nombre = None
    apellido = None
    email = None
    telefono = None
    dniPasaporte = None
    nombreUsuario = None
    fechaCreacion = None

    def build(self):
        
        print("=== MAIN.PY INICIADO ===")

        if platform != "android":
            Window.size = (420, 750)

        Logger.setLevel("DEBUG")

        # load_dotenv()

        Window.clearcolor = (0.94, 0.94, 0.94, 1)

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        manejadorDePantallas = ScreenManager(transition=SlideTransition())
        manejadorDePantallas.add_widget(LoginScreen(name="login"))
        manejadorDePantallas.add_widget(MenuPrincipalScreen(name="menu_principal"))
        manejadorDePantallas.add_widget(MisReservasScreen(name="mis_reservas"))
        manejadorDePantallas.add_widget(DetalleReservaScreen(name="detalle_reserva"))
        manejadorDePantallas.add_widget(CheckinScreen(name="checkin"))
        manejadorDePantallas.add_widget(RegistroScreen(name="registro"))
        manejadorDePantallas.add_widget(MiCuentaScreen(name="mi_cuenta"))
        manejadorDePantallas.add_widget(ReservaScreen(name="crear_reserva"))

        return manejadorDePantallas


if __name__ == "__main__":
    HotelBrunoApp().run()
