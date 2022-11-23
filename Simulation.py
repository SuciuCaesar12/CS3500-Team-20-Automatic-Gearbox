import Gearbox as GB
import Engine as EN
import Speedometer as SPD
import controller as CTRL
import keyboard
import time
import Interface
from rich.live import Live
from rich.table import Table

class Simulation:
    def __init__(self):
        self.bus = {
            "rpm": 0,
            "speed": 0,
            "engine_signal": False,
            "engine_on": False,
            "gear_mode": "Park",
            "drive_mode": "Eco",
            "gear": 0,
            "warning_message": '',
            "warning_time": 0
        }

        #Create all the necessary components for the Simulation
        self.gearbox = GB.Gearbox(self.bus)
        self.engine = EN.Engine()
        self.speedometer = SPD.Speedometer()
        self.controller = CTRL.Controller()
        self.interface = Interface.Interface(self.bus)
        self.interface.create_table()


        self.exit = False
        self.engine_button = False
        self.valid_engine_button = 1000


    def __get_input(self):
        pass

    def run(self):
        """
        The main loop of our Simulation. This is where the entire program happens and all other components of the car are used.
        :return:
        """
        with Live(self.interface.create_table(), refresh_per_second=120) as live: #We do not count this as a node, since this loop always needs to be run.
            while not self.exit: #-------- 2 #
                #------------------------- 3 #
                gas = False
                self.engine_button = False
                #------------------------ 3 #

                #All cases of possible user-input that affects the car
                if keyboard.is_pressed("i") and self.valid_engine_button < 0: #-------- 4 #
                    #----------------------------------- 5 #
                    self.engine_button = True
                    self.valid_engine_button = 1000
                    #---------------------------------- 5 #

                if keyboard.is_pressed("g"): #-------- 6 #
                    gas = True #-------- 7 #

                if keyboard.is_pressed("s"): #-------- 8 #
                    self.bus["drive_mode"] = "Sport" # -------- 9 #

                if keyboard.is_pressed("e"): #-------- 10 #
                    self.bus["drive_mode"] = "Eco" #-------- 11 #

                if keyboard.is_pressed("p"): #-------- 12 #
                    self.bus["gear_mode"] = "Park" #-------- 13 #

                if keyboard.is_pressed("d"): #-------- 14 #
                    self.bus["gear_mode"] = "Drive" #-------- 15 #

                if keyboard.is_pressed("r"): #-------- 16 #
                    self.bus["gear_mode"] = "Reverse" #-------- 17 #

                if keyboard.is_pressed("n"): #-------- 18 #
                    self.bus["gear_mode"] = "Neutral" #-------- 19 #

                #----------------------------------------------------------------------------------------------------- 20 #
                #The Controller makes a decisions about what to do next
                self.bus, self.gearbox = self.controller.run(self.bus, self.engine_button, self.gearbox)

                #Then Engine calculates the new RPM and updates this in the bus
                self.bus = self.engine.run(self.bus, gas=gas)

                #The Speedometer calculates the new Speed and updates this in the bus
                self.bus = self.speedometer.calculate_speed(self.bus, gear=self.bus["gear"], rpm=self.bus["rpm"])

                self.valid_engine_button -= 1
                self.bus["warning_time"] -= 1

                #----------------------------------------------------------------------------------------------------- 20 #

                #These last statements are simple statements and we don't think they require testing.

                #Remove the warning message after enough time has passed
                if self.bus["warning_time"] < 0:
                    self.bus["warning_message"] = ""

                #Exit the Simulation by pressing 'z', interrupting the while-loop
                if keyboard.is_pressed("z"):
                    self.exit = True

                #Update the Interface by creating a new table with the updated values
                live.update(self.interface.create_table())


if __name__ == '__main__':
    sim = Simulation()
    sim.run()
