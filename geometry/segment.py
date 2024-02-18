from copy import copy

from geometry.vertice import Vertice


class Segment:
    """Classe représentant un segment dans un espace à 2 dimensions.

    Attributes:
        ends (list[Vertice]): Extrémités du segment.
    """

    def __init__(self, ends):
        """Instancie un segment.

        Args:
            ends (list[Vertice]): Extrémités du segment.
        """
        self.ends = list(ends)

    def __copy__(self):
        """Retourne une copie du segment.

        Returns:
            Segment: Nouveau segment avec des copies des extrémités du segment.
        """
        return Segment([copy(self[0]), copy(self[1])])

    def __getitem__(self, item):
        """Surcharge la méthode d'accès par les crochets pour donner accès aux extrémités du segment.

        Args:
            item (int): Index pour l'accès. (0 pour la première extrémité et 1 pour la seconde)

        Returns:
            Vertice: Une extrémité du segment.

        Raises:
            KeyError: Si l'index donné n'est pas 0 ou 1.
        """
        if item < 0 or item > 1:
            raise KeyError("Clé invalide. 0 et 1 sont les seules clés possibles !")
        return self.ends[item]

    def __mul__(self, other):
        """Produit vectoriel si other est un point ou un segment et multiplication par un scalaire si other est un réel ou un entier.

        Args:
            other (Vertice | Segment | float | int): Autre opérande.

        Returns:
            float | Vertice: 
                - Si other est un point(vector) | segment : Résultat du produit vectoriel.
                - Si other est un réel ou un entier : Nouveau vecteur résultant de la multiplication par le scalaire.

        Raises:
            NotImplemented: Opération non autorisée entre Segment et type(other).
        """
        # Multiplication par un scalaire
        if isinstance(other, int) or isinstance(other, float):
            return self.vector() * other

        # Produit vectoriel avec un point
        if isinstance(other, Vertice):
            return self.vector() * Segment([self[0], other])

        # Produit vectoriel avec un autre segment
        if isinstance(other, Segment):
            return self.vector() * other.vector()

        # Autre opérande non autorisé
        return NotImplemented(f"Opération non autorisée entre Segment et {type(other)} !")

    def __str__(self):
        """Retourne une chaîne de caractères représentant le segment.

        Returns:
            str: Chaîne de caractères représentant le segment.
        """
        return f"[{self[0]}, {self[1]}]"

    def __repr__(self):
        """Retourne une chaîne de caractère formelle représentant le segment.

        Returns:
            str: Chaîne de caractères formelle représentant le segment.
        """
        return f"Segment([{repr(self[0])}, {repr(self[1])}])"

    def __eq__(self, other):
        """Vérifie si deux segments sont égaux.

        Args:
            other (Segment): Autre segment à comparer.

        Returns:
            bool: True si les extrémités des deux segments sont identiques, False sinon.
        """
        return self[0] == other[0] and self[1] == other[1]

    def __ne__(self, other):
        """Vérifie si deux segments sont différents.

        Args:
            other (Segment): Autre segment à comparer.

        Returns:
            bool: True si les extrémités des deux segments diffèrent, False sinon.
        """
        return not self == other

    def length(self):
        """Retourne la longueur du segment.

        Returns:
            float: Longueur du segment.
        """
        return self[0].distance_to(self[1])

    def is_vertical(self):
        """Vérifie si le segment est vertical.

        Returns:
            bool: True si le segment est vertical, False sinon.
        """
        return self[0].x == self[1].x

    def is_horizontal(self):
        """Vérifie si le segment est horizontal.

        Returns:
            bool: True si le segment est horizontal, False sinon.
        """
        return self[0].y == self[1].y

    def vector(self):
        """Retourne le vecteur du segment.

        Returns:
            Vertice: Nouveau point représentant le vecteur du segment.
        """
        return self[1] - self[0]
