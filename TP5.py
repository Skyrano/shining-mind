#TP5 d'algorithmique
#Programmation par Alistair Rameau

import random
import numpy
from ImagesUtils import *

RNG = random.SystemRandom()     #on cree un generateur de nombres aleatoires 

codageAlphabet = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26, ' ':27, '.':28, '!':29, '?':30, '\'':31, '-':32}
Alphabet = { nombre:lettre for lettre, nombre in codageAlphabet.items()}        #on cree un tableau inverse pour retrouver les lettres a partir des nombres



#Cette fonction cree une image en niveau de gris a partir d'une image donnee
#Entree : 1 image a transformer en niveau de gris
#Sortie : le tableau de pixels correspondant a l'image en niveau de gris
def Grey_level(image):
        pixels = read_img(image)                #on transforme l'image en tableau de pixels
        height = get_width(pixels)              #on declare la hauteur de l'image (inverse par rapport au nom de la fonction)
        width = get_height(pixels)              #on declare la largeur de l'image (inverse par rapport au nom de la fonction)
        new_pixels = empty_img(height,width)    #on declare un  tableau de pixels vide
        
        for x in range(height):         #pour chaque ligne
                for y in range(width):  #pour chaque colonne
                        pixel_RGB = pixels[x][y]        #on stocke la valeur du pixel x,y
                        grey = 0.299*pixel_RGB[0] + 0.587*pixel_RGB[1] + 0.114*pixel_RGB[2]     #on transforme on niveau de gris ce pixel
                        new_pixels[x][y][0] = grey      #on change la valeur RGB du pixel x,y
                        new_pixels[x][y][1] = grey
                        new_pixels[x][y][2] = grey
        
        return new_pixels       #on renvoie le tableau de pixels constitue des pixels en niveau de gris de l'image donnee



