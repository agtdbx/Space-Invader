#Importation des librairies
import pygame as pg
import sys

# Imporation des autres fichiers du programme
from joueur import *
from tir import *
from ennemy import *
from button import *


class Jeu:
    """
    Classe réprésantant notre jeu
    """
    def __init__(self):
        """
        Cette méthode permet de définir les variables globales du programme
        """
        pg.init() # Initialisation de pygame

        infoObject = pg.display.Info() # On récupère la taille de l'écran
        self.screen_size = ((infoObject.current_w, infoObject.current_h - 63)) # On soustrait la taille de la barre de tâche en bas
        self.screen  = pg.display.set_mode(self.screen_size, pg.RESIZABLE) # On créer la fenêtre

        self.clock = pg.time.Clock() # Permet d'imposer une limite de fps
        self.fps = 60

        #Importation des réglages
        settings = None
        with open("saves/options.txt", "r") as f:
            a = f.read()
            f.close()
            settings = dict(eval(a))

        self.volumeMusique = settings["VolumeMusique"]
        self.volumeSon = settings["VolumeSon"]
        self.bind = settings["bind"]

        pg.mixer.music.load("sons/Context Sensitive - 20XX - 09 Cerulean.mp3") #Importaion de la musique de fonds
        pg.mixer.music.play(-1) # On dit a la musique de jouer indéfiniment

        pg.mixer.music.set_volume(self.volumeMusique/100) # On règle le volume de la musique

        self.vie = pg.image.load("images/vie.png").convert_alpha() # Importation de l'image représentant la vie du joueur
        self.sonExplosion = pg.mixer.Sound("sons/explosion.wav") # Importation du son de l'explosion d'un ennemie
        self.sonExplosion.set_volume(self.volumeSon/100)

        self.runJeu = True #Variable pour faire tourner la boucle du jeu
        self.runScore = True #Pour la boucle affichant le score
        self.runMenu = True #Pour celle du menu
        self.menu = 0

        self.perso = Joueur(self.screen_size) # On créer notre joueur
        self.projectiles = [] # La liste de projectiles
        self.ennemies = [] # D'ennemies
        self.nb_ennemy = 5 # Le nombre d'ennemie
        self.score = 0 # Et enfin le score


    def run(self):
        """
        Cette méthode permet de définir la boucle principale du jeu
        """
        while True:
            if self.menu >= 0:
                self.run_Menu()

            self.run_Jeu()

            self.run_Score()


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
        if self.key[self.bind_to_pygame_input(self.bind["droite"])]: # Si la touche associer à l'action droite est pressé, on execute le code suivant
            self.perso.move("R", self.screen_size)

        if self.key[self.bind_to_pygame_input(self.bind["gauche"])]:
            self.perso.move("L", self.screen_size)

        if self.key[self.bind_to_pygame_input(self.bind["tir"])]:
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
        settings = {"VolumeMusique" : self.volumeMusique, "VolumeSon" : self.volumeSon, "bind" : self.bind}
        with open("saves/options.txt", "w") as f: # gère close() automatiquement
            f.write(str(settings))

        pg.quit() # On quite pygame
        sys.exit()


    def bind_to_pygame_input(self, string):
        """
        Méthode servant à tranformer la touche sauvegardé dans self.bind en int pour savoir si elle est préssé
        """
        if string == "RIGHT":
            return pg.K_RIGHT
        elif string == "LEFT":
            return pg.K_LEFT
        elif string == "UP":
            return pg.K_UP
        elif string == "DOWN":
            return pg.K_DOWN
        elif string == "SPACE":
            return pg.K_SPACE
        else:
            return ord(string.lower())


    def draw_text(self, x = 0, y = 0, text = "", font_size = 30, font = "comicsans", color = (0, 0, 0), center = False):
        """
        C'est une méthode permetant d'afficher simplement du texte
        On prends en paramètre la position (x, y), le texte à afficher, la taille de la police, la police voulu, et la couleur du texte
        """
        if center:
            font1 = pg.font.SysFont(font, font_size)
            text1 = font1.render(text, 1, color)
            placement = text1.get_rect(center=(x, y))
            self.screen.blit(text1, placement)
        else:
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


    def pageMenu0(self, buts):
        """
        Méthode servant à faire notre première page du menu
        """
        self.draw_text(self.screen_size[0]//2, 50, "Space invader", 80, color = (255, 255, 255), center = True)

        for i in range(0, 3):
            but = buts[i]

            but.draw(self.screen)
            if (but.click(self.key2) and i == 0): # On le clique du premier bouton
                self.runMenu = False # Je met runMenu à false pour quitter le menu
                pg.time.wait(150) # Je met un temps d'attente pour éviter que le clique nous fasse appuyer sur plusieurs boutons d'un coup

            if (but.click(self.key2) and i == 1):
                self.menu = 1
                pg.time.wait(150)

            if (but.click(self.key2) and i == 2):
                self.quit()


    def pageMenu1(self, buts, touche_a_bind):
        """
        Méthode servant à faire notre deuxième page du menu
        """
        self.draw_text(self.screen_size[0]//2, 50, "Options", 80, color = (255, 255, 255), center = True)

        self.draw_text(self.screen_size[0]//2, 170, "Volume de la musique", 40, color = (255, 255, 255), center = True)
        self.draw_text(self.screen_size[0]//2, 210, str(self.volumeMusique)+"%", 35, color = (255, 255, 255), center = True)

        self.draw_text(self.screen_size[0]//2, 285, "Volume des effets sonores", 40, color = (255, 255, 255), center = True)
        self.draw_text(self.screen_size[0]//2, 325, str(self.volumeSon)+"%", 35, color = (255, 255, 255), center = True)

        self.draw_text(self.screen_size[0]//2, 400, "Configuration des touches", 40, color = (255, 255, 255), center = True)
        self.draw_text(self.screen_size[0]//2-180, 429, "Aller à droite : " + self.bind["droite"], 35, color = (255, 255, 255))
        self.draw_text(self.screen_size[0]//2-180, 469, "Aller à gauche : " + self.bind["gauche"], 35, color = (255, 255, 255))
        self.draw_text(self.screen_size[0]//2-180, 509, "Tirer : " + self.bind["tir"], 35, color = (255, 255, 255))

        for i in range(3, len(buts)):
            but = buts[i]
            but.draw(self.screen)
            if (but.click(self.key2) and i == 3):
                self.menu = 0
                pg.time.wait(150)

            elif (but.click(self.key2) and i == 4 and self.volumeMusique >= 10): # Si le volume de la musique peut être baissé
                self.volumeMusique -= 10 # On baisse le volume
                pg.mixer.music.set_volume(self.volumeMusique/100) # On applique le changement (le volume de 0 à 1, c'est pour ça qu'on / par 100)
                pg.time.wait(150)

            elif (but.click(self.key2) and i == 5 and self.volumeMusique <= 90):
                self.volumeMusique += 10
                pg.mixer.music.set_volume(self.volumeMusique/100)
                pg.time.wait(150)

            elif (but.click(self.key2) and i == 6 and self.volumeSon >= 10):
                self.volumeSon -= 10
                self.sonExplosion.set_volume(self.volumeSon/100)
                self.perso.set_volume_fire(self.volumeSon)
                self.sonExplosion.play() # On joue le son pour donner un apperçu de son volume
                pg.time.wait(150)

            elif (but.click(self.key2) and i == 7 and self.volumeSon <= 90):
                self.volumeSon += 10
                self.sonExplosion.set_volume(self.volumeSon/100)
                self.perso.set_volume_fire(self.volumeSon)
                self.sonExplosion.play()
                pg.time.wait(150)

            elif (but.click(self.key2) and i == 8):
                self.menu = 2
                pg.time.wait(150)
                touche_a_bind = "droite" # On indique quelle à action on cherche à assigner une touche

            elif (but.click(self.key2) and i == 9):
                self.menu = 2
                pg.time.wait(150)
                touche_a_bind = "gauche"

            elif (but.click(self.key2) and i == 10):
                self.menu = 2
                pg.time.wait(150)
                touche_a_bind = "tir"

        return touche_a_bind


    def pageMenu2(self, buts, touche_a_bind):
        """
        Méthode servant à faire notre page pour changer de touche
        """
        self.draw_text(self.screen_size[0]//2, self.screen_size[1]//2, "Appuyer sur une touche pour l'associer à cette action", 40, color = (255, 255, 255), center = True)
        for i in range(len(self.key)):
            numTouche = self.key[i]
            if numTouche != 0:
                if i == 32:
                    touche = "SPACE" # Si la touche est espace, on affiche SPACE
                    self.bind[touche_a_bind] = touche
                elif i == 275:
                    touche = "RIGHT" # Si la touche est la flèche droite, on affiche RIGHT
                    self.bind[touche_a_bind] = touche
                elif i == 276:
                    touche = "LEFT"
                    self.bind[touche_a_bind] = touche
                elif i == 273:
                    touche = "UP"
                    self.bind[touche_a_bind] = touche
                elif i == 274:
                    touche = "DOWN"
                    self.bind[touche_a_bind] = touche
                elif 97 <= i <= 122: # Sinon, on affiche la touche en majuscule
                    touche = chr(i)
                    self.bind[touche_a_bind] = touche.upper()
                self.menu = 1
                pg.time.wait(150)


    def run_Menu(self):
        """
        Méthode de la boucle du menu
        """
        #Création des boutons
        but1 = Button((self.screen_size[0]//2, self.screen_size[1]//2-100, 130, 60), ("Jouer", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but2 = Button((self.screen_size[0]//2, self.screen_size[1]//2, 130, 60), ("Options", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but3 = Button((self.screen_size[0]//2, self.screen_size[1]//2+100, 130, 60), ("Quitter", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))

        but4 = Button((self.screen_size[0]//2, self.screen_size[1]-100, 130, 60), ("Retour", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))

        but5 = Button((self.screen_size[0]//2-45, 210, 20, 20), ("-", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but6 = Button((self.screen_size[0]//2+45, 210, 20, 20), ("+", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))

        but7 = Button((self.screen_size[0]//2-45, 325, 20, 20), ("-", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but8 = Button((self.screen_size[0]//2+45, 325, 20, 20), ("+", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))

        but9 = Button((self.screen_size[0]//2+140, 440, 95, 25), ("Changer", 30, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but10 = Button((self.screen_size[0]//2+140, 480, 95, 25), ("Changer", 30, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))
        but11 = Button((self.screen_size[0]//2+140, 520, 95, 25), ("Changer", 30, "comicsans", (255, 255, 255)), ((100, 100, 100), (150, 150, 150)))

        buts = list()
        buts.extend([but1, but2, but3, but4, but5, but6, but7, but8, but9, but10, but11])

        touche_a_bind = ""

        while self.runMenu:
            self.screen.fill((0, 0, 0))
            self.input()

            if self.menu == 0:
                self.pageMenu0(buts)

            elif self.menu == 1:
                touche_a_bind = ""
                touche_a_bind = self.pageMenu1(buts, touche_a_bind)

            elif self.menu == 2:
                self.pageMenu2(buts, touche_a_bind)

            pg.display.update()



    def run_Jeu(self):
        """
        Méthode de la boucle du jeu
        """
        pg.mouse.set_visible(False) #On fait disparaitre la soire pour plus de confort

        self.perso = Joueur(self.screen_size) # On créer notre joueur
        self.perso.set_volume_fire(self.volumeSon)
        self.projectiles = [] # La liste de projectiles
        self.ennemies = [] # D'ennemies
        self.nb_ennemy = 5 # Le nombre d'ennemie
        self.score = 0 # Et enfin le score

        self.runScore = True

        while self.runJeu: # Boucle pour le jeu
            self.input()
            self.tick()
            self.render()
            self.clock.tick(self.fps)


    def run_Score(self):
        """
        Méthode de la boucle de l'affichage du score
        """
        pg.mouse.set_visible(True)

        scores = list()
        with open("saves/scores.txt", "r") as f:
            a = f.read()
            f.close()
            scores = list(eval(a))

        scores.append(self.score)
        scores.sort(reverse = True)

        if len(scores) > 5:
            scores.pop(len(scores)-1)

        with open("saves/scores.txt", "w") as f: # gère close() automatiquement
            f.write(str(scores))

        but1 = Button((self.screen_size[0]//2, self.screen_size[1]-300, 130, 60), ("Rejouer", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (200, 200, 200)))
        but2 = Button((self.screen_size[0]//2, self.screen_size[1]-200, 130, 60), ("Menu", 40, "comicsans", (255, 255, 255)), ((100, 100, 100), (200, 200, 200)))

        while self.runScore: # Boucle pour l'affichage du score
            self.input()
            self.screen.fill((0, 0, 0))
            self.draw_text((self.screen_size[0])//2, 200, "Votre score : " + str(self.score), 50, color = (0, 200, 0), center = True)

            pg.draw.rect(self.screen, (50, 50, 50), (self.screen_size[0]//2-100, 300, 200, 50*len(scores)))

            for i in range(len(scores)):
                self.draw_text(self.screen_size[0]//2-80, 315 + i*50, str(i+1)+". "+str(scores[i]), 40, color = (255, 255, 255))

            but1.draw(self.screen)
            if (but1.click(self.key2)):
                self.runScore = False
                self.runJeu = True

            but2.draw(self.screen)
            if (but2.click(self.key2)):
                self.runScore = False
                self.runMenu = True

            pg.display.update()



Jeu().run() # On lance le jeu