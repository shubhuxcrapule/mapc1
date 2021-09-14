"""
    Voyageur de commerce dans le 14eme arrondissement de Paris
    Réalisé par  Célina Hadjara et Kenza Igoudjilene
"""

import geopy
import pandas as pd
from geopy.distance import geodesic
import networkx as nx
from matplotlib import pyplot as plt


class EnsembleDisjoint:
    """
    Cette classe permet de gérer les ensembles disjoints. Deux éléments sont
    considérés dans le même ensemble s'ils ont le même parent.
    """
    parent = {}

    # Création de n ensemble disjoints, état de départ de notre graphe
    def __init__(self, N):
        for i in range(N):
            self.parent[i] = i

    # Fonction qui permet de retrouver le parent le plus lointain
    def get_parent(self, k):
        if self.parent[k] == k:
            return k

        return self.get_parent(self.parent[k])

    # Union de deux ensembles jusque là disjoints
    def Union(self, a, b):
        x = self.get_parent(a)
        y = self.get_parent(b)

        self.parent[x] = y


def Kruskal(arcs, nombre_sommets):
    """
    Construction de l'arbre couvrant minimum à l'aide de l'algorithme de Kruskal
    Les paramètres sont :
        - Les arcs du graphe au format (début, fin, longueur)
        - Le nombre de sommets dans le graph
    """

    Arbre_minimum = []
    ed = EnsembleDisjoint(nombre_sommets)
    index = 0

    while len(Arbre_minimum) != nombre_sommets - 1:
        (src, dest, weight) = arcs[index]
        index = index + 1
        x = ed.get_parent(src)
        y = ed.get_parent(dest)

        if x != y:
            Arbre_minimum.append((src, dest, weight))
            ed.Union(x, y)

    return Arbre_minimum


# Parcours en profondeur recursif
def parcours_profondeur_recursive(graph, noeud, dejaVu=[]):
    print('En cours de visite :', noeud)
    dejaVu.append(noeud)
    for voisin in graph[noeud]:
        if voisin not in dejaVu:
            parcours_profondeur_recursive(graph, voisin, dejaVu)


# Parcours en profondeur recursif
def parcours_profondeur_recursive2(graph, noeud, dejaVu=[]):
    print('En cours de visite :', noeud)
    dejaVu.append(noeud)
    for voisin in graph[noeud]:
        if voisin not in dejaVu:
            parcours_profondeur_recursive(graph, voisin, dejaVu)


def distance(data,a,b,variables_numeriques):
    """
    Cette fonction permet de calculer la distance entre deux éléments.
    Les paramètres sont :
        - Les données du graph
        - Noeud du départ graphe
        - Noeud de la destination graphe
        - Les coordonnées latitude et longitude
    """
    for v in variables_numeriques:
        return geopy.distance.geodesic(data[v][a], data[v][b])


def generation_graphe(data):
    """
    Cette fonction permet de d'ajouter des acrs entre tout les noeds.
    Les paramètres sont :
        - Les données du graph
    """
    list_arcs=[]
    H = nx.Graph()
    (nb_lignes, nb_col) = data.shape
    for a in range(nb_lignes):
        for b in range(a+1, nb_lignes):
            d=distance(data,a,b,variables_numeriques).km
            list_arcs.append((a,b,d))
            H.add_edge(a,b,weight=d)
    return list_arcs


def generation_graphe2(data):
    cat_list = data.to_dict(orient='records')
    list_c = []
    list_cat = []
    nb = 0
    for v in cat_list :
        if v["catégorie"] == "Elément d'architecture" :
            nb +=1
        list_c.append(v["catégorie"])
    print ('Nombre de sommet - Catégorie - ',nb)

    A = nx.Graph()
    (nb_lignes, nb_col) = data.shape
    for a in range(nb_lignes):
        for b in range(a+1, nb_lignes):
            d=distance(data,a,b,variables_numeriques).km
            if a == "Elément d'architecture" or b == "Elément d'architecture" :
                list_cat.append((a,b,d))
                A.add_edge(a,b,weight=d)

    return list_cat



if __name__ == '__main__':
    data = pd.read_excel('paris-.xlsx' )
    variables_numeriques = ["geo_point_2d"]

    #Liste des arcs au format (début, fin, longueur)
    arcs = generation_graphe(data)
    print("Nombre d'arcs avant Kruskal :",len(arcs)," arcs")
    print('*'*25)

    #Trier la distance
    arcs.sort(key=lambda x: x[2])
    nombre_sommets = 67

    #Appliquer l'algorithme de Kruskal
    arcs2=Kruskal(arcs, nombre_sommets)
    print("Nombre d'arcs après Kruskal :",len(arcs2), "arcs")
    print('*'*25)

    #Génération de graph Kruskal
    H = nx.Graph()
    list_s_d={}

    for i in arcs2:
        src, dest, weight=i
        list_s_d[src] = dest
        H.add_edge(src, dest, weight=weight)

    options = {
        'node_color' : 'red',
        'node_size'  : 5,
        'edge_color' : 'tab:gray',
        'with_labels': True,
    }
    plt.figure(figsize=(20,20))
    plt.title("Voyageur de commerce - TSP")
    pos=nx.spring_layout(H, k= 0.15, iterations= 20)
    nx.draw_networkx_edges(H, pos, alpha= 0.4)
    nx.draw(H,pos,**options)

    keys_list = []
    for cle,valeur in list_s_d.items():
        keys_list.append(cle)

    noeud_depart = keys_list[0]
    print('Arc de départ du DFS :' ,noeud_depart)
    print('*'*25)

    print('Parcours en profondeur récursif :')
    parcours_profondeur_recursive(H, noeud_depart)
    print('*'*25)
    print('*'*25)
    plt.savefig("VoyageurDeCommerce.png")

    #############################################################################

    #Liste des arcs au format (début, fin, longueur)
    arcs_cat = generation_graphe2(data)
    print("Nombre d'arcs avant Kruskal - Catégorie - :",len(arcs_cat)," arcs")
    print('*'*25)

    #Trier la distance
    arcs_cat.sort(key=lambda x: x[2])
    nombre_sommets = 33

    #Appliquer l'algorithme de Kruskal
    arcs2_cat=Kruskal(arcs, nombre_sommets)
    print("Nombre d'arcs après Kruskal - Catégorie - :",len(arcs2_cat), "arcs")
    print('*'*25)

    #Génération de graph Kruskal selon la catégorie voulue

    A = nx.Graph()
    list_s_d_cat={}

    for i in arcs2_cat:
        src, dest, weight=i
        list_s_d_cat[src] = dest
        A.add_edge(src, dest, weight=weight)

    options = {
        'node_color' : 'blue',
        'node_size'  : 5,
        'edge_color' : 'tab:gray',
        'with_labels': True,
    }
    plt.figure(figsize=(20,20))
    plt.title("Voyageur de commerce - Catégorie -")
    pos=nx.spring_layout(A, k= 0.15, iterations= 20)
    nx.draw_networkx_edges(A, pos, alpha= 0.4)
    nx.draw(A,pos,**options)

    keys_list_cat = []
    for cle,valeur in list_s_d_cat.items():
        keys_list_cat.append(cle)

    noeud_depart_cat = keys_list_cat[9]
    print('Arc de départ du DFS - Catégorie - :' ,noeud_depart_cat)
    print('*'*25)

    print('Parcours en profondeur récursif - Catégorie - :')
    parcours_profondeur_recursive2(A, noeud_depart_cat)
    print('*'*25)

    plt.savefig("VoyageurDeCommerceCatégorie.png")

    plt.show()
    plt.close()






