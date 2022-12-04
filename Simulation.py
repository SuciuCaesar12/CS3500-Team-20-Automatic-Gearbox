#!/usr/bin/env python
import Gearbox as GB
import Engine as EN
import Speedometer as SPD
import controller as CTRL
import keyboard
import time
import Interface
from rich.live import Live
from rich.table import Table
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk


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

        # Create all the necessary components for the Simulation
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
        with Live(self.interface.create_table(),
                  refresh_per_second=120) as live:  # We do not count this as a node, since this loop always needs to be run.
            while not self.exit:  # -------- 2 #

                # ------------------------- 3 #
                gas = False
                self.engine_button = False
                # ------------------------ 3 #

                # All cases of possible user-input that affects the car
                if keyboard.is_pressed("i") and self.valid_engine_button < 0:  # -------- 4 #
                    # ----------------------------------- 5 #
                    self.engine_button = True
                    self.valid_engine_button = 1000
                    # ---------------------------------- 5 #

                if keyboard.is_pressed("g"):  # -------- 6 #
                    gas = True  # -------- 7 #

                if keyboard.is_pressed("s"):  # -------- 8 #
                    self.bus["drive_mode"] = "Sport"  # -------- 9 #

                if keyboard.is_pressed("e"):  # -------- 10 #
                    self.bus["drive_mode"] = "Eco"  # -------- 11 #

                if keyboard.is_pressed("p"):  # -------- 12 #
                    self.bus["gear_mode"] = "Park"  # -------- 13 #

                if keyboard.is_pressed("d"):  # -------- 14 #
                    self.bus["gear_mode"] = "Drive"  # -------- 15 #

                if keyboard.is_pressed("r"):  # -------- 16 #
                    self.bus["gear_mode"] = "Reverse"  # -------- 17 #

                if keyboard.is_pressed("n"):  # -------- 18 #
                    self.bus["gear_mode"] = "Neutral"  # -------- 19 #

                # ----------------------------------------------------------------------------------------------------- 20 #
                # The Controller makes a decisions about what to do next
                self.bus, self.gearbox = self.controller.run(self.bus, self.engine_button, self.gearbox)

                # Then Engine calculates the new RPM and updates this in the bus
                self.bus = self.engine.run(self.bus, gas=gas)

                # The Speedometer calculates the new Speed and updates this in the bus
                self.bus = self.speedometer.calculate_speed(self.bus, gear=self.bus["gear"], rpm=self.bus["rpm"])

                self.valid_engine_button -= 1
                self.bus["warning_time"] -= 1

                # ----------------------------------------------------------------------------------------------------- 20 #

                # These last statements are simple statements and we don't think they require testing.

                # Remove the warning message after enough time has passed
                if self.bus["warning_time"] < 0:
                    self.bus["warning_message"] = ""

                # Exit the Simulation by pressing 'z', interrupting the while-loop
                if keyboard.is_pressed("z"):
                    self.exit = True

                # Update the Interface by creating a new table with the updated values
                live.update(self.interface.create_table())

    # Gui function to dissplay all variables of the car
    def gui(self):

        # rpm dial
        if self.bus.get("rpm") == 0:
            rpm = tk.StringVar(value=str(self.bus.get("rpm"))[:5] + " RPM      ")
        else:
            rpm = tk.StringVar(value=str(self.bus.get("rpm"))[:5] + " RPM")
        rpm_dial = tk.Label(root, bg="black", fg="red", textvariable=rpm,
                            font=('Helvatical bold', 20))
        rpm_dial.place(x=190, y=220)

        # speed dial
        if self.bus.get("speed") == 0:
            speed = tk.StringVar(value=str(self.bus.get("speed"))[:4] + " Km/h  ")
        else:
            speed = tk.StringVar(value=str(self.bus.get("speed"))[:4] + " Km/h ")
        speed_dial = tk.Label(root, bg="black", fg="yellow", textvariable=speed,
                              font=('Helvatical bold', 20))
        speed_dial.place(x=570, y=220)

        # engine
        if self.bus.get("engine_on") == True:
            engine_state = tk.StringVar(value="Engine: On")
        else:
            engine_state = tk.StringVar(value="Engine: Off")
        engine_dis = tk.Label(root, bg="black", fg="white",
                              textvariable=engine_state, font=('Helvatical bold', 10))
        engine_dis.place(x=380, y=190)

        # gear
        gear_state = tk.StringVar(value="Gear: " + str(self.bus.get("gear")))
        gear_dis = tk.Label(root, bg="black", fg="white",
                            textvariable=gear_state, font=('Helvatical bold', 10))
        gear_dis.place(x=380, y=210)

        # gear mode
        if str(self.bus.get("gear_mode")) == "Drive":
            gear_mode_state = tk.StringVar(value="Gear Mode: " + str(self.bus.get("gear_mode")) + "   ")
        else:
            gear_mode_state = tk.StringVar(value="Gear Mode: " + str(self.bus.get("gear_mode")))

        gear_mode_dis = tk.Label(root, bg="black", fg="white",
                                 textvariable=gear_mode_state, font=('Helvatical bold', 10))
        gear_mode_dis.place(x=380, y=230)

        # drive mode
        drive_mode_dis1 = tk.Label(root, bg="black", fg="white",
                                   text="Drive Mode:", font=('Helvatical bold', 10))
        drive_mode_dis1.place(x=380, y=250)
        if str(self.bus.get("drive_mode")) == "Eco":
            drive_mode_dis = tk.Label(root, bg="black", fg="green",
                                      text=str(self.bus.get("drive_mode")) + "  ", font=('Helvatical bold', 10))
            drive_mode_dis.place(x=450, y=250)
        else:
            drive_mode_dis = tk.Label(root, bg="black", fg="yellow",
                                      text=str(self.bus.get("drive_mode")), font=('Helvatical bold', 10))
            drive_mode_dis.place(x=450, y=250)

        # error message
        if len(self.bus.get("warning_message")) > 3:
            if self.bus["warning_time"] < 10:
                self.bus["warning_time"] = 500
            error_msg = tk.StringVar(value=str(self.bus.get("warning_message")))
        else:
            error_msg = tk.StringVar(value="                                ")
        error_dis = tk.Label(root, bg="black", fg="red",
                             textvariable=error_msg, font=('Helvatical bold', 10))
        error_dis.place(x=370, y=280)

        # Destroy window on Simultion exit
        if self.exit == True:
            root.destroy()

        root.after(100, self.gui)


