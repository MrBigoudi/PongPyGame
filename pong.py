import pygame
from pygame.locals import *

def afficheScore(s1, s2):
    """ Affiche les scores du joueur 1 et 2"""
    fenetre.blit(haut, (0,0))
    font=pygame.font.Font(pygame.font.match_font('arialblack'), 100, bold=True)
    text = font.render(str(s1),True,(230,170, 230))
    l,h = font.size(str(s1))
    fenetre.blit(text, (250-l//2,50-h//2))
    text = font.render(str(s2),True,(230,170, 170))
    l,h = font.size(str(s2))
    fenetre.blit(text, (750-l//2,50-h//2))


def enfoncee(key):
    """
    Fonction qui est déclenchée lorsque on appuie sur
    une touche. On met à  jour la liste Touches
    """
    if not key in Touches:
        Touches.append(key)

def relachee(key):
    """
    Fonction qui est déclenchée lorsque on relâche une
    touche. On met à  jour la liste Touches
    """
    if key in Touches:
        Touches.remove(key)

pygame.init()
fenetre = pygame.display.set_mode((1000,600))

# Déclaration des variables globales
continuer = True
Touches = []

# Chargement des images
haut = pygame.image.load("haut.png").convert()
fenetre.blit(haut, (0,0))
gauche = pygame.image.load("gauche.png").convert()
fenetre.blit(gauche, (0,100))
terrain = pygame.image.load("centre.png").convert()
fenetre.blit(terrain, (100,100))
droite = pygame.image.load("droite.png").convert()
fenetre.blit(droite, (900,100))

# Creation de la balle et des joueurs
# coord initiales balle
Xinit=500
Yinit=350
balle = { 'X':Xinit, 'Y':Yinit, 'VX':2, 'VY':-3, 'L':32, 'H':32 }
balle['sprite']=pygame.image.load("balle.png").convert_alpha()

P1 = { 'X':110, 'Y':350, 'L':16, 'H':100 }
P1['sprite']=pygame.image.load("R1.png").convert_alpha()

P2 = { 'X':890, 'Y':350, 'L':16, 'H':100 }
P2['sprite']=pygame.image.load("R2.png").convert_alpha()

def place(D):
    """
    place D' sprite at X and Y coordinates
    """
    #conversion coordonne milieu sprite
    fenetre.blit(D['sprite'], (D['X']-D['L']//2,D['Y']-D['H']//2))

def mise_a_jour_affichage():
    """
    affiche les images
    """
    fenetre.blit(terrain, (100,100))
    place(balle)
    place(P1)
    place(P2)


def mise_a_jour_coord_balle():
    """
    met a jour les coordonnes de la balle
    """
    balle['X']+=balle['VX']
    balle['Y']+=balle['VY']
    gestion_rebonds()
    gestion_but()


def gestion_rebonds():
    """
    change la direction de la balle apres collision
    """
    # murs hauts et bas
    # attention taille balle
    if (balle['Y']-balle['H']//2<130) or (balle['Y']+balle['H']//2>570):
        balle['VY']=-1*balle['VY']


def gestion_but():
    """
    change la direction de la balle apres un but
    """
    if (balle['X']-balle['L']//2<100):
        balle['X']=Xinit
        balle['Y']=Yinit
        balle['VX']=-1*balle['VX']
        s1 += 1

    elif (balle['X']-balle['L']//2>900):
        balle['X']=Xinit
        balle['Y']=Yinit
        balle['VX']=-1*balle['VX']
        s2 += 1

def raquetteUP(J):
    """
    augmente la valeur Y du joueur
    """
    J['Y']-=5

def raquetteDOWN(J):
    """
    augmente la valeur Y du joueur
    """
    J['Y']+=5

def mise_a_jour_coord_joueurs():
    """
    deplace la raquette de gauche avec les touches x et s
    deplace la raquette de droite avec les touches up et down
    """
    if K_s in Touches:
        raquetteUP(P1)
    if K_x in Touches:
        raquetteDOWN(P1)
    if K_UP in Touches:
        raquetteUP(P2)
    if K_DOWN in Touches:
        raquetteDOWN(P2)

clock = pygame.time.Clock()
while continuer:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT :
            continuer = False
        elif event.type == KEYDOWN :
            enfoncee(event.key)
        elif event.type == KEYUP :
            relachee(event.key)
    # ici on réalise l'animation
    mise_a_jour_affichage()
    afficheScore(s1, s2)
    mise_a_jour_coord_balle()
    mise_a_jour_coord_joueurs()

    # Mise à jour de l'écran
    pygame.display.flip()
print('Fin')
pygame.quit()
