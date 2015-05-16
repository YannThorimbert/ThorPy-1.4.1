from pygame.locals import KEYDOWN, K_t

from thorpy.elements.pressable import Pressable
from thorpy.miscgui.constants import STATE_NORMAL, STATE_PRESSED


class KeyTogglable(Pressable):

    """Keyboard togglable element"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None, typ=KEYDOWN, key=K_t):
        """<typ> is the pygame_event type and <key> is the key number"""
        super(KeyTogglable, self).__init__(text, elements, normal_params,
                                           press_params)
        self._set_press_reaction(typ, args=dict({"key": key}))
##        self.set_key(key, typ)
        self._reactions.pop(REAC_UNPRESS)

    def set_key(self, key, event_type=KEYDOWN):
        self._set_press_reaction(event_type, args=dict({"key": key}))

    def _reaction_press(self, event):
        if self.current_state_key == STATE_NORMAL:
            Pressable._press(self)
        elif self.current_state_key == STATE_PRESSED:
            Pressable._unpress(self)
            self.run_user_func()
