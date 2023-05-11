# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:42:04 2022

@author: Peio
"""

# on rajoute random
import pyxel, random

TRANSPARENT_COLOR = 0

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.raquette_a = 60
        self.raquette_b = 60
        self.balle_x = 60
        self.balle_y = 60

        # chargement des images
        pyxel.load("res.pyxres")

        pyxel.run(self.update, self.draw)
       
        
        


    def deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.raquette_b<120:
            self.raquette_b += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.raquette_b>0:
            self.raquette_b += -1
        if pyxel.btn(pyxel.KEY_DOWN) and self.raquette_a<120:
            self.raquette_a += 1
        if pyxel.btn(pyxel.KEY_UP) and self.raquette_a>0:
            self.raquette_a += -1
            


    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()

    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
       


        pyxel.camera()

            # vaisseau (carre 8x8)
        pyxel.rect(17, self.raquette_a, 6, 12, 5)
        pyxel.rect(103, self.raquette_b, 6, 12, 4)
        pyxel.rect(self.balle_x, self.balle_y, 8, 8, 1)


Jeu()