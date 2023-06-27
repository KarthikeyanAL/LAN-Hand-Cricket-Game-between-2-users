import socket
from _thread import *
import pickle
from game import Game
server= "127.0.0.1"
port= 5555 # >1024 because of privileges port
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port)) #one parameter we passing using  tuple
except socket.error as e:
    str(e)
s.listen()
print("Waiting for the connection, Server is Started")
connected = set()
games={}
id_Count=0
over= int(input('Enter Number of overs per innings: '))
over*=6
over1=over
def threaded_client(conn, p,game_Id):
    global id_Count
    conn.send(str.encode(str(p)))# send player number
    reply=""
    while True:
        try:
            data=conn.recv(4096).decode()# receive score input
            if game_Id in games:
                game=games[game_Id]
                if not data:
                    break
                else:
                    if data=="reset":
                        game.resetWent()
                    elif data=="score":
                        print("no problem")
                        print("here game.done_bat[0] = ", game.done_bat[0], "and the game.done_bat[0] =", game.done_bat[1])
                        if ((game.done_bat[0]==1 and game.bothWent()) or over1!=0):
                            print("2nd player as a batsman")#chase
                            game.score[1]=game.batsman(1,0,game.score[1],over1)
                            print("completed_1")
                            over1 -= 1;
                        elif game.bothWent() or over==0:#bat first
                            print("1st player as a batsman")
                            game.score[0] = game.batsman(0,1,game.score[0],over)
                            print("completed_2")
                            over -= 1;
                        game.resetWent() #resetted-after every ball
                    elif data !="get":
                            game.play(p,data) #game initiation
                conn.sendall(pickle.dumps(game))#byte-to-obj
            else:
                break
        except:
            break # control will be shifted to 2 nd player
    print("Lost the connection")
    try:
        del games[game_Id]#delete objects
        print("Closing the Game",game_Id)
    except:
        pass
    id_Count-=1
    conn.close()
while True:
    conn,addr=s.accept()
    print("Connected to the :", addr)
    id_Count +=1
    p=0
    game_Id=(id_Count - 1)//2  #game id for 2 players
    print(id_Count)
    if id_Count%2==1: #for 1 st player
        games[game_Id]=Game(game_Id)#invoking Game class
        print("Creating a new_game...")
    else:
        print("2nd is connected")  #for 2nd player
        games[game_Id].ready=True
        p=1
    start_new_thread(threaded_client,(conn,p,game_Id))
