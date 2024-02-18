"""
Implémentation de l'objet Polygone dans un espace à 2 dimensions.
"""

import importlib
from copy import copy
from itertools import islice, cycle

import largestinteriorrectangle as lir
import numpy as np

import geometry.utilities.utils
from geometry.segment import Segment
from geometry.vertice import Vertice


class Polygon:
    """
    Classe représentant un polygone dans un espace à 2 dimensions.

    Attributes:
        vertices (list[Vertice]):
            Points du polygone.
    """


    DEFAULT_RANDOM_SPACE_WIDTH = 1280.
    DEFAULT_RANDOM_SPACE_LENGTH = 720.

    def __init__(self, vertices=None):
        """
        Instancie un polygone.

        Args:
            vertices (list[Vertice]):
                Points du polygone. (par défaut à [])
        """
        self.vertices = [] if not vertices else list(vertices)

    def __getitem__(self, item):
        """
        Surcharge la méthode d'accès par les crochets pour donner accès
        aux sommets du polygone.

        Args:
            item (int):
                Index pour l'accès. (0 ≤ item < |sommets|)
        Returns:
            Vertice:
                Un sommet du polygone
        Raises:
            KeyError:
                Si l'index donné n'est pas entre 0 et |sommets| - 1.
        """
        if item < 0 or item >= len(self):
            raise KeyError("Clé invalide !")

        return self.vertices[item]

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant le polygone.

        Returns:
            str:
                Chaîne de caractères représentant le polygone.
        """
        return "\n".join(str(segment) for segment in self.segments())

    def __repr__(self):
        """
        Retourne une chaîne de caractères formelle représentant le polygone.

        Returns:
            str:
                Chaîne de caractères formelle représentant le polygone.
        """
        vertices = ",".join(repr(vertice) for vertice in self.vertices)
        return f"Polygon({vertices})"

    def __len__(self):
        """
        Retourne le nombre de points dans le polygone.

        Returns:
            int:
                Nombre de points dans le polygone.
        """
        return len(self.vertices)

    def couples(self):
        """
        Retourne une liste consécutive de paires de points du polygone.

        Returns:
            list[tuple(Vertice, Vertice)]:
                Liste de tuples, chacun contenant deux points consécutifs du polygone.
        """
        return zip(self.vertices, islice(cycle(self.vertices), 1, None))

    def segments(self):
        """
        Retourne une liste des segments du polygone.

        Returns:
            list[Segment]:
                Liste des segments du polygone.
        """
        return map(Segment, self.couples())

    def area(self):
        """
        Retourne l'aire du polygone.

        Returns:
            float:
                Aire du polygone.
        """
        return sum(vertice1 * vertice2 for vertice1, vertice2 in self.couples()) / 2

    def perimeter(self):
        """
        Retourne le périmètre du polygone.

        Returns:
            float:
                Périmètre du polygone.
        """
        return sum(segment.length() for segment in self.segments())

    def add_vertice(self, vertice, simplify=False):
        """
        Ajoute un point au polygone.
        Attention ! Si le polygone était simple, après l'ajout
        du point, ce ne serait peut-être plus le cas.

        Args:
            vertice (Vertice):
                Point à ajouter.
            simplify (bool):
                Si True, le polygone sera simple. (par défaut à False)
        """
        self.vertices.append(vertice)

        if simplify:
            self.simplify()

    def center(self):
        """
        Retourne le barycentre.

        Returns:
            Vertice:
                Point central du polygone.
        Raises:
            AssertionError:
                Nombre de sommets ≤ 3.
        """
        assert len(self) >= 3, "Nombre de sommets <= 3 !"

        return Vertice(
            sum(vertice[0] for vertice in self.vertices) / len(self),
            sum(vertice[1] for vertice in self.vertices) / len(self)
        )

    def simplify(self):
        """
        Rend le polygone simple en utilisant la méthode de tri par angle.
        (Angular-Sorting)
        """
        # Point central
        center = self.center()

        # Tri des points basés sur l'angle
        self.vertices.sort(key=lambda vertice: vertice.angle(center))

    def convex_hull(self):
        """
        Retourne l'enveloppe convexe du polygone en utilisant le parcours
        de Graham.

        Returns:
            Polygon:
                Nouveau polygone représentant l'enveloppe convexe du polygone.
        """
        vertices = [copy(vertice) for vertice in self.vertices]

        # Recherche du pivot
        vertices.sort(key=lambda vertice: (vertice.y, vertice.x))

        # Tri des sommets par angle croissant par rapport au pivot
        # Les sommets d'angle égal seront triés par abscisse croissante.
        vertices[1:] = sorted(vertices[1:], key=lambda vertice: (vertice.angle(vertices[0]), vertice.x))

        vertices_stack = [
            vertices[0], vertices[1]
        ]

        # Construction itérative de l'enveloppe convexe
        for index in range(2, len(vertices)):
            # Attente d'un tournant à gauche
            while len(vertices_stack) >= 2 and (Segment([vertices_stack[1], vertices_stack[0]]) * vertices[index]) > 0:
                vertices_stack.pop()
            vertices_stack.append(vertices[index])

        return Polygon(vertices_stack)

    def is_convex(self):
        """
        Vérifie si un polygone est convexe.

        Returns:
            bool:
                True si le polygone est convexe, False sinon.
        """
        vertices_count = len(self)
        if vertices_count < 4:
            return True

        current_orientation = 0
        for index in range(vertices_count):
            segment = Segment(
                [self[index], self[(index + 1) % vertices_count]]
            )
            next_vertice = self[(index + 2) % vertices_count]

            # Tournant à gauche si signe du produit vectoriel est négatif.
            # Tournant à droite si le signe du produit est positif.
            product = segment * next_vertice
            orientation = geometry.utilities.utils.sign(product)

            # Vecteurs non collinéaires ?
            if product != 0:
                # Premièr segment
                if current_orientation == 0:
                    current_orientation = orientation
                # Le tournant courant diffère du tournant précédent.
                elif current_orientation != orientation:
                    return False

        return True

    def largestinteriorrectangle(self):
        """
        Retourne le plus grand rectangle inclu dans le polygone.

        Returns:
            Rectangle:
                Plus grand rectangle intérieur du polygone.
        """
        # La liste des sommets est convertie au format requis par la librairie largestinteriorrectangle.
        lir_format_polygon = np.array([[[vertice.x, vertice.y] for vertice in self.vertices]], np.int32)

        # Le plus grand rectangle intérieur est ensuite calculé.
        lir_format_rectangle = lir.lir(lir_format_polygon)

        # On récupère les sommets limites du rectangle.
        top_left = lir.pt1(lir_format_rectangle)
        top_left = Vertice(top_left[0], top_left[1])

        bottom_right = lir.pt2(lir_format_rectangle)
        bottom_right = Vertice(bottom_right[0], bottom_right[1])

        # Dimensions du rectangle
        dimensions = bottom_right - top_left

        rectangle = importlib.import_module("geometry.shapes.rectangle").Rectangle
        return rectangle(top_left, dimensions.y, dimensions.x)

    @classmethod
    def random(cls, space=None, vertices_count=3, simplify=False, convex=False):
        """
        Retourne un polygone généré aléatoirement.

        Args:
            space (Rectangle):
                Rectangle représentant l'espace dans lequel
                les sommets du polygone seront tirés au hasard.
                (par défaut à (1280 x 720))
            vertices_count (int):
                Nombre de points dans le polygone. (> 3) (par défaut à 3)
            simplify (bool):
                Si True, le polygone sera simple. (par défaut à False)
            convex (bool):
                Si True, le polygone sera forcément convexe. (par défaut à False)
                Attention ! L'enveloppe convexe sera retournée, il se peut donc
                qu'il n'y ait pas autant de sommets que demandés.
        Returns:
            Polygon:
                Nouveau polygone aléatoire.
        Raises:
            ValueError:
                Le nombre de sommets est inférieur à 3.
        """
        if not space:
            # Import dynamique de la classe Rectangle
            rectangle = importlib.import_module("geometry.shapes.rectangle").Rectangle
            space = rectangle(
                Vertice(), cls.DEFAULT_RANDOM_SPACE_LENGTH,
                cls.DEFAULT_RANDOM_SPACE_WIDTH
            )

        # Nombre de sommets
        if vertices_count < 3:
            raise ValueError("Nombre de sommets minimal : 3 !")

        # Création d'un polygone quelconque
        polygon = Polygon()
        for _ in range(vertices_count):
            polygon.add_vertice(Vertice.random(space))

        # Polygone convexe
        if convex:
            return polygon.convex_hull()

        # 'Simplification' du polygone
        if simplify:
            polygon.simplify()

        return polygon
