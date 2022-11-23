class Gearbox:
    def __init__(self, bus):
        self.Gear = bus["gear"]
        self.Gearmode = bus["gear_mode"]

    def Change_Gear(self, bus, new_Gear):
        """
        Update the Gear in the internal logic of the Gearbox.
        :param bus: internal state values like RPM, Speed, ...
        :param new_Gear: Gear the Gearbox should switch to.
        :return: updated bus.3
        """
        self.Gear = new_Gear
        bus["gear"] = self.Gear
        return bus

    def Change_Gearmode(self, bus, new_Gearmode):
        """
        Update the Gear Mode in the internal logic of the Gearbox.
        :param bus: internal state values like RPM, Speed, ...
        :param new_Gearmode: Gear Mode the Gearbox should switch to.
        :return: updated bus.
        """
        self.Gearmode = new_Gearmode
        bus["gear_mode"] = self.Gearmode
        return bus