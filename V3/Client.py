import threading
import time
import socket
from JeuYahtzee import JeuYahtzee

class Client:
    """Classe client pour se connecter à un serveur Yahtzee et jouer une partie."""
    
    def __init__(self, host=None, port=65432):
        """
        Initialise le client et se connecte au serveur.
        
        Args:
            host (str, optional): Adresse IP du serveur. Par défaut, utilise l'adresse locale.
            port (int): Port du serveur (défaut: 65432).
        """
        self.FORMAT = 'utf-8'
        self.BITS = 1024
        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname()) if host is None else host
        self.ADDR = (self.SERVER, self.PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)
        
        self.isInit = False #Si le client est le créateur du salon
        self.id = None
        self.vainceur = (None, 0)
        self.start_game = threading.Event()
        self.end_game = threading.Event()
        self.wait_list = threading.Event()
        self.salons_dispo = []
        
        self.jeu = JeuYahtzee()
        self.recv = threading.Thread(target=self.recevoir)
        self.recv.start()
        
    def envoyer(self, msg: str) -> None:
        """
        Envoie un message au serveur.

        Args:
            msg (str): Message à envoyer.
        """
        time.sleep(0.1)
        self.socket.send(msg.encode(self.FORMAT))

    def recevoir(self) -> None:
        """Écoute les messages du serveur dans un thread séparé."""
        while True:
            try:
                msg = self.socket.recv(self.BITS).decode(self.FORMAT)
                if not msg:
                    break
                type_msg, data = msg.split(':', 1)
                if type_msg == "HELLO":
                    self.id = data
                    print(f"Vous êtes le client {self.id}")
                elif type_msg == "CMD":
                    if data == "START":
                        self.start_game.set()
                    elif data == "INIT":
                        buff = input("Souhaitez-vous lancer la partie maintenant ? (yes/no) : ")
                        while buff.upper() not in ["YES", "Y"]:
                            time.sleep(1)
                            buff = input("Souhaitez-vous lancer la partie maintenant ? (yes/no) : ")
                        self.isInit = True
                        self.envoyer("CMD:START")
                    elif data == "WAIT" and not self.isInit:
                        print("En attente du lancement de la partie...")
                    elif data == "DISCONNECT":
                        break
                elif type_msg == "WINNER":
                    id, score = data.split(':')
                    self.vainceur = (int(id), int(score))
                    self.end_game.set()
                elif type_msg == "LIST":
                    self.salons_dispo = data
                    self.wait_list.set()
                elif type_msg == "CHAT":
                    source, message = data.split(':', 1)
                    if source != f"Message de client {self.id} " :
                        print(data)
                else:
                    print(f"Message reçu : {data}")
            except (ConnectionResetError, ValueError, Exception) as e:
                print(f"Connexion fermée : {e}")
                break
        print("\nDéconnexion du serveur.")
                
    def deconnexion(self) -> None:
        """Ferme la connexion avec le serveur."""
        self.envoyer("CMD:DISCONNECT")
        time.sleep(0.2)
        self.recv.join()
        self.socket.close()
        
    def chatter(self) -> None:
        """
        Active le mode chat permettant aux joueurs d'envoyer des messages au serveur.

        Le joueur peut taper '/retour' ou '/r' pour quitter le chat.
        """
        while True:
                choix = input("\nJouer [ENTRER] - Chatter (C): ")
                if choix.upper() in ["CHATTER", "C"]:
                    print("Mode chat (tapez '/retour' (ou /r) pour quitter)")
                    while True:
                        msg = input()
                        if msg.upper() in ["/RETOUR", "/R"]:
                            break
                        self.envoyer(f"CHAT:Message de client {self.id} : {msg}")
                else:
                    break

    def jouer_partie(self) -> None:
        """
        Joue une partie complète, envoie le score final au serveur,
        et affiche le résultat (victoire/défaite).
        """
        for tour in range(9): # 9 tours
            self.chatter()
            self.jeu.jouer_tour()
            score_client = self.jeu.afficher_score()
        
        self.envoyer(f"SCORE:{str(score_client)}")
        self.end_game.wait()
        self.end_game.clear()
        if score_client >= self.vainceur[1]:
            print("| VOUS AVEZ GAGNE          |")
        else:
            print(f"| CLIENT {self.vainceur[0]:<9} | {self.vainceur[1]:>5} |")
            print("+------------------+-------+")
            print("| VOUS AVEZ PERDU          |")
        print("+--------------------------+")     
        
    def menu(self):
        """Affiche le menu principal du client et gère les choix de connexion au salon."""
        print("Veuillez faire un choix.")
        print("1. Rejoindre un salon")
        print("2. Créer un salon")
        print("3. Quitter")
        choix = int(input("Votre choix : "))
        while choix < 1 or 3 < choix :
            print("Choix invalide, veuillez réessayer (1/2/3)")
            choix = int(input("Votre choix : "))
        if choix == 1:
            self.envoyer("CHOICE:LIST")
            self.wait_list.wait()
            self.wait_list.clear()
            if self.salons_dispo == '[]':
                print("\nAucun salon disponible.\n")
                self.menu()
            print("\nSalons disponibles :", self.salons_dispo)
            print("Veuillez choisir un salon.")
            choix = input("Votre choix (Retour ?): ")
            while choix not in self.salons_dispo and choix.upper() not in ["RETOUR", "R"]:
                print("Salon invalide, veuillez réessayer.")
                choix = input("Votre choix : ")
            if choix.upper() in ["RETOUR", "R"]:
                self.menu()
            self.envoyer(f"JOIN:{choix}")
        elif choix == 2:
            self.envoyer("CHOICE:CREATE")
        else:
            self.deconnexion()
            self.recv.join()
            return
        
        self.start_game.wait()
        self.start_game.clear()
        self.jouer_partie()

def main() -> None:
    """Point d'entrée principal pour exécuter le client."""
    client = Client()
    print("Adresse du client :\n   ", client.SERVER, ":", client.PORT)
    client.menu()

if __name__ == '__main__':
    main()