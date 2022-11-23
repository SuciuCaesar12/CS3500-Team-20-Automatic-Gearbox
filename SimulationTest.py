import unittest
import Simulation as sim

class Simulation_Test(unittest.TestCase):
    def setUp(self):
        self.simulation = sim.Simulation()

    def test_initiator(self):
        self.assertEqual(self.simulation.bus["rpm"], 0)
        self.assertEqual(self.simulation.bus["speed"], 0)
        self.assertFalse(self.simulation.bus["engine_signal"])
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")
        self.assertEqual(self.simulation.bus["gear"], 0)
        self.assertEqual(self.simulation.bus["warning_message"], '')


    def test_exit_loop(self): #Tests exiting the loop --> path 1
        self.assertFalse(self.simulation.exit)
        self.simulation.run()
        self.assertTrue(self.simulation.exit)

    def test_no_presses(self): #path 2
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")
        self.assertNotEqual(self.simulation.bus["drive_mode"],"Sport")
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Drive")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Reverse")
        self.assertNotEqual(self.simulation.bus["gear_mode"], "Neutral")
        self.assertEqual(self.simulation.bus["rpm"], 0)
        self.assertEqual(self.simulation.bus["speed"], 0)

    def test_loop(self): #path 3
        self.simulation.run()
        self.assertLess(self.simulation.valid_engine_button, 999 ) #If it is less than 999, we know the loop has been executed at least 2 times

    def test_engine_button(self): #path 4
        self.simulation.run()
        self.assertEqual(self.simulation.bus["engine_on"], True)

    def test_gas(self): #path 5
        self.simulation.run()
        self.assertNotEqual(self.simulation.bus["rpm"], 0)

    def test_sport_mode(self): #path 6
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Sport")

    def test_eco_mode(self): #path 7
        self.simulation.run()
        self.assertEqual(self.simulation.bus["drive_mode"], "Eco")

    def test_gear_park(self): #path 8
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Park")

    def test_gear_drive(self): #Path 9
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Drive")

    def test_gear_reverse(self): #Path 10
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Reverse")

    def test_gear_neutral(self): #Path 11
        self.simulation.run()
        self.assertEqual(self.simulation.bus["gear_mode"], "Neutral")

if __name__ == '__main__':
    unittest.main()
