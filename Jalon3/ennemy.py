import pygame as pg
import random
import time

from tir import *

class Ennemy():

    def __init__(self, x = 100, y = 100, vitesse = 10, typ = 1):
        """
        Ce qui ce passe lors de la création de l'ennemi
        """
        self._x = x
        self._y = y
        self._vitesse = vitesse
        self._typ = typ
        self._alive = True

        if self._typ == 1: # Selon le type d'ennemy, on change la taille, le nombre de point, le nombre de vie
            self._width = 110
            self._height = 80
            self._life = 1
            self._score = 10
            self._sprite = pg.image.load("images/Ennemy1.png").convert_alpha()

        elif self._typ == 2:
            self._width = 120
            self._height = 80
            self._life = 3
            self._score = 30
            self._sprite = pg.image.load("images/Ennemy2.png").convert_alpha()

        elif self._typ == 3:
            self._width = 80
            self._height = 80
            self._life = 1
            self._cycle = random.randint(3, 10)
            self._last = 0
            self._score = 20
            self._sprite = pg.image.load("images/Ennemy3.png").convert_alpha()

        elif self._typ == 4:
            self._width = 240
            self._height = 105
            self._life = 5
            self._cycle = 2
            self._last = 0
            self._score = 150
            self._sprite = pg.image.load("images/Ennemy4.png").convert_alpha()

        elif self._typ == 5:
            self._width = 130
            self._height = 200
            self._life = 5
            self._score = 100
            self._sprite = pg.image.load("images/Ennemy5.png").convert_alpha()


    def draw(self, fen):
        """
        Méthode gérant l'affichage de l'ennemi
        """
        fen.blit(self._sprite, (self._x, self._y), ((self._life-1)*self._width, 0, self._width, self._height))



    def tir(self, list_projectile_ennemy):
        """
        Méthode gérant le tir du ennemi de type 3
        """
        if time.time() - self._last >= self._cycle:
            self._last = time.time()
            if self._typ == 3:
                p = Projectile(self._x + self._width//2, self._y + self._height, -10, (255, 255, 255))
                list_projectile_ennemy.append(p)
            elif self._typ == 4:
                p1 = Projectile(self._x + 70, self._y + self._height, -10, (255, 255, 255))
                p2 = Projectile(self._x + 250, self._y + self._height, -10, (255, 255, 255))
                list_projectile_ennemy.extend([p1, p2])
        return list_projectile_ennemy



    def move(self, fen_size):
        """
        Méthode gérant le déplacement de l'ennemi
        """
        if self._typ < 5:
            if self._x + self._width > fen_size[0]:
                self._vitesse *= -1
                self._y += fen_size[1]//10

            elif self._x < 0:
                self._vitesse *= -1
                self._y += fen_size[1]//10

            self._x += self._vitesse
        else:
            self._y += self._vitesse


    def collid(self, entity):
        """
        Méthode gérant la collision entre l'ennemi et une entité (projectile ou joueur)
        """
        rect = pg.Rect(self._x, self._y, self._width, self._height) # On créer un rectangle représentant la hitbox de l'entité

        return rect.colliderect(entity.get_pos()) # On vérifie la collision via la méthode colliderect -> renvois True s'il y a collision


    def touch(self):
        """
        Méthode gérant les actions lié au fait que l'ennemy soit touché
        """
        self._life -= 1
        if self._life == 0:
            self._alive = False


    def is_alive(self):
        """
        Méthode nous disant si l'ennemy est en vie
        """
        return self._alive


    def getScore(self):
        """
        Méthode nous donnant le score de l'ennemy
        """
        return self._score


    def getType(self):
        """
        Méthode nous donnant le type de l'ennemy
        """
        return self._typ


    def get_pos(self):
        """
        Méthode nous donnant la position et la taille de l'ennemy
        """
        return (self._x, self._y, self._width, self._height)
