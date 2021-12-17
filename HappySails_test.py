import unittest
import math

from related_functions import angle_between_two_vectors, angle_by_sin_cos
from main import Boat



test_boat = Boat(3.34, 170, 1)


class HappySailsTest(unittest.TestCase):
    def test_angle_between_two_vectors(self):
        self.assertEqual(angle_between_two_vectors(60, 10), 50)
    
    def test_angle_between_two_vectors_big_first(self):
        self.assertEqual(angle_between_two_vectors(5, 100), 95)
    
    def test_angle_between_two_vectors_smaller(self):
        self.assertEqual(angle_between_two_vectors(17, 271), 106)

    def test_angle_by_sin_cos(self):
        self.assertEqual(angle_by_sin_cos(1, 0), 90)

    def test_angle_by_sin_cos_aproximity(self):
        self.assertAlmostEqual(angle_by_sin_cos(-1/2, -math.sqrt(3)/2), 210)
    
    def test_angle_by_sin_cos_mistakes_due_to_non_null_epsilon(self):
        self.assertNotAlmostEqual(angle_by_sin_cos(0.999999999, -0.0000447213), math.degrees(1.570751605))
    
    def test_mainsheet_operate(self):
        test_boat.mainsheet_operate(loosen = True)
        self.assertEqual(test_boat.mainsheet, 1)

    def test_sail_angle_to_wind(self):
        test_boat.mainsheet = 0
        self.assertEqual(test_boat.sail_angle_to_wind(), 90)

    def test_sail_angle_to_wind(self):
        test_boat.mainsheet = 27
        test_boat.course = 230
        self.assertEqual(test_boat.sail_angle_to_wind(), 103)

if __name__ == '__main__':
    unittest.main()