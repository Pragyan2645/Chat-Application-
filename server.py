import socket , threading                             

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

def listen_messages(client,username):
    while True:
        message = client.recv(2048).decode('utf-8')

        if message != '':
            final_msg = username + '~' + message
            send_mesg_to_all(final_msg)
        else:
            print(f"Messages send by {username} is empty")

def send_msg(client,message):
    client.sendall(message.encode())

def send_mesg_to_all(message):
    for user in active_clients:
        send_msg(user[1], message)

def client_handler(client):
    
    while True:
        username = client.recv(2048).decode('utf-8')

        if username != '':
            active_clients.append((username,client))
            break
        else:
            print("Username isn't defined")

    threading.Thread(target=listen_messages, args=(client,username, )).start()


def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"server running on {HOST} {PORT}")

    except:
        print(f"unable to bind host{HOST} and PORT {PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client,address = server.accept()

        print(f"successfully connected client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()



if __name__ == '__main__':
    main()
