from dataclasses import dataclass
from typing import TypeAlias

RGBA: TypeAlias = tuple[int, int, int, float]

@dataclass(frozen=True, slots=True)
class RGBColor:
    r: int
    g: int
    b: int

    def __post_init__(self):
        for v in (self.r, self.g, self.b):
            if not (0 <= v <= 255):
                raise ValueError("RGB value out of range")

    def sample(self, u: float, v: float) -> RGBA:
        return self.r, self.g, self.b, 1.0

    def get_color_source(self):
        return self.r, self.g, self.b

@dataclass(frozen=True, slots=True)
class RGBAColor:
    r: int
    g: int
    b: int
    a: float = 1.0

    def __post_init__(self):
        for v in (self.r, self.g, self.b):
            if not (0 <= v <= 255):
                raise ValueError("RGB value out of range")
        if not (0.0 <= self.a <= 1.0):
            raise ValueError("Alpha value out of range")

    def sample(self, u: float, v: float) -> RGBA:
        return self.r, self.g, self.b, self.a

    def get_color_source(self):
        return self.r, self.g, self.b, self.a

Color: TypeAlias = RGBColor | RGBAColor

Fill: TypeAlias = Color
