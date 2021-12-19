import unittest
import math

from related_functions import angle_between_two_vectors, angle_by_sin_cos
from main import Boat


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
        test_boat1 = Boat(3.34, 170, 1)
        test_boat1.mainsheet_operate(loosen = True)
        self.assertEqual(test_boat1.mainsheet, 1)

    def test_sail_angle_to_wind(self):
        test_boat2 = Boat(3.34, 170, 1)
        test_boat2.mainsheet = 1
        self.assertEqual(test_boat2.sail_angle_to_wind(), 89)

    def test_sail_angle_to_wind(self):
        test_boat3 = Boat(3.34, 170, 1)
        test_boat3.mainsheet = 27
        test_boat3.course = 230
        self.assertEqual(test_boat3.sail_angle_to_wind(), 103)

    def test_sail_force_longitudinal_start(self):
        test_boat4 = Boat(3.34, 170, 1)
        self.assertAlmostEqual(test_boat4.sail_force_longitudinal(),0)
    
    def test_sail_force_longitudinal_negative(self):
        test_boat5 = Boat(3.34, 170, 1)
        test_boat5.course = 0
        test_boat5.mainsheet = 90
        self.assertAlmostEqual(test_boat5.sail_force_longitudinal(),-150)
    
    def test_max_speed(self):
        test_boat6 = Boat(3.34, 170, 1)
        self.assertAlmostEqual(test_boat6.max_speed,2.1070495881480813)
    
    def test_acceleration_max_speed(self):
        test_boat7 = Boat(3.34, 170, 1)
        test_boat7.course = 180
        test_boat7.mainsheet = 90
        test_boat7.speed = test_boat7.max_speed
        self.assertLessEqual(test_boat7.acceleration(test_boat7.sail_force_longitudinal()),0)
    
if __name__ == '__main__':
    unittest.main()