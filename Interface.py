import time
import random

from rich.live import Live
from rich.table import Table

class Interface():
    def __init__(self, bus):
        self.bus = bus

    def create_table(self):
        """
        Make a new table using the values in the bus.
        :return: table functioning as the user interface.
        """
        self.table = Table()
        self.table.add_column("RPM")
        self.table.add_column("SPEED")
        self.table.add_column("DRIVE MODE")
        self.table.add_column("GEAR MODE")
        self.table.add_column("GEAR")
        self.table.add_column("ENGINE ON")
        self.table.add_column("    WARNING MESSAGE    ")

        self.table.add_row(str(round(self.bus["rpm"], 1)),
                           str(round(self.bus["speed"], 1)),
                           ("[green]" + self.bus["drive_mode"]) if self.bus["drive_mode"] == "Eco" else ("[yellow]"+self.bus["drive_mode"]),
                           self.bus["gear_mode"],
                           str(self.bus["gear"]),
                           ("[green]" + str(self.bus["engine_on"]) if self.bus["engine_on"] else ("[red]"+str(self.bus["engine_on"]))),
                           "[red]"+self.bus["warning_message"])
        return self.table