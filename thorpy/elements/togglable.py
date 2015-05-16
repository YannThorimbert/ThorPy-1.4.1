from thorpy.elements.clickable import Clickable
from thorpy.miscgui import constants


class Togglable(Clickable):
    """Mouse-togglable element"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None):
        super(Togglable, self).__init__(text, elements, normal_params,
                                        press_params)
        self._count = 0

    def _reaction_press(self, event):
        if self._count < 1:
            tag = constants.STATE_NORMAL
        else:
            tag = constants.STATE_PRESSED
        if self.collide(event.pos, tag):
            self._press()

    def _press(self):
        Clickable._press(self)
        self._count += 1

    def _unpress(self):
        if self._count == 2:
            self._count = 0
            Clickable._unpress(self)
