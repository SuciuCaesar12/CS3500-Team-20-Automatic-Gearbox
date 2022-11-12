class Engine:
    def __init__(self):
        self.RPM = 0
        self.Engine_On = False

    def run(self, bus, gas):
        if bus["engine_signal"]:
            self.Engine_On = not self.Engine_On

        if self.Engine_On:
            if gas:
                self.RPM += 0.1 / 1  # is gonna be gear once the controller is involved
            else:
                self.RPM -= 0.05
        else:
            self.RPM = 0
        bus["rpm"] = self.RPM
        return bus
