from JeuDeDes import JeuDeDes
from Actions import Actions
from typing import Dict, Optional, List

class JeuYahtzee:
    """Classe principale gérant le déroulement d'une partie de Yahtzee."""
    
    CATEGORIES = {
        1: "Un", 2: "Deux", 3: "Trois", 4: "Quatre",
        5: "Cinq", 6: "Six", 7: "Brelan", 8: "Carre",
        9: "Yahtzee"
    }

    def __init__(self):
        """Initialise une partie avec des dés, un score vierge et une liste de parties."""
        self.actions = Actions()
        self.jeu_de_des = JeuDeDes(self.actions.jeu)
        self.scores: Dict[str, Optional[int]] = {cat: None for cat in self.CATEGORIES.values()}
        self.parties: List[int] = []

    def enregistrer_score(self, categorie: str) -> None:
        """
        Enregistre le score dans une catégorie non utilisée.
        
        Args:
            categorie (str): Nom de la catégorie (ex: 'Brelan').
            
        Raises:
            ValueError: Si la catégorie est invalide ou déjà utilisée.
        """
        if categorie not in self.scores or self.scores[categorie] is not None:
            print(f"Catégorie {categorie} non valide ou déjà utilisée.")
            return

        score_methods = {
            "Un": self.jeu_de_des.un,
            "Deux": self.jeu_de_des.deux,
            "Trois": self.jeu_de_des.trois,
            "Quatre": self.jeu_de_des.quatre,
            "Cinq": self.jeu_de_des.cinq,
            "Six": self.jeu_de_des.six,
            "Brelan": self.jeu_de_des.brelan,
            "Carre": self.jeu_de_des.carre,
            "Yahtzee": self.jeu_de_des.yahtzee
        }

        score = score_methods.get(categorie, lambda: 0)()
        self.scores[categorie] = score
        print(f"Score enregistré pour {categorie} : {score}")

    def choix_categorie(self) -> None:
        """Demande interactivement au joueur de choisir une catégorie disponible."""
        while True:
            self.afficher_categories_disponibles()
            try:
                choix = int(input("Choisissez une catégorie : "))
                categorie = self.CATEGORIES.get(choix)
                if categorie and self.scores[categorie] is None:
                    self.enregistrer_score(categorie)
                    break
                print("Catégorie non valide ou déjà utilisée. Choisissez une autre catégorie.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")

    def afficher_categories_disponibles(self) -> None:
        """Affiche les catégories disponibles sous forme de tableau numéroté."""
        print("\n+---------+---+")
        for numero, nom in self.CATEGORIES.items():
            print(f"| {nom.ljust(7)} | {numero} |")
        print("+---------+---+")

    def afficher_score(self) -> int:
        """
        Affiche le tableau des scores et calcule le total.
        
        Returns:
            int: Score total de la partie.
        """
        score_final = sum(score for score in self.scores.values() if score is not None)
        print("\n+------------------+-------+")
        print("| Catégorie        | Score |")
        print("+------------------+-------+")
        for categorie, score in self.scores.items():
            score_display = str(score) if score is not None else "N/A"
            print(f"| {categorie:<16} | {score_display:>5} |")
        print("+------------------+-------+")
        print(f"| TOTAL            | {score_final:>5} |")
        print("+------------------+-------+")
        return score_final

    def jouer_tour(self) -> None:
        """Exécute un tour complet avec jusqu'à 3 lancers et sélection de catégorie."""
        print("\n--- Nouveau tour ---")
        for i in range(3):
            if i == 0:
                self.actions.lancer_des()
            else:
                garder = self.actions.garder_des()
                self.actions.lancer_des(garder=garder)
                print("Dés gardés :")
                self.actions.afficher_des_gardes(garder)
            
            print("Dés actuels :")
            self.actions.afficher_des()
            
            if i == 2:
                self.choix_categorie()

    def jouer_partie(self, nombre_tours: int) -> None:
        """
        Gère une partie complète sur un nombre de tours spécifié.
        
        Args:
            nombre_tours (int): Nombre de tours à jouer.
        """
        print("Bienvenue au jeu de Yahtzee !")
        for tour in range(nombre_tours):
            print(f"\nTour {tour + 1}/{nombre_tours}")
            self.jouer_tour()
        
        score_final = self.afficher_score()
        self.fin_de_partie(score_final)

    def fin_de_partie(self, score_final: int) -> None:
        """
        Finalise la partie et enregistre le score.
        
        Args:
            score_final (int): Score total de la partie.
        """
        self.parties.append(score_final)
        self.afficher_score_total()

    def afficher_score_total(self) -> None:
        """Affiche le score cumulé de toutes les parties jouées."""
        score_total = sum(self.parties)
        print(f"\nScore total après {len(self.parties)} parties : {score_total}")