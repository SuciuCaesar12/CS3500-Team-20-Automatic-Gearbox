import unittest
import Engine as En

class EngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = En.Engine()
        self.engine.RPM = 0
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

    def test_engine_off(self): #Path 1
        """
        Test whether the engine stays off and the RPM stays 0.
        """
        self.engine.run(self.bus, False)
        self.assertFalse(self.bus["engine_on"])
        self.assertEqual(self.bus["rpm"], 0)

    def test_no_gas(self): #Path 2
        """
        Test whether we can turn the Engine on and the RPM decreases when no gas is provided.
        """
        self.bus["engine_signal"] = True
        self.engine.RPM = 100
        self.bus["rpm"] = 100
        self.engine.run(self.bus, False)
        self.assertEqual(self.bus["rpm"], (100 - 0.1))
        self.assertTrue(self.engine.Engine_On)
        self.assertTrue(self.bus["engine_on"])

    def test_gear_0(self): #Path 3
        """
        Test what happens when gas is provided in gear 0 (neutral gear).
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.bus["rpm"] = 100
        self.engine.RPM = 100
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 100 + (0.1  / (1+1e-6)))
        self.assertEqual(self.bus["gear"], self.engine.current_gear) #We test node 19 here, so we don't need to perform this check in the other tests.

    def test_gear_not0(self): #Path 4
        """
        Test what happens when gas is provided in any other gear except 0.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.engine.RPM = 100
        self.bus["rpm"] = 100
        self.engine.current_gear = 1
        self.bus["gear"] = 1
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 100 + (0.1 / (abs(self.bus['gear']) + 1e-6)))

    def test_negative_gear(self): #Path 5
        """
        Test what happens when we switch from neutral gear (0) to reverse (-1). RPM should stay 0.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.bus["gear"] = -1
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 0)

    def test_switch_up_zero(self): #Path 6
        """
        Test whether the RPM stays 0 when we switch from gear 0 (neutral) to drive (gear 1).
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.bus["gear"] = 1
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 0)
        self.assertEqual(self.bus["gear"], self.engine.current_gear)

    def test_switch_up(self): #Path 7
        """
        Test whether the RPM gets reset to 1500 when we switch up gears in Drive.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.engine.current_gear = 1
        self.bus["gear"] = 2
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 1500)

    def test_switch_down_zero(self): #Path 8
        """
        Test what happens when we switch from Drive to Neutral/Park (gear 0). RPM should become 0.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.bus["gear"] = 0
        self.engine.current_gear = 1
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 0)

    def test_switch_down(self): #Path 9
        """
        Test what happens when we switch down gears in Drive. RPM should become 2000.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.bus["gear"] = 1
        self.engine.current_gear = 2
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 2000)

    def test_negative_rpm(self): #Path 10
        """
        Test what happens when no gas is given when the engine is stationary. Should stay 0 RPM.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.engine.RPM = 0
        self.bus["rpm"] = 0
        self.engine.run(self.bus, False)
        self.assertEqual(self.bus["rpm"], 0)

    def test_upper_limit(self): #Path 11
        """
        Test what happens to the RPM when it reaches its upper limit of 4500. It should stay capped at 4500.
        """
        self.bus["engine_on"] = True
        self.engine.Engine_On = True
        self.engine.RPM = 4600
        self.bus["rpm"] = 4600
        self.engine.run(self.bus, True)
        self.assertEqual(self.bus["rpm"], 4500)

if __name__ == '__main__':
    unittest.main()