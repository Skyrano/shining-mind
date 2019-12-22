#Projet de programmation impérative
#Developpé par Alistair Rameau


from dijkstra import *
import random
import math
from PIL import Image
import matplotlib.pyplot as plt
import statistics


#Cette fonction retourne les coordonnées du point par rapport à un point donné et une direction voulue
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


#Cette fonction retourne la distance entre 2 cases
def Distance(x,y,endX,endY):
    return math.sqrt((endX - x)*(endX - x) + (endY - y)*(endY - y))


#Cette fonction met un nombre dans une liste triée au bon emplacement et retourne la liste et l'index auquel on a placé le nombre
def PutInList(number,liste):
    if len(liste) == 0: #si a liste est vide on le place au premier emplacement
        liste.append(number)
        return liste,0
    else:
        i = 0
        while i < len(liste):   #on cherche le premier élément de la liste qui soit plus grand que le nombre à placer
            if number <= liste[i]:
                liste.insert(i,number)  #et on insert le nombre à cet emplacement
                return liste,i
            i +=1
        liste.append(number)
        return liste,i


#Cette fonction créée un individu d'une certaine longueur et retourne la valeur de ses dépaclement prévus
def CreatePath(length):
    path = []
    for i in range(length):
        path.append(random.randint(0,7))
    return path


#Cette fonction calcule le score d'un individu à partir de sa case finale et du nombre de pas qu'il a parcouru
def Fitness(x,y,endX,endY,step):
    return int(Distance(x,y,endX,endY) + step/2)   #le nombre step permet d'eviter en partie le problème des chemins qui arrivent aux même endroit mais avec plus de déplacements (des retours en arrière par exemple)
                                                    #ceepndant on le divise par 2 pour le pas trop pénaliser les chemins qui vont reellement plus loin en contourant des chemins qui ne menent pas au but 

#Cette fonction teste un individu en utilisant une stratégie de retour en arrière dasn le cas d'un cul de sac et retourne le resultat de la fonction de fitness
def TestPathBackward(maze,path,stX,stY,endX,endY):
    matrix = maze.copy()    #on copie le labyrinthe pour pouvoir y faire des modifications non définitives
    x,y = stX,stY
    step = 0    #le step représente le nombre de déplacements réels effectués depuis le point de départ (par exemple, essayer d'aller dans un mur ne compte pas)
    for i in range(len(path)): 
        if len(AdjacentBrut_List(matrix,x,y,1)) != 0:   #si on est à porté du but alors on s'arrête et on met le fitness a zéro
            return 0        #on vérifie ensuite (en dessous) si l'on est dans un cul de sac
        #on est dans un cul de sac si on n'a pas de case non visitée où aller et si il n'y a qu'un seul endroit déjà visité ou l'on peut aller
        #de plus il ne faut pas qu'l y ait de connexion avec le départ ou la sortie
        elif len(AdjacentBrut_List(matrix,x,y,0)) == 0 and len(AdjacentBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentBrut_List(matrix,x,y,2)) == 0 and len(AdjacentBrut_List(matrix,x,y,1)) == 0:
            while len(AdjacentBrut_List(matrix,x,y,0)) == 0 and len(AdjacentBrut_List(matrix,x,y,3)) == 1 and maze[x][y] != 2 and maze[x][y] != 1 and len(AdjacentBrut_List(matrix,x,y,2)) == 0 and len(AdjacentBrut_List(matrix,x,y,1)) == 0:
                maze[x][y] = -1     #si on est dans un cul de sac alors on ajoute des murs (phéromones) jusqu'a sortir du cul de sac
                matrix[x][y] = -1
                x,y = AdjacentBrut_List(matrix,x,y,3)[0]
            break
        else:
            nx,ny = Deplacement(path[i],x,y) 
            if maze[nx,ny] != -1:   #on verifie si le prchain déplacement est possible
                x,y = nx,ny #si oui on se déplace dans cette case
                step += 1
            matrix[x][y] = 3    #on pose une marque du passage de l'individu
    
    return Fitness(x,y,endX,endY,step)  #on calcule et on retourne le score de l'individu


#Cette fonction évalue un population dans un certain labyrinthe et retourne la liste des individus triés par leur score et le score correspondant
def TestPopulation(population,maze,stX,stY,endX,endY):
    fitness = []
    path_sorted = []
    for i in range(len(population)):
        fitness,index = PutInList(TestPathBackward(maze,population[i],stX,stY,endX,endY),fitness)   #pour chaque individu on calcule son score et on le trie dans la liste 
        path_sorted.insert(index,population[i])
    return path_sorted,fitness


