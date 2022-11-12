class Gearbox:
    def __init__(self, bus):
        self.Gear = bus["gear"]
        self.Gearmode = bus["gear_mode"]

    def Change_Gear(self, bus, new_Gear):
        self.Gear = new_Gear
        bus["gear"] = self.Gear
        return bus

    def Change_Gearmode(self, bus, new_Gearmode):
        self.Gearmode = new_Gearmode
        bus["gear_mode"] = self.Gearmode
        return bus