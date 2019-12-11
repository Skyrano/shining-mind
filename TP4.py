#TP4 d'algorithmique
#Programmation par Alistair Rameau

import random


#Cette fonction cree un tableau de nombres entiers aleatoires en fonctions des parametres entres par l'utilisateur
#Entrees : 2 nombre (la taille du tableau a creer et le nombre maximal possible pour les nombres du tableau)
#Sortie : le tableau d'entiers aleatoires
def Random_List(taille, nmax):
    liste = []
    for i in range(taille):
        liste.append(random.randint(0,nmax))    #on remplit le tableau de nombres entiers aleatoires entre 0 et nmax
    return liste


#Cette fonction trie un tableau en utilisant la methode du tri par selection
#On permute chaque element du tableau avec l'element suivant le plus petit (y compris lui meme)
#Entrees : le tableau a trier
#Sortie : le tableau trie
def Tri_Selection(liste):
    if len(liste) > 1:      #si on a un tableau d'au moins 2 valeurs on fait l'algorithme
        for i in range(len(liste)):     #pour chaque element du tableau
            minimum = liste[i:].index(min(liste[i:]))   #on selectionne l'element le plus petit entre l'indice actuel (compris) et la fin du tableau
            liste[i], liste[i+minimum] = liste[i+minimum], liste[i]     #et on le permute avec l'element actuel
    return liste


#Cette fonction trie un tableau en utilisant la methode du tri par insertion
#On verifie pour chaque element du tableau a quel indice precedent il faut l'inserer
#Entrees : le tableau a trier
#Sortie : le tableau trie
def Tri_Insertion(liste):
    if len(liste) > 1:      #si on a un tableau d'au moins 2 valeurs on fait l'algorithme
        for i in range(len(liste)):     #pour chaque element du tableau
            for y in range(i):      #on  verifie dans les element precedents
                if liste[i] < liste[y]:     #si un de ces elements est plus grand que l'element actuel
                    liste.insert(y,liste[i])    #on insert l'element actuel a la place de l'element plus grand (decalage de 1)
                    del liste[i+1]      #et on supprime l'element copie
                    break
    return liste


#Cette fonction fusionne 2 tableaux tries en gardant le tri effectif
#Les 2 tableaux etant supposés tries (par recursivite cela est vrai), la plus petite valeur du tableau final est la plus petite valeur parmi les premieres valeurs de chaque tableau
#On prend donc la plus petite valeur des 2 et on la concatenne avec la fusion du reste de la liste de cet element avec l'autre liste a fusionner
#Entrees : les 2 tableaux tries a fusionner
#Sortie : le tableau trie
def Fusion(listeA,listeB):
    if listeB == []:    #si la listeB est vide la fusion est egale a la listeA
        return listeA
    if listeA == []:    #si la listeA est vide la fusion est egale a la listeB
        return listeB
    
    if listeA[0] < listeB[0]:   #si la premiere valeur de la listeA est plus petite que la premiere valeur de la listeB
        return   [listeA[0]] + Fusion(listeA[1:],listeB)    #on concatenne cette valeur avec la fusion du reste de la liste et de la listeB
    else:                                   #sinon
        return  [listeB[0]] + Fusion(listeA,listeB[1:])     #on concatenne l'autre valeur avec la fusion du reste de la liste et de la listeA


#Cette fonction trie un tableau en utilisant la methode du tri fusion
#On separe le tableau en 2, et on trie recursivement les 2 parties avec l'algorithme tri fusion, puis on fusionne le resultat des deux tris
#Entrees : le tableau a trier
#Sortie : le tableau trie
def Tri_Fusion(liste):
    if len(liste) > 1:      #si on a un tableau d'un moins 2 valeurs on fait l'algorithme
        m = len(liste)//2       #on separe le tableau en partie a peu pres egales
        return Fusion(Tri_Fusion(liste[:m]), Tri_Fusion(liste[m:]))     #on fusionne le resultat du tri fusion de chaque partie
    else: 
        return liste
    
    
     


for i in range(5):
    
    liste = Random_List(10*i+10,100)
    print("Liste non triee : ")
    print(liste)

    print("\nSelection : ")
    print(Tri_Selection(liste))
    print("\nInsertion : ")
    print(Tri_Insertion(liste))
    print("\nFusion : ")
    print(Tri_Fusion(liste))
    print("\n")
    
    

