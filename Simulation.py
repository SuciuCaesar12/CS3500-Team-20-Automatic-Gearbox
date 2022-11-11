import Gearbox as GB
import Engine as EN
import Speedometer as SPD
import keyboard

class Simulation:
    def __init__(self):
        self.Gearbox = GB.Gearbox("P")
        self.Engine = EN.Engine()
        self.Speedometer = SPD.Speedometer()

    def run(self):
        #Most of this stuff should take place in the Controller, but I tested it here for now.
        self.Gearbox.Gear = 6
        while True:
            if keyboard.is_pressed("a"):
                while True:
                    if keyboard.is_pressed("a"):
                        speed = self.Speedometer.calculate_speed(True, self.Gearbox.Gear)
                        print(speed)
                    else:
                        speed = self.Speedometer.calculate_speed(False, self.Gearbox.Gear)
                        print(speed)

sim = Simulation()
sim.run()


"""
while True:
    if keyboard.is_pressed("a"):
        while True:
            if keyboard.is_pressed("a"):
                speed += 0.001
                print(speed)
            else:
                speed -= 0.0001
                print(speed)
                
"""