import pygame as pg

class Projectile():
    """
    Classe réprésentant nos projectiles
    """

    def __init__(self, x, y, vitesse = 35, color = (255, 0, 0)):
        """
        Ce qui ce passe lors de la création du projecile
        """
        self._x = x
        self._y = y
        self._width = 7
        self._height = 30
        self._vitesse = vitesse
        self._color = color


    def draw(self, fen):
        """
        Méthode gérant l'affichage du projectile
        """
        pg.draw.rect(fen, self._color, (self._x, self._y, self._width, self._height))


    def move(self):
        """
        Méthode gérant le déplacement du projectile
        """
        self._y -= self._vitesse


    def collid(self, entity):
        """
        Méthode gérant la collision entre le tir et une entité (projectile)
        """
        rect = pg.Rect(self._x, self._y, self._width, self._height) # On créer un rectangle représentant la hitbox de l'entité

        return rect.colliderect(entity.get_pos()) # On vérifie la collision via la méthode colliderect -> renvois True s'il y a collision


    def get_pos(self):
        return (self._x, self._y, self._width, self._height)