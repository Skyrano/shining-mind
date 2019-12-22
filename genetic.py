from dijkstra import *
import random
import math
from PIL import Image
import matplotlib.pyplot as plt
import statistics


def Deplacement(choix,x,y):
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
    return x,y

def InvDeplacement(choix,x,y):
    if choix == 0:
        x,y = x,y-1
    elif choix == 1:
        x,y = x+1,y-1
    elif choix == 2:
        x,y = x+1,y
    elif choix == 3:
        x,y = x+1,y+1
    elif choix == 4:
        x,y = x,y+1
    elif choix == 5:
        x,y = x-1,y+1
    elif choix == 6:
        x,y = x-1,y
    elif choix == 7:
        x,y = x-1,y-1
    return x,y


def RandomCase(x,y):
    choix = random.randint(0,7)    #from right and trigno = 0 1 2 3 4 5 6 7
    x,y = Deplacement(choix,x,y)
    return choix,x,y


def DeplacementCross(choix,x,y):
    if choix == 0:
        x,y = x,y+1
    elif choix == 1:
        x,y = x-1,y
    elif choix == 2:
        x,y = x,y-1
    elif choix == 3:
        x,y = x+1,y
    return x,y


def InvDeplacementCross(choix,x,y):
    if choix == 0:
        x,y = x,y-1
    elif choix == 1:
        x,y = x+1,y
    elif choix == 2:
        x,y = x,y+1
    elif choix == 3:
        x,y = x-1,y
    return x,y


def RandomCaseCross(x,y):
    choix = random.randint(0,3)     #from right and trigno = 0 1 2 3
    x,y = DeplacementCross(choix,x,y)
    return choix,x,y


def Distance(x,y,endX,endY):
    return math.sqrt((endX - x)*(endX - x) + (endY - y)*(endY - y))


def PutInList(number,liste):
    if len(liste) == 0:
        liste.append(number)
        return liste,0
    else:
        i = 0
        while i < len(liste):
            if number <= liste[i]:
                liste.insert(i,number)
                return liste,i
            i +=1
        liste.append(number)
        return liste,i


def CreatePathCross(length):
    path = []
    for i in range(length):
        path.append(random.randint(0,3))
    return path


def TestPath(maze,stX,stY,length,endX,endY):
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
    return path, Distance(x,y,endX,endY)


def TestPathOld(maze,stX,stY,length,endX,endY,k):
    matrix = maze.copy()
    x,y = stX,stY
    path = []
    for i in range(length):
        if len(AdjacentCrossBrut_List(matrix,x,y,1)) != 0:
            break
        elif len(AdjacentCrossBrut_List(matrix,x,y,0)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentCrossBrut_List(matrix,x,y,2)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,1)) == 0:
            maze[x][y] = -1
            path.pop()
            break
        else:
            numero,rx,ry = RandomCaseCross(x,y)
            if maze[rx,ry] != -1:
                x,y = rx,ry
            matrix[x][y] = 3        
            path.append(numero)
    return path, Distance(x,y,endX,endY) + len(path)


def TestPathNew(maze,path,stX,stY,endX,endY):
    matrix = maze.copy()
    x,y = stX,stY
    for i in range(len(path)):
        if len(AdjacentCrossBrut_List(matrix,x,y,1)) != 0:
            break
        elif len(AdjacentCrossBrut_List(matrix,x,y,0)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentCrossBrut_List(matrix,x,y,2)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,1)) == 0:
            maze[x][y] = -1
            break
        else:
            nx,ny = DeplacementCross(path[i],x,y)
            if maze[nx,ny] != -1:
                x,y = nx,ny
            matrix[x][y] = 3
    return int(Distance(x,y,endX,endY) + len(path)/2)


def TestPathBackward(maze,path,stX,stY,endX,endY,mapping):
    matrix = maze.copy()
    x,y = stX,stY
    for i in range(len(path)):
        if len(AdjacentCrossBrut_List(matrix,x,y,1)) != 0:
            return 0
        elif len(AdjacentCrossBrut_List(matrix,x,y,0)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentCrossBrut_List(matrix,x,y,2)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,1)) == 0:
            while len(AdjacentCrossBrut_List(matrix,x,y,0)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentCrossBrut_List(matrix,x,y,2)) == 0 and len(AdjacentCrossBrut_List(matrix,x,y,1)) == 0:
                maze[x][y] = -1
                matrix[x][y] = -1
                x,y = AdjacentCrossBrut_List(matrix,x,y,3)[0]
            break
        else:
            nx,ny = DeplacementCross(path[i],x,y)
            if maze[nx,ny] != -1:
                x,y = nx,ny
            matrix[x][y] = 3
    
    return int(Distance(x,y,endX,endY) + len(path)/2)


def InitalPop(number,length):
    population = []
    for i in range(number):
        population.append(CreatePathCross(length))
    return population


def TestPopulation(population,maze,stX,stY,endX,endY):
    fitness = []
    path_sorted = []
    for i in range(len(population)):
        fitness,index = PutInList(TestPathBackward(maze,population[i],stX,stY,endX,endY),fitness)
        path_sorted.insert(index,population[i])
    return path_sorted,fitness


def Selection(population_tested, taux_select):
    morta = int(taux_select*len(population_tested))
    path = []
    fitness = []
    for i in range(morta):
        path.append(population_tested[i])
    return path


def Reproduction(population,nb_enfant):
    for i in range(nb_enfant):
        cut = random.randint(int(0.4*len(population[0])),int(0.6*len(population[0])))
        path1 = random.choice(population)
        path2 = random.choice(population)
        while path2 == path1:
            path2 = random.choice(population)
        population.append(path1[:cut]+path2[cut:])
    return population


def MutationCross(population,taux_muta):
    muta = int(taux_muta*len(population))
    for i in range(muta):
        path = random.randint(0,len(population)-1)
        index = random.randint(0,len(population[path])-1)
        population[path][index] = random.randint(0,3)
    return population


def InitializeMap(X,Y):
    maze, zeros = ConstructMaze(X,Y)
    mapping = Dijkstra(maze,zeros)
    stX,stY = RandomCoord(maze,0)
    endX,endY = RandomCoord(maze,0)
    maze[stX][stY] = 2
    maze[endX][endY] = 1
    return maze,mapping,stX,stY,endX,endY


def Genese(N,L):
    return InitalPop(N,L)
    
    
def Evolution(pop_init,X,Y,nG,ts,tm):
    fit_liste = []
    maze,mapping,stX,stY,endX,endY = InitializeMap(X,Y)
    MatrixPrinting(maze,"Maze.bmp")
    N = len(pop_init)
    Ne = int(N*(1-ts))
    
    for i in range(nG):
        pop_ordered,fitness = TestPopulation(pop_init,maze,stX,stY,endX,endY)
        print(fitness)
        if 0 in fitness == True:
            print("Solution trouvee")
            break 
        fit_liste.append(statistics.mean(fitness))
        MatrixPrinting(maze,"Maze{}.bmp".format(i))
        
        selection = Selection(pop_ordered,ts)
        print("selection ",selection)
        repro = Reproduction(selection,Ne)
        print("repro ",repro)
        mutation = MutationCross(repro,tm)
        print("mutation",mutation)
        
        print("\n")
        
        input()
     
    plt.plot(fit_liste)
    plt.show()
    plt.close()
        
population = Genese(5,10)

Evolution(population,50,50,10,0.5,1.0)

"""
img = Image.open('Maze.bmp')
img.show()
"""
