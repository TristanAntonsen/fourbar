import numpy as np
from display import display
import matplotlib.pyplot as plt

class Joint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Link():
    def __init__(self, js, je, length):
        self.js = js
        self.je = je
        self.length = length

class Linkage():
    def __init__(self, joints, links):
        self.joints = joints
        self.links = links

### Link lengths

l0 = 7
l1 = 3
l2 = 7.5
l3 = 4.5

### Joints

jo = Joint(0,0)
jc = Joint(l0, 0)

### Links
link0 = Link(jo, jc, 7)
link1 = Link(jo, None, 3)
link2 = Link(None, None, 7.5)
link3 = Link(None, jc, 4.5)

### Drive angle

theta2 = np.pi / 10

### Calculating intermediate angles
# Derivation of angles:
# https://www.youtube.com/watch?v=4O-XPJ7flLU

a_c = np.sqrt(l0**2 + l1**2 + 2 * l0 * l1 * np.cos(theta2))
beta = np.arccos((l0 + a_c**2 - l1**2) / (2 * l0 * a_c))
psi = np.arccos((l2 ** 2 + a_c ** 2 - l3 ** 2) / (2 * l2 * a_c))
lmda = np.arccos((l3 ** 2 + a_c ** 2 - l2 ** 2) / (2 * l3 * a_c))

### Calculating main angles

theta3 = psi - beta
theta4 = np.pi - lmda - beta

if theta2 > np.pi:
    theta3 = psi + beta
    theta4 = np.pi - lmda + beta

### Remaining joint positions

ja = Joint(l1 * np.cos(theta2), l1 * np.cos(theta2))
jb = Joint(jc.x + l3 * np.cos(theta4), l3 * np.sin(theta4))

### Completing links
link1.je, link2.js = ja, ja
link2.j3, link3.js = jb, jb

joints = [jo, ja, jb, jc]

plt.figure(figsize=(5,5))

plt.plot([jo.x, ja.x], [jo.y, ja.y])
plt.plot([ja.x, jb.x], [ja.y, jb.y])
plt.plot([jb.x, jc.x], [jb.y, jc.y])
plt.plot([jc.x, jo.x], [jc.y, jo.y])

plt.show()

