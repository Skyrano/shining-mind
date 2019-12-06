#Projet de programmation imperative
#Developpe par Alistair Rameau


import numpy
import random
from ImagesUtils import *


def MatrixPrinting(matrix):
    tailleX,tailleY = matrix.shape
    pixels = empty_img(tailleX, tailleY)
    for i in range(tailleX):
        for j in range(tailleY):
            if matrix[i][j] == 0:
                pass
            elif matrix[i][j] == -1:
                pixels[i][j][0] = 255
            elif matrix[i][j] == -88:
                pixels[i][j][1] = 255
            elif matrix[i][j] == 1:
                pixels[i][j][2] = 255
            else:
                pixels[i][j][1] = int(matrix[i][j]/1000)
                
    write_img("Maze.bmp",pixels)
    
    
def InitMap(tailleX,tailleY,number):
    matrix =  numpy.zeros((tailleX,tailleY), dtype = int)
    if number != 0:
        for i in range(tailleX):
            for j in range(tailleY):
                matrix[i][j] = number
    return matrix

def MosaicMap(tailleX,tailleY):
    mosaic =  numpy.zeros((tailleX,tailleY), dtype = int)
    for i in range(tailleX):
        for j in range(tailleY):
            if i%2 == 0 or j%2 == 0:
                mosaic[i][j] = -1
            else:
                mosaic[i][j] = 1
    return mosaic
        

def Adjacence(matrix,i,j,k,l):
    if abs(i-k) <= 1 and abs(j-l) <= 1 and abs(i-k)+abs(j-l) in {1,2}:
        return True
    else:
        return False

def Adjacent_List(matrix,i,j):
    liste = []
    x,y = matrix.shape
    for k in range(x):
        for l in range(y):
            if Adjacence(matrix,i,j,k,l):
                liste.append((k,l))
    return liste


def AdjacenceCross(matrix,i,j,k,l):
    if (abs(i-k) == 1 and abs(j-l) == 0) or (abs(i-k) == 0 and abs(j-l) == 1):
        return True
    else:
        return False




def AdjacentCross_List(matrix,x,y,number,xmax,ymax):
    cross = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    liste = []
    for (i,j) in cross:
        if i >= 0 and i < xmax and j >= 0 and j < ymax:
            if matrix[i][j] == number:
                liste.append((i,j))
    return liste


def AdjacentCross2_List(matrix,x,y,number,xmax,ymax):
    cross = [(x-2,y),(x+2,y),(x,y-2),(x,y+2)]
    liste = []
    for (i,j) in cross:
        if i >= 0 and i < xmax and j >= 0 and j < ymax:
            if matrix[i][j] == number:
                liste.append((i,j))
    return liste


def AdjacentCrossBrut_List(matrix,x,y,number):
    cross = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    liste = []
    for (i,j) in cross:
        if matrix[i][j] == number:
            liste.append((i,j))
    return liste


def AdjacentCrossBrut_TotalList(matrix,x,y):
    cross = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    liste = []
    for (i,j) in cross:
        liste.append((i,j))
    return liste


def CleanList(matrix,liste,number):
    lenght = len(liste)
    i = 0
    while i < lenght:
        x,y = liste[i]
        if matrix[x][y] == number:
            del liste[i]
            lenght -= 1
        else:
            i += 1
    return liste


def RandomCoord(matrix,number):
    tailleX,tailleY = matrix.shape
    rdX,rdY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)
    while matrix[rdX][rdY] != number:
        rdX,rdY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)
    return rdX,rdY


def ConstructMaze(tailleX,tailleY):
    if tailleX%2 == 0:
        tailleX += 1
    if tailleY%2 == 0:
        tailleY += 1
    matrix = MosaicMap(tailleX,tailleY)
    stX,stY = RandomCoord(matrix,1)
    stack = [(stX,stY)]
    x,y = stX,stY
    matrix[x][y] = 0
    zeros = 1
    run = 1
    while run != 0:
        liste = AdjacentCross2_List(matrix,x,y,1,tailleX,tailleY)
        if len(liste) == 0:
            x,y = stack[-1]
            stack.pop()
            if (x,y) == (stX,stY):
                run = 0
        else:
            xr,yr = random.choice(liste)
            matrix[int((xr+x)/2)][int((yr+y)/2)] = 0
            matrix[xr][yr] = 0
            zeros += 2
            stack.append((xr,yr))
            x,y = xr,yr
                
    return matrix,zeros
        


def MatrixCount(matrix, number):
    count = 0
    x,y = matrix.shape
    for i in range(x):
        for j in range(y):
            if matrix[i][j] == number:
                count += 1
    return count
    

def InitMurs(matrix,murs):
    for i,j in murs:
        matrix[i][j] = -1
    return matrix


def Dijkstra(grille,zeros):
    counter = 1
    matrix = numpy.copy(grille)
    stX,stY = RandomCoord(matrix,0)
    matrix[stX][stY] = counter
    zeros -= 1
    liste = [(stX,stY)]
    liste_next = []
    while zeros > 0 :
        for (i,j) in liste:
            for k,l in AdjacentCrossBrut_List(matrix,i,j,0):
                    matrix[k][l] = counter+1
                    zeros -= 1
                    liste_next.append((k,l))
        counter += 1
        liste = liste_next
        liste_next = []
    return matrix


def Pathfinding(grille,mapping,x,y):
    minimum = mapping[x][y]
    trace = -88
    matrix = numpy.copy(grille)
    while mapping[x][y] != 1:
        for k,l in AdjacentCrossBrut_TotalList(mapping,x,y):
            if mapping[k][l] < mapping[x][y] and mapping[k,l] not in {trace,-1}:
                minimum = mapping[k][l]
                x_next,y_next = k,l
        matrix[x][y] = trace
        x,y = x_next,y_next
    matrix[x][y] = 1
    return matrix



maze,zeros = ConstructMaze(10000,10000)
print("Maze : ",maze)

mapping = Dijkstra(maze,zeros)
print("Mapping : ",mapping)


x,y = RandomCoord(maze,0)
path = Pathfinding(maze,mapping,x,y)
print("Path : ",path)

MatrixPrinting(path)