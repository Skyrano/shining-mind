#Projet de programmation impérative
#Developpé par Alistair Rameau


import numpy
import random
from ImagesUtils import *


#Cette fonction permet de print un matrice dans un fichier. On choisit la couleur du pixel en fonction de la valeur
def MatrixPrinting(matrix,filename):
    tailleX,tailleY = matrix.shape
    pixels = empty_img(tailleX, tailleY)
    for i in range(tailleX):
        for j in range(tailleY):
            if matrix[i][j] == 0:
                pass
            elif matrix[i][j] == -1:    #correspond à un mur
                pixels[i][j][0] = 255
            elif matrix[i][j] == -88:   #correspond au tracé de la trajectoire
                pixels[i][j][1] = 255
            elif matrix[i][j] == 1:     #correspond à la sortie
                pixels[i][j][2] = 255
            elif matrix[i][j] == 2:     #correspond au point de départ
                pixels[i][j][1] = 255
                pixels[i][j][2] = 255
            elif matrix[i][j] == 3:     #correspond au chemin d'un individu
                pixels[i][j][0] = 255
                pixels[i][j][1] = 255
            elif matrix[i][j]/10 < 255:
                pixels[i][j][1] = int(matrix[i][j]/10)      #On gère ici les valeurs élevées (dans le cas du mapping de dijkstra par exemple)
            elif matrix[i][j]/10 > 255 and matrix[i][j]/10 < 510:   #on delimite en 3 couleurs et on divise la valeur de la case pour permettre un dégradé des couleurs correct 
                pixels[i][j][1] = 255
                pixels[i][j][2] = int((matrix[i][j]-255)/10)    #cette disposition de valeurs est prévue pour un labyrinthe de 300x300
            elif matrix[i][j]/10 > 510 and matrix[i][j]/10 < 765:
                pixels[i][j][1] = 255
                pixels[i][j][2] = 255
                pixels[i][j][0] = int((matrix[i][j]-510)/10)
                
    write_img(filename,pixels)
    
    
#Cette fonction retourne une mosaique dans un tableau (alternance de 1 et -1)
def MosaicMap(tailleX,tailleY):
    mosaic =  numpy.zeros((tailleX,tailleY), dtype = int)   #on utilise les matices de numpy pour gérer les tableaux de nombres (labyrinthes)
    for i in range(tailleX):
        for j in range(tailleY):
            if i%2 == 0 or j%2 == 0:
                mosaic[i][j] = -1
            else:
                mosaic[i][j] = 1
    return mosaic
 
 
#Cette fonction retourne les cases adjacentes (distance de 2 cases, ou un case sautée) d'une matrice en vérifiant si celles-ci contiennent la valeur voulue et si celles-ci sont dans les limites du tableau 
#Cette fonction, contrairement à la suivante, ne vérifie pas les cases adjacente de la case testée 
def Adjacent2_ListNoRecur(matrix,x,y,number,xmax,ymax):
    cross = [(x-2,y),(x+2,y),(x,y-2),(x,y+2),(x-2,y-2),(x-2,y+2),(x+2,y-2),(x+2,y+2)]   #on code en brut les positions relatives des cases (gain de vitesse) à vérifier
    liste = []
    for (i,j) in cross:
        if i >= 0 and i < xmax and j >= 0 and j < ymax:
            if matrix[i][j] == number:
                liste.append((i,j))     #si la valeur est dans les limites et si celle si est bien egale à la valeur de demandée, on l'ajoute à la liste des valeurs retournées
    return liste


#Cette fonction retourne les cases adjacentes (distance de 2 cases) d'une matrice en vérifiant si celles-ci contiennent la valeur voulue et si celles-ci sont dans les limites du tableau 
#Cette fonction vérifie en plus les cases adjacentes de chaque case testée à l'aide de a fonction précédente
def Adjacent2_List(matrix,x,y,number,xmax,ymax):
    cross = [(x-2,y),(x+2,y),(x,y-2),(x,y+2),(x-2,y-2),(x-2,y+2),(x+2,y-2),(x+2,y+2)]
    liste = []
    for (i,j) in cross:
        if i >= 0 and i < xmax and j >= 0 and j < ymax:
            if matrix[i][j] == number and len(Adjacent2_ListNoRecur(matrix,i,j,0,xmax,ymax)) == 1: #on vérifie que la case possède bien un seul voisin deja traversé (case actuelle)
                liste.append((i,j))
    return liste


#Cette fonction retourne les cases adjacentes mais sans vérifier les limites du tableau (gain de vitesse) pour les cas ou cette verification est inutile
def AdjacentBrut_List(matrix,x,y,number):
    cross = [(x-1,y),(x+1,y),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]
    liste = []
    for (i,j) in cross:
        if matrix[i][j] == number:
            liste.append((i,j))
    return liste


#Cette foncton retourne simplement la liste des cases adjacentes à la case demandée sans aucune vérification
def AdjacentBrut_TotalList(matrix,x,y):
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]


