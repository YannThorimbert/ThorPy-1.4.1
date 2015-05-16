"""VarSet is used when you need to acess some non-constant variable that could
have been modified by the user through the GUI interface during execution.
"""

##from collections import namedtuple

from thorpy._utils.functions import obtain_valid_object
from thorpy.elements.slidersetter import SliderXSetter
from thorpy.elements.inserter import Inserter
from thorpy.elements.checker import Checker
from thorpy.elements.colorsetter import ColorSetter
from thorpy.elements.browser import Browser
from thorpy.elements.browserlight import BrowserLight
from thorpy.miscgui import constants


def get_handler_for(variable):
    typ = type(variable.value)
    value = variable.value
    text = variable.text
    limits = variable.limits
    handler_type = variable.handler_type
    handler = None
    if handler_type:
        if handler_type == "color_choice":
            handler = ColorSetter(text=text, value=value)
        elif handler_type == "file_choice":
            limits.setdefault("launcher", False)
            limits.setdefault("light", True)
            limits.setdefault("ddl_size", None)
            limits.setdefault("folders", True)
            limits.setdefault("file_types", None)
            limits.setdefault("files", True)
            if limits["light"]:
                handler = BrowserLight(text=text, path=value,
                                     ddl_size=limits["ddl_size"],
                                     folders=limits["folders"],
                                     files=limits["files"],
                                     file_types=limits["file_types"])
            else:
                handler = Browser(text=text, path=value,
                                 ddl_size=limits["ddl_size"],
                                 folders=limits["folders"],
                                 files=limits["files"],
                                 file_types=limits["file_types"])
        else:
            handler = obtain_valid_object(handler_type, value=value, typ=typ,
                                          text=text, limits=limits)
    elif typ is tuple:
        if len(value) == 3:
            handler = ColorSetter(text=text, value=value)
    elif (typ is str) or not(limits):
        handler = Inserter(text, value=str(value), value_type=typ)
    elif (typ is int) or (typ is float):
        handler = SliderXSetter(100,
                                limits,
                                text,
                                typ=typ,
                                initial_value=value)
    elif typ is bool:
        handler = Checker(variable.text, value=variable.value,
                          checked=variable.value)
    if handler:
        handler.rank = variable.rank
        return handler
    else:
        raise Exception(
            "Variable doesn't have default handler: " +
            str(varname))

class Variable(object):
    """Basic type for Varsetter's variables."""

    def __init__(self, value, text, limits, handler_type, rank, help_text):
        self.value = value
        self.text = text
        self.limits = limits
        self.handler_type = handler_type
        self.rank = rank
        self.help_text = help_text

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class LinkedVariable(Variable):
    """Use this if you need to link an object's variable to the Varsetter."""

    def __init__(self, father, name, text, limits, handler_type, rank,
                    help_text):
        father_value = getattr(father, name)
        Variable.__init__(self, father_value, text, limits, handler_type, rank,
                            help_text)
        self.father = father
        self.name = name

    def set_value(self, value):
        Variable.set_value(self, value)
        setattr(self.father, self.name, value)


class FuncLauncher(Variable):
    """Use this if you need to execute a function just after setting the value.
    """

    def __init__(
            self,
            func,
            dictargs,
            value,
            text,
            limits,
            handler_type,
            rank,
            help_text):
        Variable.__init__(self, value, text, limits, handler_type, rank, help_text)
        self.func = func
        self.dictargs = dictargs


class PostFuncLauncher(FuncLauncher):

    def set_value(self, value):
        Variable.set_value(self, value)
        self.func(self.dictargs)


class PreFuncLauncher(FuncLauncher):

    def set_value(self, value):
        self.func(self.dictargs)
        Variable.set_value(self, value)


class VarSet(object):
    """Dynamically creates attributes so that one can acess them as if they were
    variables of a module.
    """

    EXCEPTION_TEXT = "Tried to name a variable like a built-in attribute\
                      or method. Please use the syntax hack provided by\
                      thorpy. It is also possible that you try to add a\
                      key that already exist. In that case use the method\
                      set_variable of this object."

    def __init__(self, variables=None):
        if not variables:
            variables = {}
        self.variables = variables
        self._current_rank = -1

    def add(self, varname, value, text, limits=None, handler_type=None,
            rank=None, help_text=None):
        rank = self._get_rank() if rank is None else rank
        if not varname in self.__dict__:
            v = Variable(value, text, limits, handler_type, rank, help_text)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def add_link(self, varname, obj, text, limits=None, handler_type=None,
                 rank=None, help_text=None):
        """Use this if you need to link an object's variable to the Varsetter.
        """
        rank = self._get_rank() if rank is None else rank
        if not varname in self.__dict__:
            v = LinkedVariable(obj, varname, text, limits, handler_type, rank,
                                help_text)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def add_func(self, varname, func, dictargs, value, text, limits=None,
                 handler_type=None, rank=None, post=True, help_text=None):
        """Use this if you need to execute a function just before/after
        setting the value.
        """
        rank = self._get_rank() if rank is None else rank
        if not varname in self.__dict__:
            if post:
                v = PostFuncLauncher(
                    func,
                    dictargs,
                    value,
                    text,
                    limits,
                    handler_type,
                    rank,
                    help_text)
            else:
                v = PreFuncLauncher(
                    func,
                    dictargs,
                    value,
                    text,
                    limits,
                    handler_type,
                    rank,
                    help_text)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def set_value(self, varname, value):
        self.variables[varname].set_value(value)
        setattr(self, varname, value)

    def get_value(self, varname):
        return self.variables[varname].get_value()

    def set_variable(self, varname, variable):
        self.variables[varname] = variable
        setattr(self, varname, variable.value)

##    def get_handlers(self):
##        handlers = {}
##        for varname in self.variables:
##            handler = get_handler_for(self.variables[varname])
##            handlers[varname] = handler
##        return handlers

    def get_handlers(self):
        handlers = {}
        for varname, variable in self.variables.items():
            handler = get_handler_for(variable)
            handlers[varname] = (handler, variable)
        return handlers

    def _get_rank(self):
        self._current_rank += 1
        return self._current_rank
