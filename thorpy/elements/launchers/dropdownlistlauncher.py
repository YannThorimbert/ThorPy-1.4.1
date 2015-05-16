from os.path import normpath, basename

from thorpy.elements.clickable import Clickable
from thorpy.elements.ddlf import DropDownListFast
from thorpy.elements.launchers._launcher import _Launcher
from thorpy.miscgui import constants, functions, style, painterstyle
from thorpy.menus.tickedmenu import TickedMenu


class DropDownListLauncher(_Launcher):

    def __init__(self,
                 name_txt,
                 file_txt,
                 titles,
                 normal_params=None,
                 ddlf_size=None,
                 folders=False,
                 file_width=None,
                 show_select=True,
                 selected=None,
                 click_quit=True):
        ddlf_size = style.DDL_SIZE if ddlf_size is None else ddlf_size
        file_width = style.FILE_WIDTH if file_width is None else file_width
        self.show_select = show_select
        if not self.show_select:
            file_txt = ""
        _Launcher.__init__(self, file_txt, normal_params, click_quit)
        self.file_width = file_width
        # to launch
        self.launched_element = DropDownListFast(ddlf_size, titles, folders=folders)
        self.launched_element.finish()
        self._deny_child(self.launched_element)
        self.launched_element._dv.x = 2
        # name
        self._name_element = self._get_name_element(name_txt)
        self._name_element.user_func = self.launch_ddlf
        if not self.show_select:
            self.get_storer_rect = self._name_element.get_storer_rect
        self.add_elements(list([self._name_element]))
        self.selected = selected

    def unblit(self, rect=None):
        functions.debug_msg("unblit" + str(self))
        self._name_element.unblit(rect)
        _Launcher.unblit(self, rect)

    def _get_name_element(self, name):
        painter = functions.obtain_valid_painter(
            painterstyle.DEF_PAINTER,
            size=style.SIZE)
        el = Clickable(name)
        el.set_painter(painter)
        el.finish()
        return el

    def launch_ddlf(self):
        self._set_branch_last()
        r = self.get_storer_rect()
        self.launched_element.set_topleft(r.bottomleft)
        self.add_elements([self.launched_element])
        tm = TickedMenu(self.launched_element)
        if self.click_quit:
            self._quit_when_click(self.launched_element)
        self.launched_element._set_selecter(tm)
        tm.refresh()
        tm.play()
        if self.click_quit:
            self.launched_element.deactivate_reaction(constants.REAC_CLICKQUIT)
        if self.launched_element._clicked:
            text = normpath(self.launched_element._clicked)
            text = basename(text)
            self.selected = text
            functions.debug_msg(self.selected)
            if self.show_select:
                size = (self.file_width, self.get_fus_size()[1])
                self.set_text(text, size=size)
        self._deny_child(self.launched_element)
        self._unlaunch()


    def _refresh_pos(self):
        self_left = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l = self_left - (self._name_element.get_fus_size()[0] + style.NAME_SPACING)
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))

    def finish(self):
        _Launcher.finish(self)

    def scale_to_title(self):
        self._name_element.scale_to_title()
##        self._name_element.stick_to(self, "left", "right")
        self._refresh_pos()
