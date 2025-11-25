from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.factory import Factory
from services.detalleReservaServices import (
    obtenerDetalleReserva,
    obtenerInfoHabitacion,
    borrarReserva
)
from baseScreen import BaseScreen

class DetalleReservaScreen(BaseScreen):

    reservaActual = None  

    def cargar_detalle(self, id_reserva):
        self.reserva_id = id_reserva

        ok, reserva = obtenerDetalleReserva(id_reserva)
        if not ok:
            print("No se encontró la reserva")
            return

        habitacion_ok, habitacion = obtenerInfoHabitacion(reserva.get('habitacion_id'))
        if not habitacion_ok:
            habitacion = None

        detalle_item = Factory.ReservaDetalleItem()

        detalle_item.ids.texto.text = (
            f"Reserva #{reserva.get('id', '?')}\n"
            f"Nombre: {reserva.get('nombre','')} {reserva.get('apellido','')}\n"
            f"Email: {reserva.get('email','')}\n"
            f"DNI: {reserva.get('documento','')}\n"
            f"Teléfono: {reserva.get('telefono','')}\n"
            f"Fecha Registro: {reserva.get('fecha_registro','')}\n"
            f"Noches: {reserva.get('noches',0)}, Niños: {reserva.get('ninios',0)}, Adultos: {reserva.get('adultos',0)}\n"
            f"Entrada: {reserva.get('fecha_entrada','')} → Salida: {reserva.get('fecha_salida','')}\n"
            f"Check-in: {'Realizado' if reserva.get('checkin',False) else 'Pendiente'}\n"
        )

        if habitacion:
            detalle_item.ids.texto.text += (
                f"\nHabitación:\n"
                f"Numero: {habitacion.get('numero','')}\n"
                f"Tipo: {habitacion.get('tipo','')}\n"
                f"Capacidad: {habitacion.get('capacidad','')}\n"
                f"Precio: {habitacion.get('precio','')}"
            )

        self.reservaActual = reserva

        if reserva.get('checkin', False):
            detalle_item.ids.btn_checkin.text = "Check-In completado"
            detalle_item.ids.btn_checkin.disabled = True
        else:
            detalle_item.ids.btn_checkin.text = "Hacer Check-In"
            detalle_item.ids.btn_checkin.disabled = False
            detalle_item.ids.btn_checkin.bind(on_release=self._hacer_checkin)

        detalle_item.ids.btn_borrar.bind(on_release=self._borrar_reserva)

        self.ids.detalle_container.clear_widgets()
        self.ids.detalle_container.add_widget(detalle_item)

    def _borrar_reserva(self, *args):
        if not self.reservaActual:
            return
        ok = borrarReserva(self.reservaActual.get('id'))
        if ok:
            print("Reserva eliminada correctamente")
        else:
            print("Error al borrar la reserva")

        app = App.get_running_app()
        app.root.current = "mis_reservas"
        app.root.get_screen("mis_reservas").cargar_reservas()

    def _hacer_checkin(self, *args):
        if not self.reservaActual:
            return

        app = App.get_running_app()
        checkin_screen = app.root.get_screen("checkin")
        checkin_screen.cargarDatosReserva(self.reservaActual)
        app.root.current = "checkin"
