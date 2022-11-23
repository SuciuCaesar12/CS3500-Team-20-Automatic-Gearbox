import unittest
import Simulation as sim

class Simulation_Test(unittest.TestCase):
    def setUp(self):
        self.simulation = sim.Simulation()

    def test_initiator(self):
        """
        Test whether the bus is initalized properly.
        :return:
        """
        self.assertEqual(self.simulation.bus["rpm"], 0)
        self.assertEqual(self.simulation.bus["speed"], 0)
        self.assertFalse(self.simulation.bus["engine_signal"])
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")
        self.assertEqual(self.simulation.bus["gear"], 0)
        self.assertEqual(self.simulation.bus["warning_message"], '')


    def test_exit_loop(self): #Path 1
        """
        Test whether we are able to exit the loop.
        :return:
        """
        self.assertFalse(self.simulation.exit)
        self.simulation.run()
        self.assertTrue(self.simulation.exit)

    def test_no_presses(self): #Path 2
        """
        Test whether the Simulation behaves as expected when we provide no input.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")
        self.assertNotEqual(self.simulation.bus["drive_mode"],"Sport")
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Drive")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Reverse")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Neutral")
        self.assertEqual(self.simulation.bus["rpm"], 0)
        self.assertEqual(self.simulation.bus["speed"], 0)

    def test_loop(self): #Path 3
        """
        Test whether the loop runs successfully.
        :return:
        """
        self.simulation.run()
        self.assertLess(self.simulation.valid_engine_button, 999 ) #If it is less than 999, we know the loop has been executed at least 2 times

    def test_engine_button(self): #Path 4
        """
        Test whether we are able to turn on the Engine.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["engine_on"], True)

    def test_gas(self): #Path 5
        """
        Test whether the RPM increases when giving gas.
        :return:
        """
        self.simulation.run()
        self.assertNotEqual(self.simulation.bus["rpm"], 0)

    def test_sport_mode(self): #Path 6
        """
        Test whether we can switch to Sport mode.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Sport")

    def test_eco_mode(self): #Path 7
        """
        Test whether we can switch to Eco mode.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")

    def test_gear_park(self): #Path 8
        """
        Test whether we can switch to Park.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")

    def test_gear_drive(self): #Path 9
        """
        Test whether we can switch to Drive from Park.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Drive")

    def test_gear_reverse(self): #Path 10
        """
        Test whether we can switch to Reverse from Park.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Reverse")

    def test_gear_neutral(self): #Path 11
        """
        Test whether we can switch to Neutral from Park.
        :return:
        """
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Neutral")

if __name__ == '__main__':
    unittest.main()
