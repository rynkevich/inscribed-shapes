from math import cos, pi, sin, trunc, tan
from operator import truediv


class InscribedShape:
    def __init__(self, n_angles, circumscribed_circle_radius, nesting_level, shift_angle):
        self.__n_angles = n_angles
        self.__circumscribed_circle_radius = circumscribed_circle_radius
        self.__nesting_level = nesting_level
        self.__shift_angle = shift_angle
        self.__vertices = None

    def draw(self, renderer, default_window_size, actual_window_size, color=None):
        if self.__vertices is None:
            self.__vertices = self.__get_inscribed_vertices()
        for level in range(self.__nesting_level):
            for vertex_i in range(self.__n_angles):
                x1, y1 = self.__map_to_window_coordinates(
                    self.__vertices[level][vertex_i], default_window_size, actual_window_size)
                x2, y2 = self.__map_to_window_coordinates(
                    self.__vertices[level][(vertex_i + 1) % self.__n_angles], default_window_size, actual_window_size)
                renderer.draw_line((x1, y1, x2, y2), color)
        renderer.present()

    def __get_inscribed_vertices(self):
        vertices = [self.__get_outer_vertices()]
        for level_i in range(self.__nesting_level):
            mu = tan(self.__shift_angle) / (tan(self.__shift_angle) + 1)
            previous_level_vertices = vertices[level_i]
            level_vertices = []
            for vertex_i in range(self.__n_angles):
                x = (1 - mu) * previous_level_vertices[vertex_i][0] \
                    + mu * previous_level_vertices[(vertex_i + 1) % self.__n_angles][0]
                y = (1 - mu) * previous_level_vertices[vertex_i][1] \
                    + mu * previous_level_vertices[(vertex_i + 1) % self.__n_angles][1]
                level_vertices.append((x, y))
            vertices.append(level_vertices)
        return vertices

    def __get_outer_vertices(self):
        vertices = []
        first_point_angular_coordinate = 3 * pi / 2 - pi / self.__n_angles
        for vertex_i in range(self.__n_angles):
            x = self.__circumscribed_circle_radius \
                * cos(first_point_angular_coordinate + 2 * pi * vertex_i / self.__n_angles)
            y = self.__circumscribed_circle_radius \
                * sin(first_point_angular_coordinate + 2 * pi * vertex_i / self.__n_angles)
            vertices.append((x, y))
        return vertices

    @staticmethod
    def __map_to_window_coordinates(point, default_window_size, actual_window_size):
        x, y = point
        x_scaling_coeff, y_scaling_coeff = tuple(map(truediv, actual_window_size, default_window_size))
        max_y = actual_window_size[1]
        x = trunc(x * x_scaling_coeff) + actual_window_size[0] // 2
        y = max_y - (trunc(y * y_scaling_coeff) + actual_window_size[1] // 2)
        return x, y
