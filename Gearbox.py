#Add in type assertions to make sure input is of proper type? --> maybe not, only in Driver input since all the input for this class will come from Controller
#And we define these in/outputs.

class Gearbox:
    def __init__(self, Gearmode):
        self.Gear = 0
        self.Gearmode = Gearmode

    def Change_Gear(self, new_Gear):
        self.Gear = new_Gear
        return "OK"

    def Change_Gearmode(self, new_Gearmode):
        self.Gearmode = new_Gearmode
        return "OK"