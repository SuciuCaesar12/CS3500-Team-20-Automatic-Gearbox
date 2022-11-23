import math
import numpy as np

class Speedometer:
    def __init__(self):
        self.speed = 0

    def calculate_speed(self, bus, gear, rpm):
        """
        Calculate the approximated speed of the vehicle using the current Gear and RPM.
        :param bus: internal state values like RPM, Speed, ...
        :param gear: the current Gear.
        :param rpm: the current RPM.
        :return: bus updated with a new value for speed.
        """
        if gear == -1: #-------- 1 #
            self.speed = gear * math.sqrt(rpm) / 3 #-------- 2 #
        else:
            self.speed = np.sign(gear) * ((gear ** 1.001) * math.sqrt(rpm)) / 3 #-------- 3 #
        bus["speed"] = self.speed #-------- 4 #
        return bus
