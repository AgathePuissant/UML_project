# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:13:17 2019
@author: Agathe, Augustin,  Eliott 
"""
import random as rd
import networkx as nx
import matplotlib.pyplot as plt

class Entity(object):
    """
    Définit l'objet entité
    
    La classe possède un constructeur pour initialiser les attributs pertinents
    et une méthode pour afficher les attributs dans la consoles.
    
    """
    
    def __init__(self,
                 _nom='',
                 _proba_connexion=rd.random(),
                 _proba_consulter=rd.random(),
                 _proba_accepter=rd.random(),
                 _proba_transmettre=rd.random()):
        
        """
        _nom (str):
            nom de l'entité. Il appartient à l'utilisateur de ne pas mettre 
            d'homonymes.
        
        _proba_connexion(float):
            probabilité de connexion avec une autre entité au sein du réseau
        
        _proba_consulter(float):
            probabilité de consulter une information disponible
        
        _proba_accepter(float):
            probabilité de'accepter une information au moment de la consultation
        
        _proba_transmettre(float):
            probabilité de transmettre une information indépendamment de la
            consultation
        """
        
        self.voisin = list() #stocke le nom des voisins de l'entité
        self.nom=_nom #rajoute le numéro de l'entité pour pouvoir les repérer dans le réseau
        self.proba_connexion = _proba_connexion
        self.proba_consulter = _proba_consulter
        self.proba_accepter = _proba_accepter
        self.proba_transmettre = _proba_transmettre
        
    def afficher_caracteristiques(self):
        """
        afficher les informations dans la console
        """
        print("Entité numéro :", self.nom)
        print("les voisins sont :", [v.nom for v in self.voisin])
        print("proba de connexion :", self.proba_connexion)
        print("proba de consultation :", self.proba_consulter)
        print("proba de bonne appréciation :", self.proba_accepter)
        print("proba de transmission :", self.proba_transmettre)
        print()
    
class Info(object):
    
    """
    Définit l'objet Information
    
    La classe possède un constructeur pour initialiser les attributs pertinents
    et une méthode pour afficher les attributs dans la consoles.
    
    """
    
    def __init__(self, _id):
        
        """
        _id (type définit par l'utilisateur):
            identifiant/nom de l'information. l appartient à l'utilisateur de
            ne pas mettre d'homonymes.
        """
        
        self.id = _id
        
        self.entity_passed = list()
        self.entity_passed_time_tracker = list()
        self.consulted_by = list()
        self.consulted_by_time_tracker = list()
        self.accepted_by = list()
        self.accepted_by_time_tracker = list()
        
        self.entity_last = list()
        
        self.no_consultation_couter = {}  # On rajoute un compteur pour pouvoir enlever les infos du reseaux
        self.not_consulted_anymore_by = list()
        
        self.activity_time = 0 #temps pour lequel l'info est consultable par encore au moins 1 entité
        
    def affiche_caracteristiques(self):
        
        """
        afficher les informations dans la console
        """
        
        print("id de l'information :", self.id)
        print("entités visitées : ", len(self.entity_passed))
        print("entités qui ont consultés l'info : ", len(self.consulted_by))
        print("entités qui ont appréciés l'info : ", len(self.accepted_by))
        print("Compteur de non consultation de l'info : ", self.no_consultation_couter)
        print("Nombre de pas en activité : ", self.activity_time)
        print()
    
class Reseau(object):
    
    """
    Définit un objet réseau comme une liste d'entités qui ont potentiellement
    des voisins.
    """
    
    def __init__(self):
        """
        Le Constructeur initialise uniquement un attibut *entities* en tant que 
        liste vide.
        Une initialisation complète d'un réseau se fait avec la méthode 
        *initialiser_reseau*
        """
        self.entities = list()
    
    def initialiser_reseau(self,
                           _nb_bon_public,
                           _proba_bon_public,
                           _nb_mauvais_public,
                           _proba_mauvais_public):
        """
        Initialise une réseau avec *_nb_bon_public+_nb_mauvais_public* enitités
        au total. Pour chaque type de public, on définit sa probabilité d'apprécier
        une information
        
        _nb_bon_public (int):
            nombre d'entités que l'on souhaite initialiser avec la probabilité
            *_proba_bon_public* d'apprécier une information
                          
        _proba_bon_public (float):
            probabilité d'apprécier une information pour les entités considérées
            comme bon public.
        
        _nb_mauvais_public:
            nombre d'entités que l'on souhaite initialiser avec la probabilité
            *_proba_mauvais_public* d'apprécier une information
        
        _proba_mauvais_public:
            probabilité d'apprécier une information pour les entités considérées
            comme mauvais public.
        """
        
        self.entities = self.initialiser_public(_nb_bon_public,_proba_bon_public)+ \
                        self.initialiser_public(_nb_mauvais_public,_proba_mauvais_public)
       
        for i in range(len(self.entities)) :
            self.entities[i].nom=str(i) #défini le nom de chaque entité (utile dans calculer distance)
            for j in range(len(self.entities)) :
                coin=rd.random()
                if (coin<self.entities[i].proba_connexion
                    and self.entities[i].nom!=self.entities[j].nom 
                    and (self.entities[i].nom not in
                         [self.entities[j].voisin[k].nom for k in range(
                                                 len(self.entities[j].voisin))])
                    and (self.entities[j].nom not in
                         [self.entities[i].voisin[k].nom for k in range (
                                                 len(self.entities[i].voisin))])):
                    
                    self.entities[i].voisin.append(self.entities[j])
                    self.entities[j].voisin.append(self.entities[i])
                    
        
        graph={} #on crée un dictionnaire qui stocke en clé le nom de chaque entité et dans les valeurs le nom des voisins de chaque entité
        
        for i in range(len(self.entities)) :
            graph[self.entities[i].nom]=[self.entities[i].voisin[j].nom for
                                      j in range (len(self.entities[i].voisin))]
            
        self.graph=graph
        
        
    def initialiser_public(self, _nb_entities, _proba_accept):
        """
        Initialise les entités associées à un type de public.
        
        _nb_entities (int):
            nombre d'entités que l'on souhaite initialiser
            
        _proba_accept (float):
            probabilité des entités que l'on initialise d'appréciier l'information.
            
        RETOURNE --> La liste des entités initialisées.
        
        """
        
        return [Entity(_nom = str(i),
                       _proba_connexion=rd.random(),
                       _proba_consulter=rd.random(),
                       _proba_accepter=_proba_accept,
                       _proba_transmettre=rd.random()) for i in range(_nb_entities)]
    
    def calculer_chemin(self, _entity_A, _entity_B, path=[]):
        """
        Retourne le plus court chemin entre _entity_A et _entity_B.
        Fonctionne de manière récursive.
        """
        
        #fonction contruite à partir de https://www.python.org/doc/essays/graphs/
        
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
        utilise le module networkx pour retourner la distance maximale possible
        entre deux entités du réseau
        """
        return nx.diameter(nx.DiGraph(self.graph))
    
    def affiche_caracteristiques(self):
        """
        affiche les caractéristiques de toutes les entités du réseau.
        """
        for _entity in self.entities:
            _entity.afficher_caracteristiques()
    
    def affiche_reseau(self):
        """
        utiliser le module networkx pour représenter le graphe
        """
        nx.draw_networkx(nx.DiGraph(self.graph),with_labels=True)
        
        
class Simulation(object):
    
    """
    Créer l'objet simulation. Une simulation consiste à injecter des informations
    dans un réseau et à déplacer ces informations sur le réseau si les entités
    le décident. Len entités peuvent aussi consulter l'information et potentiellement 
    l'apprécier.
    Il est possible de suivre les statistiques de chacunes des informations après 
    une simulation avec la méthode *visualisation*
    """
    
    def __init__(self):
        """
        Le constructeur initialise deux attributs **informations* et
        *activeç_informations* en tant que liste vide.
        
        Une initialisation complète d'une simulation se fait avec la méthode 
        *initialiser_simulation*
        """
        self.informations = list()#liste de toutes les informations dans la simu
        self.active_information = list()#liste de toutes les info de la simu
        #injectées dans le réseau
    
    def initialiser_simulation(self, reseau, nb_info=3, nb_pas_max_info=3, 
                               nb_max_pas = 10):
        
        """
        Initialise une réseau avec *_nb_bon_public+_nb_mauvais_public* enitités
        au total. Pour chaque type de public, on définit sa probabilité d'apprécier
        une information
        
        reseau (Reseau):
            l'objet reseau sur lequel la simulation va tourner 
                          
        nb_info (int):
            Le nombre d'info que l'on injecte dans le réseau
        
        nb_pas_max_info (int):
            nombre de pas qu'une information reste consultable en arrivant sur
            une nouvelle entité lorsqu'elle n'est pas consultée immédiatment
        
        nb_max_pas (int):
            nombre de pas maximal de la simulation.
        """
        
        self.simu_reseau = reseau
    
        #nb_info=random.randint(nb_pas,nb_pas*2)
        for i in range(nb_info):
            self.informations.append(Info(i))
            
            
        self.nb_pas=nb_max_pas
        self.nb_pas_info_max=nb_pas_max_info
    
    def recieve_information(self, _entity, _info):
        """
        gère les opérations lorsqu'une entité reçoit une information
        
        _entity (Entity):
            entité qui reçoit *_info*
            
        _info (Info):
            information reçue par *_entity*
        """
        _info.entity_passed.append(_entity)
        _info.no_consultation_couter[_entity.nom] = 0
        self.test_consulter(_entity, _info)
    
    def test_consulter(self, _entity, _info):
        """
        gère les opérations pour vérifier si une entité consulte une information
        
        _entity (Entity):
            entité que tente de consulter *_info*
            
        _info (Info):
            information potentiellement consultée par *_entity*
        """
        if (_entity not in _info.not_consulted_anymore_by and
            _entity not in _info.consulted_by):
            if rd.random() < _entity.proba_consulter:
                    _info.consulted_by.append(_entity)
                    self.test_apprecier(_entity, _info)
            else:
                _info.no_consultation_couter[_entity.nom]+=1
                if (_info.no_consultation_couter[_entity.nom] == self.nb_pas_info_max):
                    _info.not_consulted_anymore_by.append(_entity)
    
    def test_apprecier(self, _entity, _info):
        """
        gère les opération pour vérifier si une entité apprécie une information
        
        _entity (Entity):
            entité qui peut apprécier *_info*
            
        _info (Info):
            information potentiellement appréciée par *_entity*
        """
        if rd.random() < _entity.proba_accepter:
            _info.accepted_by.append(_entity)
    
    def transmettre_les_informations(self):
        
        """
        gère les opérations pour transmettre les informations à disposition des
        entités
        """
        
        for _info in self.active_information:#pour chaque info
            nouvelles_positions = list()#liste des futures positions de l'info
            for _entity in _info.entity_last:#pour chaque dernière positions de l'info
                if (rd.random() < _entity.proba_transmettre):#on regarde si on transmet
                    for _voisin in _entity.voisin:#pour tous les voisins
                        
                        if (_voisin not in _info.entity_passed):#si l'info n'est pas déjà allé sur le voisin
                            self.recieve_information(_voisin, _info)
                            nouvelles_positions.append(_voisin)
                
                self.test_consulter(_entity, _info)#test de consulation car l'info est toujours sur l'entité
                
                if (_entity not in _info.not_consulted_anymore_by
                    and _entity not in _info.consulted_by):#si le délais de consultation n'est pas écoulé
                    nouvelles_positions.append(_entity)
            
            _info.entity_last = nouvelles_positions
    
    def update_activity(self):
        """
        Construit les statistiques des informations au fur et à mesure.
        
        1.
            le temps passé dans le réseau en étant encore consultable par au moins
            une entité (même si cette dernière n'est pas accessible)
        2.
            le nombre d'entités visitées
        3.
            le nombre d'entités qui ont consulté l'information
        4.
            le nombre d'entité qui ont apprécié l'information
        """
        for _info in self.active_information:#pour chaque info
            
            if (len(_info.not_consulted_anymore_by+_info.consulted_by) != 
                len(self.simu_reseau.entities)):
                _info.activity_time += 1
            
            _info.entity_passed_time_tracker.append(len(_info.entity_passed))
            _info.consulted_by_time_tracker.append(len(_info.consulted_by))
            _info.accepted_by_time_tracker.append(len(_info.accepted_by))
        
    def affiche_caracteristiques(self):
        """
        affiche les caractérsitiques de toutes les infiormations de la
        simulation
        """
        for _info in self.informations:
            _info.affiche_caracteristiques()
           
    def run_simulation(self): # en entrée, 
        
        """
        démarre la simulation et gère les opération la concernant
        """
        
        pas_total=0        
        info_to_inject_index = 0
        for k in range(self.nb_pas):
            if (len(self.active_information) != len(self.informations)):
                current_info = self.informations[info_to_inject_index]
                
                self.active_information.append(current_info)
                info_to_inject_index += 1
                
                first_reciever = rd.choice(self.simu_reseau.entities)
                current_info.entity_last.append(first_reciever)
                self.recieve_information(first_reciever, current_info)
            
            self.transmettre_les_informations()
            
            self.update_activity()
                
            pas_total+=1
    
    def visualisation(self):
        """
        Génère les graphes des statistiques des information dans des nouvelles
        figures
        """
        
        x = [i for i in range(self.nb_pas)]
        for _info in self.informations:
            
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            y_prestart = [0 for i in range (_info.id)]#on ajoute des 0 aux pas
            #de temps où l'info n'était pâs encore dans le réseau
            
            ax1.plot(x, y_prestart+_info.entity_passed_time_tracker, marker = "o",
                     label="Nb d'entités visités par l'info")
            ax1.plot(x, y_prestart+_info.consulted_by_time_tracker, marker = "*",
                     label="Nb d'entités qui ont consulté l'info")
            ax1.plot(x, y_prestart+_info.accepted_by_time_tracker, marker = "d",
                     label="Nb d'entités qui ont apprecié l'info")
            
            
            ax1.set_xlabel("Pas de Temps")
            ax1.set_title("Statistiques de l'information {0}".format(_info.id))
            
            plt.legend()

if __name__=='__main__':
    
    r = Reseau()
    r.initialiser_reseau(5,0.9,5,0.1)
    r.affiche_reseau()
    r.affiche_caracteristiques()
    
    simul = Simulation()
    simul.initialiser_simulation(reseau = r, nb_max_pas=15)
    simul.run_simulation()
    
    simul.affiche_caracteristiques()
    
    simul.visualisation()
    
    
    