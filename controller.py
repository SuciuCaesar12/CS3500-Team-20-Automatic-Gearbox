class Controller:

    def __init__(self):

        self.STATES = ['Idle', 'Gear_Park', 'Gear_Reverse', 'Gear_Neutral',
                       'Gear_1', 'Gear_2', 'Gear_3', 'Gear_4', 'Gear_5', 'Gear_6']
        # initialize default states
        self.current_state = 'Idle'

        # default ECO thresholds
        self.MIN_RPM = 1000
        self.MAX_RPM = 2800

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

        if bus['drive_mode'] == 'Eco':  # ---------- 1 #
            self.MIN_RPM, self.MAX_RPM = 1000, 2800  # ---------- 2 #
        else:
            self.MIN_RPM, self.MAX_RPM = 1000, 3500  # ---------- 3 #

        if self.current_state == 'Idle':  # ---------- 4 #
            if engine_button:  # ------------ 5 #
                # ------------------------------------------ 6 -- #
                self.current_state = 'Gear_Park'
                bus.update({'engine_signal': True})
                bus = gearbox.Change_Gear(bus, 0)
                bus = gearbox.Change_Gearmode(bus, 'Park')
                return bus, gearbox
                # ------------------------------------------ 6 -- #

            # ------------------------------------------ 7 -- #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, 'Park')
            return bus, gearbox
            # ------------------------------------------ 7 -- #

        if self.current_state == 'Gear_Park':  # ---------- 8 #
            if engine_button:  # ---------- 9 #
                # ------------------------------------------ 10 -- #
                self.current_state = 'Idle'
                bus.update({'engine_signal': True})
                bus = gearbox.Change_Gear(bus, 0)
                bus = gearbox.Change_Gearmode(bus, 'Park')
                return bus, gearbox
                # ------------------------------------------ 10 -- #

            if bus['gear_mode'] == 'Reverse':  # ---------- 11 #
                # ------------------------------------------ 12 -- #
                self.current_state = 'Gear_Reverse'
                return bus, gearbox
                # ------------------------------------------ 12 -- #

            if bus['gear_mode'] == 'Neutral':  # ---------- 13 #
                # ------------------------------------------ 14 -- #
                self.current_state = 'Gear_Neutral'
                return bus, gearbox
                # ------------------------------------------ 14 -- #

            if bus['gear_mode'] == 'Drive':  # ---------- 15 #
                # ------------------------------------------ 16 -- #
                self.current_state = 'Gear_1'
                return bus, gearbox
                # ------------------------------------------ 16 -- #

            # ------------------------------------------ 17 -- #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, 'Park')
            return bus, gearbox
            # ------------------------------------------ 17 -- #

        if self.current_state == 'Gear_Reverse':  # ---------- 18 #
            if engine_button:  # ---------- 19 #
                # ------------------------------------------ 20 -- #
                bus.update({'warning_message': 'Please switch to Park',
                            'warning_time': 1000})
                return bus, gearbox
                # ------------------------------------------ 20 -- #

            if bus['gear_mode'] == 'Neutral':  # ---------- 21 #
                # ------------------------------------------ 22 -- #
                self.current_state = 'Gear_Neutral'
                return bus, gearbox
                # ------------------------------------------ 22 -- #

            if bus['gear_mode'] == 'Park':  # ---------- 23 #
                if bus['speed'] == 0:  # ---------- 24 #
                    # ------------------------------------------ 25 -- #
                    self.current_state = 'Gear_Park'
                    # ------------------------------------------ 25 -- #
                else:
                    # ------------------------------------------ 26 -- #
                    bus = gearbox.Change_Gear(bus, -1)
                    bus = gearbox.Change_Gearmode(bus, 'Reverse')
                    bus.update({'warning_message': 'Car is not stationary!',
                                'warning_time': 1000})
                    # ------------------------------------------ 26 -- #
                # ------------------------------------------ 27 -- #
                return bus, gearbox
                # ------------------------------------------ 27 -- #

            # ------------------------------------------ 28 -- #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, -1)
            bus = gearbox.Change_Gearmode(bus, 'Reverse')
            return bus, gearbox
            # ------------------------------------------ 28 -- #

        if self.current_state == 'Gear_Neutral':  # ---------- 29 #
            if engine_button:  # ---------- 30 #
                # ------------------------------------------ 31 -- #
                bus.update({'warning_message': 'Please switch to Park.',
                            'warning_time': 1000})
                return bus, gearbox
                # ------------------------------------------ 31 -- #

            if bus['gear_mode'] == 'Drive':  # ---------- 32 #
                # ------------------------------------------ 33 -- #
                self.current_state = 'Gear_1'
                return bus, gearbox
                # ------------------------------------------ 33 -- #

            if bus['gear_mode'] == 'Park':  # ---------- 34 #
                # ------------------------------------------ 35 -- #
                self.current_state = 'Gear_Park'
                return bus, gearbox
                # ------------------------------------------ 35 -- #

            # ------------------------------------------ 36 -- #
            bus.update({'engine_signal': False})
            bus = gearbox.Change_Gear(bus, 0)
            bus = gearbox.Change_Gearmode(bus, 'Neutral')
            return bus, gearbox
            # ------------------------------------------ 36 -- #

        for gear_level in range(1, 7):  # ---------- 37 #
            if self.current_state == 'Gear_' + str(gear_level):  # ---------- 38 #
                if engine_button:  # ---------- 39 #
                    # ------------------------------------------ 40 -- #
                    bus.update({'warning_message': 'Please switch to Park.',
                                'warning_time': 1000})
                    return bus, gearbox
                    # ------------------------------------------ 40 -- #

                if bus['gear_mode'] == 'Park':  # ---------- 41 #
                    if bus['speed'] == 0:  # ---------- 42 #
                        # ------------------------------------------ 43 -- #
                        self.current_state = 'Gear_Park'
                        return bus, gearbox
                        # ------------------------------------------ 43 -- #
                    else:
                        # ------------------------------------------ 44 -- #
                        bus.update({'engine_signal': False,
                                    'warning_message': 'Car is not stationary!',
                                    'warning_time': 1000})
                        bus = gearbox.Change_Gear(bus, gear_level)
                        bus = gearbox.Change_Gearmode(bus, 'Drive')
                        return bus, gearbox
                        # ------------------------------------------ 44 -- #

                if bus['gear_mode'] == 'Neutral':  # ---------- 45 #
                    # ------------------------------------------ 46 -- #
                    self.current_state = 'Gear_Neutral'
                    bus.update({'engine_signal': False})
                    bus = gearbox.Change_Gear(bus, 0)
                    bus = gearbox.Change_Gearmode(bus, 'Neutral')
                    return bus, gearbox
                    # ------------------------------------------ 46 -- #

                if self.current_state != 'Gear_1':  # ---------- 47 #
                    if bus['rpm'] < self.MIN_RPM:  # ---------- 48 #
                        # ------------------------------------------ 49 -- #
                        self.current_state = 'Gear_' + str(gear_level - 1)
                        bus.update({'engine_signal': False})
                        bus = gearbox.Change_Gear(bus, gear_level - 1)
                        bus = gearbox.Change_Gearmode(bus, 'Drive')
                        return bus, gearbox
                        # ------------------------------------------ 49 -- #
                if self.current_state != 'Gear_6':  # ---------- 50 #
                    if bus['rpm'] > self.MAX_RPM:  # ---------- 51 -- #
                        # ------------------------------------------ 52 -- #
                        self.current_state = 'Gear_' + str(gear_level + 1)
                        bus.update({'engine_signal': False})
                        bus = gearbox.Change_Gear(bus, gear_level + 1)
                        bus = gearbox.Change_Gearmode(bus, 'Drive')
                        return bus, gearbox
                        # ------------------------------------------ 52 -- #

                # ------------------------------------------ 53 -- #
                bus.update({'engine_signal': False})
                bus = gearbox.Change_Gear(bus, gear_level)
                bus = gearbox.Change_Gearmode(bus, 'Drive')
                return bus, gearbox
                # ------------------------------------------ 53 -- #
