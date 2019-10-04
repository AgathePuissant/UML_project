# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:13:17 2019

@author: Agathe, Augustin,  Eliott 
"""
import random
import networkx as nx

class Entity(object):
    
    def __init__(self, _nom='', _proba_connection=random.random(), _proba_consulter=random.random(), _proba_accepter=random.random(),
                 _proba_transmettre=random.random()):
        
        self.voisin = list() #stocke le nom des voisins de l'entité
        self.nom=_nom #rajoute le numéro de l'entité pour pouvoir les repérer dans le réseau
        self.proba_connection = _proba_connection
        self.proba_consulter = _proba_consulter
        self.proba_accepter = _proba_accepter
        self.proba_transmettre = _proba_transmettre
        
    def afficher_caracteristiques(self):
        """
        afficher les informations dans la console
        """
        
        print(self.voisin)
        print(self.proba_connection)
        print(self.proba_consulter)
        print(self.proba_accepter)
        print(self.proba_transmettre)
    
class Info(object):
    def __init__(self, _id):
        self.entity_consult = list()
        self.entity_passed = list()
        self.id = _id
    
class Reseau(object):
    def __init__(self):
        self.entities = list()
    
    def initialiser_reseau(self, _nb_bon_public,_proba_bon_public,_nb_mauvais_public,_proba_mauvais_public):
        """
        initialiser le nombre d'entités
        appeller la méthode initialiser_Public pour gérer les publics au sein
        du réseau
        
        -->ajoute des entités à l'attribut *entities* de la classe

        """
        
        self.entities=self.initialiser_public(_nb_bon_public,_proba_bon_public)+self.initialiser_public(_nb_mauvais_public,_proba_mauvais_public)
       
        for i in range(len(self.entities)) :
            self.entities[i].nom=str(i) #défini le nom de chaque entité (utile dans calculer distance)
            for j in range(len(self.entities)) :
                coin=random.random()
                if coin<self.entities[i].proba_connection and self.entities[i].nom!=self.entities[j].nom and (self.entities[i].nom not in [self.entities[j].voisin[k].nom for k in range (len(self.entities[j].voisin))]) and (self.entities[j].nom not in [self.entities[i].voisin[k].nom for k in range (len(self.entities[i].voisin))]):
                    self.entities[i].voisin.append(self.entities[j])
                    self.entities[j].voisin.append(self.entities[i])
                    
        
        graph={} #on crée un dictionnaire qui stocke en clé le nom de chaque entité et dans les valeurs le nom des voisins de chaque entité
        
        for i in range(len(self.entities)) :
            graph[self.entities[i].nom]=[self.entities[i].voisin[j].nom for j in range (len(self.entities[i].voisin))]
            
        self.graph=graph
        
        
    def initialiser_public(self, _nb_entities, _proba_accept):
        """
        ajouter _nb_entities au réseau avec une probabilité d'accepter particulière.
        si _proba_accept est haute alors il s'agit d'un bon public
        
        -->ajoute des entités à l'attribut *entities* de la classe
        """
        
        return [Entity(_proba_accepter=_proba_accept) for i in range(_nb_entities)]
    
    def calculer_chemin(self, _entity_A, _entity_B, path=[]):
        """
        Retourne le plus court chemin
        """
        
        path=path+[_entity_A] #fonction récursive donc le chemin s'update à chaque nouveau "tour"
        
        if _entity_A==_entity_B : #fin du chemin
            return path
        
        if _entity_A not in self.graph.keys() : #pas de chemin possible
            return None
        
        shortest=None  #on initialise le plus court chemin à None
        
        for node in self.graph[_entity_A]: #pour chaque voisin de l'entité A
            
            if node not in path : #si on est pas déjà passé par ce voisin
                newpath=self.calculer_chemin(node,_entity_B,path) #on relance le calcul du chemin à partir de ce voisin
            
                if newpath : #si le nouveau chemin n'est pas None donc est possible
                    if not shortest or len(newpath)<len(shortest) : #si le plus court chemin existe déjà ou si le nouveau chemin est plus court que l'ancien plus court
                        shortest=newpath #le plus court chemin est update
                        
        return shortest
        
        
        
    def calculer_diametre(self):
        """
        réutiliser *calculer_chemin* entre chaque couples d'entité et retourner
        la valeur maximale.
        Rmq: probablement pas la solution la moins couteuse mais c'est certainement
        la plus simple à implémenter
        """
        return nx.diameter(nx.DiGraph(self.graph))
    
    def affiche_caracteristiques(self):
        """
        faire un affichage console de toutes les informations qui semblent
        pertinentes
        """
    
    def affiche_reseau(self):
        """
        utiliser le module networkx pour représenter le graphe
        """
        nx.draw_networkx(nx.DiGraph(self.graph),with_labels=True)
        
        
        
        
class Simulation(object):
    def __init__(self):
        self.informations = list()
    
    def initialiser_simulation(self):
        """
        initialiser le nombre d'informations et tout autre paramètres utile
        avant d'utiliser la méthode *run_simulation*
        """
    
    def run_simulation(self):
        """
        démarrer la simulation après l'initialisation.
        gérer les pas de temps -> à chaque pas de temps on déplace les infoirmations
        et on mets à jour les attirbut
        """
    

    
