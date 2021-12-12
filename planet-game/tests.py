import unittest
from planet import Planet

class PlanetTest(unittest.TestCase):
    def test_doCollision_method(self):
        planets = Planet.generatePlanetsThatWillCollide()
        planet1 = planets[0]
        planet2 = planets[1]
        
        while(not(planet1.collides(planet2))):
            planet1.updatePosition()
            planet2.updatePosition()

        pinitial1 = planet1.momentum()
        pinitial2 = planet2.momentum()
        pinitialtotal = pinitial1 + pinitial2

        planet1.doCollision(planet2)

        pfinal1 = planet1.momentum()
        pfinal2 = planet2.momentum()
        pfinaltotal = pfinal1 + pfinal2
        #print("inital momentum " + str(pinitialtotal))
        #print("final momentum " + str(pfinaltotal))

        self.assertAlmostEqual(pinitialtotal, pfinaltotal, -4)

if __name__ == '__main__':
    unittest.main()


class TestSomething(unittest.TestCase):
    def test_randothing(self):
        self.assertEqual(func(true), True, "shoulda been true bitch")

if __name__ == '__main__':
    unittest.main()