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


# Déclaration des variables globales
continuer = True
Touches = []
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_PADDING_TOP = 130
WINDOW_PADDING_BOTTOM = 30
WINDOW_PADDING_SIDES = 100

BALL_RADIUS = 16
BALL_ACCELERATION = 1.1
BALL_INIT_SPEED = 2
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 16
PLAYER_PADDING = 10
PLAYER_SPEED = 5

pygame.init()
fenetre = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# Chargement des images
haut = pygame.image.load("haut.png").convert()
fenetre.blit(haut, (0,0))
gauche = pygame.image.load("gauche.png").convert()
fenetre.blit(gauche, (0,WINDOW_PADDING_SIDES))
terrain = pygame.image.load("centre.png").convert()
fenetre.blit(terrain, (WINDOW_PADDING_SIDES ,WINDOW_PADDING_SIDES))
droite = pygame.image.load("droite.png").convert()
fenetre.blit(droite, (WINDOW_WIDTH-WINDOW_PADDING_SIDES,WINDOW_PADDING_SIDES))

# Creation de la balle et des joueurs
# coord initiales balle
Xinit=500
Yinit=350

balle = { 'X':Xinit, 'Y':Yinit, 'VX':BALL_INIT_SPEED, 'VY':-1*BALL_INIT_SPEED, 'L':2*BALL_RADIUS, 'H':2*BALL_RADIUS }
balle['sprite']=pygame.image.load("balle.png").convert_alpha()

P1 = { 'X':WINDOW_PADDING_SIDES+PLAYER_PADDING, 'Y':Yinit, 'L':PLAYER_WIDTH, 'H':PLAYER_HEIGHT }
P1['sprite']=pygame.image.load("R1.png").convert_alpha()

P2 = { 'X':WINDOW_WIDTH-(WINDOW_PADDING_SIDES+PLAYER_PADDING), 'Y':Yinit, 'L':PLAYER_WIDTH, 'H':PLAYER_HEIGHT }
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
    fenetre.blit(terrain, (WINDOW_PADDING_SIDES,WINDOW_PADDING_SIDES))
    place(balle)
    place(P1)
    place(P2)

def mise_a_jour_coord_balle(s1, s2):
    """
    met a jour les coordonnes de la balle
    """
    balle['X']+=balle['VX']
    balle['Y']+=balle['VY']
    gestion_rebonds()
    return gestion_but(s1, s2)

def gestion_rebond_joueur1():
    """
    gere la collision de la balle avec le joueur P1
    """
    #test horizontal
    if((balle['X']-BALL_RADIUS)<(P1['X']+P1['L']//2)):
        #test vertical
        if ((balle['Y']+BALL_RADIUS)>(P1['Y']-P1['H']//2)) and ((balle['Y']-BALL_RADIUS)<(P1['Y']+P1['H']//2)):
            #on augmente aussi la vitesse
            balle['VX']=-1*balle['VX']*BALL_ACCELERATION

def gestion_rebond_joueur2():
    """
    gere la collision de la balle avec le joueur P2
    """
    #test horizontal
    if((balle['X']+BALL_RADIUS)>(P2['X']-P2['L']//2)):
        #test vertical
        if ((balle['Y']+BALL_RADIUS)>(P2['Y']-P2['H']//2)) and ((balle['Y']-BALL_RADIUS)<(P2['Y']+P2['H']//2)):
            #on augmente aussi la vitesse
            balle['VX']=-1*balle['VX']*BALL_ACCELERATION

def gestion_rebonds():
    """
    change la direction de la balle apres collision
    """
    # mur haut
    if (balle['Y']<(WINDOW_PADDING_TOP+BALL_RADIUS)): 
        balle['VY']=-1*balle['VY']
    #mur bas
    if (balle['Y']>(WINDOW_HEIGHT - (WINDOW_PADDING_BOTTOM+BALL_RADIUS))):
        balle['VY']=-1*balle['VY']

    gestion_rebond_joueur1()
    gestion_rebond_joueur2()
    

def balle_centre():
    """
    remet la balle au centre
    """
    balle['X'] = Xinit
    balle['Y'] = Yinit

def get_sign(x):
    """
    renvoie le signe d'un entier 
    """
    return (x>0)-(x<0)

def gestion_but(s1, s2):
    """
    gere un depacement horizontal de la balle
    Int*Int -> (Int*Int)
    """
    # cote gauche
    if(balle['X']-BALL_RADIUS<WINDOW_PADDING_SIDES):
        #inversion VX + maj speed
        balle['VX']=-1*BALL_INIT_SPEED
        balle['VY']= get_sign(balle['VY'])*BALL_INIT_SPEED
        #balle au centre
        balle_centre()
        #maj score
        return (s1, s2 +1)
    if(balle['X']+BALL_RADIUS>(WINDOW_WIDTH - WINDOW_PADDING_SIDES)):
        #inversion VX
        balle['VX']=-1*BALL_INIT_SPEED
        balle['VY']= get_sign(balle['VY'])*BALL_INIT_SPEED
        #balle au centre
        balle_centre()
        #maj score
        return (s1+1, s2)
    else:
        return (s1,s2)

def raquetteUP(J):
    """
    deplace le joueur vers le haut
    """
    #si on ne touche pas le plafond
    if(J['Y']-J['H']//2>WINDOW_PADDING_TOP):
        J['Y']-=PLAYER_SPEED

def raquetteDOWN(J):
    """
    deplace le joueur vers le bas
    """
    #si on ne touche pas le sol
    if(J['Y']+J['H']//2<(WINDOW_HEIGHT - WINDOW_PADDING_BOTTOM)):
        J['Y']+=PLAYER_SPEED

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


#main
clock = pygame.time.Clock()
s1 = 0
s2 = 0
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
    (s1, s2) = mise_a_jour_coord_balle(s1, s2)
    mise_a_jour_coord_joueurs()

    # Mise à jour de l'écran
    pygame.display.flip()

print('Fin')
pygame.quit()