""" Resultat de l'interpretation :

Liste non triee : 
[97, 89, 55, 42, 10, 17, 14, 97, 20, 17]

Selection : 
[10, 14, 17, 17, 20, 42, 55, 89, 97, 97]

Insertion : 
[10, 14, 17, 17, 20, 42, 55, 89, 97, 97]

Fusion : 
[10, 14, 17, 17, 20, 42, 55, 89, 97, 97]


Liste non triee : 
[26, 9, 18, 74, 33, 29, 56, 0, 22, 83, 36, 50, 3, 57, 18, 5, 75, 53, 77, 33]

Selection : 
[0, 3, 5, 9, 18, 18, 22, 26, 29, 33, 33, 36, 50, 53, 56, 57, 74, 75, 77, 83]

Insertion : 
[0, 3, 5, 9, 18, 18, 22, 26, 29, 33, 33, 36, 50, 53, 56, 57, 74, 75, 77, 83]

Fusion : 
[0, 3, 5, 9, 18, 18, 22, 26, 29, 33, 33, 36, 50, 53, 56, 57, 74, 75, 77, 83]


Liste non triee : 
[91, 1, 96, 36, 79, 45, 66, 100, 77, 92, 45, 84, 45, 36, 4, 62, 88, 47, 38, 52, 25, 23, 70, 20, 27, 81, 28, 43, 76, 15]

Selection : 
[1, 4, 15, 20, 23, 25, 27, 28, 36, 36, 38, 43, 45, 45, 45, 47, 52, 62, 66, 70, 76, 77, 79, 81, 84, 88, 91, 92, 96, 100]

Insertion : 
[1, 4, 15, 20, 23, 25, 27, 28, 36, 36, 38, 43, 45, 45, 45, 47, 52, 62, 66, 70, 76, 77, 79, 81, 84, 88, 91, 92, 96, 100]

Fusion : 
[1, 4, 15, 20, 23, 25, 27, 28, 36, 36, 38, 43, 45, 45, 45, 47, 52, 62, 66, 70, 76, 77, 79, 81, 84, 88, 91, 92, 96, 100]


Liste non triee : 
[48, 44, 36, 25, 96, 82, 12, 76, 87, 80, 38, 68, 68, 45, 59, 75, 20, 75, 28, 39, 25, 6, 50, 2, 24, 43, 27, 75, 56, 55, 42, 10, 13, 78, 78, 14, 94, 3, 50, 5]

Selection : 
[2, 3, 5, 6, 10, 12, 13, 14, 20, 24, 25, 25, 27, 28, 36, 38, 39, 42, 43, 44, 45, 48, 50, 50, 55, 56, 59, 68, 68, 75, 75, 75, 76, 78, 78, 80, 82, 87, 94, 96]

Insertion : 
[2, 3, 5, 6, 10, 12, 13, 14, 20, 24, 25, 25, 27, 28, 36, 38, 39, 42, 43, 44, 45, 48, 50, 50, 55, 56, 59, 68, 68, 75, 75, 75, 76, 78, 78, 80, 82, 87, 94, 96]

Fusion : 
[2, 3, 5, 6, 10, 12, 13, 14, 20, 24, 25, 25, 27, 28, 36, 38, 39, 42, 43, 44, 45, 48, 50, 50, 55, 56, 59, 68, 68, 75, 75, 75, 76, 78, 78, 80, 82, 87, 94, 96]


Liste non triee : 
[56, 60, 45, 72, 20, 68, 77, 100, 85, 33, 29, 63, 23, 18, 87, 59, 69, 21, 37, 72, 65, 76, 89, 30, 44, 65, 13, 50, 38, 8, 85, 79, 86, 93, 62, 34, 89, 2, 16, 14, 34, 32, 47, 99, 50, 25, 85, 54, 75, 98]

Selection : 
[2, 8, 13, 14, 16, 18, 20, 21, 23, 25, 29, 30, 32, 33, 34, 34, 37, 38, 44, 45, 47, 50, 50, 54, 56, 59, 60, 62, 63, 65, 65, 68, 69, 72, 72, 75, 76, 77, 79, 85, 85, 85, 86, 87, 89, 89, 93, 98, 99, 100]

Insertion : 
[2, 8, 13, 14, 16, 18, 20, 21, 23, 25, 29, 30, 32, 33, 34, 34, 37, 38, 44, 45, 47, 50, 50, 54, 56, 59, 60, 62, 63, 65, 65, 68, 69, 72, 72, 75, 76, 77, 79, 85, 85, 85, 86, 87, 89, 89, 93, 98, 99, 100]

Fusion : 
[2, 8, 13, 14, 16, 18, 20, 21, 23, 25, 29, 30, 32, 33, 34, 34, 37, 38, 44, 45, 47, 50, 50, 54, 56, 59, 60, 62, 63, 65, 65, 68, 69, 72, 72, 75, 76, 77, 79, 85, 85, 85, 86, 87, 89, 89, 93, 98, 99, 100]



"""

        