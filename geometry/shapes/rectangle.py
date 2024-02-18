"""
Implémentation de l'objet Rectangle dans un espace à 2 dimensions.
"""

import importlib

import numpy as np

from geometry.shapes.polygon import Polygon
from geometry.vertice import Vertice


class Rectangle(Polygon):
    """
    Classe représentant un rectangle dans un espace à 2 dimensions.
    Elle hérite de tous les attributs et toutes les méthodes de la
    classe Polygon à l'exception de :
    - add_vertice()
    - simplify()

    Attributes:
        length (float): Longueur du rectangle.
        width (float): Largeur du rectangle.
    """
    ...

    def __init__(self, top_left, length, width):
        """
        Instancie un rectangle.

        Args:
            top_left (Vertice):
                Sommet haut gauche du rectangle.
            length (float):
                Longueur du rectangle.
            width (float):
                Largeur du rectangle
        """
        # Création d'un rectangle, avec les dimensions
        # données, situé à l'origine
        vertices = [
            Vertice(0., 0.),
            Vertice(x=width),
            Vertice(width, length),
            Vertice(y=length),
        ]
        # Translation du rectangle au point donné.
        vertices = [vertice + top_left for vertice in vertices]

        super().__init__(vertices)
        self.length = length
        self.width = width

    def __truediv__(self, other):
        """
        Divise le rectangle en sous-rectangles.

        Args:
            other (tuple(int, int)):
                Nombre de divisions verticales, nombre de divisions horizontales. (both > 0)
        Returns:
            list(list(Rectangle)):
                Liste de listes de rectangles représentant les divisions.
                Chaque sous-liste représente une rangée horizontale.
        """
        # Autre opérande non autorisé
        if not isinstance(other, tuple) or len(other) != 2 \
                or not isinstance(other[0], int) or not isinstance(other[1], int):
            return NotImplemented(f"Opération non autorisée entre Rectangle et {type(other)} !")

        # Découpage
        vertical_values = np.linspace(self[0].y, self[2].y, other[0] + 1)
        horizontal_values = np.linspace(self[0].x, self[2].x, other[1] + 1)

        rectangles = [[None for _ in range(other[1])] for _ in range(other[0])]
        for line in range(other[0]):
            for column in range(other[1]):
                # Récupération du point de départ et des dimensions
                top_left = Vertice(horizontal_values[column], vertical_values[line])
                bottom_right = Vertice(horizontal_values[column + 1], vertical_values[line + 1])
                dimensions = bottom_right - top_left

                # noinspection PyTypeChecker
                rectangles[line][column] = Rectangle(top_left, dimensions.y, dimensions.x)

        return rectangles

    def __repr__(self):
        """
        Retourne une chaîne de caractères formelle représentant le rectangle.

        Returns:
            str:
                Chaîne de caractères formelle représentant le rectangle.
        """
        return f"Rectangle({repr(self[0])}, {self.length}, {self.width})"

    def add_vertice(self, vertice, simplify=False):
        raise NotImplemented("Cette méthode n'est pas implémentée pour la classe 'Rectangle'")

    def simplify(self):
        raise NotImplemented("Cette méthode n'est pas implémentée pour la classe 'Rectangle'")

    # noinspection PyMethodOverriding
    @classmethod
    def random(cls, space=None):
        """
        Retourne un rectangle généré aléatoirement.

        Args:
            space (Rectangle):
                Rectangle représentant l'espace dans lequel
                les sommets du rectangle seront tirés au hasard.
                (par défaut à (1280 x 720))
        Returns:
            Rectangle:
                Nouveau rectangle généré aléatoirement.
        """
        if not isinstance(space, Rectangle):
            raise TypeError("space doit être une instance de Rectangle !")

        if space is None:
            # Import dynamique de la classe Rectangle
            rectangle = importlib.import_module("geometry.shapes.rectangle").Rectangle
            space = rectangle(
                Vertice(), cls.DEFAULT_RANDOM_SPACE_LENGTH,
                cls.DEFAULT_RANDOM_SPACE_WIDTH
            )

        # Points limites
        vertice1 = Vertice.random(space)
        vertice2 = Vertice.random(space)

        if vertice1.x > vertice2.x:
            vertice1, vertice2 = Vertice(vertice2.x, vertice1.y), Vertice(vertice1.x, vertice2.y)
        if vertice1.y > vertice2.y:
            vertice1, vertice2 = Vertice(vertice1.x, vertice2.y), Vertice(vertice2.x, vertice1.y)

        dimensions = vertice2 - vertice1

        return Rectangle(
            vertice1, dimensions.y, dimensions.x
        )
