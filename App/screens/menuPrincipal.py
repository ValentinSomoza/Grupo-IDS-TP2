from widgets.styledButton import StyledButton
from baseScreen import BaseScreen

class MenuPrincipalScreen(BaseScreen):
    pass

    def abrir_mis_reservas(self, instance):
        self.go_to_screen("mis_reservas", "slide")

    def abrir_reservas(self, instance):
        self.go_to_screen("crear_reserva", "slide")

    def abrir_mi_cuenta(self, instance):
        self.go_to_screen("mi_cuenta", "fade")

    def cerrar_sesion(self, instance):
        self.go_to_screen("login", "slide")