import pygame as pg
import time


class Animation:
    """
    La classe de nos animations
    """

    def __init__(self, pos, score):
        """
        Méthode créant notre animation. Prends le centre de l'animation en paramètre x et y
        Le paramètre score permet d'afficher le score dans l'animation
        """
        self._x = pos[0]
        self._y = pos[1]
        self._width = 100
        self._height = 100
        self._score = score
        self._last = time.time()
        self._nb_image = 0
        self._nb_max_image = 8
        self._sprite = pg.image.load('images/Explosion.png').convert_alpha()
        self._fin = False


    def draw(self, fen):
        """
        Méthode définissant l'affichage de notre animation
        """
        font1 = pg.font.SysFont('comicsans', 40)
        text1 = font1.render(str(self._score), 1, (255, 255, 255))
        placement = text1.get_rect(center=(self._x, self._y))
        fen.blit(text1, placement)
        fen.blit(self._sprite, (self._x - self._width//2, self._y - self._height//2), (self._nb_image * 100, 0, self._width, self._height))


    def next_image(self):
        """
        Méthode définissant le passage à une autre image de l'animation
        """
        if time.time() - self._last > 0.05:
            self._last = time.time()
            self._nb_image += 1
            if self._nb_image > self._nb_max_image:
                self._fin = True


    def is_fin(self):
        """
        Méthode permettant de savoir si l'animation est fini ou non
        """
        return self._fin