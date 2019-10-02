# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:13:17 2019

@author: Agathe, Augustin,  Eliott 
"""

class Entity(object):
    
    def __init__(self, _proba_connection, _proba_consulter, _proba_accepter,
                 _proba_transmettre):
        
        self.voisin = list()
        self.proba_connection = _proba_connection
        self.proba_consulter = _proba_consulter
        self.proba_accepter = _proba_accepter
        self.proba_transmettre = _proba_transmettre
        
    def afficher_caracteristiques(self):
        """
        afficher les informations dans la consoles
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
    
    def initialiser_reseau(self, _nb_infos):
        """
        initialiser le nombre d'entités
        appeller la méthode initialiser_Public pour gérer les publics au sein
        du réseau
        
        -->ajoute des entités à l'attribut *entities* de la classe

        """
    
    def initialiser_public(self, _nb_entities, _proba_accept):
        """
        ajouter _nb_entities au réseau avec une probabilité d'accepter particulière.
        si _proba_accept est haute alors il s'agit d'un bon public
        
        -->ajoute des entités à l'attribut *entities* de la classe
        """
    
    def calculer_distance(self,_entity_A, entity_B):
        """
        probablement implementer Dijkstra ou un autre algo de calcul de "plus
        court chemain"
        """
    
    def calculer_diametre(self):
        """
        réutiliser *calculer_distance* entre chaque couples d'entité et retourner
        la valeur maximale.
        Rmq: probablement pas la solution la moins couteuse mais c'est certainement
        la plus simple à implémenter
        """
    
    def affiche_caractéristiques(self):
        """
        faire un affichage console de toutes les informations qui semblent
        pertinentes
        """
    
    def affiche_reseau(self):
        """
        utiliser le module networkx pour représenter le graphe
        """
        
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
    

    
