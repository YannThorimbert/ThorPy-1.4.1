from copy import copy

from pygame.event import Event, post

from thorpy.elements.element import Element
from thorpy.miscgui.state import State
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui.initializer import init_params
from thorpy.miscgui import constants, parameters, style, painterstyle

class Pressable(Element):
    """Pressable Element"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None):
        """To modify _press and _unpress reaction, assign new self._reaction_press
        and self._reaction_unpress functions !"""
        self.press_params = init_params(press_params)
        super(Pressable, self).__init__(text, elements, normal_params)
        # fusionner
        self.set_painter(painterstyle.DEF_PAINTER(size=style.SIZE))
        # reactions
        self._set_press_reaction(parameters.BUTTON_PRESS_EVENT,
                                 {"button": parameters.LEFT_CLICK_BUTTON})
        self._set_unpress_reaction(parameters.BUTTON_UNPRESS_EVENT,
                                   {"button": parameters.LEFT_CLICK_BUTTON})

    def finish(self):
        Element.finish(self)
        self.press_params._normalize(self)
        fusionner_press = self.press_params.get_fusionner()
        state_pressed = State(fusionner_press)
        self._states[constants.STATE_PRESSED] = state_pressed

    def set_style(self, new_style):
        Element.set_style(self, new_style)
        self.press_params.params["style"] = new_style

    def set_painter(self, painter, autopress=True):
        """To use before finish"""
        Element.set_painter(self, painter)
        if autopress:
            painter = copy(painter)
            painter.pressed = True
        self.press_params.params["painter"] = painter

    def _set_press_reaction(self, typ, args=None):
        """Set event which permit to toggle the element"""
        if not args:
            args = {}
        reac_pressed = Reaction(typ, self._reaction_press, args,
                                reac_name=constants.REAC_PRESSED)
        self.add_reaction(reac_pressed)

    def _set_unpress_reaction(self, typ, args=None):
        if not args:
            args = {}
        reac_unpress = Reaction(typ, self._reaction_unpress, args,
                                reac_name=constants.REAC_UNPRESS)
        self.add_reaction(reac_unpress)

    def _reaction_press(self, pygame_event):
        """Specific for pygame.MOUSEBUTTONDOWN. Needs pygame_event to treat
        arguments of the event"""
        state_ok = self.current_state == self._states[constants.STATE_NORMAL]
        if state_ok:
            if self.collide(pygame_event.pos, constants.STATE_NORMAL):
                self._press()

    def _reaction_unpress(self, pygame_event):
        """Specific for pygame.MOUSEBUTTONUP. Needs pygame_event to treat
        arguments of the event"""
        state_ok = (self.current_state_key == constants.STATE_PRESSED)
        if state_ok:
            self._unpress()
            if self.collide(pygame_event.pos, constants.STATE_PRESSED):
                self.run_user_func()

    def _press(self):
        self.unblit()
        self.change_state(constants.STATE_PRESSED)
        self.blit()
        self.update()
        ev_press = Event(constants.THORPY_EVENT,
                         id=constants.EVENT_PRESS,
                         el=self)
        post(ev_press)

    def _unpress(self):
        self.unblit()
        self.change_state(constants.STATE_NORMAL)
        self.blit()
        self.update()
