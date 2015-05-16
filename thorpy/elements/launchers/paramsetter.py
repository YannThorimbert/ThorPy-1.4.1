from pygame.event import Event, post

from thorpy.elements.launchers.boxlauncher import BoxLauncher
from thorpy.miscgui import constants, functions, style
from thorpy.painting.makeup import add_basic_help


class ParamSetter(BoxLauncher):
    """Put automatically defined elements in a box, in order to set variables.
    One can add manually some elements in box_els.
    """

    def __init__(self,
                 varsets,
                 name_txt,
                 launched_txt="",
                 box_els=None,
                 normal_params=None,
                 box_size=None,
                 bar=None,
                 file_width=style.FILE_WIDTH,
                 spawn="center",
                 click_quit=False,
                 storer_params=None):
        box_size = style.BOX_SIZE if box_size is None else box_size
        if not box_els:
            box_els = []
        self.varsets = varsets
        if not isinstance(self.varsets, list):
            self.varsets = [self.varsets]
        self.handlers = self.get_handlers() #below, will deny them so they know self
        box_els += self.handlers.values()
        show_select = False
        BoxLauncher.__init__(self,
                             name_txt,
                             launched_txt,
                             box_els,
                             normal_params,
                             box_size, bar,
                             file_width,
                             show_select,
                             spawn,
                             click_quit)

    def finish(self):
        BoxLauncher.finish(self)
        self.launched_element.fit_children(w=1.05, h=1.05, only_children=True)
        self._done_element.user_func = self.quit_save
        for h in self.handlers.values():
            self._deny_child(h)

    def get_handlers(self):
        handlers = {}
        for (i, v) in enumerate(self.varsets):
            v_handlers = v.get_handlers()
            for (varname, handler) in iter(v_handlers.items()):
                handler_element, variable = handler
                handler_element.finish()
                if variable.help_text:
                    add_basic_help(handler_element, variable.help_text)
                handlers[(i, varname)] = handler_element
        return handlers

    def quit_save(self):
        ev = Event(constants.THORPY_EVENT,
                   id=constants.EVENT_DONE,
                   el=self)
        post(ev)
        for (varset, varname), handler in iter(self.handlers.items()):
            # si varset
            self.varsets[varset].set_value(varname, handler.get_value())
            # sinon si link
            # sinon si fonction
        functions.quit_menu_func()

    def launch_box(self, done_no_save=True):
        BoxLauncher.launch_box(self, False)

