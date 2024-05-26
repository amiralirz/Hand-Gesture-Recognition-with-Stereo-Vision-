import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stereohand import StereoHand
from stereovision import Stereo
from collections import deque

COP1 = (658, 348) # location of the center of projection for camera 1
COP2 = (516, 237) # location of the center of projection for camera 2

so = Stereo(b=11, f=1080, disparity_shift=(COP1[0] - COP1[0])) # Stereo Object for Stereo hand initialization
stereo_hand_instance = StereoHand(so)

values = deque(maxlen=30)

def update_plot(val):
    values.append(val)  # Add the new value to the deque
    plt.cla()  # Clear the previous plot
    plt.plot(values)  # Plot the current values
    plt.ylim(0, max(values))  # Set axis limits based on data
    plt.draw()
    plt.pause(0.001)  # Pause briefly to avoid overwhelming the display



plt.show()
while True:
    found, pos3d = stereo_hand_instance.get_hand()
    if not found:
        continue
    x = [e[0] for e in pos3d]
    y = [e[1] for e in pos3d]
    z = [e[2] for e in pos3d]
    meanZ = sum(z) / len(z)
    update_plot(meanZ)
    

