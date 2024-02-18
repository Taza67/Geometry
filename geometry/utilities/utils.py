"""
Implémentation de fonctions utilitaires.
"""


def sign(value):
    """
    Retourne le signe d'une valeur.

    Args:
        value:
            Valeur dont le signe doit être calculé.
    Returns:
        int:
            0 si la valeur est égale à 0.
            1 si la valeur est supérieure à 0.
            -1 si la valeur est inférieure à 0.
    """
    return (value > 0) - (value < 0)
