from thorpy.elements.clickable import Clickable
from thorpy.elements.text import OneLineText
from thorpy.miscgui import constants, functions, parameters, style, painterstyle
from thorpy.miscgui.reaction import Reaction

from thorpy.menus.tickedmenu import TickedMenu
from thorpy.miscgui.storage import h_store


class _Launcher(OneLineText):

    def __init__(self, launcher_txt, normal_params=None, click_quit=False):
        OneLineText.__init__(self, text=launcher_txt,
                             normal_params=normal_params)
        self.click_quit = click_quit

    def _quit_when_click(self, element):
        reac_clickquit = Reaction(
                            reacts_to=parameters.BUTTON_UNPRESS_EVENT,
                            reac_func=element.click_quit_reaction,
                            event_args={"button": parameters.LEFT_CLICK_BUTTON},
                            reac_name=constants.REAC_CLICKQUIT)
        element.add_reaction(reac_clickquit)

    def _get_name_element(self, name):
        painter = functions.obtain_valid_painter(painterstyle.NAME_PAINTER,
                                                 size=style.SIZE)
        el = Clickable(name)
        el.set_painter(painter)
        el.set_style(style.STYLE_NAME)
        el.finish()
        return el

    def finish(self):
        OneLineText.finish(self)
        if not self.launched_element.is_finished():
            self.launched_element.finish()
        self._refresh_pos()

    def _refresh_pos(self):
        # name
        self_left = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l = self_left-(self._name_element.get_fus_size()[0]+style.NAME_SPACING)
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))
        # launcher el
        self.launcher_el.set_center((None, y))
        self.launcher_el.set_topleft((self.get_fus_rect().right + 8, None))

    def get_storer_rect(self):
        return self.get_family_rect(constants.STATE_NORMAL)

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        self._name_element.set_font_color(color, state, center_title)

    def set_font_size(self, size, state=None, center_title=True):
        """set font color for a given state"""
        self._name_element.set_font_size(size, state, center_title)

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        self._name_element.set_font_effects(biu, state, center, preserve)

    def _launch(self, done_no_save):
        self._set_branch_last()
        self.add_elements([self.launched_element])
        my = style.MARGINS[1]
        tm = TickedMenu(self.launched_element)
        if self.click_quit:
            self._quit_when_click(self.launched_element)
        tm.refresh()
        r = self.get_storer_rect()
        lr = self.launched_element.get_storer_rect()
        fr = self.launched_element.get_family_rect(only_children=True)
        bottom = fr.top + fr.height
##        h_store(self.launched_element,
##                [self._done_element, self._cancel_element],
##                ycoord=bottom-my-self._cancel_element.get_storer_rect().h)
        if self._spawn == "auto":
            if self.launched_element._bar:
                r2 = Rect((r.left, r.bottom + my + \
                              self.launched_element._bar.get_fus_size()[1]),
                          lr.size)
            else:
                r2 = Rect((r.left, r.bottom + my), lr.size)
            self.launched_element.set_topleft(r2.topleft)
        elif self._spawn == "center":
            self.launched_element.center()
        else:
            self.launched_element.set_topleft(spawn)
        if done_no_save:
            self._done_element.set_as_menu_exiter()
        self._cancel_element.set_as_menu_exiter()
        tm.play()
        if self.click_quit:
            self.launched_element.deactivate_reaction(constants.REAC_CLICKQUIT)
        self._deny_child(self.launched_element)

    def _unlaunch(self):
        a = self.get_oldest_ancester()
        if a:
            a.blit()
            a.update()

    def get_help_rect(self):
        return self._name_element.get_help_rect()
