from dijkstra import *
import random



def createPath(maze,stX,stY,length):
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
    return path


def InitalPop(matrix,number,length,stX,stY):
    population = []
    for i in range(number):
        population.append(createPath(matrix,stX,stY,length))
    return population

def Fitness(matrix,path,endX,endY):
    pass
    
    
    

maze, zeros = ConstructMaze(1000,1000)
mapping = Dijkstra(maze,zeros)
stX,stY = RandomCoord(maze,0)
endX,endY = RandomCoord(maze,0)
maze[stX][stY] = 2
maze[endX][endY] = 1

MatrixPrinting(maze,"Maze.bmp")
print(InitalPop(maze,100,10000,stX,stY))
MatrixPrinting(maze,"Maze2.bmp")
