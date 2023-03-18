import numpy as np
from display import display

class Joint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Link():
    def __init__(self, j1, j2, length):
        ### Assumes CCW order with origin as first link
        self.j1 = j1
        self.j2 = j2
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

### Fixed joints

jo = Joint(0,0)
jc = Joint(l0, 0)

### Drive angle

theta2 = 2 * np.pi / 2

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
joints = [ja, jb, jo, jc]
for j in joints:
    print(j.x, j.y)

display(1080, 1080, joints, save=False, show=True)