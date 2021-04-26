import matplotlib.pyplot as plt
import numpy as np
import random
S=0
I=1
R=2


#c'est plus pratique de faire une fonction qui centralise tous
#les tirages à partir d'une liste de probabilités dont la
#somme est 1
def tirage(liste_probabilites):
    #on utilise la fct choices du module random pour
    #choisir S,I ou R à partir de la liste de proba
    return random.choices([S,I,R],liste_probabilites)[0]

def chaine_de_markov(etat,i_matrice):
    matrice1=[[0.92,0.08,0],[0,0.93,0.07],[0,0,1]]
    matrice2=[[0.92,0.08,0],[0,0.93,0.07],[0.04,0,0.96]]
    matrice3=[[0.98,0.02,0],[0,0.93,0.07],[0,0,1]]

    liste_matrice=[matrice1,matrice2,matrice3]
    matrice=liste_matrice[i_matrice]
    return tirage(matrice[etat])

def tirage_aleatoire(t,i_matrice,etat_initial):
    if(t<=0):
        return[]
    #l'etat au debut est calculé avec la liste ETAT_INITIAL
    etat=tirage(etat_initial)
    liste=[etat]
    for _ in range(1,t):
        etat=chaine_de_markov(etat,i_matrice)
        liste.append(etat)
    return liste

def tirage_population(t,nb_pop,i_matrice,etat_initial):
    initial=True
    #la liste de tous les etats à l'instant t
    liste_etat_t=[-1 for _ in range(nb_pop)]
    #les listes indiquant le nombre d'etats à chaque instant t
    liste_S=[]
    liste_I=[]
    liste_R=[]
    res=[liste_S,liste_I,liste_R]
    for i in range(t):
        for liste in res:
            liste.append(0)
        for personne in range(nb_pop):
            if(initial):
                liste_etat_t[personne]=tirage(etat_initial)
            else:
                liste_etat_t[personne]=chaine_de_markov(liste_etat_t[personne],i_matrice)
            etat=liste_etat_t[personne]
            #on ajoute 1 à l'etat correspondant pour l'instant t
            res[etat][i]+=1
        initial=False
    return res

def graphe(t,nb_pop,i_matrice,etat_initial):
    listes=tirage_population(t,nb_pop,i_matrice,etat_initial)
    x=np.array([i for i in range(t)])
    liste_label=['sains','infectés','immunisés']
    i=0
    for liste in listes:
        y=np.array(liste)
        plt.plot(x,y,label=liste_label[i])
        i+=1
    plt.axis([0,t,0,nb_pop])
    plt.xlabel("Temps")
    plt.ylabel("Nombre de personnes dans chaque catégorie")
    plt.legend()
    plt.show()

def longueur_sequenceI(n,i_matrice,etat_initial):
   res=0
   for _ in range(n):
       compteur=0
       etat=tirage(etat_initial)
       while(etat!=R):
           if(etat==I):
               compteur+=1
           etat=chaine_de_markov(etat,i_matrice)
       res+=compteur
   return res/n

def debut_distanciation(liste_a_t):
    cpt=0
    n=len(liste_a_t)
    for etat in liste_a_t:
        if(etat==I):
            cpt+=1
    return (cpt/n)>0.3
def fin_distanciation(liste_a_t):
    cpt=0
    n=len(liste_a_t)
    for etat in liste_a_t:
        if(etat==I):
            cpt+=1
    return (cpt/n)<0.15
def choix_matrice(liste_a_t,distanciation):
    if(distanciation):
        if(fin_distanciation(liste_a_t)):
            return 0
        return 2
    else:
        if(debut_distanciation(liste_a_t)):
            return 2
        return 0
           
def partie3(t,nb_pop,etat_initial):
    distanciation=False
    i_matrice=0
    debut_dist=-1
    fin_dist=-1
    initial=True
    #la liste de tous les etats à l'instant t
    liste_etat_t=[-1 for _ in range(nb_pop)]
    #les listes indiquant le nombre d'etats à chaque instant t
    liste_S=[]
    liste_I=[]
    liste_R=[]
    res=[liste_S,liste_I,liste_R]
    for i in range(t):
        for liste in res:
            liste.append(0)
        for personne in range(nb_pop):
            if(initial):
                liste_etat_t[personne]=tirage(etat_initial)
            else:
                liste_etat_t[personne]=chaine_de_markov(liste_etat_t[personne],i_matrice)
            etat=liste_etat_t[personne]
            #on ajoute 1 à l'etat correspondant pour l'instant t
            res[etat][i]+=1
        i_matrice=choix_matrice(liste_etat_t,distanciation)
        if(i_matrice==2):
            distanciation=True
            if(debut_dist==-1):
                debut_dist=i
        else:
            distanciation=False
            if(fin_dist==-1 and debut_dist!=-1):
                fin_dist=i
        initial=False
    return [res,debut_dist,fin_dist]
   

def graphe_partie3(t,nb_pop,etat_initial):
    r=partie3(t,nb_pop,etat_initial)
    listes=r[0]
    debut_dist=r[1]
    fin_dist=r[2]
    x=np.array([i for i in range(t)])
    liste_label=['sains','infectés','immunisés']
    i=0
    for liste in listes:
        y=np.array(liste)
        plt.plot(x,y,label=liste_label[i])
        i+=1
    plt.plot([debut_dist,debut_dist],[0,nb_pop],color="b")
    plt.plot([fin_dist,fin_dist],[0,nb_pop],color="b")
    plt.axis([0,t,0,nb_pop])
    plt.xlabel("Temps")
    plt.ylabel("Nombre de personnes dans chaque catégorie")
    plt.legend()
    plt.show()
    
    
    
    
