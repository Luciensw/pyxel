import pyxel


def draw_rect(x,y,w,h,c):
    pyxel.rect(x-w/2,y-h/2,w,h,c)

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.raquette_a = 64
        self.raquette_b = 64
        self.raquette_w = 4
        self.raquette_h = 16
        self.balle_x = 64
        self.balle_y = 64

        # chargement des images
        pyxel.load("res.pyxres")

        pyxel.run(self.update, self.draw)
       
        
        


    def deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.raquette_b<128-self.raquette_h/2:
            self.raquette_b += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.raquette_b>0+self.raquette_h/2:
            self.raquette_b += -1
        if pyxel.btn(pyxel.KEY_DOWN) and self.raquette_a<128-self.raquette_h/2:
            self.raquette_a += 1
        if pyxel.btn(pyxel.KEY_UP) and self.raquette_a>0+self.raquette_h/2:
            self.raquette_a += -1

    def collision_balle(self):
        if self.balle_y < self.raquette_a and self.balle_y > self.raquette_a-self.raquette_h:
            pyxel.quit()
            


    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()
        self.collision_balle()


    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""
        pyxel.cls(0)
        pyxel.camera()
        draw_rect(20, self.raquette_a, self.raquette_w, self.raquette_h, 5)
        draw_rect(108, self.raquette_b, self.raquette_w, self.raquette_h, 4)
        draw_rect(self.balle_x, self.balle_y, 8, 8, 1)


Jeu()