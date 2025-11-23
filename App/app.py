from kivy.app import App
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from baseScreen import BaseScreen

from screens.ingreso import LoginScreen
from screens.menuPrincipal import MenuPrincipalScreen
from dotenv import load_dotenv
from kivy.lang import Builder

from kivy.uix.screenmanager import (
    FadeTransition,
    SlideTransition,
    SwapTransition,
    WipeTransition,
    FallOutTransition,
    RiseInTransition,
    CardTransition
)

Builder.load_file("kv/ingreso.kv")
Builder.load_file("kv/menuPrincipal.kv")

class HotelBrunoApp(App):

    def build(self):
        Logger.setLevel("DEBUG")
        load_dotenv()

        Window.clearcolor = (0.94, 0.94, 0.94, 1)

        manejadorDePantallas = ScreenManager(transition=SlideTransition())
        manejadorDePantallas.add_widget(LoginScreen(name="login"))
        manejadorDePantallas.add_widget(MenuPrincipalScreen(name="menu_principal"))

        return manejadorDePantallas

if __name__ == "__main__":
    HotelBrunoApp().run()