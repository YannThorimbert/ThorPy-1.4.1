from os.path import basename, normpath

from pygame import Rect

from thorpy.elements.ghost import Ghost
from thorpy.elements.element import Element
from thorpy.elements.clickable import Clickable
from thorpy.elements.box import Box
from thorpy.elements.launchers._launcher import _Launcher
from thorpy.miscgui import constants, functions, style, painterstyle
from thorpy.menus.tickedmenu import TickedMenu
from thorpy.miscgui.storage import h_store, store

class BrowserLauncher(_Launcher):

    def __init__(self,
                 browser,
                 name_txt,
                 file_txt,
                 launcher_txt,
                 normal_params=None,
                 file_width=None,
                 show_select=True,
                 click_quit=False):
        """<browser> : the browser to be launched. Can either be a Browser
                       instance or a BrowserLight instance.
        <name_txt> : the text that stands before the (optionnal) file name and
                     the button to launch browser.
        <file_txt> : the default value shown to the user.
        <launcher_txt> : the text on the launcher button.
        """
        file_width = style.FILE_WIDTH if file_width is None else file_width
        self.show_select = show_select
        if not self.show_select:
            file_txt = ""
        _Launcher.__init__(self, "", normal_params, click_quit)
        self._spawn = "center"
        self.file_width = file_width
        self._done_element = Clickable(style.OK_TXT)
        self._done_element.finish()
        self._cancel_element = Clickable(style.CANCEL_TXT)
        self._cancel_element.finish()
        g = Ghost([self._done_element, self._cancel_element])
        g.finish()
        g.englobe_childrens()
        g.rank = float("inf")
        store(g, g.get_elements(), "h")
        # to launch : must not be in self._elements!
        self.browser = browser
        box = Box(elements=[self.browser, g],
                  storer_params=None)
        box.finish()
        self.launched_element = box
        self._deny_child(self.launched_element)
        # launcher
        self.launcher_el = self.get_launcher_element(launcher_txt)
        self.launcher_el.user_func = self.launch_box
        # name
        self._name_element = self._get_name_element(name_txt)
        self._name_element.user_func = self.launch_box
        self._file_element = self._get_file_element(file_txt)
        self.add_elements([self._name_element, self.launcher_el, self._file_element])

    def finish(self):
        _Launcher.finish(self)
        self.launched_element.set_prison()
        self.browser.set_prison()
        self.browser._ddlf.set_prison()
##        h_store(self, self.get_elements())
##        self.stick_to(self.launcher_el, "right", "left")

    def get_storer_rect(self):
        return self.get_family_rect(self.current_state_key, False)

    def get_launcher_element(self, name):
        size = (style.SIZE[0], style.Y_SMALL_SIZE)
        painter = functions.obtain_valid_painter(
            painterstyle.BROWSER_LAUNCHER_PAINTER,
            size=size)
        el = Clickable(name)
        el.set_painter(painter)
        el.set_style(style.STYLE_BROWSER_LAUNCHER)
        el.finish()
        return el

    def _get_file_element(self, name):
        painter = functions.obtain_valid_painter(painterstyle.NAME_PAINTER,
                                                 size=style.SIZE)
        el = Element(name)
        el.set_painter(painter)
        el.set_style(style.STYLE_NAME)
        el.finish()
        return el

    def _refresh_pos(self):
        h_store(self, self.get_elements())

    def launch_box(self, done_no_save=True):
        self._launch(done_no_save)
        # ## special browserlauncher handling
        if self.browser._something_selected:
            if self.show_select:
                text = normpath(self.browser._selected._inserted)
                text = basename(text)
                self._file_element.set_text(text,
                              size=(self.file_width, self.get_fus_rect().h),
                              cut=True)
            helpjail = self.father
            self._name_element.add_basic_help(self.browser._selected._value,
                                              jail=helpjail)
        # ##
        self._unlaunch()

    def scale_to_title(self, margins=None, state=None):
        self.launcher_el.scale_to_title(margins, state)
        self._refresh_pos()

##    def get_storer_rect(self):
##        if not self.show_select:
##            return self._name_element.get_storer_rect()
##        else:
##            return _Launcher.get_storer_rect(self)