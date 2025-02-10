from JeuDeDes import JeuDeDes
from typing import List, Dict, Callable, Optional
import random

class Actions:
    """Classe gérant les actions du jeu Yahtzee, incluant le lancer de dés et la gestion des scores."""
    
    NB_DES = 5
    MIN_VALEUR = 1
    MAX_VALEUR = 6
    
    def __init__(self):
        """
        Initialise une instance de Actions avec des dés aléatoires, un score initialisé à zéro,
        et un dictionnaire de fonctions de calcul de score.
        """
        self.jeu = self.generer_des_aleatoires()
        self.jeu_de_des = JeuDeDes(self.jeu)
        self.score = 0
        self.score_functions = {
            'Un': self.jeu_de_des.un,
            'Deux': self.jeu_de_des.deux,
            'Trois': self.jeu_de_des.trois,
            'Quatre': self.jeu_de_des.quatre,
            'Cinq': self.jeu_de_des.cinq,
            'Six': self.jeu_de_des.six,
            'Brelan': self.jeu_de_des.brelan,
            'Carre': self.jeu_de_des.carre,
            'Yahtzee': self.jeu_de_des.yahtzee,
        }

    def generer_des_aleatoires(self) -> List[int]:
        """
        Génère une liste de 5 dés avec des valeurs aléatoires entre 1 et 6.
        
        Returns:
            List[int]: Liste des valeurs générées (ex: [3, 1, 5, 2, 4]).
        """
        return [random.randint(self.MIN_VALEUR, self.MAX_VALEUR) for _ in range(self.NB_DES)]

    def lancer_des(self, garder: Optional[List[int]] = None) -> None:
        """
        Relance les dés non spécifiés dans la liste `garder` et met à jour l'instance JeuDeDes.
        
        Args:
            garder (Optional[List[int]]): Indices (0 à 4) des dés à conserver. Par défaut, relance tous.
        """
        garder = garder or []
        for i in range(self.NB_DES):
            if i not in garder:
                self.jeu[i] = random.randint(self.MIN_VALEUR, self.MAX_VALEUR)
        self.jeu_de_des = JeuDeDes(self.jeu)

    def garder_des(self) -> List[int]:
        """
        Demande interactivement au joueur de choisir les dés à garder.
        
        Returns:
            List[int]: Liste des indices valides (0 à 4) saisis par l'utilisateur.
        """
        while True:
            try:
                choix = input("\nEntrez les indices des dés à garder (1-5, séparés par des espaces) : ").strip()
                if not choix:
                    return []
                indices = [int(i) - 1 for i in choix.split()]
                if all(0 <= i < self.NB_DES for i in indices):
                    return indices
                print(f"Les indices doivent être entre 1 et {self.NB_DES}")
            except ValueError:
                print("Veuillez entrer des nombres valides séparés par des espaces")

    def afficher_des(self) -> None:
        """Affiche les dés actuels dans un format visuel (ex: | 3 | 1 | 5 | 2 | 4 |)."""
        self.afficher_bordure()
        print("| " + " | ".join(map(str, self.jeu)) + " |")
        self.afficher_bordure()

    def afficher_des_gardes(self, garder: List[int]) -> None:
        """
        Affiche uniquement les dés gardés, masque les autres.
        
        Args:
            garder (List[int]): Indices des dés à afficher (ex: [0, 2] affiche le premier et troisième dé).
        """
        self.afficher_bordure()
        print("|", end=" ")
        for i in range(self.NB_DES):
            print(f"{self.jeu[i] if i in garder else ' '} |", end=" ")
        print()
        self.afficher_bordure()

    def afficher_bordure(self) -> None:
        """Affiche une ligne de séparation horizontale pour l'affichage des dés."""
        print("+---" * self.NB_DES + "+")

    def enregistrer_score(self, categorie: str) -> int:
        """
        Calcule et enregistre le score pour une catégorie spécifiée.
        
        Args:
            categorie (str): Nom de la catégorie (ex: 'Brelan', 'Un').
            
        Returns:
            int: Score calculé. Retourne 0 si la catégorie est invalide.
        """
        score_function = self.score_functions.get(categorie)
        if score_function:
            score = score_function()
            self.score += score
            return score
        print(f"Catégorie '{categorie}' invalide")
        return 0

    def voir_score(self) -> None:
        """Affiche le score cumulé actuel du joueur."""
        print(f"\nScore actuel : {self.score}")

    def __str__(self) -> str:
        """Retourne une représentation textuelle de l'état du jeu."""
        return f"Dés actuels: {self.jeu} - Score: {self.score}"