from __future__ import annotations
from dataclasses import dataclass, field
from fill import Fill

@dataclass
class Node:
    _parent: Node | None = field(init=False, default=None)
    _children: list[Node] = field(init=False, default_factory=list)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: Node | None):
        if self._parent is value:
            return

        if self._parent is not None:
            self._parent._children.remove(self)

        self._parent = value
        if value is not None:
            value._children.append(self)

    @property
    def children(self):
        return self._children

@dataclass
class Shape(Node):
    x: float
    y: float
    bg: Fill

    def draw_rectangle(self, x: float, y: float, width: float, height: float, bg: Fill) -> Rectangle:
        rectangle = Rectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            bg=bg
        )
        rectangle.parent = self

        return rectangle

    def draw_circle(self, x: float, y: float, radius: float, bg: Fill) -> Circle:
        circle = Circle(
            x=x,
            y=y,
            radius=radius,
            bg=bg
        )
        circle.parent = self

        return circle

@dataclass
class Rectangle(Shape):
    width: float
    height: float

@dataclass
class Circle(Shape):
    radius: float
