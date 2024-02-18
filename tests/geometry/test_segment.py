import unittest
from copy import copy

import geometry.vertice
from geometry.segment import Segment
from geometry.vertice import Vertice


class SegmentTests(unittest.TestCase):

    def setUp(self):
        self.vertice1 = Vertice(1, 2)
        self.vertice2 = Vertice(3, 4)
        self.segment = Segment([self.vertice1, self.vertice2])

    def test_segment_length_is_calculated_correctly(self):
        self.assertEqual(self.segment.length(), self.vertice1.distance_to(self.vertice2))

    def test_segment_vector_is_calculated_correctly(self):
        self.assertEqual(self.segment.vector(), self.segment[1] - self.segment[0])

    def test_multiplication_of_segment_and_scalar_results_in_new_vertex(self):
        result = self.segment * 2
        expected = self.segment.vector() * 2
        self.assertEqual(result, expected)

    def test_multiplication_of_segment_and_vector_results(self):
        result = self.segment * self.segment[0]
        expected = 0
        self.assertEqual(result, expected)

    def test_multiplication_of_segment_and_segment(self):
        result = self.segment * geometry.segment.Segment([self.segment[1], self.segment[1]])
        expected = 0
        self.assertEqual(result, expected)

    def test_segment_copy_is_equal_to_original(self):
        segment_copy = copy(self.segment)
        self.assertEqual(segment_copy, self.segment)

    def test_segment_copy_is_not_same_instance_as_original(self):
        segment_copy = copy(self.segment)
        self.assertNotEqual(id(segment_copy), id(self.segment))

    def test_segment_str_representation_is_correct(self):
        self.assertEqual(str(self.segment), f"[{self.vertice1}, {self.vertice2}]")

    def test_segment_repr_representation_is_correct(self):
        self.assertEqual(repr(self.segment), f"Segment([{repr(self.vertice1)}, {repr(self.vertice2)}])")

    def test_segment_is_not_vertical(self):
        self.assertFalse(self.segment.is_vertical())

    def test_segment_is_not_horizontal(self):
        self.assertFalse(self.segment.is_horizontal())


if __name__ == '__main__':
    unittest.main()
