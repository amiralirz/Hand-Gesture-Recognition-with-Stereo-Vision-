import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from stereohand import StereoHand

stereo_hand_instance = StereoHand()

fig, ax = plt.subplots(1, 2)
point1, = ax[0].plot([0], [0], color="red")
point2, = ax[1].plot([0], [0], color="green")

ax[0].set_xlim(0, 40)
ax[0].set_ylim(-10, 20)
ax[1].set_xlim(-40, 100)
ax[1].set_ylim(-100, 100)

def update(frame):
    found, pos3d = stereo_hand_instance.get_hand()
    if not found:
        return (0, 0)
    # point.set_data([x], [y])
    x = [e[0] for e in pos3d]
    y = [e[1] for e in pos3d]
    z = [e[2]*10 for e in pos3d]
    point1.set_data(x, y)
    point2.set_data(x, [z[0]]*21)
    return point1, point2

# Create the animation
ani = FuncAnimation(
    fig,
    update,
    interval=100,  # Update every 100 milliseconds
)

plt.show()


