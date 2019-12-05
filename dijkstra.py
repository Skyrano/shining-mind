#Projet de programmation imperative
#Developpe par Alistair Rameau


import numpy
import random


def MatrixPrinting(matrix):
    x,y = matrix.shape
    for i in range(x):
        for j in range(y):
            if matrix[i][j] == -1:
                print(1,end='')
            elif matrix[i][j] == 0:
                print(0,end='')
            else:
                print(5,end='')
            print(' ',end='')
        print()

def InitMap(tailleX,tailleY,number):
    matrix =  numpy.zeros((tailleX,tailleY), dtype = int)
    if number != 0:
        for i in range(tailleX):
            for j in range(tailleY):
                matrix[i][j] = number
    return matrix

def MosaicMap(matrix):
    mosaic = numpy.copy(matrix)
    x,y = mosaic.shape
    for i in range(x):
        for j in range(y):
            if i%2 != 0 and j%2 != 0:
                mosaic[i][j] = 0
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

def AdjacentCross_List(matrix,x,y,number):
    cross = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    liste = []
    xmax,ymax = matrix.shape
    for (i,j) in cross:
        if i < xmax and j < ymax:
            if matrix[i][j] == number:
                liste.append((i,j))
    return liste

def AdjacentCross2_List(matrix,x,y,number):
    cross = [(x-2,y),(x+2,y),(x,y-2),(x,y+2)]
    liste = []
    xmax,ymax = matrix.shape
    for (i,j) in cross:
        if i >= 0 and i < xmax and j >= 0 and j < ymax:
            if matrix[i][j] == number:
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



def ConstructMaze(tailleX,tailleY):
    matrix = MosaicMap(InitMap(tailleX,tailleY,-1))
    stX,stY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)
    while matrix[stX][stY] != 0:
        stX,stY = random.randint(0,tailleX-1), random.randint(0,tailleY-1)
    stack = [(stX,stY)]
    x,y = stX,stY
    matrix[x][y]=1
    run = 1
    
    while run != 0:
        liste = AdjacentCross2_List(matrix,x,y,0)
        if len(liste) == 0:
            x,y = stack[-1]
            stack.pop()
            if (x,y) == (stX,stY):
                run = 0
        else:
            xr,yr = random.choice(liste)
            matrix[int((xr+x)/2)][int((yr+y)/2)] = 1
            matrix[xr][yr] = 1
            stack.append((xr,yr))
            x,y = xr,yr
            
    x,y = matrix.shape
    for i in range(x):
        for j in range(y):
            if matrix[i][j] == 1:
                matrix[i][j] = 0            
    return matrix
        


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

def Dijkstra(grille,goalX,goalY):
    counter = 1
    matrix = numpy.copy(grille)
    matrix[goalX][goalY] = counter
    x,y = matrix.shape
    while MatrixCount(matrix,0) > 0 :
        for i in range(x):
            for j in range(y):
                if matrix[i][j] == counter:
                    for k,l in Adjacent_List(matrix,i,j):
                        if matrix[k][l] == 0:
                            matrix[k][l] = counter+1 
        counter += 1
    return matrix


def PathSearch(grille,mapping,x,y):
    minimum = mapping[x][y]
    trace = -88
    matrix = numpy.copy(grille)
    while mapping[x][y] != 1:
        for k,l in Adjacent_List(mapping,x,y):
            if mapping[k][l] < mapping[x][y] and mapping[k,l] not in {trace,-1}:
                minimum = mapping[k][l]
                x_next,y_next = k,l
        matrix[x][y] = trace
        x,y = x_next,y_next
    matrix[x][y] = trace
    return matrix    



murs = [(7,5),(6,5),(5,5),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(4,11),(4,10),(4,9),(4,8),(4,7),(4,6),(4,5)]
grille = InitMap(10,12,0)
grille = InitMurs(grille,murs)
print(grille)


mapping = Dijkstra(grille,8,9)
path = PathSearch(grille,mapping,0,2)

print(MosaicMap(InitMap(10,10,-1)))

maze = ConstructMaze(100,100)
MatrixPrinting(maze)