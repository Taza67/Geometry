import unittest

from geometry.shapes.rectangle import Rectangle
from geometry.vertice import Vertice


class RectangleTests(unittest.TestCase):

    def setUp(self):
        self.top_left = Vertice(1, 2)
        self.length = 3
        self.width = 4
        self.rectangle = Rectangle(self.top_left, self.length, self.width)
        self.rectangle2 = Rectangle(Vertice(0, 0), 10, 10)
        self.space = Rectangle(Vertice(0, 0), 1280, 720)

    def test_rectangle_str_representation_is_correct(self):
        self.assertEqual(str(self.rectangle), "\n".join(str(segment) for segment in self.rectangle.segments()))

    def test_rectangle_repr_representation_is_correct(self):
        self.assertEqual(repr(self.rectangle), f"Rectangle({repr(self.top_left)}, {self.length}, {self.width})")

    def test_rectangle_length_is_correct(self):
        self.assertEqual(len(self.rectangle), 4)

    def test_rectangle_area_is_calculated_correctly(self):
        self.assertEqual(self.rectangle.area(), self.length * self.width)

    def test_rectangle_perimeter_is_calculated_correctly(self):
        self.assertEqual(self.rectangle.perimeter(), 2 * (self.length + self.width))

    def test_rectangle_center_is_calculated_correctly(self):
        self.assertEqual(self.rectangle.center(),
                         Vertice(self.top_left[0] + self.width / 2, self.top_left[1] + self.length / 2))

    def test_rectangle_division_creates_correct_number_of_subrectangles(self):
        subrectangles = self.rectangle2 / (2, 2)
        self.assertEqual(len(subrectangles), 2)
        self.assertEqual(len(subrectangles[0]), 2)

    def test_rectangle_division_creates_subrectangles_with_correct_dimensions(self):
        subrectangles = self.rectangle2 / (2, 2)
        for row in subrectangles:
            for subrectangle in row:
                self.assertEqual(subrectangle.length, 5)
                self.assertEqual(subrectangle.width, 5)

    def test_rectangle_division_raises_error_for_non_tuple_operand(self):
        with self.assertRaises(TypeError):
            self.rectangle2 / 2

    def test_rectangle_division_raises_error_for_tuple_operand_with_incorrect_length(self):
        with self.assertRaises(TypeError):
            self.rectangle2 / (2,)

    def test_rectangle_division_raises_error_for_tuple_operand_with_non_integer_elements(self):
        with self.assertRaises(TypeError):
            self.rectangle2 / (2.5, 2.5)

    def test_add_vertice_raises_not_implemented(self):
        with self.assertRaises(TypeError):
            self.rectangle.add_vertice(Vertice(0, 0))

    def test_simplify_raises_not_implemented(self):
        with self.assertRaises(TypeError):
            self.rectangle.simplify()

    def test_rectangle_random_creates_rectangle_with_positive_dimensions(self):
        random_rectangle = Rectangle.random(self.space)
        self.assertGreater(random_rectangle.length, 0)
        self.assertGreater(random_rectangle.width, 0)

    def test_rectangle_random_creates_different_rectangles(self):
        random_rectangle1 = Rectangle.random(self.space)
        random_rectangle2 = Rectangle.random(self.space)
        self.assertNotEqual(random_rectangle1, random_rectangle2)

    def test_rectangle_random_raises_error_for_non_rectangle_space(self):
        with self.assertRaises(TypeError):
            Rectangle.random(space="not a rectangle")


if __name__ == '__main__':
    unittest.main()
