import random
from sys import stdout

from geometry.shapes.polygon import Polygon
from geometry.shapes.rectangle import Rectangle
from geometry.vertice import Vertice


class Collection:
    """Représente une collection de polygones.
    
    Cette classe permet de gérer une collection de polygones, offrant des fonctionnalités
    pour accéder aux polygones, les ajouter et les imprimer dans différents formats.
    
    Attributes:
        polygons (list[Polygon]): Ensemble de polygones.
    """
    DEFAULT_RANDOM_SPACE_WIDTH = 1280.
    DEFAULT_RANDOM_SPACE_LENGTH = 720.

    def __init__(self, polygons=None):
        """Initialise une collection de polygones.
        
        Args:
            polygons (list[Polygon], optional): Ensemble de polygones. Par défaut à [].
        """
        self.polygons = [] if not polygons else list(polygons)

    def __getitem__(self, item):
        """Permet l'accès aux polygones via les crochets.
        
        Args:
            item (int): Index pour l'accès aux polygones.
            
        Returns:
            Polygon: Un polygone de la collection.
            
        Raises:
            IndexError: Si l'index n'est pas entre 0 et le nombre de polygones - 1.
        """
        if item < 0 or item >= len(self):
            raise IndexError("Clé invalide !")
        return self.polygons[item]

    def __str__(self):
        """Représente la collection de polygones sous forme de chaîne de caractères.
        
        Returns:
            str: Chaîne de caractères représentant le polygone.
        """
        return "\n\n".join(str(polygon) for polygon in self.polygons)

    def __repr__(self):
        """Représentation formelle de la collection de polygones.
        
        Returns:
            str: Chaîne de caractères formelle représentant le polygone.
        """
        polygons = ",".join(repr(polygon) for polygon in self.polygons)
        return f"Collection({polygons})"

    def __len__(self):
        """Retourne le nombre de polygones dans la collection.
        
        Returns:
            int: Nombre de polygones.
        """
        return len(self.polygons)

    def __add__(self, other):
        """Ajoute un polygone ou une collection à la collection actuelle.
        
        Args:
            other (Polygon | Collection): Polygone ou collection à ajouter.
            
        Returns:
            Collection: Nouvelle collection résultante.
            
        Raises:
            NotImplemented: Si l'opération est non autorisée.
        """
        if isinstance(other, Polygon):
            return Collection(self.polygons + [other])
        if isinstance(other, Collection):
            return Collection(self.polygons + other.polygons)
        return NotImplemented(f"Opération non autorisée entre Collection et {type(other)} !")

    def poly_file_print(self, file=stdout):
        """Imprime la collection dans un format spécifique pour les fichiers 'poly'.
        
        Args:
            file (_io.TextIOWrapper, optional): Fichier de sortie. Par défaut à stdout.
        """
        for index, polygon in enumerate(self.polygons):
            for vertice in polygon.vertices:
                print(f"{index} {vertice.x} {vertice.y}", file=file)

    @classmethod
    def random(cls, options=None):
        """
        Retourne une collection de polygones générés alétoirement.

        Args:
            options (dict, optional): Options à appliquer. Defaults to None.
                - type (int | str): Type de polygones :
                    - 'polygon' or 1 : Polygones. (default)
                    - 'rectangle' or 0 : Rectangles.
                    - 'simple' or 2 : Polygones.
                    - 'convex' or 3 : Polygones convexes.

                - count (int): Nombre de polygones à générer. (default to 3) Doit être supérieur à 0.
                - form (dict): Contraintes sur les polygones.
                    - min_vertices_count (int): Nombre de sommets minimal. (default to 3)
                    - max_vertices_count (int): Nombre de sommets maximal. (default to 16)

                - space (dict): Contraintes sur l'espace.
                    - space (Rectangle): Rectangle représentant l'espace dans lequel les sommets du polygone seront tirés au hasard. (default to (1280 x 720))
                    - divisions (int, int): Nombre de divisions récursives verticales et horizontales de l'espace. (default to (2, 2))

                    Attention ! Ces nombres devront être cohérents avec le nombre de polygones à générer. Par exemple, si le nombre de polygones à générer est égal à 16 alors si le nombre de divisions est nul, l'espace sera divisé en 16.

        Returns:
            Collection: Collection aléatoire de polygones.
        """

        def check_options(user_options):
            """
            Crée et valide un dictionnaire d'options basé sur les entrées de l'utilisateur et les contraintes.

            Args:
                user_options (dict): Dictionnaire d'options fourni par l'utilisateur.

            Returns:
                dict: Dictionnaire d'options validé.
            """

            def validate_options(given_options):
                """
                Valide les options en fonction des contraintes.

                Args:
                    given_options (dict): Dictionnaire d'options.

                Raises:
                    ValueError: Si une des contraintes n'est pas respectée.
                """
                valid_types = ['polygon', 'rectangle', 'simple', 'convex', 1, 0, 2, 3]
                if 'type' in given_options and given_options['type'] not in valid_types:
                    raise ValueError("Type invalide. Valeurs possibles : 'polygon', 'rectangle', 'simple', 'convex', "
                                     "1, 0, 2, 3.")

                if 'count' in given_options and (
                        not isinstance(given_options['count'], int) or given_options['count'] <= 0):
                    raise ValueError("Nombre de polygones invalide. count doit être supérieur à 0.")

                if 'form' in given_options:
                    if 'min_vertices_count' in given_options['form'] and (
                            not (isinstance(given_options['form']['min_vertices_count'], int) and not (
                                    given_options['form']['min_vertices_count'] < 3))):
                        raise ValueError("min_vertices_count invalide. Doit être un entier supérieur ou égal à 3.")

                    if 'max_vertices_count' in given_options['form'] and (
                            not (isinstance(given_options['form']['max_vertices_count'], int) and not (
                                    given_options['form']["max_vertices_count"] < 3))):
                        raise ValueError("max_vertices_count invalide. Doit être un entier supérieur ou égal à 3.")

                if 'space' in given_options:
                    if ('space' in given_options['space'] and given_options['space']['space'] is not None and
                            not isinstance(given_options['space']['space'], Rectangle)):
                        raise ValueError("space invalide. Doit être une instance de Rectangle.")

                    if 'divisions' in given_options['space'] and (
                            not (isinstance(given_options['space']['divisions'], tuple) and
                                 given_options['space']['divisions'][0] >= 0 and
                                 given_options['space']['divisions'][1] >= 0)):
                        raise ValueError("divisions invalide. Doit être un tuple d'entiers supérieurs ou égaux à 0.")

            # Valeurs par défaut
            default_options = {
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

            if user_options is None:
                return default_options

            # Mise à jour des options par défaut avec les options de l'utilisateur
            default_options.update(user_options)

            # Vérification des options
            validate_options(default_options)

            return default_options

        def generate_polygon(form, space, polygon_type):
            """
            Retourne un polygone aléatoire en fonction du type demandé.

            Args:
                form (int, int): Limites (min, max) du nombre de sommets du polygone. (max ≥ min ≥ 3)
                space (Rectangle): Espace dans lequel les points du polygone sont tirés.
                polygon_type (int | str): Type de polygones :
                    - 'polygon' or 1 : Polygones.
                    - 'rectangle' or 0 : Rectangles.
                    - 'simple' or 2 : Polygones.
                    - 'convex' or 3 : Polygones convexes.

            Returns:
                Polygon | Rectangle: Polygone généré aléatoirement.

            Raises:
                AssertionError: Contraintes sur le paramètre space non respectées.
                ValueError: Contraintes sur le paramètre polygon_type non respectées.
            """
            assert isinstance(space, Rectangle), "space doit être une instance de Rectangle !"

            vertices_count = random.randint(form['min_vertices_count'], form['max_vertices_count'])

            match polygon_type:
                case 0 | 'polygon':
                    return Polygon.random(space, vertices_count)
                case 1 | 'rectangle':
                    return Rectangle.random(space)
                case 2 | 'simple':
                    return Polygon.random(space, vertices_count, simplify=True)
                case 3 | 'convex':
                    return Polygon.random(space, vertices_count, simplify=True)
                case _:
                    raise ValueError("Type de polygone inconnu ")

        def generate_polygons(count, polygon_type, form, space, divisions):
            """
            Retourne une collection de polygones générés aléatoirement.

            Args:
                count (int): Nombre de polygones à générer. (≥ 0)
                polygon_type (int | str): Type de polygones :
                    - 'polygon' or 1 : Polygones.
                    - 'rectangle' or 0 : Rectangles.
                    - 'simple' or 2 : Polygones.
                    - 'convex' or 3 : Polygones convexes.

                form (dict): Contraintes sur les polygones.
                    - min_vertices_count (int): Nombre de sommets minimal.
                    - max_vertices_count (int): Nombre de sommets maximal.

                space (Rectangle): Rectangle représentant l'espace dans lequel les sommets du polygone seront tirés au hasard.
                divisions (int, int): Nombre de divisions récursives verticales et horizontales de l'espace.

            Returns:
                Collection contenant les polygones.
            """
            if count == 0:
                return Collection()

            polygon = generate_polygon(form, space, polygon_type)
            if count == 1:
                return Collection([polygon])
            count -= 1

            # S'il reste des polygons à générer.
            polygon_lir = polygon.largestinteriorrectangle()

            # Divisions de l'espace
            subspaces = polygon_lir / divisions
            # Nombre de polygones par division
            subdivision_polys_count = (count % (divisions[0] * divisions[1])
                                       + count // (divisions[0] * divisions[1]))

            collection = Collection([polygon])
            for subspaces_line in subspaces:
                for subspace in subspaces_line:
                    collection += generate_polygons(subdivision_polys_count, polygon_type, form, subspace, divisions)

                    count -= subdivision_polys_count
                    if count <= 0:
                        return collection

            return collection

        # Vérification des options
        options = check_options(options)

        if options['space']['space'] is None:
            # noinspection PyTypedDict
            options['space']['space'] = Rectangle(Vertice(), cls.DEFAULT_RANDOM_SPACE_LENGTH,
                                                  cls.DEFAULT_RANDOM_SPACE_WIDTH)

        # noinspection PyTypeChecker
        return generate_polygons(options['count'], options['type'], options['form'],
                                 options['space']['space'], options['space']['divisions'])
