from pygame.locals import KEYDOWN, KEYUP, K_t

from thorpy.elements.pressable import Pressable
from thorpy.miscgui.constants import STATE_NORMAL, STATE_PRESSED


class KeyPressable(Pressable):

    """Keyboard togglable element"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None, typ=KEYDOWN, untyp=KEYUP, key=K_t):
        """<typ> is the pygame_event type and <key> is the key number"""
        super(KeyPressable, self).__init__(text, elements, normal_params,
                                           press_params)
        self._set_press_reaction(typ, args=dict({"key": key}))
        self._set_unpress_reaction(untyp, args=dict({"key": key}))

    def _reaction_press(self, event):
        if self.current_state_key == STATE_NORMAL:
            Pressable._press(self)

    def _reaction_unpress(self, event):
        if self.current_state_key == STATE_PRESSED:
            Pressable._unpress(self)
