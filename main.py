import sys
from math import pi

import sdl2
import sdl2.ext

from inscribed_shape import InscribedShape

DEFAULT_WINDOW_SIZE = (420, 420)

COLOR_WHITE = sdl2.ext.Color(r=255, g=255, b=255, a=255)

CIRCUMSCRIBED_CIRCLE_RADIUS = 200
NESTING_LEVEL = 16
SHIFT_ANGLE = pi / 16


def main():
    n_angles = int(sys.argv[1])
    shape = InscribedShape(n_angles, CIRCUMSCRIBED_CIRCLE_RADIUS, NESTING_LEVEL, SHIFT_ANGLE)

    sdl2.ext.init()
    window = sdl2.ext.Window(
        title='Inscribed Shapes',
        size=DEFAULT_WINDOW_SIZE,
        flags=sdl2.video.SDL_WINDOW_RESIZABLE
    )
    sdl2.SDL_SetWindowMinimumSize(window.window, DEFAULT_WINDOW_SIZE[0] // 2, DEFAULT_WINDOW_SIZE[1] // 2)
    window.show()

    renderer = sdl2.ext.Renderer(window)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_WINDOWEVENT:
                renderer.clear(COLOR_WHITE)
                shape.draw(renderer, DEFAULT_WINDOW_SIZE, window.size)

    sdl2.ext.quit()
    return 0


if __name__ == '__main__':
    sys.exit(main())
