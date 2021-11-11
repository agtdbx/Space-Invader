import pygame as pg

class Projectile():
    """
    Classe réprésentant nos projectiles
    """

    def __init__(self, x, y):
        """
        Ce qui ce passe lors de la création du projecile
        """
        self._x = x
        self._y = y
        self._width = 7
        self._height = 30
        self._vitesse = 35


    def draw(self, fen):
        """
        Méthode gérant l'affichage du projectile
        """
        pg.draw.rect(fen, (255, 0, 0), (self._x, self._y, self._width, self._height))


    def move(self):
        """
        Méthode gérant le déplacement du projectile
        """
        self._y -= self._vitesse


    def get_pos(self):
        return (self._x, self._y, self._width, self._height)