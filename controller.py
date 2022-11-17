class Controller:

    def __init__(self):

        self.STATES = ['Idle', 'Gear_Park', 'Gear_Reverse', 'Gear_Neutral',
                       'Gear_1', 'Gear_2', 'Gear_3', 'Gear_4', 'Gear_5', 'Gear_6']
        # initialize default states
        self.current_state = 'Idle'

        # default ECO thresholds
        self.MIN_4_6_RPM = 1000
        self.MAX_4_6_RPM = 3500

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

        if bus['drive_mode'] == 'E':
            # self.MIN_1_3_RPM, self.MAX_1_3_RPM = 1000, 2200
            self.MIN_4_6_RPM, self.MAX_4_6_RPM = 1000, 2800
        else:
            # self.MIN_1_3_RPM, self.MAX_1_3_RPM = 1000, 3000
            self.MIN_4_6_RPM, self.MAX_4_6_RPM = 1000, 3500

        if self.current_state == 'Idle':
            if engine_button:
                self.current_state = 'Gear_Park'
                bus.update({'engine_signal': True,
                            'gear': 0,
                            'gear_mode': 'Park'})
                return bus

            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Park'})
            return bus

        if self.current_state == 'Gear_Park':
            if engine_button:
                self.current_state = 'Idle'
                bus.update({'engine_signal': True,
                            'gear': 0,
                            'gear_mode': 'Park'})
                return bus

            if bus['gear_mode'] == 'Reverse':
                self.current_state = 'Gear_Reverse'
                return bus

            if bus['gear_mode'] == 'Neutral':
                self.current_state = 'Gear_Neutral'
                return bus

            if bus['gear_mode'] == 'Drive':
                self.current_state = 'Gear_1'
                return bus

            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Park'})
            return bus

        if self.current_state == 'Gear_Reverse':
            if bus['gear_mode'] == 'Neutral':
                self.current_state = 'Gear_Neutral'
                return bus

            if bus['gear_mode'] == 'Park':
                if bus['speed'] == 0:
                    self.current_state = 'Gear_Park'
                else:
                    bus.update({'warning_message': 'SPEED != 0'})
                return bus

            bus.update({'engine_signal': False,
                        'gear': -1,
                        'gear_mode': 'Reverse'})
            return bus

        if self.current_state == 'Gear_Neutral':
            if bus['gear_mode'] == 'Drive':
                self.current_state = 'Gear_1'
                return bus

            if bus['gear_mode'] == 'Park':
                self.current_state = 'Gear_Park'
                return bus

            bus.update({'engine_signal': False,
                        'gear': 0,
                        'gear_mode': 'Neutral'})
            return bus

        if self.current_state == 'Gear_1':
            if bus['gear_mode'] == 'Park':
                if bus['speed'] == 0:
                    self.current_state = 'Gear_Park'
                else:
                    bus.update({'warning_message': 'SPEED != 0'})
                return bus

            if bus['gear_mode'] == 'Neutral':
                self.current_state = 'Gear_Neutral'
                return bus

            if bus['rpm'] > self.MAX_4_6_RPM:
                self.current_state = 'Gear_2'
                bus.update({'engine_signal': False,
                            'gear': 2,
                            'gear_mode': 'Drive'})
                return bus

            bus.update({'engine_signal': False,
                        'gear': 1,
                        'gear_mode': 'Drive'})
            return bus

        for gear_level in range(2, 6):
            if self.current_state == 'Gear_' + str(gear_level):
                if bus['rpm'] < self.MIN_4_6_RPM:
                    self.current_state = 'Gear_' + str(gear_level - 1)
                    bus.update({'engine_signal': False,
                                'gear': gear_level - 1,
                                'gear_mode': 'Drive'})
                    return bus
                if bus['rpm'] > self.MAX_4_6_RPM:
                    self.current_state = 'Gear_' + str(gear_level + 1)
                    bus.update({'engine_signal': False,
                                'gear': gear_level + 1,
                                'gear_mode': 'Drive'})
                    return bus

                bus.update({'engine_signal': False,
                            'gear': gear_level,
                            'gear_mode': 'Drive'})
                return bus

        if self.current_state == 'Gear_6':
            if bus['rpm'] < self.MIN_4_6_RPM:
                self.current_state = 'Gear_5'
                bus.update({'engine_signal': False,
                            'gear': 5,
                            'gear_mode': 'Drive'})
                return bus

            bus.update({'engine_signal': False,
                        'gear': 6,
                        'gear_mode': 'Drive'})
            return bus
