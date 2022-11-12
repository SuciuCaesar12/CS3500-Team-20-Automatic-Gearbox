import Gearbox as GB
import Engine as EN
import Speedometer as SPD
import keyboard

class Simulation:
    def __init__(self):
        self.bus = {
            "rpm": 0,
            "speed": 0,
            "engine_signal": False,
            "gear_mode": "Park",
            "drive_mode": "Eco",
            "gear": 0
        }

        self.gearbox = GB.Gearbox(self.bus)
        self.engine = EN.Engine()
        self.speedometer = SPD.Speedometer()
        #self.controller = CTRL.Controller(self.bus)

    def run(self):
        i = 0
        self.bus["gear"] = 1     #Have to delete this later on, but for testing the Gear cannot be 0.
        while True:

            gas = False
            engine_button = False

            if keyboard.is_pressed("i"):
                engine_button = True

            if keyboard.is_pressed("g"):
                gas = True

            if keyboard.is_pressed("s"):
                self.bus["drive_mode"] = "Sport"

            if keyboard.is_pressed("e"):
                self.bus["drive_mode"] = "Eco"

            if keyboard.is_pressed("p"):
                self.bus["gear_mode"] = "Park"

            if keyboard.is_pressed("d"):
                self.bus["gear_mode"] = "Drive"

            if keyboard.is_pressed("r"):
                self.bus["gear_mode"] = "Reverse"

            if keyboard.is_pressed("n"):
                self.bus["gear_mode"] = "Neutral"


            self.bus = self.engine.give_Gas(self.bus, gear=self.bus["gear"], gas=gas)
            self.bus = self.speedometer.calculate_speed(self.bus, gear=self.bus["gear"], rpm=self.bus["rpm"])
            if i % 100 == 0:
                print("RPM " + str(self.bus["rpm"]))
                print("Speed " + str(self.bus["speed"]))
            i += 1
            #self.controller.run(self.bus, engine_button)

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