from thorpy.elements.element import Element
from thorpy.miscgui.storage import Storer
from thorpy.miscgui import functions, style, painterstyle


class Box(Element):

    def __init__(self, bartext="", elements=None, normal_params=None,
                 storer_params=None, size=None, put_lift=True):
        Element.__init__(self, "", elements, normal_params)
        self.storer_params = storer_params
        if self.storer_params is None:
            self.storer_params = dict()
        self._size = size
        self._has_lift = False
        self._put_lift = put_lift
        self._bartext = bartext
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
                                                 size=size,
                                                 radius=style.BOX_RADIUS)
        self.set_painter(painter)

    def add_lift(self, axis="vertical", typ="normal"):
        Element.add_lift(self, axis, typ)
        self._has_lift = True

    def store(self, size=None):
        """
        size:
            'auto' or None : autoset_framesize
            elif size : set_size and center.
        """
        size = self._size if not size else size
        storer = Storer(self, **self.storer_params)
        if size and not size == "auto":
            self.set_size(size)
            storer.center()
        elif size == "auto" or size is None:
            storer.autoset_framesize()
        (x, y) = self.is_family_bigger()
        if y and not self._put_lift:
            self.add_lift("vertical")
##            self._lift.active_wheel = True
            self._lift.active_wheel = False
        self.set_prison()
        if self._bartext:
            self.add_bar(self._bartext)
        for e in self.get_elements():
            e._lock_jail = True

    def set_size(self, size, state=None, center_title=True, adapt_text=True,
                 cut=None, margins=style.MARGINS, refresh_title=False):
        Element.set_size(self, size, state, center_title, adapt_text, cut, margins,
                         refresh_title)
        if self._lift:
            self.remove_elements([self._lift])
            self.refresh_lift()

    def finish(self):
        Element.finish(self)
        self.store()
