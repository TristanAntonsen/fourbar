from PIL import Image, ImageDraw




def display(width, height, joints, **kwargs):

    padding = 20 # px
    scale = 10 # global scale

    background_color = (200, 200, 200)

    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    def center_ellipse(x,y,r,c):
        draw.ellipse([x - r, y - r, x + r, y + r],fill=c)

    draw.rectangle((padding, padding, width - padding, height - padding), background_color)

    center_ellipse(padding,height - padding, 10, 'black')

    joint_radius = 15

    for joint in joints:
        display_joint = (joint[0] * scale, height - joint[1] * scale)
        print(display_joint)
        center_ellipse(*display_joint, joint_radius, 'red')
        

    if kwargs.get("save"):
        img.save("display.png")
    if kwargs.get("show"):
        img.show()


if __name__ == "__main__":
    joints = [
        (10, 10),
        (100, 10),
        (90, 40),
        (15, 20)
    ]
    display(1080, 1080, joints, save=True, show=False)