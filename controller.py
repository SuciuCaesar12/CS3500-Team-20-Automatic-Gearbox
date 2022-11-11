class Controller:

    def __init__(self):

        self.gear = 0
        self.gear_mode = 'Park'
        self.drive_mode = 'ECO'
        self.states = ['Engine_Off', 'Engine_On', 'Gear_Park', 'Gear_Reverse', 'Gear_Neutral',
                       'Gear_1', 'Gear_2', 'Gear_3', 'Gear_4', 'Gear_5', 'Gear_6']
        self.current_state = 'Gear_Park'

        self.min_rpm = 0
        self.max_rpm = 2000

    def run(self):
        pass
