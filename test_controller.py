import unittest

from controller import Controller


class UnitTestController(unittest.TestCase):

    def __init_bus_controller(self):
        bus = {
            "rpm": 0,
            "speed": 0,
            "engine_signal": False,
            "gear_mode": "Park",
            "drive_mode": "Eco",
            "gear": 0,
            'warning_message': ''
        }
        controller = Controller()
        return bus, controller

    def __config_park_state(self):
        bus, controller = self.__init_bus_controller()

        bus = controller.run(bus=bus, engine_button=False)
        bus = controller.run(bus=bus, engine_button=True)  # change state in 'Gear_Park'

        return bus, controller

    def __config_reverse_state(self):
        bus, controller = self.__config_park_state()

        bus.update({'gear_mode': 'Reverse'})
        bus = controller.run(bus=bus, engine_button=False)  # change state in 'Gear_Reverse'
        bus = controller.run(bus=bus, engine_button=False)

        return bus, controller

    def __config_neutral_state(self):
        bus, controller = self.__config_reverse_state()

        bus.update({'gear_mode': 'Neutral'})
        bus = controller.run(bus=bus, engine_button=False)  # change state in 'Gear_Neutral'
        bus = controller.run(bus=bus, engine_button=False)

        return bus, controller

    def __config_drive_state(self):
        bus, controller = self.__config_neutral_state()

        bus.update({'gear_mode': 'Drive'})
        bus = controller.run(bus=bus, engine_button=False)  # change state in 'Gear_1'
        bus = controller.run(bus=bus, engine_button=False)

        return bus, controller

    def test_path_1(self):
        bus, controller = self.__init_bus_controller()

        bus.update({'drive_mode': 'Eco'})
        bus = controller.run(bus=bus, engine_button=False)
        bus = controller.run(bus=bus, engine_button=True)

        self.assertEqual(bus['engine_signal'], True)

    def test_path_2(self):
        bus, controller = self.__init_bus_controller()

        bus.update({'drive_mode': 'Eco'})
        bus = controller.run(bus=bus, engine_button=False)
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(bus['engine_signal'], False)

    def test_path_3(self):
        bus, controller = self.__config_park_state()

        bus = controller.run(bus=bus, engine_button=True)

        self.assertEqual(bus['engine_signal'], True)

    def test_path_4(self):
        bus, controller = self.__config_park_state()

        bus.update({'gear_mode': 'Reverse'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Reverse')

    def test_path_5(self):
        bus, controller = self.__config_park_state()

        bus.update({'gear_mode': 'Neutral'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Neutral')

    def test_path_6(self):
        bus, controller = self.__config_park_state()

        bus.update({'gear_mode': 'Drive'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_7(self):
        bus, controller = self.__config_park_state()

        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_8(self):
        bus, controller = self.__config_reverse_state()

        bus.update({'gear_mode': 'Neutral'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Neutral')

    def test_path_9(self):
        bus, controller = self.__config_reverse_state()

        bus.update({'gear_mode': 'Park',
                    'speed': 0})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_10(self):
        bus, controller = self.__config_reverse_state()

        bus.update({'gear_mode': 'Park',
                    'speed': 10})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(bus['warning_message'], 'SPEED != 0')

    def test_path_12(self):
        bus, controller = self.__config_reverse_state()

        bus_copy = bus.copy()
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(bus, bus_copy)

    def test_path_13(self):
        bus, controller = self.__config_neutral_state()

        bus.update({'gear_mode': 'Drive'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_14(self):
        bus, controller = self.__config_neutral_state()

        bus.update({'gear_mode': 'Park'})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_15(self):
        bus, controller = self.__config_neutral_state()

        bus_copy = bus.copy()
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(bus, bus_copy)

    def test_path_17(self):
        bus, controller = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 800})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_18(self):
        bus, controller = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 3000})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_3')

    def test_path_19(self):
        bus, controller = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 2000})
        bus = controller.run(bus=bus, engine_button=False)

        self.assertEqual(controller.current_state, 'Gear_2')
