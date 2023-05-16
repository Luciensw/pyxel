# AJOUTER BONUS DEPLACEMENT + REGLER VALEURS

import pyxel, random

TRANSPARENT_COLOR = 0
TUILE_ASTEROID =(2,1)
TUILE_ESPACE =(2,4)
TUILE_BONUS = (1,2)
TUILE_MUNITION = (1,3)
TUILE_MONSTRE = (2,2)
DIFFICULTE = 1

class Jeu:
    def __init__(self):
        # taille de la fenetre 128x128 pixels
        pyxel.init(128, 128, title="Nuit du c0de", quit_key=pyxel.KEY_G)

        # position initiale du vaisseau (x = 0, y = 0 : coin haut gauche)
        self.vaisseau_x = 60
        self.vaisseau_y = 60

        # vies
        self.vies = 3

        # bouclier
        self.bouclier = False
        
        #score
        self.score = 0

        #munition
        self.munition = 10

        # initialisation des tirs
        self.tirs_liste = []

        # initialisation des ennemis
        self.ennemis_liste = []

        # initialisation des explosions
        self.explosions_liste = []
        
        # initialisation des explosions
        self.asteroid_liste = []

        # initialisation des bonus
        self.bonus_liste = []

        # chargement des images
        pyxel.load("images.pyxres")
        pyxel.image(0).rect(16, 16, 8, 8, TRANSPARENT_COLOR)
        
        self.scroll_y = 1080

        pyxel.run(self.update, self.draw)
       
        
    def deplacement(self):
        """déplacement avec les touches de directions : zqsd"""

        if pyxel.btn(pyxel.KEY_D) and self.vaisseau_x<120:
            self.vaisseau_x += 1.25
        if pyxel.btn(pyxel.KEY_Q) and self.vaisseau_x>0:
            self.vaisseau_x += -1.25
        if pyxel.btn(pyxel.KEY_S) and self.vaisseau_y<120:
            self.vaisseau_y += 1.25
        if pyxel.btn(pyxel.KEY_Z) and self.vaisseau_y>0:
            self.vaisseau_y += -1.25
        if pyxel.btn(pyxel.KEY_F):
            self.bouclier = not self.bouclier


    def tirs_creation(self):
        """création d'un tir avec la barre d'espace"""
        if self.munition > 0:
            if pyxel.btnr(pyxel.KEY_SPACE):
                self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8])
                self.munition -= 1


    def tirs_deplacement(self):
        """déplacement des tirs vers le haut et suppression quand ils sortent du cadre"""

        for tir in  self.tirs_liste:
            tir[1] -= 1
            if  tir[1]<-8:
                self.tirs_liste.remove(tir)


    def bonus_creation(self):
        if (pyxel.frame_count % 300*DIFFICULTE == 0):
            self.bonus_liste.append([random.randint(8, 120), -8, random.randint(0, 1)])


    def bonus_deplacement(self):
        for bonus in self.bonus_liste:
            bonus[1] += 1
            if  bonus[1]> 136:
                self.bonus_liste.remove(bonus)


    def ennemis_creation(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % 30 == 0):
            self.ennemis_liste.append([random.randint(0, 120), 0])


    def ennemis_deplacement(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""              

        for ennemi in self.ennemis_liste:
            ennemi[1] += 1
            if  ennemi[1]>128:
                self.ennemis_liste.remove(ennemi)


    def vaisseau_suppression(self):
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:
            if ennemi[0] <= self.vaisseau_x+8 and ennemi[1] <= self.vaisseau_y+8 and ennemi[0]+8 >= self.vaisseau_x and ennemi[1]+8 >= self.vaisseau_y and not self.bouclier:
                self.ennemis_liste.remove(ennemi)
                self.vies -= 1
                # on ajoute l'explosion
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)


    def ennemis_suppression(self):
        """disparition d'un ennemi et d'un tir si contact"""

        for ennemi in self.ennemis_liste:
            for tir in self.tirs_liste:
                if ennemi[0] <= tir[0]+8 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1]:
                    self.ennemis_liste.remove(ennemi)
                    self.tirs_liste.remove(tir)
                    self.explosions_creation(ennemi[0], ennemi[1])
                    self.score += 5


    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            
            explosion[2] +=1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    def scroll(self):
        if self.scroll_y>0:
            self.scroll_y -= 1
        else :
            self.scroll_y =1080
        self.apparition_ennemi(self.scroll_y,self.scroll_y+1)
            

    def detect_collision_aster(self):
        y = self.vaisseau_y+self.scroll_y
        x1 = self.vaisseau_x // 8
        y1 = y // 8
        x2 = (self.vaisseau_x + 8 - 1) // 8
        y2 = (y + 8 - 1) // 8
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                tuile = pyxel.tilemap(0).pget(xi, yi)
                if tuile == TUILE_ASTEROID and not self.bouclier:
                    print("asteroid")
                    self.vies -= 1
                    pyxel.tilemap(0).pset(xi, yi, TUILE_ESPACE)
                    self.explosions_creation(xi*8, self.vaisseau_y)
                    return xi*8, yi*8
                
    def apparition_ennemi(self,y1, y2):
         yt1 = pyxel.floor(y1 / 8)
         yt2 = pyxel.ceil(y2 / 8)
         
         for y in range(yt1, yt2 + 1):
             for x in range(16):
                 tuile = pyxel.tilemap(0).pget(x, y)
                 if tuile == TUILE_MONSTRE:
                     pyxel.tilemap(0).pset(x, y, TUILE_ESPACE)
                     self.ennemis_liste.append([x*8,y*8-y1])
                
                   
    
    def detect_bonus(self):
        for bonus in self.bonus_liste:
            if bonus[0] <= self.vaisseau_x+8 and bonus[1] <= self.vaisseau_y+8 and bonus[0]+8 >= self.vaisseau_x and bonus[1]+8 >= self.vaisseau_y:
                if bonus[2] == 0:
                    if self.vies < 5:
                        self.vies += 1
                else:
                    self.munition += 10
                self.bonus_liste.remove(bonus)

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()

        # creation des tirs en fonction de la position du vaisseau
        self.tirs_creation()
        
        self.detect_collision_aster()
        
        self.detect_bonus()

        # mise a jour des positions des tirs
        self.tirs_deplacement()

        # creation des ennemis
        #self.ennemis_creation()

        # mise a jour des positions des ennemis
        self.ennemis_deplacement()

        # suppression des ennemis et tirs si contact
        self.ennemis_suppression()

        # suppression du vaisseau et ennemi si contact
        self.vaisseau_suppression()

        # evolution de l'animation des explosions
        self.explosions_animation()

        # creation et déplacement des bonus
        self.bonus_creation()
        self.bonus_deplacement()
        
        self.scroll()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
       


        # si le vaisseau possede des vies le jeu continue
        if self.vies > 0:

            pyxel.camera()
           
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y,  128, 128, TRANSPARENT_COLOR)
            
            #affichage score
            pyxel.text(5, 5, f"SCORE : {self.score}", 7)

            #affichage munitions
            pyxel.text(5, 120, f"Munitions : {self.munition}", 7)

            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)


            # affichage des vies
            if self.vies < 5 :
                pyxel.text(100, 5, 'VIES:'+ str(self.vies), 7)
            if self.vies == 5:
                pyxel.text(80, 5, 'VIES:'+ str(self.vies)+'(Max)', 7)

            # vaisseau (carre 8x8)
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8, TRANSPARENT_COLOR)

            if self.bouclier:
                pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 32, 0, 8, 8, TRANSPARENT_COLOR)

            # tirs
            for tir in self.tirs_liste:
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)

            # ennemis
            for ennemi in self.ennemis_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8)

            # bonus
            for bonus in self.bonus_liste:
                if bonus[2] == 0:
                    pyxel.blt(bonus[0], bonus[1], 0, 8, 16, 8, 8)
                else:
                    pyxel.blt(bonus[0], bonus[1], 0, 8, 24, 8, 8)

            pyxel.image(0).rect(16, 16, 8, 8, TRANSPARENT_COLOR)

            
        # sinon: GAME OVER
        else:
            pyxel.camera(0, self.scroll_y)
            pyxel.text(50,64+self.scroll_y, 'GAME OVER', 7)

Jeu()