#Cette fonction élimine une certaine partie des individus les moins performants et retourne la liste des individus suffisament performant 
def Selection(population_tested, taux_select):
    select = int(taux_select*len(population_tested)) #on calcule un nombre de selectionnés par rapport au taux de selection au au nombre d'individus
    path = []
    fitness = []
    for i in range(select):
        path.append(population_tested[i])
    return path


#Cette fonction fait se reproduire les individus 2 par 2 et retourne la population avec les nouveaux individus
def Reproduction(population,nb_enfant):
    for i in range(nb_enfant):
        cut = random.randint(int(0.4*len(population[0])),int(0.6*len(population[0])))   #on choisit de couper le génome aléatoirement entre 40% et 60% du génome
        path1 = random.choice(population)   #on choisit aléatoirement 2 parents
        path2 = random.choice(population)
        while path2 == path1:
            path2 = random.choice(population)
        population.append(path1[:cut]+path2[cut:])  #on créé un fils
    return population


#Cette fonction fait muter un certain nombre d'individu et retourne la population avec les mutations effectuées
def Mutation(population,taux_muta):
    muta = int(taux_muta*len(population))   #on calcule le nombre de mutations par rapport au taux de mutation et au nombre d'individus
    for i in range(muta):
        path = random.randint(0,len(population)-1)  #on choisit aléatoirement un chemin et un déplacement de ce chemin
        index = random.randint(0,len(population[path])-1)
        population[path][index] = random.randint(0,7)   #on fait muter ce déplacement aléatoirement
    return population


#Cette fonction initialise un labyrinthe d'une certaine taille et revnoie sa matrice associée, son mapping dijkstra et ses points de départ et d'arrivée
def InitializeMap(X,Y):
    maze, zeros = ConstructMaze(X,Y)
    mapping = Dijkstra(maze,zeros)
    stX,stY = RandomCoord(maze,0)
    endX,endY = RandomCoord(maze,0)
    maze[stX][stY] = 2
    maze[endX][endY] = 1
    return maze,mapping,stX,stY,endX,endY


#Cette fonction retourne une population d'un certain nombre d'individus possédant une certaine longueur
def Genese(number,length):
    population = []
    for i in range(number):
        population.append(CreatePath(length))
    return population
    

#Cette fonction fait évoluer une population un certains nombre de fois selon des critères données (nombre de génération, taux de sélection et taux de mutation)    
#Puis elle affiche un graphique de l'évolution de la moyenne du score des individus de chaque génération
def Evolution(pop_init,X,Y,nG,ts,tm):
    fit_liste = []
    maze,mapping,stX,stY,endX,endY = InitializeMap(X,Y) #on créé le labyrinthe qui servira pour tester les individus
    MatrixPrinting(maze,"Maze.bmp")
    N = len(pop_init)
    Ne = int(N*(1-ts))  #on calcule le nombre d'enfant de facon à garder une population stable
    
    for i in range(nG):
        pop_ordered,fitness = TestPopulation(pop_init,maze,stX,stY,endX,endY)   #on teste la population de chaque génération
        print(i,fitness)        #on affiche le numéro de la génération et le score de ses individus
        if 0 in fitness == True:    #si on a un score de zero de les individus alors l'un d'entre eux a trouvé la sortie
            print("Solution trouvée")
            break 
        fit_liste.append(statistics.mean(fitness))
        MatrixPrinting(maze,"Maze{}.bmp".format(i))
        
        selection = Selection(pop_ordered,ts)   #on effectue la sélection, la reproduction et la mutation des individus
        repro = Reproduction(selection,Ne)
        mutation = Mutation(repro,tm)
        
        print("\n")
     
    plt.plot(fit_liste) #on fois toutes les générations faites, on peut afficher le graphique
    plt.title("Evolution de la Fitness en fonction des générations")
    plt.xlabel("Numéro de la génération")
    plt.ylabel("Moyenne de la Fitness")
    plt.show()
    plt.close()
    
    
    
N = 100
L = 1000
nG = 100
ts = 0.8
tm = 0.1
 
population = Genese(N,L)

Evolution(population,100,100,nG,ts,tm)