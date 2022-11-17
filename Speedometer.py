import math
import numpy as np

class Speedometer:
    def __init__(self):
        self.speed = 0

    def calculate_speed(self, bus, gear, rpm):
        if gear == -1:
            self.speed = gear * math.sqrt(rpm) / 3
        else:
            self.speed = np.sign(gear) * ((gear ** 1.001) * math.sqrt(rpm)) / 3
        bus["speed"] = self.speed
        return bus
