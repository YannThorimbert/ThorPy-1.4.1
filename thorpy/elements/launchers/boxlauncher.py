from pygame import Rect

from thorpy.elements.ghost import Ghost
from thorpy.elements.text import OneLineText
from thorpy.elements.clickable import Clickable
from thorpy.elements.launchers._launcher import _Launcher
from thorpy.elements.box import Box
from thorpy.miscgui import constants, functions, style, painterstyle
from thorpy.menus.tickedmenu import TickedMenu
from thorpy.miscgui.storage import store


class BoxLauncher(_Launcher):

    def __init__(self,
                 name_text,
                 launched_text="",
                 box_els=None,
                 normal_params=None,
                 box_size=None,
                 bar=None,
                 file_width=None,
                 show_select=True,
                 spawn="center",
                 click_quit=False,
                 storer_params=None):
        """Usage of bar is discouraged"""
##        box_size = style.BOX_SIZE if box_size is None else box_size
        file_width = style.FILE_WIDTH if file_width is None else file_width
        if not box_els:
            box_els = []
        self.show_select = show_select
        _Launcher.__init__(self, "", normal_params, click_quit)
        self.file_width = file_width
        # to launch
        (box, _done_element, _cancel_element) = self._get_launched_el(
            box_els, box_size, storer_params)
        self.launched_element = box
        self._deny_child(self.launched_element)
        self._done_element = _done_element
        self._cancel_element = _cancel_element
        self._spawn = spawn
        if bar:
            self.launched_element.add_bar(launched_text)
        elif launched_text:
            title_element = OneLineText(launched_text)
            title_element.finish()
            title_element.rank = -float("inf")
            title_element.set_font_color(style.TITLE_FONT_COLOR)
            title_element.set_font_size(style.TITLE_FONT_SIZE)
            self.launched_element.add_elements([title_element])
            self.launched_element.store()
        # name
        self._name_element = self._get_name_element(name_text)
        self._name_element.user_func = self.launch_box
        self.add_elements([self._name_element])

    def _get_launched_el(self, els, size, storer_params):
        _done_element = Clickable(style.OK_TXT)
        _cancel_element = Clickable(style.CANCEL_TXT)
        _done_element.finish()
        _cancel_element.finish()
        g = Ghost([_done_element, _cancel_element])
        g.finish()
        g.englobe_childrens()
        g.rank = float("inf")
        store(g, g.get_elements(), "h")
        els += [g]
        box = Box(elements=els, size=size, storer_params=storer_params)
        box.finish() #box stores its elements
        return box, _done_element, _cancel_element

    def _get_name_element(self, name):
        painter = functions.obtain_valid_painter(painterstyle.DEF_PAINTER,
                                                 size=style.SIZE)
        el = Clickable(name)
        el.set_painter(painter)
        el.finish()
        return el

    def get_storer_rect(self):
        if not self.show_select:
            return self._name_element.get_storer_rect()
        else:
            return _Launcher.get_storer_rect(self)

    def scale_to_title(self, margins=None, state=None):
        self._name_element.scale_to_title(margins, state)

    def launch_box(self, done_no_save=True):
        self._launch(done_no_save)
        self._unlaunch()

    def _refresh_pos(self):
        self_left = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l = self_left-(self._name_element.get_fus_size()[0]+style.NAME_SPACING)
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))