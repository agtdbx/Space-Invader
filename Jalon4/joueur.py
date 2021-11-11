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
        self._max_life = 3
        self._alive = True # Si le joueur est vivant
        self._sprite = pg.image.load("images/Perso.png").convert_alpha() # L'image de notre joueur || Le .convert_alpha() sert à enlever la transparence d'une image. Pygame à beaucoup de mal avec ça alors ça nous fait gagner beaucoup de perf
        self._sonTir = pg.mixer.Sound("sons/tir.wav") # Le son lorsqu'on tire
        self._boost = []
        self._last_boost = time.time()
        self._boost_speed = False
        self._boost_shield = False
        self._boost_multi_fire = False
        self._boost_coldown_fire = False
        self._shield_sprite = pg.image.load("images/shield.png").convert_alpha()
        self._degat = False
        self._last_degat = 0


    def draw(self, fen):
        """
        Méthode gérant l'affichage du joueur
        """
        if not self._degat:
            fen.blit(self._sprite, (self._x, self._y), (self._width, 0, self._width, self._height)) # Affichage de l'image
            if self._boost_shield:
                fen.blit(self._shield_sprite, (self._x-8, self._y-30))
        else:
            if time.time() - self._last_degat > 0.1:
                self._degat = False
            fen.blit(self._sprite, (self._x, self._y), (0, 0, self._width, self._height))
            if self._boost_shield:
                fen.blit(self._shield_sprite, (self._x-8, self._y-30))


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
        if not self._boost_coldown_fire:
            if  time.time() - self._time >= self._coldown: # Si le temps est supérieur au coldown, on peut tirer
                self._sonTir.play() # On joue le son du tir
                self._time = time.time() # On défini a nouveau l'attribut temps pour éviter les tirs à répétitions
                if not self._boost_multi_fire:
                    if not self._boost_speed:
                        p = Projectile(self._x + self._width//2, self._y) # On creer un projectile
                        projectiles.append(p) # On l'ajoute à la liste des projectiles
                    else:
                        p = Projectile(self._x + self._width//2, self._y, 70)
                        projectiles.append(p)
                else:
                    if not self._boost_speed:
                        p1 = Projectile((self._x + self._width//2)-15, self._y)
                        p2 = Projectile((self._x + self._width//2)+15, self._y)
                        projectiles.extend([p1, p2])
                    else:
                        p1 = Projectile((self._x + self._width//2)-15, self._y, 70)
                        p2 = Projectile((self._x + self._width//2)+15, self._y, 70)
                        projectiles.extend([p1, p2])
        else:
            if  time.time() - self._time >= self._coldown/2:
                self._sonTir.play()
                self._time = time.time()
                if not self._boost_multi_fire:
                    if not self._boost_speed:
                        p = Projectile(self._x + self._width//2, self._y)
                        projectiles.append(p)
                    else:
                        p = Projectile(self._x + self._width//2, self._y, 70)
                        projectiles.append(p)
                else:
                    if not self._boost_speed:
                        p1 = Projectile((self._x + self._width//2)-15, self._y)
                        p2 = Projectile((self._x + self._width//2)+15, self._y)
                        projectiles.extend([p1, p2])
                    else:
                        p1 = Projectile((self._x + self._width//2)-15, self._y, 70)
                        p2 = Projectile((self._x + self._width//2)+15, self._y, 70)
                        projectiles.extend([p1, p2])
        return projectiles


    def touch(self):
        """
        Méthode gérant le fait d'être touché par un ennemi
        """
        if not self._boost_shield:
            self._life -= 1
            self._last_degat = time.time()
            self._degat = True
            if self._life == 0:
                self._alive = False
        else:
            for b in self._boost:
                if b[0] == "shield":
                    b[1] = 0


    def regen(self):
        """
        Méthode gérant la régération de vie du joueur après avoir tué la soucoupe
        """
        self._life += 1
        if self._life > self._max_life:
            self._life = self._max_life


    def is_alive(self):
        """
        Méthode nous disant si le joueur est un vie
        """
        return self._alive


    def getLife(self):
        """
        Méthode nous donnant le nombre de vie du joueur
        """
        return self._life


    def get_pos(self):
        """
        Méthode nous donnant la position du joueur
        """
        return (self._x, self._y, self._width, self._height)


    def get_boost(self):
        """
        Méthode nous donnant les boosts actifs sur le joueur
        """
        return self._boost


    def set_volume_fire(self, volume):
        """
        Méthode permettant de changer le volume du son des tirs
        """
        self._sonTir.set_volume(volume/100)


    def ajouter_boost(self, boost):
        """
        Méthode gérant l'ajout d'un boost pour le joueur
        boost : [nom, durée]
        """
        est_dedans = False
        for b in self._boost:
            if b[0] == boost[0]:
                b[1] = boost[1]
                est_dedans = True

        if not est_dedans:
            self._boost.append(boost)


    def update_boost(self):
        """
        Méthode gérant les boost du joueur
        """
        if time.time() - self._last_boost > 0.1:
            self._last_boost = time.time()
            delete_boost = set()
            self._boost_speed = False
            self._boost_shield = False
            self._boost_multi_fire = False
            self._boost_coldown_fire = False
            for i in range(len(self._boost)):
                b = self._boost[i]
                if  b[0] == "speed":
                    self._boost_speed = True
                elif b[0] == "shield":
                    self._boost_shield = True
                elif b[0] == "multi-fire":
                    self._boost_multi_fire = True
                elif b[0] == "coldown-fire":
                    self._boost_coldown_fire = True
                b[1] -= 1
                if b[1] <= 0:
                    delete_boost.add(i)

            i = 0
            for b in delete_boost:
                self._boost.pop(b - i)
                i += 1
