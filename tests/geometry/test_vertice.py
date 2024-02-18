import unittest

import geometry.segment
import geometry.vertice


class TestVertice(unittest.TestCase):

    def setUp(self):
        self.vertice1 = geometry.vertice.Vertice(1, 2)
        self.vertice2 = geometry.vertice.Vertice(3, 4)
        self.vertice3 = geometry.vertice.Vertice(1, 2)
        self.segment = geometry.segment.Segment([self.vertice1, self.vertice2])

    def test_addition_of_two_vertices_results_in_new_vertex(self):
        result = self.vertice1 + self.vertice2
        self.assertEqual(result, geometry.vertice.Vertice(4, 6))

    def test_subtraction_of_two_vertices_results_in_new_vertex(self):
        result = self.vertice1 - self.vertice2
        self.assertEqual(result, geometry.vertice.Vertice(-2, -2))

    def test_multiplication_of_vertex_and_scalar_results_in_new_vertex(self):
        result = self.vertice1 * 2
        self.assertEqual(result, geometry.vertice.Vertice(2, 4))

    def test_multiplication_of_two_vertices(self):
        expected = self.vertice1.x * self.vertice2.y - self.vertice1.y * self.vertice2.x
        result = self.vertice1 * self.vertice2
        self.assertEqual(result, expected)

    def test_multiplication_of_vertex_and_segment(self):
        expected = self.vertice3 * self.segment.vector()
        result = self.vertice3 * self.segment
        self.assertEqual(result, expected)

    def test_division_of_vertex_and_scalar_results_in_new_vertex(self):
        result = self.vertice1 / 2
        self.assertEqual(result, geometry.vertice.Vertice(0.5, 1))

    def test_equality_of_two_identical_vertices_returns_true(self):
        self.assertTrue(self.vertice1 == self.vertice3)

    def test_inequality_of_two_different_vertices_returns_true(self):
        self.assertTrue(self.vertice1 != self.vertice2)

    def test_less_than_comparison_of_two_vertices(self):
        self.assertTrue(self.vertice1 < self.vertice2)

    def test_greater_than_comparison_of_two_vertices(self):
        self.assertTrue(self.vertice2 > self.vertice1)

    def test_distance_between_two_vertices(self):
        distance = self.vertice1.distance_to(self.vertice2)
        self.assertAlmostEqual(distance, 2.8284, places=4)

    def test_angle_between_two_vertices(self):
        angle = self.vertice1.angle(self.vertice2)
        self.assertAlmostEqual(angle, -2.35619, places=4)


if __name__ == '__main__':
    unittest.main()
