from socket import *
from threading import *

clients = set()

#Fonction pour le Thread
def clientThread(clientSocket, clientAddress):
    while True:
        message = clientSocket.recv(1024).decode("utf-8")
        print(clientAddress[0] + ":" + str(clientAddress[1]) + " : " + message)
        for client in clients:
            if client is not clientSocket:
                client.sendall(message.encode("utf-8"))
                # client.sendall((clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message ).encode("utf-8"))

        # Persister les messages dans le fichier chat.txt
        fichier = open("discussions.txt", "a")
        fichier.write("\n" + message)
        fichier.close()

        if not message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + clientAddress[1] + " disconnected")
            break

    clientSocket.close()

######## Creation Socket
hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
hostIP = "localhost"
portNumber = 5500
hostSocket.bind((hostIP, portNumber))
hostSocket.listen(5)
print("Attente de Connexion client...")

while True:
    clientSocket, clientAddress = hostSocket.accept()
    # Recuperation du contenu du fichier chat.txt
    fichier = open("discussions.txt", "r")
    old_chat = fichier.read()
    clientSocket.send(old_chat.encode("utf-8"))
    fichier.close()

    clients.add(clientSocket)
    print("Une connexion est établie à l'adresse ",
          clientAddress[0] + ":" + str(clientAddress[1]))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress, ))
    thread.start()
