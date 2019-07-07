from itertools import chain
from math import trunc
from operator import truediv

from sdl2 import render
from sdl2.ext import Renderer


class CartesianRenderer(Renderer):
    def __init__(self, window, index=-1, logical_size=None,
                 flags=render.SDL_RENDERER_ACCELERATED):
        Renderer.__init__(self, window, index, logical_size, flags)
        self.__default_window_size = window.size

    def draw_line(self, points, color=None):
        mapped_points = self.__map_points_to_window_coordinates(points)
        Renderer.draw_line(self, mapped_points, color)

    def draw_point(self, points, color=None):
        mapped_points = self.__map_points_to_window_coordinates(points)
        Renderer.draw_point(self, mapped_points, color)

    def draw_rect(self, rects, color=None):
        mapped_rects = self.__map_rects_to_window_coordinates(rects)
        Renderer.draw_rect(self, mapped_rects, color)

    def fill(self, rects, color=None):
        mapped_rects = self.__map_rects_to_window_coordinates(rects)
        Renderer.fill(self, mapped_rects, color)

    def __map_rects_to_window_coordinates(self, rects):
        points = list(chain(map(lambda rect: (rect[0], rect[1]), rects)))
        mapped_points = self.__map_points_to_window_coordinates(points)
        return [(mapped_points[i][0], mapped_points[i][1], rects[i][2], rects[i][3]) for i in range(len(rects))]

    def __map_points_to_window_coordinates(self, points):
        actual_window_size = self.rendertarget.size
        x_scaling_factor, y_scaling_factor = tuple(map(truediv, actual_window_size, self.__default_window_size))
        mapped_points = []
        for pair_i in range(0, len(points), 2):
            x, y = points[pair_i], points[pair_i + 1]
            x = trunc(x * x_scaling_factor) + actual_window_size[0] // 2
            y = actual_window_size[1] - (trunc(y * y_scaling_factor) + actual_window_size[1] // 2)
            mapped_points.append(x)
            mapped_points.append(y)
        return mapped_points
