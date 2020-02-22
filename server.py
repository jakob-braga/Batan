import socket
from _thread import *
import pickle
from game import Game
from player import Player
from structs import *


class Server:
    def __init__(self):
        self.ip = "192.168.1.110"
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = None
        self.idCount = 0

        self.game = Game()

    def socket_bind(self):
        try:
            self.s.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        self.s.listen(2)
        print("Waiting for a connection, Server Started")
        self.connected = set()

    def threaded_client(self, conn, p):
        print('player id is:', self.game.players[p].playerId)
        print('id count is:', self.idCount)
        conn.send(pickle.dumps(self.game.players[p]))
        print('player', p, 'ready')

        while True:
            try:
                data = pickle.loads(conn.recv(2048*8*2))

                if not data:
                    print('no data... breaking')
                    break
                else:

                    if data != 'get' and isinstance(data, str):
                        getattr(self.game, data)()
                    elif isinstance(data, Player):
                        self.game.update_player(data)
                    elif isinstance(data, dict):
                        getattr(self.game, data['call'])(data['data'])

                    self.game.vp_updates()

                    conn.sendall(pickle.dumps(self.game))
            except Exception as e:
                print(e)
                break

        print("Lost connection")
        try:
            print("lost client ", p)
        except:
            pass
        self.game.players.pop(p)
        self.idCount -= 1
        # this is a bug if you cant figure out why later you suck, (p is not a constant spot if
        # more than 1 player disconnects) TODO this
        conn.close()

    def run_server(self):
        while True:
            connect, addr = self.s.accept()
            print("Connected to:", addr)

            self.idCount += 1
            self.game.players.append(Player(self.idCount - 1))

            start_new_thread(self.threaded_client, (connect, self.idCount - 1))


server = Server()

server.socket_bind()

server.run_server()
