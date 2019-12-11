from dijkstra import *
import random
import math



def RandomCase(x,y):
    choix = random.randint(0,7)     #from right and trigno = 0 1 2 3 4 5 6 7
    if choix == 0:
        x,y = x,y+1
    elif choix == 1:
        x,y = x-1,y+1
    elif choix == 2:
        x,y = x-1,y
    elif choix == 3:
        x,y = x-1,y-1
    elif choix == 4:
        x,y = x,y-1
    elif choix == 5:
        x,y = x+1,y-1
    elif choix == 6:
        x,y = x+1,y
    elif choix == 7:
        x,y = x+1,y+1
    
    return choix,x,y


def RandomCaseCross(x,y):
    choix = random.randint(0,3)     #from right and trigno = 0 1 2 3
    if choix == 0:
        x,y = x,y+1
    elif choix == 1:
        x,y = x-1,y
    elif choix == 2:
        x,y = x,y-1
    elif choix == 3:
        x,y = x+1,y
    
    return choix,x,y


def Distance(x,y,endX,endY):
    return math.sqrt((endX - x)*(endX - x) + (endY - y)*(endY - y))


def createPath(maze,stX,stY,length,endX,endY):
    matrix = maze.copy()
    x,y = stX,stY
    path = []
    matrix[x][y] = 3
    breaked = 0
    for i in range(length):
        if len(AdjacentCrossBrut_List(matrix,x,y,1)) != 0:
            break
        liste = AdjacentCrossBrut_List(matrix,x,y,0)
        if len(liste) == 0:
            maze[x][y] = -1
            x,y = path[-1]
            path.pop()
            while len(path) > 1:
                liste = AdjacentCrossBrut_List(matrix,x,y,0)
                if len(liste) == 0:
                    maze[x][y] = -1
                    x,y = path[-1]
                    path.pop()
                else:
                    break
            break
        else:
            next_case = random.choice(liste)    
            x,y = next_case
            matrix[x][y] = 3
            path.append(next_case)
    return path, Fitness(path,endX,endY)


def createPathNew(maze,stX,stY,length,endX,endY):
    matrix = maze.copy()
    x,y = stX,stY
    path = []
    matrix[x][y] = 3
    breaked = 0
    for i in range(length):
        if len(AdjacentCrossBrut_List(matrix,x,y,1)) != 0:
            break
        if len(AdjacentCrossBrut_List(matrix,x,y,0)) == 0:
            maze[x][y] = -1
            x,y = path[-1]
            path.pop()
            while len(path) > 1:
                liste = AdjacentCrossBrut_List(matrix,x,y,0)
                if len(liste) == 0:
                    maze[x][y] = -1
                    x,y = path[-1]
                    path.pop()
                else:
                    break
            break
        else:
            numero,rx,ry = RandomCaseCross(x,y)
            if maze[rx,ry] != -1: 
                x,y = rx,ry
                matrix[x][y] = 3
            path.append(numero)
    return path, Distance(x,y,endX,endY) + len(path)


def InitalPop(matrix,number,length,stX,stY,endX,endY):
    population = []
    for i in range(number):
        path, fitness = createPath(matrix,stX,stY,length,endX,endY)
        population.append([i,path,fitness])
    return population


def Selection(fitness,taux):
    pass
        
    
    

maze, zeros = ConstructMaze(1000,1000)
mapping = Dijkstra(maze,zeros)
stX,stY = RandomCoord(maze,0)
endX,endY = RandomCoord(maze,0)
maze[stX][stY] = 2
maze[endX][endY] = 1

MatrixPrinting(maze,"Maze.bmp")
pop_init = InitalPop(maze,100,1000,stX,stY,endX,endY)
MatrixPrinting(maze,"Maze2.bmp")

for i in range(len(pop_init)):
    print(pop_init[i])


