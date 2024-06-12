import socket
import json

class Client:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 9999
        self.connected = False
        self.ready = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, player):
        if not self.connected:
            self.client.connect((self.host, self.port))
            self.connected = True
            data = json.dumps({"id": str(player.userId), "name": player.name, "colour": player.colour, "coords": [player.player_rect.x, player.player_rect.y]})
            self.send(data)

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.client.send(json.dumps({"disconnect": True}).encode('utf-8'))
            self.client.shutdown(socket.SHUT_RDWR)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ready = False
    
    def send(self, msg):
        self.client.sendall(msg.encode('utf-8'))

    def receive(self):
        msg = self.client.recv(1024)
        return msg.decode()
