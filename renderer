import sys
import numpy as np
import numpy.typing as npt
from collections.abc import Callable
from typing import TypeAlias

RGB: TypeAlias = tuple[int, int, int]
RGBA: TypeAlias = tuple[int, int, int, float]
SampleColor: TypeAlias = Callable[[int, int], RGBA]
ColorSource: TypeAlias = SampleColor | RGB | RGBA

Point: TypeAlias = tuple[int, int]

ESC = "\x1b"

def format_ansi(last: str, *params: int | str):
    return f"{ESC}[{';'.join(str(p) for p in params)}{last}"

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def is_opaque(color: RGB | RGBA):
    return len(color) == 3 or color[3] > 0.999

class Renderer:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._buffer = np.zeros((height, width, 3), dtype=np.uint8)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _get_pixel(self, x: int, y: int) -> npt.NDArray[np.uint8]:
        if not (0 <= x < self.width):
            raise ValueError("X out of range")
        if not (0 <= y < self.height):
            raise ValueError("Y out of range")

        return self._buffer[y, x]

    def get_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        pixel = self._get_pixel(x, y)

        return int(pixel[0]), int(pixel[1]), int(pixel[2])

    def draw_pixel(self, x: int, y: int, color: RGB | RGBA):
        pixel = self._get_pixel(x, y)

        if is_opaque(color):
            pixel[0] = color[0]
            pixel[1] = color[1]
            pixel[2] = color[2]
        else:
            pixel[0] = int(lerp(int(pixel[0]), color[0], color[3]))
            pixel[1] = int(lerp(int(pixel[1]), color[1], color[3]))
            pixel[2] = int(lerp(int(pixel[2]), color[2], color[3]))

    def fill(self, color_source: ColorSource) -> None:
        if isinstance(color_source, tuple) and is_opaque(color_source):
            self._buffer[:] = color_source
        else:
            for y in range(self._height):
                for x in range(self._width):
                    self.draw_pixel(x, y, color_source(x, y))

    def draw_rectangle(self, left_x: int, top_y: int, width: int, height: int, color_source: ColorSource) -> None:
        x0, x1 = left_x, left_x + width
        y0, y1 = top_y, top_y + height

        x0, x1 = max(0, x0), min(self._width, x1)
        y0, y1 = max(0, y0), min(self._height, y1)

        if isinstance(color_source, tuple):
            if is_opaque(color_source):
                self._buffer[y0:y1, x0:x1] = (color_source[0], color_source[1], color_source[2])
            else:
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        self.draw_pixel(x, y, color_source)
        else:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    self.draw_pixel(x, y, color_source(x - x0, y - y0))

    def draw_circle(self, center_x: int, center_y: int, radius: int, color_source: ColorSource) -> None:
        y0, y1 = center_y - radius, center_y + radius
        y0, y1 = max(0, y0), min(self._height, y1)

        for y in range(y0, y1):
            dx = int((radius ** 2 - (y - center_y) ** 2) ** 0.5)
            x0, x1 = center_x - dx, center_x + dx
            x0, x1 = max(0, x0), min(self._width, x1)

            if isinstance(color_source, tuple):
                if is_opaque(color_source):
                    self._buffer[y, x0:x1] = color_source
                else:
                    for x in range(x0, x1):
                        self._buffer[y, x] = color_source
            else:
                for x in range(x0, x1):
                    self._buffer[y, x] = color_source(x - x0, y - y0)

    def draw_line(self, start: Point, end: Point, thickness: int, color_source: ColorSource) -> None:
        raise NotImplemented

    def draw_polygon(self, vertices: list[Point], color_source: ColorSource) -> None:
        raise NotImplemented

    def present(self) -> None:
        out: list[str] = [format_ansi("J", 2), format_ansi("H")]
        current: list[int] | None = None

        for row in self._buffer:
            for pixel in row:
                if current is None or current != pixel.tolist():
                    out.append(format_ansi("m", 48, 2, pixel[0], pixel[1], pixel[2]))
                    current = pixel.tolist()
                out.append("  ")

            current = None
            out.append(format_ansi("m", 49) + "\n")

        sys.stdout.write("".join(out))
        self._buffer.fill(0)
