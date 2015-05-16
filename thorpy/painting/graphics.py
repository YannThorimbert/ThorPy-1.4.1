"""Provides some functions that can be used to produce procedural graphical
elements.
"""
# -*- coding: utf-8 -*-
from math import sin, cos, pi, radians, hypot

try:
    from pygame import surfarray
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

import pygame.draw
from pygame import Surface, RLEACCEL, SRCALPHA, Rect
from pygame.transform import rotate

from thorpy._utils.colorscomputing import mid_color, different_color, grow_color, normalize_color
from thorpy._utils.rectscomputing import get_top_coords, get_bottom_coords
from thorpy._utils.images import load_image, change_color_on_img_ip
from thorpy._utils.colorscomputing import get_alpha_color as gac
from thorpy.miscgui import constants, functions

def blit_arrow_on(img_path, img_colorkey, img_colorsource, arrow_color, side,
                  surface):
    img = load_image(filename=img_path, colorkey=img_colorkey)
    rotation = 0  # default rotation : 0 (top)
    if side == "bottom":
        rotation = 180
    elif side == "right":
        rotation = -90
    elif side == "left":
        rotation = 90
    img = rotate(img, rotation)
    change_color_on_img_ip(img, img_colorsource, arrow_color, img_colorkey)
    img.set_colorkey(img_colorkey, RLEACCEL)
    rect = img.get_rect()
    rect.center = surface.get_rect().center
    rect.move_ip((-1, -1))
    surface.blit(img, rect.topleft)

def illuminate_dist(points, rect, xp, yp):
    min_dist = hypot(rect.w, rect.h)
    for (x, y) in points:
        d = hypot(xp - x, yp - y)
        if d < min_dist:
            min_dist = d
    return min_dist

def illuminate_multicolor_toalpha():
    pass

def illuminate_alphacolor_toalpha():
    pass

def illuminate_color_toalpha():
    pass

def illuminate_multicolor_precise(): #avec threshold
    pass

def illuminate_alphacolor_precise(): #avec threshold
    pass

def illuminate_color_precise(): #avec threshold
    pass

def illuminate_multicolor_except():
    pass

def illuminate_alphacolor_except(surface, color_except, color_target,
                                 color_bulk=None, subrect=None, factor=1.,
                                 fadout=2, bulk_alpha=255):
    """
    mode : "except" means all the pixels that are not color_source.
           "exact" means all the pixels that are exacly color_source.
    Set fadout to 0 and bulk_alpha to 255 if you do not want alpha fade out.
    """
    if not HAS_NUMPY:
        raise Exception("Could not use surfarray module from PyGame.\
                     NumPy is probably missing.")
    rect = surface.get_rect()
    newsurf = pygame.Surface(rect.size, SRCALPHA, depth=surface.get_bitsize()).convert_alpha()
    newsurf.blit(surface, (0, 0))
    if subrect:
        rect = subrect
    arrayrgb = surfarray.pixels3d(newsurf)
    arraya = surfarray.pixels_alpha(newsurf)
    points = []
    max_d = hypot(rect.w, rect.h)
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            if tuple(arrayrgb[x][y]) != color_except:
                points.append((x, y))
    if points:
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                if not (x, y) in points:
                    d = 1. - illuminate_dist(points, rect, x, y) / max_d
                    d = 255 * factor * d**fadout
                    arraya[x][y] = d
                    arrayrgb[x][y] = color_target
                else:
                    if color_bulk:
                        arrayrgb[x][y] = color_bulk
                    if bulk_alpha:
                        arraya[x][y] = bulk_alpha
    else:
        functions.debug_msg("No points for illuminate alpha except")
    return newsurf

def illuminate_color_except(surface, color_except, color_target, color_bulk=None,
                            subrect=None, factor=1., fadout=2):
    """
    mode : "except" means all the pixels that are not color_source.
           "exact" means all the pixels that are exacly color_source.
    """
    if not HAS_NUMPY:
        raise Exception("Could not use surfarray module from PyGame.\
                     NumPy is probably missing.")
    rect = surface.get_rect()
    newsurf = pygame.Surface(rect.size, depth=surface.get_bitsize()).convert()
    newsurf.blit(surface, (0, 0))
    if subrect:
        rect = subrect
    arrayrgb = surfarray.pixels3d(newsurf)
    points = []
    max_d = hypot(rect.w, rect.h)
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            if tuple(arrayrgb[x][y]) != color_except:
                points.append((x, y))
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            if not (x, y) in points:
                d = 1. - illuminate_dist(points, rect, x, y) / max_d
                d = d**fadout
                color = grow_color(factor * d, color_target)
                color = normalize_color(color)
                arrayrgb[x][y] = color
            elif color_bulk:
                arrayrgb[x][y] = color_bulk
    return newsurf


