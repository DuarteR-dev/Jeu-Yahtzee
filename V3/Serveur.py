import time
import socket
import threading

class Serveur:
    """Classe serveur gérant les connexions multi-clients pour un jeu Yahtzee en réseau."""
    
    def __init__(self, host=None, port=65432):
        """
        Initialise le serveur avec une configuration réseau.
        
        Args:
            host (str, optional): Adresse IP. Par défaut, utilise l'adresse locale.
            port (int): Port d'écoute (défaut: 65432).
            
        Raises:
            socket.error: Si le bind échoue.
        """
        self.FORMAT = 'utf-8'
        self.BITS = 1024
        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname()) if host is None else host
        self.ADDR = (self.SERVER, self.PORT)
        self.clients = []
        self.salons_libres = []
        self.salons_occupes = []
        self.salons = {} # {id_salon: [client1, client2, ...], ...}
        self.score_clients = []
        self.finished = {} # {id_salon : nb_cli_termine}
        self.wait_events = {} # {id_salon: threading.Event(), ...}
        self.start_events = {} # {id_salon: threading.Event(), ...}
        self.serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serveur_socket.bind(self.ADDR)
        except socket.error as e:
            print(f"Erreur de bind : {e}")
            raise
        
    def envoyer(self, msg: str, conn: socket.socket) -> None:
        """
        Envoie un message à un client spécifique.
        
        Args:
            msg (str): Message à envoyer.
            conn (socket.socket): Connexion du client cible.
        """
        time.sleep(0.1)
        conn.send(msg.encode(self.FORMAT))
        print(f"[SERVEUR] envoie : \"{msg}\" à client {self.indice_client(conn)}")

    def envoyer_a_tous(self, msg: str, id_salon: str) -> None:
        """
        Diffuse un message à tous les clients d'un même salon.

        Args:
            msg (str): Message à diffuser.
            id_salon (str): Identifiant du salon concerné.
        """
        time.sleep(0.1)
        clients_du_salon = self.salons.get(id_salon, [])
        if clients_du_salon == []:
            print(f"Le salon {id_salon} est vide.")
            return
        
        for client in clients_du_salon:
            self.envoyer(msg, client)
            print(f"[SERVEUR] envoie : \"{msg}\" à client {self.indice_client(client)}")

    def recevoir(self, conn: socket.socket) -> str:
        """
        Reçoit un message d'un client.

        Args:
            conn (socket.socket): Connexion du client.

        Returns:
            str: Message décodé.

        Raises:
            socket.error: En cas d'erreur de réception.
        """
        msg = conn.recv(self.BITS).decode(self.FORMAT)
        print(f"[SERVEUR] a reçu : \"{msg}\" de client {self.indice_client(conn)}")        
        return msg

    def deconnexion(self, conn: socket.socket) -> None:
        """
        Ferme la connexion d'un client et le retire de la liste.

        Args:
            conn (socket.socket): Connexion du client à fermer.
        """
        self.envoyer("CMD:DISCONNECT", conn)
        time.sleep(0.2)
        conn.close()
        if conn in self.clients:
            self.clients.remove(conn)
            
    def indice_client(self, conn: socket.socket) -> int:
        """
        Trouve l'indice d'un client dans la liste des connexions.
        
        Args:
            conn (socket.socket): Connexion client.
            
        Returns:
            int: Indice du client, ou longueur de la liste si non trouvé.
        """
        for i, client_conn in enumerate(self.clients):
            if client_conn == conn:
                return i
        return len(self.clients)
    
    def creer_salon(self, id_salon: str, client: socket.socket) -> None:
        """
        Ajoute un nouveau salon avec un client.

        Args:
            id_salon (str): L'identifiant du salon.
            client (Client): Le client à ajouter au salon.
        """
        if id_salon not in self.salons:
            self.salons[id_salon] = [client]
            self.finished[id_salon] = 0
            self.wait_events[id_salon] = threading.Event()
            self.start_events[id_salon] = threading.Event()
            if id_salon not in self.salons_libres:
                self.salons_libres.append(id_salon)
        else:
            print(f"Le salon {id_salon} existe déjà.")

    def rejoindre_salon(self, id_salon: str, client: socket.socket) -> bool:
        """
        Ajoute un client à un salon existant.

        Args:
            id_salon (str): L'identifiant du salon.
            client (socket.socket): Le client à ajouter au salon.

        Returns:
            bool: True si le client a rejoint le salon, False sinon.
        """
        if id_salon in self.salons_libres and id_salon not in self.salons_occupes:
            if id_salon in self.salons:
                self.salons[id_salon].append(client)
                return True
            else:
                print(f"Le salon \"{id_salon}\" n'existe pas.")
        else:
            print(f"Le salon \"{id_salon}\" n'est pas libre.")
        
        return False

    def supprimer_salon(self, id_salon: str) -> None:
        """
        Supprime un salon.

        Args:
            id_salon (str): L'identifiant du salon à supprimer.
        """
        if id_salon in self.salons_libres:
            self.salons_libres.remove(id_salon)
        if id_salon in self.salons_occupes:
            self.salons_occupes.remove(id_salon)
        if id_salon in self.wait_events:
            del self.wait_events[id_salon]
        if id_salon in self.start_events:
            del self.start_events[id_salon]
        if id_salon in self.salons :
            self.salons[id_salon].clear()
            del self.salons[id_salon]
            del self.finished[id_salon]
            print(f"Le salon {id_salon} a été supprimé.")
        else:
            print(f"Le salon {id_salon} n'existe pas.")
            
    def meilleur_score_salon(self, id_salon: str) -> tuple:
        """
        Trouve le client avec le meilleur score dans un salon.

        Args:
            id_salon (str): L'identifiant du salon.

        Returns:
            tuple: (ID du client gagnant, score le plus élevé).
        """
        id_clients = []
        for c in self.salons[id_salon]:
            id_clients.append(self.indice_client(c))
            
        meilleur_score = 0
        meilleur_client = None
    
        for id in id_clients:
            score_client = self.score_clients[id]
            if score_client > meilleur_score:
                meilleur_score = score_client
                meilleur_client = id
        
        return meilleur_client, meilleur_score

    def handle_client(self, client: socket.socket, addr: tuple[str, int]) -> None:
        """
        Gère la communication avec un client pendant une partie.
        
        Args:
            client (socket.socket): Connexion du client.
            addr: Adresse du client.
        """
        print(f"[NOUVELLE CONNEXION] {addr} connecté.")
        id_client = self.indice_client(client)
        id_salon = None
        while True:
            type_msg, data = self.recevoir(client).split(':', 1) 
            if type_msg == "CMD":
                if data == "DISCONNECT":
                    self.deconnexion(client)
                    return
                else:
                    print("Erreur, commande inconnue.")
                    print(f"Commande reçue : {data}")
                    return
            elif type_msg == "CHOICE":
                if data == "CREATE":
                    print(f"[CREATE] Client {id_client} crée le salon salon_{id_client}")
                    id_salon = f"salon_{id_client}"
                    self.creer_salon(f"salon_{id_client}", client)
                    self.start_events[id_salon].wait()
                    self.start_events[id_salon].clear()
                    self.envoyer("CMD:INIT", client)
                    self.envoyer_a_tous("CMD:WAIT", id_salon)
                    break
                elif data == "LIST":
                    self.envoyer(f"LIST:{self.salons_libres}", client)
            elif type_msg == "JOIN":
                id_salon = data
                self.start_events[id_salon].set()
                print(f"[JOIN] Client {id_client} rejoint le salon {id_salon}")
                self.rejoindre_salon(id_salon, client)
                self.envoyer(f"HELLO:{id_client}", client)
                break
            else:
                print("Erreur, message inconnu.")
                print(f"Message reçu : {type_msg} : {data}")
                return
        
        self.jouer_partie(client, id_client, id_salon)

    def jouer_partie(self, client: socket.socket, id_client: int, id_salon: str) -> None:
        """
        Gère une partie complète pour un client dans un salon.

        Args:
            client (socket.socket): Client jouant la partie.
            id_client (int): Identifiant du client.
            id_salon (str): Identifiant du salon.
        """
        while len(self.salons[id_salon]) < 2:
            time.sleep(1)
        
        playing = True
        while playing:
            type_msg, data = self.recevoir(client).split(':', 1)
            if type_msg == "CMD":
                if data == "START":
                    self.envoyer(f"HELLO:{id_client}", client)
                    self.salons_libres.remove(f"salon_{id_client}")
                    self.salons_occupes.append(f"salon_{id_client}")
                    self.envoyer_a_tous("CMD:START", id_salon)
                if data == "DISCONNECT":
                    self.deconnexion(client)
                    playing = False
            elif type_msg == "SCORE":
                self.score_clients[id_client] = int(data)
                playing = False
            elif type_msg == "CHAT":
                self.envoyer_a_tous(f"CHAT:{data}", id_salon)
        
        self.finished[id_salon] += 1
        if self.finished[id_salon] == len(self.salons[id_salon]):
            self.wait_events[id_salon].set()
            
        self.wait_events[id_salon].wait()
        self.wait_events[id_salon].clear()
        vainceur, score = self.meilleur_score_salon(id_salon)
        self.envoyer(f"WINNER:{vainceur}:{score}", client)
        time.sleep(0.2)
        self.supprimer_salon(id_salon)
        self.deconnexion(client)
        
    def start(self) -> None:
        """Démarre le serveur et accepte les connexions entrantes."""
        self.serveur_socket.listen()
        print(f"[ECOUTE] Le serveur écoute sur {self.SERVER}")

        try:
            while True:
                conn, addr = self.serveur_socket.accept()
                self.clients.append(conn)
                self.score_clients.append(0)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"[CONNEXIONS ACTIVES] {threading.active_count() - 1}")
        
        except KeyboardInterrupt:
            print("\n[ARRÊT] Fermeture du serveur...")
            self.serveur_socket.close()

def main() -> None:
    """Point d'entrée principal pour exécuter le serveur."""
    serveur = Serveur()
    print("Adresse du serveur :\n   ", serveur.SERVER, ":", serveur.PORT)
    print("[DÉMARRAGE] le serveur démarre...")
    serveur.start()

if __name__ == '__main__':
    main()