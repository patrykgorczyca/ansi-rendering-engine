from renderer import Renderer
from node import Node, Rectangle, Circle
from fill import Fill, RGBColor, Color
from typing import TypeAlias
from functools import partial

RGBA: TypeAlias = tuple[int, int, int]
RGB: TypeAlias = tuple[int, int, int]

class Scene:
    def __init__(self, width: int, height: int, bg: Fill = RGBColor(255, 255, 255)):
        self._renderer = Renderer(width, height)
        self._canvas = Rectangle(x=0, y=0, bg=bg, width=width, height=height)

    @property
    def canvas(self):
        return self._canvas

    def _draw_rectangle(self, rectangle: Rectangle):
        renderer = self._renderer

        renderer.draw_rectangle(
            left_x=rectangle.x,
            top_y=rectangle.y,
            width=rectangle.width,
            height=rectangle.height,
            color_source=rectangle.bg.get_color_source()
        )

    def _draw_circle(self, circle: Circle):
        renderer = self._renderer

        p = partial(
            renderer.draw_circle,
            center_x=circle.x,
            center_y=circle.y,
            radius=circle.radius
        )

        if isinstance(circle.bg, Color):
            color = circle.bg.sample(0, 0)

            if isinstance(circle.bg, RGBColor):
                p(color_source=(color[0], color[1], color[2]))
            else:
                p(color_source=(color[0], color[1], color[2], color[3]))

    def _draw_node(self, node: Node):
        match node:
            case Rectangle():
                self._draw_rectangle(node)
            case Circle():
                self._draw_circle(node)

        for child in node.children:
            self._draw_node(child)

    def render(self):
        self._draw_node(self._canvas)
        self._renderer.present()
