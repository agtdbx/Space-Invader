import pygame as pg


class Ennemy():

    def __init__(self, x = 100, y = 100, vitesse = 10, score = 10):
        """
        Ce qui ce passe lors de la création de l'ennemi
        """
        self._x = x
        self._y = y
        self._width = 110
        self._height = 80
        self._vitesse = vitesse
        self._score = score
        self._sprite = pg.image.load("images/Ennemy.png").convert_alpha()


    def draw(self, fen):
        """
        Méthode gérant l'affichage de l'ennemi
        """
        fen.blit(self._sprite, (self._x, self._y))


    def move(self, fen_size):
        """
        Méthode gérant le déplacement de l'ennemi
        """
        if self._x + self._width > fen_size[0]:
            self._vitesse *= -1
            self._y += fen_size[1]//10

        elif self._x < 0:
            self._vitesse *= -1
            self._y += fen_size[1]//10

        self._x += self._vitesse


    def collid(self, entity):
        """
        Méthode gérant la collision entre l'ennemi et une entité (projectile ou joueur)
        """
        rect = pg.Rect(self._x, self._y, self._width, self._height) # On créer un rectangle représentant la hitbox de l'entité

        return rect.colliderect(entity.get_pos()) # On vérifie la collision via la méthode colliderect -> renvois True s'il y a collision


    def getScore(self):
        return self._score
