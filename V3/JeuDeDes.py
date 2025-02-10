from typing import List

class JeuDeDes:
    """Classe représentant un jeu de dés et fournissant des méthodes de calcul de scores."""
    
    def __init__(self, jeu: List[int]) -> None:
        """
        Initialise un jeu de 5 dés avec validation des valeurs.
        
        Args:
            jeu (List[int]): Liste de 5 entiers entre 1 et 6.
            
        Raises:
            ValueError: Si la liste est invalide (longueur incorrecte ou valeurs hors limites).
        """
        if len(jeu) != 5 or not all(1 <= val <= 6 for val in jeu):
            raise ValueError("Le jeu doit contenir exactement 5 valeurs comprises entre 1 et 6.")
        self.jeu = jeu

    def calcul_numero(self, numero: int) -> int:
        """
        Somme des dés correspondant au numéro spécifié.
        
        Args:
            numero (int): Valeur cible entre 1 et 6.
            
        Returns:
            int: Somme des dés égaux à `numero`.
        """
        return sum(val for val in self.jeu if val == numero)

    def how_many_occ(self) -> List[int]:
        """
        Compte les occurrences de chaque valeur de dé (1 à 6).
        
        Returns:
            List[int]: Liste où l'index i représente le nombre de dés de valeur i+1.
        """
        return [self.jeu.count(i) for i in range(1, 7)]

    def brelan(self) -> int:
        """
        Vérifie la présence d'un brelan (3 dés identiques).
        
        Returns:
            int: Somme totale des dés si brelan trouvé, sinon 0.
        """
        return sum(self.jeu) if 3 in self.how_many_occ() else 0

    def carre(self) -> int:
        """
        Vérifie la présence d'un carré (4 dés identiques).
        
        Returns:
            int: Somme totale des dés si carré trouvé, sinon 0.
        """
        return sum(self.jeu) if 4 in self.how_many_occ() else 0

    def yahtzee(self) -> int:
        """
        Vérifie la présence d'un Yahtzee (5 dés identiques).
        
        Returns:
            int: 50 si Yahtzee trouvé, sinon 0.
        """
        return 50 if 5 in self.how_many_occ() else 0
    
    # Méthodes pour les catégories numériques
    def un(self) -> int:
        """Retourne la somme des dés de valeur 1."""
        return self.calcul_numero(1)

    def deux(self) -> int:
        """Retourne la somme des dés de valeur 2."""
        return self.calcul_numero(2)

    def trois(self) -> int:
        """Retourne la somme des dés de valeur 3."""
        return self.calcul_numero(3)

    def quatre(self) -> int:
        """Retourne la somme des dés de valeur 4."""
        return self.calcul_numero(4)

    def cinq(self) -> int:
        """Retourne la somme des dés de valeur 5."""
        return self.calcul_numero(5)

    def six(self) -> int:
        """Retourne la somme des dés de valeur 6."""
        return self.calcul_numero(6)