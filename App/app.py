from kivy.app import App
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from dotenv import load_dotenv

from screens.ingreso import LoginScreen
from screens.menuPrincipal import MenuPrincipalScreen
from screens.misReservas import MisReservasScreen
from screens.detalleReserva import DetalleReservaScreen
from screens.checkin import CheckinScreen

Builder.load_file("kv/ingreso.kv")
Builder.load_file("kv/menuPrincipal.kv")
Builder.load_file("kv/misReservas.kv")
Builder.load_file("kv/detalleReserva.kv")
Builder.load_file("kv/checkin.kv")

class HotelBrunoApp(App):
    id_usuario = None
    nombre = None
    apellido = None
    email = None
    telefono = None
    dniPasaporte = None
    nombreUsuario = None

    def build(self):
        Logger.setLevel("DEBUG")
        load_dotenv()

        Window.clearcolor = (0.94, 0.94, 0.94, 1)

        manejadorDePantallas = ScreenManager(transition=SlideTransition())
        manejadorDePantallas.add_widget(LoginScreen(name="login"))
        manejadorDePantallas.add_widget(MenuPrincipalScreen(name="menu_principal"))
        manejadorDePantallas.add_widget(MisReservasScreen(name="mis_reservas"))
        manejadorDePantallas.add_widget(DetalleReservaScreen(name="detalle_reserva"))
        manejadorDePantallas.add_widget(CheckinScreen(name="checkin"))

        return manejadorDePantallas

if __name__ == "__main__":
    HotelBrunoApp().run()