#!/usr/bin/env python3

from geometry.collection import Collection

if __name__ == "__main__":
    options = {
        'type': 'rectangle',
        'count': 500,
        'form': {
            'min_vertices_count': 5,
            'max_vertices_count': 16,
        },
        'space': {
            'space': None,
            'divisions': (2, 2)
        }
    }

    collection = Collection.random(options)
    with open("test.poly", "w+") as file:
        collection.poly_file_print(file)
