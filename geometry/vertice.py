"""
Implémentation de l'objet Point dans un espace à deux dimensions.
"""

import importlib
import random
from math import sqrt, atan2


class Vertice:
    """
    Classe représentant un point dans un espace à 2 dimensions.

    Attributes:
        x (float): Coordonnée x du point.
        y (float): Coordonnée y du point.
    """

    def __init__(self, x=0., y=0.):
        """
        Instancie un point.

        Args:
            x (float): Coordonnée x du point. (default à 0)
            y (float): Coordonnée y du point. (default à 0)
        """
        self.x = float(x)
        self.y = float(y)

    def __copy__(self):
        """
        Retourne une copie du point.

        Returns:
            Vertice: Nouveau point ayant les mêmes coordonnées que le point.
        """
        return Vertice(self.x, self.y)

    def __getitem__(self, item):
        """
        Surcharge la méthode d'accès par les crochets pour donner accès
        aux coordonnées x et y du point.

        Args:
            item (int | str):
                Index ou clé pour l'accès. (0 || 'x' pour x et 1 || 'y' pour y)
        Returns:
            Coordonnée x ou y du point.
        Raises:
            KeyError:
                Si la clé donnée n'est pas 0, 'x', 1, ou 'y'.
        """
        if item == 0 or item == 'x':
            return self.x
        if item == 1 or item == 'y':
            return self.y

        raise KeyError("Clé invalide. 0, 'x', 1 et 'y' sont les seules clés possibles !")

    def __add__(self, other):
        """
        Additionne les coordonnées de deux points.

        Args:
            other (Vertice): Autre point à ajouter.
        Returns:
            Vertice: Nouveau point résultant de l'addition.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return Vertice(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Soustrait les coordonnées de deux points.

        Args:
            other (Vertice): Autre point à soustraire.
        Returns:
            Vertice: Nouveau point résultant de la soustraction.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return Vertice(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """
        Produit vectoriel si other est un point ou un segment et
        multiplication par un scalaire si other est un réel ou un entier.

        Args:
            other (Vertice | Segment | float | int):
                Autre opérande.
        Returns:
            float | Vertice:
                - Si other est un point ou un segment :
                    Résultat du produit vectoriel.
                - Si other est un réel ou un entier :
                    Nouveau point résultant de la multiplication par
                    le scalaire.
        """
        # Multiplication par un scalaire
        if isinstance(other, int) or isinstance(other, float):
            return Vertice(self.x * other, self.y * other)

        # Produit vectoriel avec un point
        if isinstance(other, Vertice):
            return self.x * other.y - self.y * other.x

        # Produit vectoriel avec un segment
        segment = importlib.import_module("geometry.segment").Segment
        if isinstance(other, segment):
            return self * other.vector()

        # Autre opérande non autorisé
        return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

    def __truediv__(self, factor):
        """
        Divise les coordonnées du point par un scalaire.

        Args:
            factor (float):
                Diviseur.
        Returns:
            Vertice:
                Nouveau point résultant de la division.
        """
        # Autre opérande non autorisé
        if not isinstance(factor, float) and not isinstance(factor, int):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(factor)} !")

        return Vertice(self.x / factor, self.y / factor)

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant le point.

        Returns:
            str:
                Chaîne de caractères représentant le point.
        """
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """
        Retourne une chaîne de caractère formelle représentant le point.

        Returns:
            str:
                Chaîne de caractères formelle représentant le point.
        """
        return f"Vertice({self.x}, {self.y})"

    def __eq__(self, other):
        """
        Vérifie si deux points sont égaux.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées sont égales, sinon False.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        Vérifie si deux points ne sont pas égaux.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées diffèrent, sinon False.
        """
        return not self == other

    def __ge__(self, other):
        """
        Vérifie si un point est supérieur ou égal à un autre point.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées du premier point sont supérieures
            ou égales à celles du second, False sinon.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return self.x >= other.x and self.y >= other.y

    def __gt__(self, other):
        """
        Vérifie si un point est supérieur à un autre point.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées du premier point sont supérieures
                à celles du second, False sinon.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return self.x > other.x and self.y > other.y

    def __le__(self, other):
        """
        Vérifie si un point est inférieur ou égal à un autre point.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées du premier point sont inférieures
                ou égales à celles du second, False sinon.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return self.x <= other.x and self.y <= other.y

    def __lt__(self, other):
        """
        Vérifie si un point est inférieur à un autre point.

        Args:
            other (Vertice):
                Autre point à comparer.
        Returns:
            bool:
                True si les coordonnées du premier point sont inférieures
                à celles du second, False sinon.
        """
        # Autre opérande non autorisé
        if not isinstance(other, Vertice):
            return NotImplemented(f"Opération non autorisée entre Vertice et {type(other)} !")

        return self.x < other.x and self.y < other.y

    def distance_to(self, other=None):
        """
        Retourne la distance euclidienne entre deux points.

        Args:
            other (Vertice):
                Autre point du segment. (par défaut à l'origine (0, 0))
        Returns:
            float:
                Distance euclidienne entre les deux points.
        """
        if other is None:
            other = Vertice()

        # Rend la fonction symétrique
        if self < other:
            return other.distance_to(self)

        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle(self, center=None):
        """
        Calcule l'angle du point avec un centre.

        Args:
            center (Vertice):
                Centre de référence. (par défaut à l'origine (0, 0))
        Returns:
            float:
                Angle du point par rapport au centre.
        """
        if center is None:
            center = Vertice()

        return atan2(self.y - center.y, self.x - center.x)

    @classmethod
    def random(cls, space):
        """
        Retourne un point tiré aléatoirement dans un espace.

        Args:
            space (Rectangle):
                Espace dans lequel le point est tiré.
        Returns:
            Point:
                Nouveau point aléatoire situé dans l'espace.
        """
        random_x = random.randint(
            int(space.vertices[0].x), int(space.vertices[2].x)
        )
        random_y = random.randint(
            int(space.vertices[0].y), int(space.vertices[2].y)
        )

        return Vertice(random_x, random_y)
