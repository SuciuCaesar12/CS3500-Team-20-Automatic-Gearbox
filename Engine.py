import math

class Engine:
    def __init__(self):
        self.RPM = 0
        self.Engine_On = False

    def start_Engine(self, Engine_BTN):
        self.Engine_On = Engine_BTN

    def give_Gas(self, Gear, Speed, gear_ratio):
        #https://www.quora.com/How-do-you-calculate-the-engine-RPM-with-a-gear-ratio
        wheel_RPM = Speed*1000/(60*2*math.pi*0.5)
        self.RPM = wheel_RPM*gear_ratio*4
        return self.RPM