import unittest

import sys

print(sys.path)

from geometry.shapes.polygon import Polygon
from geometry.vertice import Vertice


class PolygonTests(unittest.TestCase):

    def setUp(self):
        self.vertice1 = Vertice(1, 2)
        self.vertice2 = Vertice(3, 4)
        self.vertice3 = Vertice(5, 6)
        self.polygon = Polygon([self.vertice1, self.vertice2, self.vertice3])
        self.polygon2 = Polygon([Vertice(0, 0), Vertice(1, 0), Vertice(0, 1)])
        self.simple_convex_polygon = Polygon([Vertice(0, 0), Vertice(1, 0), Vertice(0, 1)])
        self.simple_non_convex_polygon = Polygon([Vertice(0, 0), Vertice(1, 0), Vertice(0.2, 0.2), Vertice(0, 1)])
        self.complex_convex_polygon = Polygon([Vertice(0, 0), Vertice(1, 0), Vertice(1, 1), Vertice(0, 1)])
        self.complex_non_convex_polygon = Polygon(
            [Vertice(0, 0), Vertice(1, 0), Vertice(0.5, 0.5), Vertice(1, 1), Vertice(0, 1)])
        self.polygon4 = Polygon([Vertice(0, 0), Vertice(0, 1), Vertice(1, 1), Vertice(1, 0)])

    def test_is_convex_with_simple_convex_polygon(self):
        self.assertTrue(self.simple_convex_polygon.is_convex())

    def test_is_convex_with_simple_non_convex_polygon(self):
        self.assertFalse(self.simple_non_convex_polygon.is_convex())

    def test_is_convex_with_complex_convex_polygon(self):
        self.assertTrue(self.complex_convex_polygon.is_convex())

    def test_is_convex_with_complex_non_convex_polygon(self):
        self.assertFalse(self.complex_non_convex_polygon.is_convex())

    def test_polygon_str_representation_is_correct(self):
        self.assertEqual(str(self.polygon), "\n".join(str(segment) for segment in self.polygon.segments()))

    def test_polygon_repr_representation_is_correct(self):
        self.assertEqual(repr(self.polygon),
                         f"Polygon({','.join(vertice.__repr__() for vertice in self.polygon.vertices)})")

    def test_polygon_length_is_correct(self):
        self.assertEqual(len(self.polygon), 3)

    def test_polygon_area_is_calculated_correctly(self):
        self.assertEqual(self.polygon.area(),
                         sum(vertice1 * vertice2 for vertice1, vertice2 in self.polygon.couples()) / 2)

    def test_polygon_perimeter_is_calculated_correctly(self):
        self.assertEqual(self.polygon.perimeter(), sum(segment.length() for segment in self.polygon.segments()))

    def test_polygon_center_is_calculated_correctly(self):
        self.assertEqual(self.polygon.center(),
                         Vertice(sum(vertice[0] for vertice in self.polygon.vertices) / len(self.polygon),
                                 sum(vertice[1] for vertice in self.polygon.vertices) / len(self.polygon)))

    def test_polygon_simplify_does_not_change_polygon(self):
        original_vertices = self.polygon2.vertices.copy()
        self.polygon2.simplify()
        self.assertEqual(self.polygon2.vertices, original_vertices)

    def test_polygon_convex_hull_returns_same_polygon_for_triangle(self):
        convex_hull = self.polygon2.convex_hull()
        self.assertEqual(convex_hull.vertices, self.polygon2.vertices)

    def test_polygon_random_creates_polygon_with_correct_number_of_vertices(self):
        random_polygon = Polygon.random(vertices_count=5)
        self.assertEqual(len(random_polygon.vertices), 5)

    def test_polygon_random_raises_error_for_less_than_three_vertices(self):
        with self.assertRaises(ValueError):
            Polygon.random(vertices_count=2)

    def test_largest_interior_rectangle_with_square_polygon4(self):
        rectangle = self.polygon4.largestinteriorrectangle()
        self.assertEqual(rectangle[0], Vertice(0, 0))
        self.assertEqual(rectangle.length, 1)
        self.assertEqual(rectangle.width, 1)

    def test_largest_interior_rectangle_with_non_square_polygon4(self):
        self.polygon4 = Polygon([Vertice(0, 0), Vertice(0, 2), Vertice(2, 2), Vertice(2, 0)])
        rectangle = self.polygon4.largestinteriorrectangle()
        self.assertEqual(rectangle[0], Vertice(0, 0))
        self.assertEqual(rectangle.length, 2)
        self.assertEqual(rectangle.width, 2)

    def test_largest_interior_rectangle_with_irregular_polygon4(self):
        self.polygon4 = Polygon([Vertice(0, 0), Vertice(0, 2), Vertice(1, 1), Vertice(2, 0)])
        rectangle = self.polygon4.largestinteriorrectangle()

        self.assertEqual(rectangle[0], Vertice(0, 0))
        self.assertEqual(rectangle.length, 1)
        self.assertEqual(rectangle.width, 1)


if __name__ == '__main__':
    unittest.main()
