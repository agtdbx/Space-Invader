import pygame as pg
import time

from tir import *

class Joueur():
    """
    Classe réprésentant notre joueur
    """

    def __init__(self, fen_size):
        """
        Définition de ses variables
        """
        self._width = 140 # Largeur
        self._height = 70 # Hauteur
        self._x = fen_size[0]//2 - self._width//2 # Position x
        self._y = fen_size[1] - self._height - 10 # Position y
        self._vitesse = 20 # Vitesse de déplacement
        self._coldown = 0.6
        self._time = 0
        self._life = 3 # Le nombre de vie
        self._alive = True # Si le joueur est vivant
        self._sprite = pg.image.load("images/Perso.png").convert_alpha() # L'image de notre joueur || Le .convert_alpha() sert à enlever la transparence d'une image. Pygame à beaucoup de mal avec ça alors ça nous fait gagner beaucoup de perf
        self._sonTir = pg.mixer.Sound("sons/tir.wav") # Le son lorsqu'on tire


    def draw(self, fen):
        """
        Méthode gérant l'affichage du joueur
        """
        fen.blit(self._sprite, (self._x, self._y)) # Affichage de l'image


    def move(self, sens, fen_size):
        """
        Méthode gérant le déplacement du joueur
        """
        if sens == "L" and self._x >= self._vitesse: # SI la touche [flèche gauche] est touché et que le joueur peut aller à gauche, le joueur va à gauche
            self._x -= self._vitesse

        elif sens == "R" and (self._x + self._width) <= (fen_size[0] - self._vitesse):
            self._x += self._vitesse


    def fire(self, projectiles):
        """
        Méthode gérant l'action "tirer" du joueur
        """
        if  time.time() - self._time >= self._coldown: # Si le temps est supérieur au coldown, on peut tirer
            self._sonTir.play() # On joue le son du tir
            p = Projectile(self._x + self._width//2, self._y) # On creer un projectile
            projectiles.append(p) # On l'ajoute à la liste des projectiles
            self._time = time.time() # On défini a nouveau l'attribut temps pour éviter les tirs à répétitions
        return projectiles


    def touch(self):
        """
        Méthode gérant le fait d'être touché par un ennemi
        """
        self._life -= 1
        if self._life == 0:
            self._alive = False


    def is_alive(self):
        return self._alive


    def getLife(self):
        return self._life


    def get_pos(self):
        return (self._x, self._y, self._width, self._height)


    def set_volume_fire(self, volume):
        self._sonTir.set_volume(volume/100)

