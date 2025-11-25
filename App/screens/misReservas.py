from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.factory import Factory
from baseScreen import BaseScreen

from services.misReservasService import obtenerReservas

class MisReservasScreen(BaseScreen):

    def on_enter(self):
        self.cargar_reservas()

    def cargar_reservas(self):
        app = App.get_running_app()

        if not app.id_usuario:
            print("App: El usuario no está logeado")
            return

        ok, resultado = obtenerReservas(app.id_usuario)

        if ok:
            reservas = resultado
            self.mostrar_reservas(reservas)
        else:
            print("Error:", resultado)

    def mostrar_reservas(self, reservas):
        contenedor = self.ids.lista_reservas
        contenedor.clear_widgets()

        if not reservas:
            no_reserva_item = Factory.ReservaItem()
            no_reserva_item.ids.texto.text = "No tenés reservas actualmente."
            contenedor.add_widget(no_reserva_item)
            return

        for reserva in reservas:
            item = Factory.ReservaItem()

            reserva_id = reserva.get('id', '?')
            nombre = reserva.get('nombre', '')
            apellido = reserva.get('apellido', '')
            email = reserva.get('email', '')
            telefono = reserva.get('telefono', '')
            documento = reserva.get('documento', '')
            fecha_registro = reserva.get('fecha_registro', '')
            noches = reserva.get('noches', 0)
            ninios = reserva.get('ninios', 0)
            adultos = reserva.get('adultos', 0)
            fecha_entrada = reserva.get('fecha_entrada', '')
            fecha_salida = reserva.get('fecha_salida', '')
            checkin = "Realizado" if reserva.get('checkin', False) else "Pendiente"

            item.ids.texto.text = (
                f"Reserva #{reserva_id}\n"
                f"Nombre: {nombre} {apellido}\n"
                f"Email: {email}\n"
                f"DNI: {documento}\n"
                f"Teléfono: {telefono}\n"
                f"Fecha Registro: {fecha_registro}\n"
                f"Noches: {noches}, Niños: {ninios}, Adultos: {adultos}\n"
                f"Entrada: {fecha_entrada} → Salida: {fecha_salida}\n"
                f"Check-in: {checkin}"
            )
            
            item.ids.btn_detalle.bind(
                on_release=lambda btn, id_reserva=reserva_id: self.abrirDetalleReserva(id_reserva)
            )

            contenedor.add_widget(item)

    def abrirDetalleReserva(self, id_reserva):
        app = App.get_running_app()
        detalle_screen = app.root.get_screen("detalle_reserva")
        detalle_screen.cargar_detalle(id_reserva)
        app.root.current = "detalle_reserva"