def info():
    window = tk.Tk()
    window.geometry("150x280+50+50")
    window.title("Information")
    message = "          -- Controls --" \
              "\n Ignition: 'I'\n" \
              "\n Gear Modes:" \
              "\n\t Drive: 'D'"\
              "\n\t Park: 'P'"\
              "\n\t Reverse: 'R'"\
              "\n\t Neutral: 'N'\n"\
              "\n Drive Modes:"\
              "\n\t Sport: 'S'"\
              "\n\t Eco: 'E'\n"\
              "\n Gas(accelerate): 'G'" \
              "\n\n Exit window: 'Z'"
    info = tk.Text(window,font=('Cooper Std Black', 10))
    info.pack()
    info.insert(tk.END,message)
    window.mainloop()


if __name__ == '__main__':
    root = tk.Tk()  # starting tkinter window
    root.title("Car Controller Simulation")
    ico = Image.open('car.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
    background_image = tk.PhotoImage(file="dashboard_image.png")
    background_label = tk.Label(root, image=background_image)
    background_label.pack()
    background_label.lower()
    sim = Simulation()
    Thread(target=sim.run).start()  # running simulation function
    Thread(target=sim.gui).start()  # running gui funtion
    infoBtn = tk.Button(root, text="i", command=info, bg="blue", fg="white",font=('Times New Roman', 12))
    infoBtn.place(x=10, y=10)
    root.mainloop()
