# **Manuel d'Utilisation - Jeu de Yahtzee V1**

---

## **Introduction**
Ce projet est un jeu de Yahtzee en réseau où un serveur gère plusieurs clients qui peuvent jouer ensemble. Chaque client se connecte à la meme partie, et le serveur détermine le gagnant en fonction des scores.

---

## **1. Installation et Prérequis**
### **1.1. Environnement**
- Assurez-vous d’avoir tous les fichiers suivants :
  - `Serveur.py`
  - `Client.py`
  - `JeuYahtzee.py`
  - `JeuDeDes.py`
  - `Actions.py`
(Pour tester les fonctions du jeu vous pouvez utiliser le fichier suivant)
  - `Test.py`

### **1.2. Bibliothèques Python**
Les bibliothèques utilisées sont incluses dans Python de base (`socket`, `threading`, `time`, `random`). Aucune installation supplémentaire n'est requise.

---

## **2. Démarrage du Jeu**
### **2.1. Lancement du Serveur**
Avant que les joueurs puissent se connecter, le serveur doit être lancé.

1. Ouvrir un terminal et naviguer vers le dossier contenant les fichiers.
2. Exécuter la commande :
   ```sh
   python3 Serveur.py
   ```
3. Le serveur écoute les connexions des clients et attend qu'au moins deux joueurs se connectent avant de commencer une partie.

---

### **2.2. Connexion des Clients**
Chaque joueur doit se connecter au serveur en lançant une instance du client.

1. Ouvrir un terminal pour chaque joueur.
2. Exécuter la commande suivante pour se connecter au serveur :
   ```sh
   python3 Client.py
   ```
3. Une fois connecté, chaque client reçoit un identifiant unique.

---

### **2.3. Démarrage de la Partie**
- Le premier joueur (client `0`) a la responsabilité de démarrer la partie en tapant `YES` lorsque le programme lui demande :
  ```
  Souhaitez-vous lancer la partie maintenant ? (yes/no) :
  ```
- Tous les autres clients verront un message "En attente du lancement de la partie..." jusqu'à ce que la partie commence.

---

## **3. Déroulement d'une Partie**
Chaque client joue 3 tours pour essayer de maximiser son score.

### **3.1. Lancer les Dés**
- À chaque tour, le joueur peut lancer les dés jusqu'à 3 fois.
- Après chaque lancer, il peut choisir quels dés conserver et relancer les autres.

### **3.2. Choisir une Catégorie**
À la fin des 3 lancers, le joueur doit choisir une catégorie dans laquelle enregistrer son score :
```
+---------+---+
| Un      | 1 |
| Deux    | 2 |
| Trois   | 3 |
| Quatre  | 4 |
| Cinq    | 5 |
| Six     | 6 |
| Brelan  | 7 |
| Carre   | 8 |
| Yahtzee | 9 |
+---------+---+
```
- Le joueur entre un numéro correspondant à la catégorie désirée.
- Une fois la catégorie choisie, son score est enregistré et ne peut plus être modifié.

---

## **4. Fin de la Partie et Résultats**
- Après 9 tours, le score total de chaque joueur est envoyé au serveur.
- Le serveur compare les scores et annonce le gagnant.
- Chaque joueur voit un message indiquant s'il a gagné ou perdu.

---

## **5. Déconnexion**
- Une fois la partie terminée, le serveur ferme les connexions et les clients se déconnectent automatiquement.
- Si vous souhaitez relancer une partie, il faut redémarrer les clients.

---

## **6. Notes Importantes**
- Minimum 2 joueurs sont nécessaires pour commencer une partie.
- Le client `0` doit obligatoirement lancer la partie.
- Le serveur reste actif tant qu’il n’est pas arrêté manuellement (`Ctrl + C`).
- Si un client se déconnecte avant la fin, la partie peut être annulée.

---

## **7. Exemples de Commandes**
### **Démarrer le serveur**
```sh
python3 Serveur.py
```
### **Connecter un client**
```sh
python3 Client.py
```
### **Démarrer la partie (client 0)**
```
Souhaitez-vous lancer la partie maintenant ? (yes/no) :
> YES
```