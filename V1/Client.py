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
        self.id = None
        self.vainceur = (None, 0)
        self.start_game = threading.Event()
        self.end_game = threading.Event()
        self.jeu = JeuYahtzee()
        self.recv = threading.Thread(target=self.recevoir)
        self.recv.start()
        
    def envoyer(self, msg: str) -> None:
        """Envoie un message au serveur."""
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
                    if self.id == "0":
                        buff = input("Souhaitez-vous lancer la partie maintenant ? (yes/no) : ")
                        while buff.upper() not in ["YES", "Y"]:
                            time.sleep(1)
                            buff = input("Souhaitez-vous lancer la partie maintenant ? (yes/no) : ")
                        self.envoyer("CMD:START")
                    else:
                        print("En attente du lancement de la partie...")
                elif type_msg == "CMD":
                    if data == "START":
                        self.start_game.set()
                elif type_msg == "WINNER":
                    id, score = data.split(':')
                    self.vainceur = (int(id), int(score))
                    self.end_game.set()
                else:
                    print(f"Message reçu : {data}")
            except (ConnectionResetError, ValueError, Exception) as e:
                print(f"Connexion fermée : {e}")
                break
        print("\nDéconnexion du serveur.")
                
    def deconnexion(self) -> None:
        """Ferme la connexion avec le serveur."""
        time.sleep(0.2)
        self.recv.join()  
        self.socket.close()

    def jouer_partie(self) -> None:
        """
        Joue une partie complète, envoie le score final au serveur,
        et affiche le résultat (victoire/défaite).
        """
        for tour in range(9): # 9 tours
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
        self.deconnexion()
              
def main() -> None:
    """Point d'entrée principal pour exécuter le client."""
    client = Client()
    print("Adresse du client :\n   ", client.SERVER, ":", client.PORT)
    client.start_game.wait()
    client.start_game.clear()
    client.jouer_partie()

if __name__ == '__main__':
    main()