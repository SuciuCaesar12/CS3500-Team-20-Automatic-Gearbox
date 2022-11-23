class Engine:
    def __init__(self):
        self.RPM = 0
        self.current_gear = 0
        self.Engine_On = False

    def run(self, bus, gas):
        """
        Calculate the new RPM based on the values in the bus.
        :param bus: internal state values like RPM, Speed, ...
        :param gas: bool whether the user pressed the gas.
        :return: bus with updated value for RPM.
        """

        if bus["engine_signal"]: #1
            self.Engine_On = not self.Engine_On
            bus["engine_on"] = self.Engine_On
            #----------------------------------2

        if self.Engine_On: #3
            if gas: #4
                if bus['gear'] == 0 and bus["gear_mode"] != "Park": #5
                    self.RPM += 0.1 / (1 + 1e-6)  # 6
                elif bus["gear_mode"] == "Park":
                    #In Park mode it should not be possible to give gas to the Engine.
                    self.RPM = 0
                else:
                    self.RPM += 0.1 / (abs(bus['gear']) + 1e-6) #7
            #If the Driver does not press the gas, the RPM should decrease
            else:
                self.RPM -= 0.1 #8

            #When switching down to Gear -1 from Gear 0 or up to Gear 0 from -1, the RPM should stay 0
            if bus['gear'] == -1 and self.current_gear == 0 or (self.current_gear == -1 and bus['gear'] == 0): #9
                self.RPM = 0 #10

            #In all other cases of switching up or down except when in Gear 0, the RPM is set to a realistic 'starter' value.
            else:
                if bus['gear'] > self.current_gear: #11
                    if self.current_gear == 0: #12
                        self.RPM = 0 #13
                    else:
                        self.RPM = 1500 #14
                if bus['gear'] < self.current_gear: #15
                    if bus['gear'] == 0: #16
                        self.RPM = 0 #17
                    else:
                        self.RPM = 2000 #18
            self.current_gear = bus['gear'] #19

            #RPM cannot be negative.
            if self.RPM < 0: #20
                self.RPM = 0 #21

            #We cap the RPM at 4500
            if self.RPM > 4500: #22
                self.RPM = 4500 #23

        #If the Engine is off, the RPM should always be 0.
        else:
            self.RPM = 0 #24

        #Update and return the bus.
        bus["rpm"] = self.RPM
        return bus
    #-----------------------25
