class Controller:

    def __init__(self):

        self.STATES = ['Idle', 'Gear_Park', 'Gear_Reverse', 'Gear_Neutral',
                       'Gear_1', 'Gear_2', 'Gear_3', 'Gear_4', 'Gear_5', 'Gear_6']
        # initialize default states
        self.current_state = 'Idle'

        # default ECO thresholds
        self.MIN_RPM = 1000
        self.MAX_RPM = 3500

    def run(self, bus, engine_button):
        """
        Component which runs the entire logic of our system.
        :param bus: internal state values like RPM, Gear,...
        :param gear_mode: Park, Neutral, Reverse, Drive
        :param engine_button: True/False
        :param drive_mode: ECO, Sport
        :param speed: float32
        :return:
        """

        if bus['drive_mode'] == 'E':  # ---------- 1 #
            self.MIN_RPM, self.MAX_RPM = 1000, 2800  # ---------- 2 #
        else:
            self.MIN_RPM, self.MAX_RPM = 1000, 3500  # ---------- 3 #

        if self.current_state == 'Idle':  # ---------- 4 #
            if engine_button:  # ------------ 5 #
                # ------------------------------------------ 6 -- #
                self.current_state = 'Gear_Park'
                bus.update({'engine_signal': True,
                            'gear': 0,
                            'gear_mode': 'Park'})
                return bus
                # ------------------------------------------ 6 -- #

            # ------------------------------------------ 7 -- #
            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Park'})
            return bus
            # ------------------------------------------ 7 -- #

        if self.current_state == 'Gear_Park':  # ---------- 8 #
            if engine_button:  # ---------- 9 #
                # ------------------------------------------ 10 -- #
                self.current_state = 'Idle'
                bus.update({'engine_signal': True,
                            'gear': 0,
                            'gear_mode': 'Park'})
                return bus
                # ------------------------------------------ 10 -- #

            if bus['gear_mode'] == 'Reverse':  # ---------- 11 #
                # ------------------------------------------ 12 -- #
                self.current_state = 'Gear_Reverse'
                return bus
                # ------------------------------------------ 12 -- #

            if bus['gear_mode'] == 'Neutral':  # ---------- 13 #
                # ------------------------------------------ 14 -- #
                self.current_state = 'Gear_Neutral'
                return bus
                # ------------------------------------------ 14 -- #

            if bus['gear_mode'] == 'Drive':  # ---------- 15 #
                # ------------------------------------------ 16 -- #
                self.current_state = 'Gear_1'
                return bus
                # ------------------------------------------ 16 -- #

            # ------------------------------------------ 17 -- #
            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Park'})
            return bus
            # ------------------------------------------ 17 -- #

        if self.current_state == 'Gear_Reverse':  # ---------- 18 #
            if bus['gear_mode'] == 'Neutral':  # ---------- 19 #
                # ------------------------------------------ 20 -- #
                self.current_state = 'Gear_Neutral'
                return bus
                # ------------------------------------------ 20 -- #

            if bus['gear_mode'] == 'Park':  # ---------- 21 #
                if bus['speed'] == 0:  # ---------- 22 #
                    # ------------------------------------------ 23 -- #
                    self.current_state = 'Gear_Park'
                    # ------------------------------------------ 23 -- #
                else:
                    # ------------------------------------------ 24 -- #
                    bus.update({'warning_message': 'SPEED != 0'})
                    # ------------------------------------------ 24 -- #
                # ------------------------------------------ 25 -- #
                return bus
                # ------------------------------------------ 25 -- #

            # ------------------------------------------ 26 -- #
            bus.update({'engine_signal': False,
                        'gear': -1,
                        'gear_mode': 'Reverse'})
            return bus
            # ------------------------------------------ 26 -- #

        if self.current_state == 'Gear_Neutral':  # ---------- 27 #
            if bus['gear_mode'] == 'Drive':  # ---------- 28 #
                # ------------------------------------------ 29 -- #
                self.current_state = 'Gear_1'
                return bus
                # ------------------------------------------ 29 -- #

            if bus['gear_mode'] == 'Park':  # ---------- 30 #
                # ------------------------------------------ 31 -- #
                self.current_state = 'Gear_Park'
                return bus
                # ------------------------------------------ 31 -- #

            # ------------------------------------------ 32 -- #
            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Neutral'})
            return bus
            # ------------------------------------------ 32 -- #

        for gear_level in range(1, 7):  # ---------- 33 #
            if self.current_state == 'Gear_' + str(gear_level):  # ---------- 34 #
                if self.current_state != 'Gear_1':  # ---------- 35 #
                    if bus['rpm'] < self.MIN_RPM:  # ---------- 36 #
                        # ------------------------------------------ 37 -- #
                        self.current_state = 'Gear_' + str(gear_level - 1)
                        bus.update({'engine_signal': False,
                                    'gear': gear_level - 1,
                                    'gear_mode': 'Drive'})
                        return bus
                        # ------------------------------------------ 37 -- #
                if self.current_state != 'Gear_6':  # ---------- 38 #
                    if bus['rpm'] > self.MAX_RPM:  # ---------- 39 -- #
                        # ------------------------------------------ 40 -- #
                        self.current_state = 'Gear_' + str(gear_level + 1)
                        bus.update({'engine_signal': False,
                                    'gear': gear_level + 1,
                                    'gear_mode': 'Drive'})
                        return bus
                        # ------------------------------------------ 40 -- #

                # ------------------------------------------ 41 -- #
                bus.update({'engine_signal': False,
                            'gear': gear_level,
                            'gear_mode': 'Drive'})
                return bus
                # ------------------------------------------ 41 -- #
