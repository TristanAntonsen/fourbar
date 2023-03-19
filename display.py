import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def display(width, height, joints, **kwargs):

    padding = 20 # px
    scale = 25 # global scale
    origin = (width / 2, height / 2)
    background_color = (200, 200, 200)

    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    def center_ellipse(x,y,r,c):
        ## flips y coordinate
        x = x * scale
        y = height - y * scale
        draw.ellipse([x - r, y - r, x + r, y + r],fill=c)

    draw.rectangle((padding, padding, width - padding, height - padding), background_color)

    center_ellipse(*origin, 10, 'black')

    joint_radius = 8

    for joint in joints:
        center_ellipse(
            joint.x,
            joint.y,
            joint_radius, 
            'red')
        

    if kwargs.get("save"):
        img.save("display.png")
    if kwargs.get("show"):
        img.show()


if __name__ == "__main__":
    from fourbar import Joint, calculate_positions
    joints = [
        Joint(0, 0),
        Joint(7, 0),
        Joint(6, 4),
        Joint(1, 3)
    ]
    display(1080, 1080, joints, save=True, show=False)
