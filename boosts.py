import pygame as pg
import random


class Boost:
    """
    La classe de nos boosts
    """

    def __init__(self, pos, speed, nom = "None"):
        """
        Méthode gérant la création de nos boosts
        """
        if nom == "None": # Si pas de nom préciser, on choisit au pif un nom
            liste_nom = ["speed", "shield", "multi-fire", "coldown-fire"]
            self._nom = liste_nom[random.randint(0, len(liste_nom))-1]

        else:
            self._nom = nom # Sinon on prends le nom en paramètre
        self._x = pos[0]
        self._y = pos[1]
        self._width = 50
        self._height = 50
        self._speed = speed
        self._duree = 150
        self._sprite = pg.image.load('images/boost_'+self._nom+'.png').convert_alpha()


    def draw(self, fen):
        """
        Méthode gérant l'affichage de nos boosts
        """
        fen.blit(self._sprite, (self._x + self._width//2, self._y + self._height//2))


    def move(self):
        """
        Méthode gérant le mouvement du boost
        """
        self._y += self._speed


    def get_info(self):
        """
        Méthode servant )à nous donner les informations du boost
        """
        return [self._nom, self._duree]


    def collid(self, entity):
        """
        Méthode gérant la collision entre le boost et une entité (projectile)
        """
        rect = pg.Rect(self._x + self._width//2, self._y + self._height//2, self._width, self._height) # On créer un rectangle représentant la hitbox de l'entité

        return rect.colliderect(entity.get_pos()) # On vérifie la collision via la méthode colliderect -> renvois True s'il y a collision


    def get_pos(self):
        """
        Méthode nous donnant la position du boost
        """
        return (self._x, self._y, self._width, self._height)