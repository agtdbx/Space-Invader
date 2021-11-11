#Importation des librairies
import pygame as pg
import sys

# Imporation des autres fichiers du programme
from joueur import *
from tir import *
from ennemy import *


class Jeu:
    """
    Classe réprésantant notre jeu
    """
    def __init__(self):
        """
        Cette méthode permet de définir les variables globales du programme
        """
        pg.init() # Initialisation de pygame
        pg.mouse.set_visible(False) #On fait disparaitre la soire pour plus de confort

        infoObject = pg.display.Info() # On récupère la taille de l'écran
        self.screen_size = ((infoObject.current_w, infoObject.current_h - 63)) # On soustrait la taille de la barre de tâche en bas
        self.screen  = pg.display.set_mode(self.screen_size, pg.RESIZABLE) # On créer la fenêtre

        self.clock = pg.time.Clock() # Permet d'imposer une limite de fps
        self.fps = 60

        pg.mixer.music.load("sons/Context Sensitive - 20XX - 09 Cerulean.mp3") #Importaion de la musique de fonds
        pg.mixer.music.play(-1) # On dit a la musique de jouer indéfiniment
        pg.mixer.music.set_volume(0.8) # On règle le volume de la musique

        self.vie = pg.image.load("images/vie.png").convert_alpha() # Importation de l'image représentant la vie du joueur
        self.sonExplosion = pg.mixer.Sound("sons/explosion.wav") # Importation du son de l'explosion d'un ennemie

        self.runJeu = True #Variable pour faire tourner la boucle du jeu

        self.perso = Joueur(self.screen_size) # On créer notre joueur
        self.projectiles = [] # La liste de projectiles
        self.ennemies = [] # D'ennemies
        self.nb_ennemy = 5 # Le nombre d'ennemie
        self.score = 0 # Et enfin le score


    def run(self):
        """
        Cette méthode permet de définir la boucle principale du jeu
        """
        while self.runJeu: # Boucle pour le jeu
            self.input()
            self.tick()
            self.render()
            self.clock.tick(self.fps)

        pg.mouse.set_visible(True)

        while True: # Boucle pour l'affichage du score
            self.input()
            self.screen.fill((0, 0, 0))
            self.draw_text((self.screen_size[0]-120)//2, (self.screen_size[1]-30)//2, str(self.score), font_size = 50, color = (0, 200, 0))
            pg.display.update()


    def input(self):
        """
        Cette méthode perrmet de gérer les entrées du programme (clic de sourie, appuie de touche)
        """
        for event in pg.event.get(): # On dit à notre programme de tout arrêter quand on appuie sur la croix en haut à droite
            if event.type == pg.QUIT:
                self.quit()
        self.key = pg.key.get_pressed()
        self.key2 = pg.mouse.get_pressed()


    def tick(self):
        """
        C'est dans cette méthode que vont s'effectuer tous les calculs des différents éléments de notre programme.
        Par exemple, quand on appuie sur la touche [Flèche gauche], c'est ici qu'on va calculer nle déplacement du joueur
        """
        if self.key[pg.K_RIGHT]: # Si la touche [Flèche droite] est pressé, on execute le code suivant
            self.perso.move("R", self.screen_size)

        if self.key[pg.K_LEFT]:
            self.perso.move("L", self.screen_size)

        if self.key[pg.K_UP]:
            self.projectiles = self.perso.fire(self.projectiles)

        delete_ennemy = set() # On créer des ensembles pour stocker les ennemies qui vont disparaitre lors de ce passage. On utilise un ensemble pour éviter de supprimer plusieurs fois le même ennemie, ce que ferai planter le programme
        delete_projectile = set()

        touch = False # Pour vérifier si le joueur est touché

        if len(self.ennemies) == 0: # S'il n'y a plus d'ennemie, on en fait réaparaitre
            if self.nb_ennemy < 40:
                self.nb_ennemy += self.nb_ennemy//3 # On augmente le nombre d'ennemie pour augmenter la difficulter (Mais on limite à 40 pour éviter que ce soit infasable)
            self.spawn_ennemie()

        for i in range(len(self.ennemies)): # Pour tout les ennemies
            ennemy = self.ennemies[i]
            ennemy.move(self.screen_size) # On les fait bouger
            if ennemy.collid(self.perso): # On vérifie s'il touche le joueur
                self.perso.touch()
                touch = True
                break
            for j in range(len(self.projectiles)):
                p = self.projectiles[j]
                if ennemy.collid(p): #On vérifie parmi les projectiles si y'en a un qui touche l'ennemie
                    self.sonExplosion.play() #On joue le son de l'explosion
                    self.score += ennemy.getScore()
                    delete_ennemy.add(ennemy) # On dit qu'il faut supprimer cet ennemie puisqu'il est mort
                    delete_projectile.add(p) #Si le projectile touche un ennemie, il disparait (C'est trop peté sinon)
                    break

        if touch: # Si le joueur est touché, on fait disparaitre tous les ennemies puis on les fait réaparaitre en haut, avec le même nombre
            self.ennemies = []
            self.projectiles = []
            self.spawn_ennemie()
        else: # Sinon on supprimer tout les ennemies
            for ennemy in delete_ennemy:
                self.ennemies.remove(ennemy)

        for i in range(len(self.projectiles)): #Même démarche que pour les ennemies
            p = self.projectiles[i]
            p.move()
            size = p.get_pos()
            if size[1]- size[3] < 0: # Si le projectile sort de l'écran, il disparait
                delete_projectile.add(p)

        for p in delete_projectile:
            self.projectiles.remove(p)


        if not self.perso.is_alive(): # Si le joueur n'est plus en vie, alors
            self.runJeu = False


    def render(self): # appel à d'autres fonctions self.render_*() pour l'affichage
        """
        C'est cette méthode qui va gérer l'affichage. Les élements du programme ont déjà bouger, maintenant il ne reste plus qu'à les afficher à l'écran
        """
        self.screen.fill((0, 0, 0)) # On affiche un écran noir pour effacer tous les autres dessins du précédents passage

        self.draw_text(20, 20, "SCORE", color = (255, 255, 255)) # On affiche le score
        self.draw_text(100, 20, str(self.score), color = (0, 200, 0))

        self.draw_text(self.screen_size[0]-240, 20, "LIVES", color = (255, 255, 255)) # Les vies
        self.screen.blit(self.vie, (self.screen_size[0]-165, 16), (0, 0, 50*self.perso.getLife(), 20))

        self.perso.draw(self.screen) # On affiche le joueur

        for ennemy in self.ennemies: # Les ennemies
            ennemy.draw(self.screen)

        for tir in self.projectiles: # Les projectiles
            tir.draw(self.screen)

        pg.display.update() # On update, c'est à dire qu'on applique tous les changements précédents à la fenêtre


    def quit(self):
        """
        C'est la méthode, qui va s'executer lorsqu'on veut arrêter le programme
        """
        pg.quit() # On quite pygame
        sys.exit()


    def draw_text(self, x = 0, y = 0, text = "", font_size = 30, font = "comicsans", color = (0, 0, 0)):
        """
        C'est une méthode permetant d'afficher simplement du texte
        On prends en paramètre la position (x, y), le texte à afficher, la taille de la police, la police voulu, et la couleur du texte
        """
        font1 = pg.font.SysFont(font, font_size)
        text1 = font1.render(text, 1, color)
        self.screen.blit(text1, (x, y))


    def spawn_ennemie(self):
        """
        Cette méthode s'occupe de faire apparaitre les ennemies
        """
        x = 0
        y = 1
        sens = 1
        for i in range(self.nb_ennemy):
            if sens == 1:
                ennemy = Ennemy(x * 150, y * self.screen_size[1]//10, 10) # On fait en sorte que les ennemies apparaissent en fonctions de leur mouvement (de droite à gauche, puis en descend d'un cran, de gauche à droite et ainsi de suite)
            else:
                ennemy = Ennemy(x * 150, y * self.screen_size[1]//10, -10)
            self.ennemies.append(ennemy)
            x += sens
            if x * 150 > self.screen_size[0] - 150: # On vérifie si on peut mettre un ennemie sont sortir de la fenêtre. Si c'est pas le cas, on descend d'un cran qui on change de sens
                sens = -1
                x += sens
                y += 1
            elif x == 0 and sens == -1:
                sens = 1
                y += 1


Jeu().run() # On lance le jeu