##def illuminate_monocolor(surface, color_source, color_target, max_alpha=255):
##    #faire avec une color_source, multicolor, tester arraycopy au lieu de copy,surfarray
####    arraysurf = surfarray.pixels2d(surface)
##    (w, h) = surface.get_size()
##    #create fully transparent frame
##    newsurf = pygame.Surface((w, h), SRCALPHA, 32).convert_alpha()
####    surfarray.blit_array(newsurf, arraysurf)
##    newsurf.blit(surface, (0, 0))
##    arrayrgb = surfarray.pixels3d(newsurf)
##    arraya = surfarray.pixels_alpha(newsurf)
####    for x in range(w): #inverser boucle?
####        for y in range(h):
######            if arrayrgb[x][y][0] == color_source[0]:
######                if arrayrgb[x][y][1] == color_source[1]:
######                    if arrayrgb[x][y][2] == color_source[2]:
####            arraya[x][y] = 255
####            arrayrgb[x][h/2] = (255, 0, 0)
##    for x in range(w):
##        arraya[x][h/2] = min(4*x, 255)
##    return newsurf


##def illuminate_monocolor(surface, color_source, color_target, max_alpha=255):
##    #faire avec une color_source, multicolor, tester arraycopy au lieu de copy,surfarray
##    arraysurf = surfarray.pixels2d(surface)
##    (w, h) = surface.get_size()
##    #create fully transparent frame
##    newsurf = pygame.Surface((w, h), SRCALPHA, 32).convert_alpha()
##    surfarray.blit_array(newsurf, arraysurf)
##    arrayrgb = surfarray.pixels3d(newsurf)
##    arraya = surfarray.pixels_alpha(newsurf)
##    for x in range(w):
##        arrayrgb[x][h/2] = (255, 0, 0)
##        arraya[x][h/2] = min(x, 255)
##    return newsurf


##def illuminate_monocolor_ip(surface, color_source, color_target, max_alpha=255):
##    #faire avec une color_source, multicolor, tester arraycopy au lieu de copy,surfarray
##    (w, h) = surface.get_size()
####    s = pygame.Surface((w, h), flags=SRCALPHA).convert_alpha() #!enlever convert?
##    surface.convert_alpha()
##    pa = PixelArray(surface)
####    pixelcopy.surface_to_array(s, surface, kind="A", opaque=255, clear=0)
##    for x in range(w): #tester inversion de boucle
##        pa[x, h/2] = (0, 0, 255, min(x, 255))
####        for y in range(h):
####    img = pa.make_surface()
####    return img


def from_function_alpha(surface):
    if not HAS_NUMPY:
        raise Exception("Could not use surfarray module from PyGame.\
                     NumPy is probably missing.")
    size = surface.size
    newsurf = pygame.Surface(size, SRCALPHA, depth=surface.get_bitsize()).convert_alpha()
    newsurf.blit(surface, (0, 0))
    if subrect:
        rect = subrect
    arrayrgb = surfarray.pixels3d(newsurf)
    arraya = surfarray.pixels_alpha(newsurf)
    points = []
    max_d = hypot(rect.w, rect.h)
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            if tuple(arrayrgb[x][y]) != color_except:
                points.append((x, y))
    if points:
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                if not (x, y) in points:
                    d = 1. - illuminate_dist(points, rect, x, y) / max_d
                    d = 255 * factor * d**fadout
                    arraya[x][y] = d
                    arrayrgb[x][y] = color_target
                else:
                    if color_bulk:
                        arrayrgb[x][y] = color_bulk
                    if bulk_alpha:
                        arraya[x][y] = bulk_alpha


