from kivy.uix.modalview import ModalView
from kivy.properties import NumericProperty
from datetime import date
import calendar
from kivy.factory import Factory


class SimpleDatePicker(ModalView):
    
    callback = None

    current_year = NumericProperty(date.today().year)
    current_month = NumericProperty(date.today().month)
    current_day = NumericProperty(date.today().day)

    def __init__(self, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def open_panel(self, mode):
        popup = Factory.PickerPopup()

        grid = popup.ids.options_grid
        grid.clear_widgets()

        if mode == "year":
            values = range(self.current_year, self.current_year + 11)

        elif mode == "month":
            values = range(1, 13)

        elif mode == "day":
            num_days = calendar.monthrange(self.current_year, self.current_month)[1]
            values = range(1, num_days + 1)

        from kivy.uix.button import Button
        for v in values:
            btn = Button(text=str(v), size_hint_y=None, height=40)
            btn.bind(on_release=lambda inst, m=mode: self.select_value(m, inst.text, popup))
            grid.add_widget(btn)

        popup.open()

    def select_value(self, mode, value, popup):
        value = int(value)

        if mode == "year":
            self.current_year = value
        elif mode == "month":
            self.current_month = value
        elif mode == "day":
            self.current_day = value

        popup.dismiss()

    def confirm_date(self):
        fecha = f"{self.current_year:04d}-{self.current_month:02d}-{self.current_day:02d}"
        if self.callback:
            self.callback(fecha)
        self.dismiss()