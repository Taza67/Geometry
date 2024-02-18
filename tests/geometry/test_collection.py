import unittest

from geometry.collection import Collection
from geometry.shapes.polygon import Polygon
from geometry.shapes.rectangle import Rectangle
from geometry.vertice import Vertice


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.polygon1 = Polygon([Vertice(0, 0), Vertice(1, 0), Vertice(0, 1)])
        self.polygon2 = Polygon([Vertice(0, 0), Vertice(2, 0), Vertice(0, 2)])
        self.collection = Collection([self.polygon1, self.polygon2])
        self.default_options = {
            'type': 'polygon',
            'count': 3,
            'form': {
                'min_vertices_count': 3,
                'max_vertices_count': 16,
            },
            'space': {
                'space': None,
                'divisions': (2, 2)
            }
        }

    def test_random_collection_with_default_options(self):
        collection = Collection.random()
        self.assertEqual(len(collection), 3)

    def test_random_collection_with_custom_options(self):
        options = {
            'type': 'rectangle',
            'count': 5,
            'form': {
                'min_vertices_count': 4,
                'max_vertices_count': 4,
            },
            'space': {
                'space': Rectangle(Vertice(), 1000, 1000),
                'divisions': (1, 1)
            }
        }
        collection = Collection.random(options)
        self.assertEqual(len(collection), 5)
        self.assertTrue(all(isinstance(polygon, Rectangle) for polygon in collection))

    def test_random_collection_with_invalid_options(self):
        options = {
            'type': 'invalid',
            'count': 'invalid',
            'form': {
                'min_vertices_count': 'invalid',
                'max_vertices_count': 'invalid',
            },
            'space': {
                'space': 'invalid',
                'divisions': 'invalid'
            }
        }
        with self.assertRaises(ValueError):
            _ = Collection.random(options)

    def test_random_collection_with_invalid_polygon_type(self):
        options = {'type': 'invalid'}
        with self.assertRaises(ValueError):
            _ = Collection.random(options)

    def test_random_collection_with_invalid_count(self):
        options = {'count': 'invalid'}
        with self.assertRaises(ValueError):
            _ = Collection.random(options)

    def test_random_collection_with_invalid_form(self):
        options = {'form': {'min_vertices_count': 'invalid', 'max_vertices_count': 'invalid'}}
        with self.assertRaises(ValueError):
            _ = Collection.random(options)

    def test_random_collection_with_invalid_space(self):
        options = {'space': {'space': 'invalid', 'divisions': 'invalid'}}
        with self.assertRaises(ValueError):
            _ = Collection.random(options)

    def test_collection_initialization_creates_empty_collection(self):
        collection = Collection()
        self.assertEqual(len(collection), 0)

    def test_collection_initialization_creates_collection_with_polygons(self):
        self.assertEqual(len(self.collection), 2)

    def test_getitem_returns_correct_polygon(self):
        self.assertEqual(self.collection[0], self.polygon1)
        self.assertEqual(self.collection[1], self.polygon2)

    def test_getitem_raises_error_for_invalid_index(self):
        with self.assertRaises(IndexError):
            _ = self.collection[2]

    def test_str_returns_correct_representation(self):
        self.assertEqual(str(self.collection), f"{str(self.polygon1)}\n\n{str(self.polygon2)}")

    def test_repr_returns_correct_representation(self):
        self.assertEqual(repr(self.collection), f"Collection({repr(self.polygon1)},{repr(self.polygon2)})")

    def test_len_returns_correct_length(self):
        self.assertEqual(len(self.collection), 2)

    def test_add_returns_new_collection_with_added_polygon(self):
        polygon3 = Polygon([Vertice(0, 0), Vertice(3, 0), Vertice(0, 3)])
        new_collection = self.collection + polygon3
        self.assertEqual(len(new_collection), 3)
        self.assertEqual(new_collection[2], polygon3)

    def test_add_returns_new_collection_with_added_collection(self):
        polygon3 = Polygon([Vertice(0, 0), Vertice(3, 0), Vertice(0, 3)])
        collection2 = Collection([polygon3])
        new_collection = self.collection + collection2
        self.assertEqual(len(new_collection), 3)
        self.assertEqual(new_collection[2], polygon3)

    def test_add_raises_error_for_invalid_type(self):
        with self.assertRaises(TypeError):
            _ = self.collection + "invalid"


if __name__ == '__main__':
    unittest.main()