def linear_h_monogradation(surface, xi, xf, c_target, c_source):
    """Draw a colour gradiation on <surface> along an horizontal line going from
    xi to xf pixels. It linearly interpolates colors c_target to c_source.
    """
    L = xf - xi
    h = surface.get_height()
    for pix in range(L):
        r = (c_target[0] - c_source[0]) * pix // L + c_source[0]
        g = (c_target[1] - c_source[1]) * pix // L + c_source[1]
        b = (c_target[2] - c_source[2]) * pix // L + c_source[2]
        start = (pix + xi, 0)
        end = (pix + xi, h)
        pygame.draw.line(surface, (r, g, b), start, end)
    return surface

def linear_v_monogradation(surface, yi, yf, c_target, c_source, xi=0, xf=None):
    """Draw a colour gradiation on <surface> along an horizontal line going from
    xi to xf pixels. It linearly interpolates colors c_target to c_source.
    """
    L = yf - yi
    if xf is None:
        xf = surface.get_width() - xi
    for pix in range(L):
        r = (c_target[0] - c_source[0]) * pix // L + c_source[0]
        g = (c_target[1] - c_source[1]) * pix // L + c_source[1]
        b = (c_target[2] - c_source[2]) * pix // L + c_source[2]
        start = (xi, pix + yi)
        end = (xf, pix + yi)
        pygame.draw.line(surface, (r, g, b), start, end)
    return surface

def linear_h_multigradation(surface, colors):
    """Draw a colour gradiation on <surface> along an horizontal line. It
    linearly interpolates all the colors in <colors>.
    surface : a pygame Surface.
    colors : a list of colors whose length is >= 2.
    """
    n = len(colors)
    w = surface.get_width()
    L = w // (n - 1)
    for (i, c_source) in enumerate(colors):
        if i + 1 == n:
            break
        else:
            xi = i * L
            xf = xi + L
            c_target = colors[i+1]
            linear_h_monogradation(surface, xi, xf, c_target, c_source)
    return surface

def linear_v_multigradation(surface, colors):
    """Draw a colour gradiation on <surface> along an horizontal line. It
    linearly interpolates all the colors in <colors>.
    surface : a pygame Surface.
    colors : a list of colors whose length is >= 2.
    """
    n = len(colors)
    h = surface.get_height()
    L = h // (n - 1)
    for (i, c_source) in enumerate(colors):
        if i + 1 == n:
            break
        else:
            yi = i * L
            yf = yi + L
            c_target = colors[i+1]
            linear_v_monogradation(surface, yi, yf, c_target, c_source)
    return surface






def draw_vector_on(surface, color, pos, vec):
    vec = (pos[0] + vec[0], pos[1] + vec[1])
    pygame.draw.line(surface, color, pos, vec)
    r = Rect(0, 0, 3, 3)
    r.center = vec
    pygame.draw.rect(surface, color, r)


def void_frame(size, bck):
    surface = Surface(size)
    try:
        surface.fill(bck)
        surface.set_colorkey(bck, RLEACCEL)
    except TypeError:
        surface.fill(WHITE)
        surface.set_colorkey(constants.WHITE, RLEACCEL)
    return surface.convert()


def simple_frame(size, color=constants.BRAY):
    surface = Surface(size)
    surface.fill(color)
    return surface.convert()


def simple_alpha_frame(size, color=constants.BRIGHT, alpha=200):
    surface = Surface(size, flags=SRCALPHA)
    color = gac(color, alpha)
    surface.fill(color)
    return surface.convert_alpha()


def shadowed_frame_border_blit(surface, rect, pressed=False, thick=1,
                               color=constants.BRAY, light=None, dark=None):
    if not light:
        light = mid_color(color, constants.WHITE)
    if not dark:
        dark = mid_color(color, constants.BLACK)
    for x in range(0, thick):
        r = rect.inflate(-x, -x)
        tc = get_top_coords(r)
        bc = get_bottom_coords(r)
        if pressed:
            pygame.draw.lines(surface, dark, False, tc, 1)
            pygame.draw.lines(surface, light, False, bc, 1)
        else:
            pygame.draw.lines(surface, light, False, tc, 1)
            pygame.draw.lines(surface, dark, False, bc, 1)


