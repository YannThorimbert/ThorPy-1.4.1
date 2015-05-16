"""The philosophy is the following : all variables and functions that starts
with an underscore are for development purpose, not 'user' use purpose.
According to Python's recommandations, single underscore indicates a variable
that user shouldn't use ; here we consider that 'user' means 'basic user', not
'developer' extending the library.
"""

__version__ = "1.4.1"

import sys
import os

# verify that pygame is on the machine
try:
    import pygame
except Exception:
    print("Pygame doesn't seem to be installed on this machine.")


# add thorpy folder to Windows and Python search paths
THORPY_PATH = os.path.abspath(os.path.dirname(__file__))
try:
    os.environ['PATH'] = ';'.join((THORPY_PATH, os.environ['PATH']))
    sys.path.append(THORPY_PATH)
except Exception:
    print("Couldn't add Thor to sys.path...\nThorPy path : " + THORPY_PATH)

USEREVENT = pygame.USEREVENT + 1 #because thorpy takes one event on pygame's userevents

#import subpackages
import thorpy.elements
import thorpy.menus
import thorpy._utils
import thorpy.miscgui
import thorpy.painting as painting
import thorpy.miscgui.application as application
import thorpy.miscgui.storage as storage

import testmodule

# not all elements are imported ; only those that can be safely used by lambda
# user.
from thorpy.elements.launchers.boxlauncher import BoxLauncher
from thorpy.elements.launchers.browserlauncher import BrowserLauncher
from thorpy.elements.launchers.dropdownlistlauncher import DropDownListLauncher
from thorpy.elements.launchers._launcher import _Launcher
from thorpy.elements.background import Background
Image = Background
from thorpy.elements.box import Box
from thorpy.elements.browserlight import BrowserLight
from thorpy.elements.browser import Browser
from thorpy.elements.checker import Checker
from thorpy.elements.clickable import Clickable
from thorpy.elements._wrappers import make_button, make_text
from thorpy.elements.colorsetter import ColorSetter
from thorpy.elements.ddlf import DropDownListFast as DropDownList
from thorpy.elements.draggable import Draggable, ClickDraggable
from thorpy.elements.element import Element
from thorpy.elements.ghost import Ghost
from thorpy.elements.hoverable import Hoverable
from thorpy.elements.hoverzone import HoverZone
from thorpy.elements.inserter import Inserter
from thorpy.elements.keypressable import KeyPressable
from thorpy.elements.keytogglable import KeyTogglable
from thorpy.elements.launchers.paramsetter import ParamSetter
from thorpy.elements.pressable import Pressable
##from thorpy.elements.text import MultilineText
from thorpy.elements.text import OneLineText, MultilineText
from thorpy.elements.slidersetter import SliderXSetter as SliderX
from thorpy.elements.togglable import Togglable
from thorpy.elements.line import Line
from thorpy.elements._makeuputils._halo import Halo
from thorpy.elements._makeuputils._shadow import StaticShadow
from thorpy.elements._makeuputils._shadow import DynamicShadow

# menus:
from thorpy.menus.tickedmenu import TickedMenu as Menu
from thorpy.menus.basicmenu import BasicMenu

# miscellaneous stuff, constants, parameters
from thorpy.miscgui.application import Application
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui import constants, functions
from thorpy.miscgui import style
from thorpy.miscgui import painterstyle
from thorpy.miscgui import parameters
from thorpy.miscgui.initializer import Initializer
from thorpy.miscgui.state import State
from thorpy.miscgui.storage import Storer, store
from thorpy.miscgui.title import Title
from thorpy.miscgui.varset import VarSet
from thorpy.miscgui import theme
from thorpy.miscgui.theme import set_theme as set_theme

from thorpy.painting.writer import Writer
from thorpy.painting import makeup

from thorpy.gamestools.basegrid import BaseGrid
from thorpy.gamestools.grid import Grid

del thorpy, pygame, os, sys
