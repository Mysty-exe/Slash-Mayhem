import socket
import threading
import uuid
import random
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.started = False
        self.game = {}

        self.playerNumber = 0
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen(4)

        while True:
            socket, address = self.server.accept()

            playerInfo = b''
            while True:
                buff = socket.recv(1024)
                playerInfo += buff
                if len(buff) < 1024:
                    break
                        
            playerInfo = json.loads(playerInfo.decode())

            self.game[playerInfo["id"]] = {"ready": False, "name": playerInfo["name"], "colour": playerInfo["colour"], "coords": playerInfo["coords"]}

            thread = threading.Thread(target=self.handleClient, args=(socket, address, playerInfo["id"]))
            thread.start()

    def handleClient(self, conn, address, userId):
        connected = True

        while connected:
            data = conn.recv(1024)
            print("Received: " + data.decode('utf-8'))
            data = json.loads(data.decode('utf-8'))

            if data["disconnect"] == True:
                connected = False
                continue

            connectedPlayers = 0
            for value in self.game.values():
                if value["ready"]:
                    connectedPlayers += 1

            if not self.started:
                if data["ready"] == True:
                    if not self.game[userId]["ready"]:
                        self.game[userId]["ready"] = True
                        connectedPlayers += 1
                        if connectedPlayers == len(list(self.game.keys())) and connectedPlayers > 1:
                            self.started = True
                
                if not self.started:
                    print("Sent: " + json.dumps({"started": self.started, "connections": connectedPlayers, "players": len(list(self.game.keys()))}))
                    conn.sendall(json.dumps({"started": self.started, "connections": connectedPlayers, "players": len(list(self.game.keys()))}).encode('utf-8'))

            if self.started:
                dataToSend = {"started": True, "players": {}}
                for key, value in self.game.items():
                    if "ready" not in data.keys():
                        self.game[userId]["coords"] = data["coords"]
                    dataToSend["players"][key] = value
                conn.sendall(json.dumps(dataToSend).encode('utf-8'))

        del self.game[userId]
        conn.close()
        print("Connection Closed")

host = socket.gethostbyname(socket.gethostname())
port = 9999

server = Server(host, port)
server.start()
