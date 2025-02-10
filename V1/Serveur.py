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
        self.score_clients = []
        self.finished = 0
        self.wait_end = threading.Event()
        self.serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serveur_socket.bind(self.ADDR)
        except socket.error as e:
            print(f"Erreur de bind : {e}")
            raise

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

    def envoyer_a_tous(self, msg: str) -> None:
        """Diffuse un message à tous les clients connectés."""
        time.sleep(0.1)
        for client in self.clients:
            client.send(msg.encode(self.FORMAT))
            print(f"[SERVEUR] envoie : \"{msg}\" à client {self.indice_client(client)}")

    def recevoir(self, conn: socket.socket) -> str:
        """
        Reçoit un message d'un client.
        
        Returns:
            str: Message décodé.
            
        Raises:
            socket.error: En cas d'erreur de réception.
        """
        msg = conn.recv(self.BITS).decode(self.FORMAT)
        print(f"[SERVEUR] a reçu : \"{msg}\" de client {self.indice_client(conn)}")        
        return msg

    def deconnexion(self, conn: socket.socket) -> None:
        """Ferme la connexion d'un client et le retire de la liste."""
        conn.close()
        if conn in self.clients:
            self.clients.remove(conn)  

    def handle_client(self, client: socket.socket, addr: tuple[str, int]) -> None:
        """
        Gère la communication avec un client pendant une partie.
        
        Args:
            client (socket.socket): Connexion du client.
            addr: Adresse du client.
        """
        print(f"[NOUVELLE CONNEXION] {addr} connecté.")
        id_client = self.indice_client(client)

        while len(self.clients) < 2:
            time.sleep(1) 

        self.envoyer(f"HELLO:{id_client}", client)
        playing = True
        while playing:
            type_msg, data = self.recevoir(client).split(':', 1)
            if type_msg == "CMD":
                if data == "START":
                    self.envoyer_a_tous("CMD:START")
            elif type_msg == "SCORE":
                self.score_clients[id_client] = int(data)
                playing = False
        
        self.finished += 1
        if self.finished == len(self.clients):
            self.wait_end.set()
            
        self.wait_end.wait()
        self.wait_end.clear()
        self.envoyer(f"WINNER:{self.vainceur()}:{max(self.score_clients)}", client)
        time.sleep(0.2)
        self.finished -= 1
        self.deconnexion(client)
        
    def vainceur(self) -> int:
        """
        Détermine l'indice du client avec le score le plus élevé.
        
        Returns:
            int: Indice du gagnant.
        """
        return self.score_clients.index(max(self.score_clients))

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