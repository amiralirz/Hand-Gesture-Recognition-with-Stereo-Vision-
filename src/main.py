import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stereohand import StereoHand
from stereovision import Stereo
from collections import deque

COP1 = (658, 348) # location of the center of projection for camera 1
COP2 = (516, 237) # location of the center of projection for camera 2

so = Stereo(b=13.5, f=1080, disparity_shift=(COP1[0] - COP1[0])) # Stereo Object for Stereo hand initialization
stereo_hand_instance = StereoHand(so)

z_data = deque(maxlen=30)
x_data = deque(maxlen=30)
y_data = deque(maxlen=30)
plt.show()
log_counter = 0

while True:
    found, pos3d = stereo_hand_instance.get_hand()
    if not found:
        continue
    x = [e[0] for e in pos3d]
    y = [e[1] for e in pos3d]
    z = [e[2] for e in pos3d]
    average_z = sum(z) / len(z)
    average_x = sum(x) / len(x)
    average_y = sum(y) / len(y)
    z_data.append(average_z)  # Add the new value to the deque
    x_data.append(average_x)
    y_data.append(average_y)
    plt.cla()  # Clear the previous plot
    plt.plot(z_data, label="Z")  # Plot the current values
    plt.plot(x_data, label="X")
    plt.plot(y_data, label="Y")
    plt.legend(loc="upper left")
    plt.ylim(min(min(y_data), min(x_data)), max(max(z_data), max(x_data), max(y_data)))  # Set axis limits based on data
    plt.draw()
    plt.pause(0.001)  # Pause briefly to avoid overwhelming the display
    log_counter += 1
    if log_counter == 6:
        print(f"\t{average_x}\t{average_y}\t{average_z}")
        log_counter = 0
    