def shadowed_frame_blit(surface, rect, pressed=False, thick=1,
                        color=constants.BRAY, light=None, dark=None):
    """Blit on a surface"""
    # draw body
    pygame.draw.rect(surface, color, rect)
    # draw shadows
    shadowed_frame_border_blit(
        surface,
        rect,
        pressed,
        thick,
        color,
        light,
        dark)


def shadowed_frame(size, pressed=False, thick=1,
                   color=constants.BRAY, light=None, dark=None):
    """Returns a sdl surface.
    Function used as default design for elements."""
    if size[1] < 1:
        size = (size[0], 16)
    surface = Surface(size)
    shadowed_frame_blit(
        surface,
        pygame.Rect(
            (0,
             0),
            size),
        pressed,
        thick,
        color,
        light,
        dark)
    return surface.convert()


def basic_cursor(height, thickness=1, color=constants.BLACK):
    begin = (0, 0)
    end = (0, height)
    surface = Surface((thickness, height))
    pygame.draw.line(surface, color, begin, end, thickness)
    return surface.convert()


def basic_bckgr(size, color=constants.BLACK):
    surface = Surface(size)
    surface.fill(color)
    return surface.convert()


def regular_polygon(
        radius,
        sides,
        thickness=0,
        angle=0.,
        color=constants.BLACK):
    """Angle is the offset angle in degrees"""
    surface = Surface((2 * radius, 2 * radius))
    different = different_color(color)
    surface.fill(different)
    surface.set_colorkey(different, RLEACCEL)
    angle = radians(angle)
    alpha = 2 * pi / sides  # constant
    # building points
    points = list()
    for i in range(sides):
        ai = i * alpha + angle
        pix = cos(ai) * radius + radius
        piy = sin(ai) * radius + radius
        points.append((pix, piy))
    pygame.draw.polygon(surface, color, points, thickness)
    return surface.convert()


def classic_lift_button(size=(16, 16), side="top", arrow_color=constants.BLACK,
                        frame_args=None):
    if not frame_args:
        frame_args = {}
    frame_args["size"] = size
    frame = shadowed_frame(**frame_args)
    img = load_image(name="data/arrow.bmp", colorkey=constants.WHITE)
    rotation = 0
    if side == "bottom":
        rotation = 180
    elif side == "right":
        rotation = -90
    elif side == "left":
        rotation = 90
    img = rotate(img, rotation)
    change_color_on_img_ip(img, BLACK, arrow_color, constants.WHITE)
    img.set_colorkey(constants.WHITE, RLEACCEL)
    rect = img.get_rect()
    rect.center = frame.get_rect().center
    rect.move_ip((-1, -1))
    frame.blit(img, rect.topleft)
    return frame


def cross(surface, rect, thick=1, color=(0, 0, 0)):
    pygame.draw.line(surface, color, rect.topleft, rect.bottomright, thick)
    pygame.draw.line(surface, color, rect.bottomleft, rect.topright, thick)


##def aadashed(surface, a, b, N=-50, start=False):
##    (x0, y0) = a
##    (xf, yf) = b
##    if N < 0:  # in this case abs(N) is the length of the dashes
##        V = numpy.array(numpy.array([x0, y0]) - numpy.array([xf, yf]))
##        L = numpy.linalg.norm(V)  # length of the line
##        N = int(L / (2 * abs(N)))  # get number of dashes
##    X = numpy.linspace(x0, xf, N)
##    Y = numpy.linspace(y0, yf, N)
##    for i in range(N - 1):
##        if (i + start) % 2 == 0:
##            pygame.draw.aaline(
##                surface, (0, 0, 0), (X[i], Y[i]), (X[i + 1], Y[i + 1]))


def aadashed_lines(surface, points, N=50, start=True):
    distance = 0
    for i in range(1, len(points)):
        a = points[i - 1]
        b = points[i]
        length = hypot(b[0] - a[0], b[1] - a[1])
        if length + distance < N:
            distance += length
            pygame.draw.aaline(surface, (0, 0, 0), a, b)
        else:
            pass



##
# def dashedRect(surface, color, rect, N=-3, start=False):
# dashedLine(surface,color,rect.topleft,rect.topright,N,start)
# dashedLine(surface,color,rect.topleft,rect.bottomleft,N,start)
# dashedLine(surface,color,rect.bottomleft,rect.bottomright,N,start)
# dashedLine(surface,color,rect.topright,rect.bottomright,N,start)
