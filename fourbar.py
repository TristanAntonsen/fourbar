# Derivation of angle equations from:
# https://www.youtube.com/watch?v=4O-XPJ7flLU

import numpy as np

### Link lengths

l0 = 7
l1 = 3
l2 = 7.5
l3 = 4.5

### Fixed joints

jo = (0,0)
jc = (l0, 0)

### Drive angle

theta2 = 100

### Calculating intermediate angles

a_c = np.sqrt(l0**2 + l1**2 + 2 * l0 * l1 * np.cos(theta2))
beta = np.arccos((l0 + a_c**2 - l1**2) / (2 * l0 * a_c))
psi = np.arccos((l2 ** 2 + a_c ** 2 - l1 ** 2) / (2 * l2 * a_c))
lmda = np.arccos((l3 ** 2 + a_c ** 2 - l2 ** 2) / (2 * l3 * a_c))

### Calculating main angles

if theta2 <= 180:
    theta3 = psi - beta
    theta4 = 180 - lmda - beta
elif theta2 > 180:
    theta3 = psi + beta
    theta4 = 180 - lmda + beta

### Remaining joint positions

ja = (l1 * np.cos(theta2), 0)
jb = (jc[0] + l3 * np.cos(theta4), l3 * np.sin(theta4))

