class Engine:
    def __init__(self):
        self.RPM = 0
        self.current_gear = 0
        self.Engine_On = False

    def run(self, bus, gas):
        if bus["engine_signal"]:
            self.Engine_On = not self.Engine_On

        if self.Engine_On:
            if gas:
                if bus['gear'] == 0:
                    self.RPM += 0.1 / (1 + 1e-6)  # is gonna be gear once the controller is involved
                else:
                    self.RPM += 0.1 / (abs(bus['gear']) + 1e-6)
            else:
                self.RPM -= 0.02

            if bus['gear'] == -1 and self.current_gear == 0 or (self.current_gear == -1 and bus['gear'] == 0):
                self.RPM = 0
            else:
                if bus['gear'] > self.current_gear:
                    if self.current_gear == 0:
                        self.RPM = 0
                    else:
                        self.RPM = 1500
                if bus['gear'] < self.current_gear:
                    if bus['gear'] == 0:
                        self.RPM = 0
                    else:
                        self.RPM = 2000
            self.current_gear = bus['gear']

            if self.RPM < 0:
                self.RPM = 0
            if self.RPM > 4500:
                self.RPM = 4500
        else:
            self.RPM = 0

        bus["rpm"] = self.RPM
        return bus
