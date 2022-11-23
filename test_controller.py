import unittest

from controller import Controller
from Gearbox import Gearbox


class UnitTestController(unittest.TestCase):

    def __init_bus_controller_gearbox(self):
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
        gearbox = Gearbox(bus=bus)
        return bus, controller, gearbox

    def __config_park_state(self):
        bus, controller, gearbox = self.__init_bus_controller_gearbox()

        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)
        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)  # change state in 'Gear_Park'

        return bus, controller, gearbox

    def __config_reverse_state(self):
        bus, controller, gearbox = self.__config_park_state()

        bus.update({'gear_mode': 'Reverse'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)  # change state in 'Gear_Reverse'
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        return bus, controller, gearbox

    def __config_neutral_state(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus.update({'gear_mode': 'Neutral'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)  # change state in 'Gear_Neutral'
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        return bus, controller, gearbox

    def __config_drive_state(self):
        bus, controller, gearbox = self.__config_neutral_state()

        bus.update({'gear_mode': 'Drive'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)  # change state in 'Gear_1'
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        return bus, controller, gearbox

    def test_path_1(self):
        bus, controller, gearbox = self.__init_bus_controller_gearbox()

        bus.update({'drive_mode': 'Eco'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)
        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)

        self.assertEqual(bus['engine_signal'], True)

    def test_path_2(self):
        bus, controller, gearbox = self.__init_bus_controller_gearbox()

        bus.update({'drive_mode': 'Eco'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(bus['engine_signal'], False)

    def test_path_3(self):
        bus, controller, gearbox = self.__config_park_state()

        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Idle')

    def test_path_4(self):
        bus, controller, gearbox = self.__config_park_state()

        bus.update({'gear_mode': 'Reverse'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Reverse')

    def test_path_5(self):
        bus, controller, gearbox = self.__config_park_state()

        bus.update({'gear_mode': 'Neutral'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Neutral')

    def test_path_6(self):
        bus, controller, gearbox = self.__config_park_state()

        bus.update({'gear_mode': 'Drive'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_7(self):
        bus, controller, gearbox = self.__config_park_state()

        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_8(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)

        self.assertEqual(bus['warning_message'], 'Please switch to Park')

    def test_path_9(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus.update({'gear_mode': 'Neutral'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Neutral')

    def test_path_10(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus.update({'gear_mode': 'Park',
                    'speed': 0})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_11(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus.update({'gear_mode': 'Park',
                    'speed': 10})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(bus['warning_message'], 'Car is not stationary!')

    def test_path_14(self):
        bus, controller, gearbox = self.__config_reverse_state()

        bus_copy = bus.copy()
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(bus, bus_copy)

    def test_path_15(self):
        bus, controller, gearbox = self.__config_neutral_state()

        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)

        self.assertEqual(bus['warning_message'], 'Please switch to Park.')

    def test_path_16(self):
        bus, controller, gearbox = self.__config_neutral_state()

        bus.update({'gear_mode': 'Drive'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_17(self):
        bus, controller, gearbox = self.__config_neutral_state()

        bus.update({'gear_mode': 'Park'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_18(self):
        bus, controller, gearbox = self.__config_neutral_state()

        bus_copy = bus.copy()
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(bus, bus_copy)

    def test_path_19(self):
        bus, controller, gearbox = self.__config_drive_state()

        bus, gearbox = controller.run(bus=bus, engine_button=True, gearbox=gearbox)

        self.assertEqual(bus['warning_message'], 'Please switch to Park.')

    def test_path_20(self):
        bus, controller, gearbox = self.__config_drive_state()

        bus.update({'gear_mode': 'Park',
                    "speed": 0})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Park')

    def test_path_21(self):
        bus, controller, gearbox = self.__config_drive_state()

        bus.update({'gear_mode': 'Park',
                    "speed": 10})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(bus['warning_message'], 'Car is not stationary!')

    def test_path_22(self):
        bus, controller, gearbox = self.__config_drive_state()

        bus.update({'gear_mode': 'Neutral'})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_Neutral')

    def test_path_23(self):
        bus, controller, gearbox = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 800})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_1')

    def test_path_24(self):
        bus, controller, gearbox = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 3000})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_3')

    def test_path_25(self):
        bus, controller, gearbox = self.__config_drive_state()

        controller.current_state = 'Gear_2'
        bus.update({'rpm': 2000})
        bus, gearbox = controller.run(bus=bus, engine_button=False, gearbox=gearbox)

        self.assertEqual(controller.current_state, 'Gear_2')
