class Controller:

    def __init__(self):

        self.STATES = ['Idle', 'Gear_Park', 'Gear_Reverse', 'Gear_Neutral',
                       'Gear_1', 'Gear_2', 'Gear_3', 'Gear_4', 'Gear_5', 'Gear_6']
        # Initialize default states
        self.current_state = 'Idle'

    def run(self, bus, engine_button, gearbox):
        """
        Component which runs the entire logic of our system.
        :param bus: internal state values like RPM, Gear,...
        :param gear_mode: Park, Neutral, Reverse, Drive
        :param engine_button: True/False
        :param drive_mode: ECO, Sport
        :param speed: float32
        :return:
        """

        if bus['drive_mode'] == 'Eco': #-------- 1 #
            self.MIN_RPM, self.MAX_RPM = 1000, 2800 #-------- 2 #
        else:
            self.MIN_RPM, self.MAX_RPM = 1000, 3500 #-------- 3 #

        if self.current_state == 'Idle': #-------- 4 #
            if engine_button: #-------- 5 #
                # -------------------------------------------6 #
                self.current_state = 'Gear_Park'

                bus.update({'engine_signal': True})
                bus = gearbox.Change_Gear(bus, 0)
                bus = gearbox.Change_Gearmode(bus, "Park")
                return bus, gearbox
                #--------------------------------------------6 #

            #---------------------------------------------7 #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, "Park")
            return bus, gearbox
            #---------------------------------------------7 #

        if self.current_state == 'Gear_Park': #-------- 8 #
            if engine_button: #-------- 9 #
                #-------------------------------------- 10 #
                self.current_state = 'Idle'
                bus.update({'engine_signal': True})
                bus = gearbox.Change_Gear(bus, 0)
                bus = gearbox.Change_Gearmode(bus, "Park")
                return bus, gearbox
                #------------------------------------- 10 #

            if bus["gear_mode"] == 'Reverse': #-------- 11 #
                #-------------------------------------- 12 #
                self.current_state = 'Gear_Reverse'
                return bus, gearbox
                #-------------------------------------- 12 #

            if bus["gear_mode"] == 'Neutral': #-------- 13 #
                #-------------------------------------- 14 #
                self.current_state = 'Gear_Neutral'
                return bus, gearbox
                #------------------------------------- 14 #

            if bus["gear_mode"] == 'Drive': #-------- 15 #
                #------------------------------------ 16 #
                self.current_state = 'Gear_1'
                return bus, gearbox
                #------------------------------------ 16 #

            #---------------------------------------- 17 #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, "Park")
            return bus, gearbox
            #---------------------------------------- 17 #

        if self.current_state == 'Gear_Reverse': #-------- 18 #
            if engine_button: #Added after CFG was made, but not enough time to revamp the whole graph and all the paths.
                bus.update({'warning_message': 'Please switch to Park.',
                            'warning_time': 1000})
                return bus, gearbox

            if bus["gear_mode"] == 'Neutral': #-------- 19 #
                #-------------------------------------- 20 #
                self.current_state = 'Gear_Neutral'
                return bus, gearbox
                #-------------------------------------- 20 #

            if bus["gear_mode"] == 'Park': #-------- 21
                if bus['speed'] == 0: #-------- 22 #
                    #-------------------------------- 23 #
                    self.current_state = 'Gear_Park'
                    #-------------------------------- 23 #
                else:
                    #---------------------------------24 #
                    bus = gearbox.Change_Gearmode(bus, "Reverse")
                    bus.update({'warning_message': 'Car is not stationary!',
                                'warning_time': 1000})
                    #---------------------------------24 #
                return bus, gearbox #----------- 25

            #--------------------------------------- 26 #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, -1)
            bus = gearbox.Change_Gearmode(bus, "Reverse")
            return bus, gearbox
            # -------------------------------------- 26 #

        if self.current_state == 'Gear_Neutral': #-------- 27#
            if engine_button: #Also added after CFG was made, same story.
                bus.update({'warning_message': 'Please switch to Park.',
                            'warning_time': 1000})
                return bus, gearbox

            if bus["gear_mode"] == 'Drive': #-------- 28 #
                #------------------------------------ 29 #
                self.current_state = 'Gear_1'
                return bus, gearbox
                #------------------------------------ 29 #

            if bus["gear_mode"] == 'Park': #-------- 30 #
                #----------------------------------- 31 #
                self.current_state = 'Gear_Park'
                return bus, gearbox
                #----------------------------------- 31 #

            #--------------------------------------- 32 #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, "Neutral")
            return bus, gearbox
            #--------------------------------------- 32 #

        if self.current_state == 'Gear_1': #-------- 33 #
            if engine_button: #Added after CFG was made...
                bus.update({'warning_message': 'Please switch to Park.',
                            'warning_time': 1000})
                return bus, gearbox

            if bus["gear_mode"] == 'Park': #-------- 34 #
                if bus['speed'] == 0: #-------- 35
                    self.current_state = 'Gear_Park' #-------- 36#
                else:
                    #----------------------------------------- 37 #
                    bus = gearbox.Change_Gearmode(bus, "Drive")
                    bus.update({'warning_message': 'Car is not stationary!',
                                'warning_time': 1000})
                    #----------------------------------------- 37 #
                return bus, gearbox #-------- 38 #

            if bus["gear_mode"] == 'Neutral': #-------- 39 #
                #-------------------------------------- 40 #
                self.current_state = 'Gear_Neutral'
                return bus, gearbox
                #-------------------------------------- 40 #

            if bus['rpm'] > self.MAX_RPM: #-------- 41 #
                #---------------------------------- 42 #
                self.current_state = 'Gear_2'
                bus.update({'engine_signal': False})
                bus = gearbox.Change_Gear(bus, 2)
                bus = gearbox.Change_Gearmode(bus, "Drive")
                return bus, gearbox
                #---------------------------------- 43 #

            #-------------------------------------- 44 $
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 1)
            bus = gearbox.Change_Gearmode(bus, "Drive")
            return bus, gearbox
            #-------------------------------------- 44 #

        for gear_level in range(2, 6): #-------- 45 #
            if self.current_state == 'Gear_' + str(gear_level): #-------- 46 #
                if engine_button: #Added after CFG was made
                    bus.update({'warning_message': 'Please switch to Park.',
                                'warning_time': 1000})
                    return bus, gearbox

                if bus['rpm'] < self.MIN_RPM: #-------- 47 #
                    #----------------------------------- 48 #
                    self.current_state = 'Gear_' + str(gear_level - 1)
                    bus.update({'engine_signal': False})
                    bus = gearbox.Change_Gear(bus, gear_level - 1)
                    bus = gearbox.Change_Gearmode(bus, "Drive")
                    return bus, gearbox
                    #---------------------------------- 48 #


                if bus['rpm'] > self.MAX_RPM: #-------- 49 #
                    #------------------------------------- 50 #
                    self.current_state = 'Gear_' + str(gear_level + 1)
                    bus.update({'engine_signal': False})
                    bus = gearbox.Change_Gear(bus, gear_level + 1)
                    bus = gearbox.Change_Gearmode(bus, "Drive")
                    return bus, gearbox
                    #------------------------------------- 50 #

                if bus["gear_mode"] == "Park": #Added after CFG was made
                    bus.update({'warning_message': 'Car is not stationary!',
                                'warning_time': 1000})

                #----------------------------------------- 51 #
                bus.update({'engine_signal': False})
                bus = gearbox.Change_Gear(bus, gear_level)
                bus = gearbox.Change_Gearmode(bus, "Drive")
                return bus, gearbox
                #----------------------------------------- 51 #

        if self.current_state == 'Gear_6': #-------- 52 #
            if bus['rpm'] < self.MIN_RPM: #-------- 53 #
                #---------------------------------- 54 #
                self.current_state = 'Gear_5'
                bus.update({'engine_signal': False})
                bus = gearbox.Change_Gear(bus, 5)
                bus = gearbox.Change_Gearmode(bus, "Drive")
                return bus, gearbox
                #---------------------------------- 54 #

            if bus["gear_mode"] == "Park": #Added after CFG was made
                bus.update({'warning_message': 'Car is not stationary!',
                            'warning_time': 1000})

            #------------------------------------- 55 #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 6)
            bus = gearbox.Change_Gearmode(bus, "Drive")
            return bus, gearbox
            #------------------------------------- 55 #