#Cette fonction tourne un image de 90 degres (direction en fonction du nombre donne par l'utilisateur)
#Entrees :une image a tourner et une direction
#Sortie : le tableau de pixels correspondant a l'image tournee
def Rotation(image,direction):
        if direction != 1 and direction != -1:  #si la direction donnee n'est pas bonne
                print("La direction doit etre egale a 1 ou -1")
                return -1
        pixels = read_img(image)
        height = get_width(pixels)
        width = get_height(pixels)
        new_pixels = empty_img(width, height)
        
        if direction == 1:      #on tourne dans le sens horaire
                for x in range(height):         #pour chaque pixel de l'image
                        for y in range(width):
                                new_pixels[y][x] = pixels[height-1-x][width-1-y]        #on fait une symetrie par rapport a la diagonale bas/gauche - haut/droite
                for x in range(height):         #pour chaque pixel de l'image
                        for y in range(width//2):
                                R,G,B = new_pixels[y][x][0],new_pixels[y][x][1],new_pixels[y][x][2]     #on recupere les valeurs RGB du pixel
                                new_pixels[y][x] = new_pixels[width-1-y][x]             #on fait la symetrie par rapport au milieu (axe horizontal)
                                new_pixels[width-1-y][x][0],  new_pixels[width-1-y][x][1], new_pixels[width-1-y][x][2]= R,G,B
        if direction == -1:     #on tourne dans le sens trigonometrique
                for x in range(height):
                        for y in range(width):
                                new_pixels[y][x] = pixels[x][y]          #on fait une symetrie par rapport a la diagonale haut/gauche - bas/droite
                for x in range(height):                 
                        for y in range(width//2):   
                                R,G,B = new_pixels[y][x][0], new_pixels[y][x][1], new_pixels[y][x][2]
                                new_pixels[y][x] = new_pixels[width-1-y][x]             #on fait la symetrie par rapport au milieu (axe horizontal)
                                new_pixels[width-1-y][x][0],  new_pixels[width-1-y][x][1], new_pixels[width-1-y][x][2]= R,G,B
                        
        return new_pixels       #on renvoie le tableau de pixels correspondant a l'image tournee de 90 degres dans la direction souhaitee



#Cette fonction chiffre un code dans une image donnee
#Entrees : une image et un code a injecter
#Sortie : le tableau de pixels correspondant a l'image avec le code ajoute
def Chiffrement(image, code):
        if len(code) > 50:              #on verifie que le code n'est pas vide ou trop grand
                print("Le code rentre est trop long")
                return -1
        if len(code) == 0:
                print("Le code rentre est vide")
                return -1
        pixels = read_img(image)
        height = get_width(pixels)
        width = get_height(pixels)
        size = height*width
        liste = []
        for i in range(len(code)):      #on cree une liste contenant le codage des lettres du codes
                liste.append(codageAlphabet[code[i]])
        max_espace = size//len(liste)   #on calcule l'espace maximal entre 2 lettres encodees
        x,y = 0,0
        while y < width and len(liste) != 0:            #pour chaque pixel de l'image, tant qu'il reste des lettres a encoder dans l'image
                while x < height and len(liste) != 0:
                        x += RNG.randint(1,max_espace)  #on se decale d'un nombre de pixels egal a un nombre entier aleatoire entre 1 et max_espace compris
                        if x >= height:         #si le nombre de pixels depasse de le nombre de pixels d'une colonne
                                y += x//height  #on incremente y du nombre de colonne passees
                                x = x%height    #et on module x par raport a la taille d'une colonne
                                
                        if pixels[x][y][2]+liste[0] < 256:      #si l'ajout du codage ne passe pas la valeur a plus de 255
                                pixels[x][y][2] = pixels[x][y][2] + liste[0]    #on ajoute le codage au canal bleu du pixel
                        else:
                                pixels[x][y][2] = pixels[x][y][2] - liste[0]    #sinon on soustrait le codage au canal bleu du pixel
                        del liste[0]    #on supprime l'element ajoute au pixel de la liste des elements a ajouter
        return pixels   #on renvoie le tableau de pixels comprenant les valeurs du codage de la chaine de caracteres



#Cette fonction dechiffre un code dans une image donnee
#Entrees : une image avec un code et l'image d'origine
#Sortie : le code contenu dans l'image
def Dechiffrement(codage,image):
        pixels = read_img(image)
        pixels_codage = read_img(codage)
        height = get_width(pixels)
        width = get_height(pixels)
        
        liste = []
        x,y = 0,0
        for y in range(width):          #pour chaque pixel de l'image
                for x in range(height):
                        if pixels_codage[x][y][2] > pixels[x][y][2]:    #si la valeur bleu du pixel de l'image modifiee est plus grande que la valeur bleu de l'image d'origine
                                difference = pixels_codage[x][y][2] - pixels[x][y][2]     #on ajoute la difference de la valeur modifiee moins la valeur d'origine a la liste des nombres codes dans l'image
                                liste.append(difference)
                        elif pixels_codage[x][y][2] < pixels[x][y][2]:  #si la valeur bleu du pixel de l'image modifiee est plus petite que la valeur bleu de l'image d'origine
                                difference = pixels[x][y][2] - pixels_codage[x][y][2]     #on ajoute la difference de la valeur d'origine moins la valeur modifiee a la liste des nombres codes dans l'image
                                liste.append(difference)
        code = ""
        for i in range(len(liste)):     #on transforme la liste des nombre trouves en une chaine de caracteres
                code = code + Alphabet[liste[i]]
        
        return code     #on renvoie la chaine de caracteres correspondant au code passe dans l'image

        
                                                     
                                                     
write_img("TUX_Grey.jpg",Grey_level("TUX.jpg"))  #on cree une image TUX_Grey.jpg correspondant a l'image TUX.jpg en niveau de gris

write_img("TUX_Rotation.jpg",Rotation("TUX.jpg",1)) #on cree une image TUX_Rotation.jpg correspondant a l'image TUX.jpg tournee de 90 degres dans le sens horaire

write_img("TUX.bmp",read_img("TUX.jpg"))   #on enregistre une version bitmap de TUX.jpg pour pouvoir l'utiliser par la suite dans la fonction de chiffrement (pas de compression venant modifier la valeur des pixels)

write_img("Chiffred.bmp",Chiffrement("TUX.bmp","LA PROGRAMMATION C'EST AMUSANT")) #on cree une image Chiffred.bmp contenant un code (une chaine de caracteres) en utilisant l'image TUX.bmp     

print(Dechiffrement("Chiffred.bmp","TUX.bmp"))  #on affiche le code contenu dans l'image Chiffred.bmp