#Cette fonction retourne les coordonnées d'un point aléatoire dans une matrice avec une valeur de cases égale à un certain nombre
def RandomCoord(matrix,number):
    tailleX,tailleY = matrix.shape  #on récupère les limites de la matrices
    rdX,rdY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)  #on cherche une case aléatoirement dans cette matrice
    while matrix[rdX][rdY] != number:       #et on en cherche une nouvelle tant que la valeur de la case n'est pas bonne
        rdX,rdY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)
    return rdX,rdY

#Cette retourne un labyrinthe calculé aléatoirement et le nombre de zéros dans le tableau (0 = passage)
def ConstructMaze(tailleX,tailleY):
    if tailleX%2 == 0:  #si les limites sont impaires, on augmente la taille de 1 pour permettre d'avoir un mur extérieur de chaque coté
        tailleX += 1
    if tailleY%2 == 0:
        tailleY += 1
    matrix = MosaicMap(tailleX,tailleY)     #on créé une mosaique de 1 et de -1
    stX,stY = RandomCoord(matrix,1) #on choisit aléatoirement un point de départ
    stack = [(stX,stY)]     #on met ce point de départ dans la stack
    x,y = stX,stY
    matrix[x][y] = 0    
    zeros = 1
    run = 1
    while run != 0:     #tant que l'on doit continuer
        liste = Adjacent2_List(matrix,x,y,1,tailleX,tailleY)    #on cherche la liste des points éligibles autour du point actuel
        if len(liste) == 0: #si la liste est nulle (pas de point) alors on revient en arrière
            x,y = stack[-1]
            stack.pop()
            if (x,y) == (stX,stY):  #si on revient en arrière jusqu'au point de départ alors on arrête
                run = 0
        else:
            xr,yr = random.choice(liste)    #si on trouve des points alors on choisit aléatoirement une des cases de la liste
            matrix[int((xr+x)/2)][int((yr+y)/2)] = 0
            matrix[xr][yr] = 0  #on met ces casses comme passage
            zeros += 2
            stack.append((xr,yr))   #et on les ajoute à la stack
            x,y = xr,yr
    
    for i in range(tailleX):    #on enlève du tableau les 1 restant
        for j in range(tailleY):
            if matrix[i][j] == 1:
                matrix[i][j] = -1
                
    return matrix,zeros
        

#Cette fonction retourne le mapping Dijkstra d'un labyrinthe (distance par rapport à un point de départ defini aléatoirement)
def Dijkstra(grille,zeros):
    counter = 1 
    matrix = numpy.copy(grille)
    stX,stY = RandomCoord(matrix,0) #on choisit un point de départ
    matrix[stX][stY] = counter
    zeros -= 1
    liste = [(stX,stY)] #on ajoute la liste des cases à verifier
    liste_next = []
    while zeros > 0 :   #tant qu'il reste des zeros
        for (i,j) in liste: #pour chaque case de la liste des cases à verifier
            for k,l in AdjacentBrut_List(matrix,i,j,0): #on verifie autour si il y a des cases dont le numéro n'a pas été calculé
                matrix[k][l] = counter+1    #on y met le numéro correspondant et on ajoute cette case à la liste suivante pour que l'on vérifie au prochain passage ses cases adjacentes
                zeros -= 1
                liste_next.append((k,l))
        counter += 1
        liste = liste_next  #on passe à la liste suivante
        liste_next = []
    return matrix


#Cette fonction donne le chemin le plus court pour aller à la sortie du labyrithe donné depuis les coordonnées données
def Pathfinding(grille,mapping,x,y):
    minimum = mapping[x][y]
    trace = -88     #on effectue le tracé de la trajectoire par le nombre -88
    matrix = numpy.copy(grille)
    while mapping[x][y] != 1:   #tant que l'on a pas atteint le but
        for k,l in AdjacentBrut_TotalList(mapping,x,y): #on cherche dans les cases adjacentes la valeur la plus faible
            if mapping[k][l] < mapping[x][y] and mapping[k,l] not in [trace,-1]:
                minimum = mapping[k][l]
                x_next,y_next = k,l
        matrix[x][y] = trace    #on pose une marque et on passe à la case avec le minimum trouvé
        x,y = x_next,y_next
    matrix[x][y] = 1
    return matrix


#Ces lignes permettent de tester le code ci-dessus uniquement
#Elles sont commentées par défaut car ce fichier est chargé par le fichier s'occupant de la génération des individus
"""
maze,zeros = ConstructMaze(300,300)
print(maze)
MatrixPrinting(maze,"Maze.bmp")

mapping = Dijkstra(maze,zeros)
print(mapping)

x,y = RandomCoord(maze,0)
path = Pathfinding(maze,mapping,x,y)
print(path)

MatrixPrinting(mapping,"Maze_mapping.bmp")
"""