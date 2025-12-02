from kivy.uix.screenmanager import (
    Screen, SlideTransition, FadeTransition, SwapTransition,
    WipeTransition, FallOutTransition, RiseInTransition
)

class BaseScreen(Screen):

    def go_to_screen(self, name, transition_type="fade"):
        transitions = {
            "slide": SlideTransition(direction="left"),
            "fade": FadeTransition(),
            "swap": SwapTransition(),
            "wipe": WipeTransition(),
            "fall": FallOutTransition(),
            "rise": RiseInTransition(),
        }

        self.manager.transition = transitions.get(transition_type, FadeTransition())
        self.manager.current = name