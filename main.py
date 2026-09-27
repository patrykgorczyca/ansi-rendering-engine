# demo file

from scene import Scene
from fill import RGBColor

def main():
    scene = Scene(width=80, height=50, bg=RGBColor(112, 197, 206))
    canvas = scene.canvas
    player = canvas.draw_rectangle(x=2, y=canvas.height // 2 - 2, width=5, height=5, bg=RGBColor(248, 88, 32))
    pipe = canvas.draw_rectangle(x=10, y=30, width=5, height=20, bg=RGBColor(115, 199, 45))
    scene.render()

if __name__ == "__main__":
    main()
