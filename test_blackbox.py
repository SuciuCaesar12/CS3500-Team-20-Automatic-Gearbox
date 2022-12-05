import unittest
from Simulation import  Simulation


class BlackboxTestController(unittest.TestCase):

    def test_turn_on_engine(self):
        """
        Test if the engine starts if the engine_button is pressed
        and if the default gear_mode is 'Park'
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()

        self.assertEqual(simulation.bus['engine_on'], True)

    def test_turn_off_engine(self):
        """
        Test if the engine stops if the engine_button is pressed while the engine is running
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.engine_button = True
        simulation.run()

        self.assertEqual(simulation.bus['engine_on'], False)

    def test_stop_engine_not_park_mode(self):
        """
        Test a safety feature.
        Engine should be turned off only when we are gear_mode is 'Park'.
        Check if the warning message is generated when we attempt to turn off the engine when gear_mode is 'Reverse'.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.bus["gear_mode"] = "Reverse"
        simulation.run()
        simulation.engine_button = True
        simulation.run()

        self.assertEqual(simulation.bus['warning_message'], 'Please switch to Park')

    def test_max_rpm_engine(self):
        """
        Test that the RPM can't go higher than 4500 even though the gas is still pressed
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.controller.current_state = 'Gear_6'
        simulation.bus['rpm'] = 1200
        simulation.bus['gear'] = 6
        simulation.run()
        # ... gas gas gas
        simulation.bus['rpm'] = 4499.9
        for i in range(15):
            simulation.gas = True
            simulation.run()

        self.assertEqual(simulation.bus['rpm'], 4500)

    def test_max_speed(self):
        """
        Test that the speed can't be higher than 134.4 even though the gas is still pressed.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.controller.current_state = 'Gear_6'
        simulation.bus['rpm'] = 1200
        simulation.bus['gear'] = 6
        simulation.run()
        # ... gas gas gas
        simulation.bus['rpm'] = 4499.9
        for i in range(15):
            simulation.gas = True
            simulation.run()

        self.assertEqual(round(simulation.bus['speed'], 1), 134.4)

    def test_max_speed_reverse(self):
        """
        Test that the maximum absolut speed in Reverse mode is 22.4 even though the gas is still pressed.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Reverse"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.controller.current_state = 'Gear_Reverse'
        simulation.bus['rpm'] = 1200
        simulation.bus['gear'] = -1
        simulation.run()
        # ... gas gas gas
        simulation.bus['rpm'] = 4499.9
        for i in range(15):
            simulation.gas = True
            simulation.run()

        self.assertEqual(round(simulation.bus['speed'], 1), -22.4)

    def test_acceleration(self):
        """
        Test if the rpm goes up when the gas is pressed
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()

        self.assertTrue(simulation.bus['rpm'] > 0)

    def test_deceleration(self):
        """
        Test if the rpm goes down when the gas is not pressed
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(10):
            simulation.gas = True
            simulation.run()
        rpm = simulation.bus['rpm']

        for i in range(5):
            simulation.gas = False
            simulation.run()

        self.assertTrue(simulation.bus['rpm'] < rpm)

    def test_non_negative_rpm(self):
        """
        Test that the rpm cannot be a negative value
        We accelerate for a few iterations, and we let the car slow down by itself
        We check if the RPM goes to 0 or below it
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        for i in range(10):
            simulation.gas = False
            simulation.run()

        self.assertEqual(simulation.bus['rpm'], 0)

    def test_set_park_mode_not_stationary(self):
        """
        Test a safety feature.
        We should switch to gear_mode 'Park' only when the speed is 0
        """
        simulation = Simulation()
        simulation.run()

        simulation.engine_button = True
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()

        simulation.bus["gear_mode"] = "Park"
        simulation.run()

        self.assertEqual(simulation.bus['warning_message'], 'Car is not stationary!')

    def test_select_mode_1(self):
        """
        Test switching drive_mode from 'Eco' to 'Sport'
        """
        simulation = Simulation()
        simulation.run()

        simulation.bus['drive_mode'] = 'Sport'
        simulation.run()

        self.assertEqual((simulation.controller.MIN_RPM, simulation.controller.MAX_RPM),
                         (1000, 3500))

    def test_select_mode_2(self):
        """
        Test switching drive_mode from 'Sport' to 'Eco'
        """
        simulation = Simulation()
        simulation.run()

        simulation.bus['drive_mode'] = 'Sport'
        simulation.run()
        simulation.bus['drive_mode'] = 'Eco'
        simulation.run()

        self.assertEqual((simulation.controller.MIN_RPM, simulation.controller.MAX_RPM),
                         (1000, 2800))

    def test_gear_increment_sport_mode(self):
        """
        Test if the controller increments the gear level when the current RPM is above the threshold
        associated to 'Sport' drive_mode.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.bus['drive_mode'] = 'Sport'
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.bus['rpm'] = 3500
        for i in range(5):
            simulation.gas = True
            simulation.run()

        self.assertEqual(simulation.bus['gear'], 2)

    def test_gear_increment_eco_mode(self):
        """
        Test if the controller increments the gear level when the current RPM is above the threshold
        associated to 'Eco' drive_mode.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.bus['drive_mode'] = 'Eco'
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.bus['rpm'] = 2800
        for i in range(5):
            simulation.gas = True
            simulation.run()

        self.assertEqual(simulation.bus['gear'], 2)

    def test_gear_decrement(self):
        """
        Test if the controller decrements the gear level when the current RPM is below the MIN threshold.
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.bus['drive_mode'] = 'Sport'
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.controller.current_state = 'Gear_2'
        simulation.bus['rpm'] = 1200
        simulation.bus['gear'] = 2
        simulation.run()
        # ...  rpm decreases
        simulation.bus['rpm'] = 1000
        for i in range(10):
            simulation.gas = False
            simulation.run()

        self.assertEqual(simulation.bus['gear'], 1)

    def test_consistent_gear(self):
        """
        Test if the gear remains constant if the current rpm is in the range
        of [MIN_RPM, MAX_RPM]
        """
        simulation = Simulation()
        CURRENT_GEAR = 4

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()

        for i in range(5):
            simulation.gas = True
            simulation.run()
        # ... gas gas gas
        simulation.controller.current_state = 'Gear_' + str(CURRENT_GEAR)
        simulation.bus['rpm'] = 1200
        simulation.bus['gear'] = CURRENT_GEAR
        simulation.run()

        for i in range(5):
            simulation.gas = False
            simulation.run()

        self.assertEqual(simulation.bus['gear'], CURRENT_GEAR)


    def test_bus_update(self):
        """
        Test if the bus gets updated at each iteration
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()
        simulation.bus["gear_mode"] = "Drive"
        simulation.run()
        simulation.run()

        bus = {
            "rpm": 0,
            "speed": 0,
            "engine_signal": False,
            "engine_on": True,
            "gear_mode": "Drive",
            "drive_mode": "Eco",
            "gear": 1,
            "warning_message": '',
            "warning_time": -4
        }

        self.assertEqual(simulation.bus, bus)

    def test_switch_neutral_park(self):
        """
        Test that the controller can switch from Neutral to Park
        Test an invalid case
        """
        simulation = Simulation()

        simulation.engine_button = True
        simulation.run()
        simulation.run()

        simulation.bus["gear_mode"] = "Neutral"
        simulation.run()
        simulation.run()

        simulation.bus["gear_mode"] = "Reverse"
        simulation.run()
        simulation.run()

        self.assertEqual(simulation.bus['gear_mode'], 'Neutral')

