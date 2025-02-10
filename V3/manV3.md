# **Manuel d'Utilisation - Jeu de Yahtzee V3**

---

## **Introduction**
Cette version du jeu de Yahtzee permet aux joueurs de discuter en temps réel pendant la partie. Un serveur gère plusieurs salons où les joueurs peuvent se connecter, jouer et échanger des messages en direct.

---

## **1. Installation et Prérequis**
### **1.1. Environnement**
- Assurez-vous d’avoir tous les fichiers suivants :
  - `Serveur.py`
  - `Client.py`
  - `JeuYahtzee.py`
  - `JeuDeDes.py`
  - `Actions.py`

### **1.2. Bibliothèques Python**
Toutes les bibliothèques utilisées sont incluses dans Python de base (`socket`, `threading`, `time`, `random`). Aucune installation supplémentaire n'est requise.

---

## **2. Démarrage du Jeu**
### **2.1. Lancement du Serveur**
Avant que les joueurs puissent se connecter, le serveur doit être lancé.

1. **Ouvrir un terminal** et naviguer vers le dossier contenant les fichiers.
2. Exécuter la commande :
   ```sh
   python3 Serveur.py
   ```
3. Le serveur écoute les connexions et permet aux joueurs de rejoindre ou créer des salons.

---

### **2.2. Connexion des Clients**
Chaque joueur doit se connecter au serveur en lançant une instance du client.

1. **Ouvrir un terminal pour chaque joueur.**
2. Exécuter la commande suivante pour se connecter au serveur :
   ```sh
   python3 Client.py
   ```
3. Une fois connecté, chaque client accède à un menu permettant de créer ou rejoindre un salon.

---

### **2.3. Gestion des Salons**
- **Créer un salon** : Un joueur peut créer un salon et attendre que d'autres joueurs le rejoignent.
- **Rejoindre un salon** : Un joueur peut voir la liste des salons disponibles et en rejoindre un.
- **Démarrage de la partie** : Le créateur du salon décide quand lancer la partie.

---

## **3. Fonctionnalité de Chat**
Les joueurs peuvent envoyer des messages tout en jouant.

### **3.1. Utiliser le Chat**
- Pour entrer en mode chat, tapez `C` lorsque le programme le propose.
- Écrivez votre message et appuyez sur `Entrée`.
- Pour quitter le mode chat, tapez `/retour` ou `/r`.

---

## **4. Déroulement d'une Partie**
Chaque client joue plusieurs tours pour tenter d'obtenir le meilleur score.

### **4.1. Lancer les Dés**
- À chaque tour, le joueur peut lancer les dés jusqu'à 3 fois.
- Après chaque lancer, il peut choisir quels dés conserver et relancer les autres.

### **4.2. Choisir une Catégorie**
- Le joueur doit choisir une catégorie pour enregistrer son score parmi celles disponibles :
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
- Une fois une catégorie choisie, elle ne peut plus être modifiée.

---

## **5. Fin de la Partie et Résultats**
- Une fois la partie terminée, le score de chaque joueur est envoyé au serveur.
- Le serveur détermine le vainqueur et affiche les résultats à tous les joueurs.

---

## **6. Déconnexion**
- Une fois la partie terminée, le serveur ferme les connexions et les clients se déconnectent automatiquement.
- Si vous souhaitez rejouer, il faut redémarrer les clients.

---

## **7. Notes Importantes**
- Minimum **2 joueurs** sont nécessaires pour commencer une partie.
- Le créateur du salon doit lancer la partie.
- Le serveur reste actif tant qu’il n’est pas arrêté manuellement (`Ctrl + C`).
- Si un client se déconnecte avant la fin, la partie peut être annulée.
- Les joueurs peuvent envoyer des messages à tout moment via le chat intégré.

---

## **8. Exemples de Commandes**
### **Démarrer le serveur**
```sh
python3 Serveur.py
```
### **Connecter un client**
```sh
python3 Client.py
```
### **Démarrer une partie (créateur du salon)**
```
Souhaitez-vous lancer la partie maintenant ? (yes/no) :
> YES
```
### **Envoyer un message dans le chat**
```
Jouer [ENTRER] - Chatter (C): C
Message: Bonjour à tous !
```
### **Quitter le mode chat**
```
> /Retour
```