import unittest
import Speedometer as Spd

class SpeedometerTest(unittest.TestCase):
    def setUp(self):
        self.Speedometer = Spd.Speedometer()
        self.bus = {
            "rpm": 0,
            "speed": 0,
            "engine_signal": False,
            "engine_on": False,
            "gear_mode": "Park",
            "drive_mode": "Eco",
            "gear": 0,
            "warning_message": ''
        }

    def test_standard(self): #Path 1
        self.bus["gear"] = 1
        self.bus["rpm"] = 2000
        self.bus = self.Speedometer.calculate_speed(self.bus, self.bus["gear"], self.bus["rpm"])
        self.assertAlmostEqual(self.bus["speed"], 14.91, 2)

    def test_reverse(self):
        self.bus["gear"] = -1
        self.bus["rpm"] = 1500
        self.bus = self.Speedometer.calculate_speed(self.bus, self.bus["gear"], self.bus["rpm"])
        self.assertAlmostEqual(self.bus["speed"], -12.91, 2)