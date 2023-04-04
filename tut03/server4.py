# Name: Piyush Singh
# Roll: 2001CS51
# server4.py


'''
A server which echoes back the expression provided by the client.
Can handle multiple clients using 'select'
'''

import socket
import select
import sys

BUFFER_SIZE = 4096

# A utility function to echo back the expression to the client socket
def respond(client_sock, client_addr):
    data = client_sock.recv(BUFFER_SIZE)
    data = str(data.decode('utf-8'))
    if data:
        print(f'The client {client_addr[1]} sent data: {data}')
    if not data:
        return False
    print(f'Echo back: {data}')
    data = data.encode('utf-8')
    client_sock.send(data)


# Similar to server3.py, except the respond function echoes back the expression.
def Main():
    n = len(sys.argv)
    if n != 3:
        print(f'Exactly Two arguments expected, {n-1} passed. Terminating')
        return
    
    global host, port

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except Exception as e:
        if type(e) == ValueError:
            print('Invalid Port Number. Terminating')
        return

    if host.lower == 'localhost':
        host = '127.0.0.1'


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)
    
    try:
        server_socket.bind((host, port))
    except Exception as e:
        if type(e) == PermissionError:
            print("Permission Denied for the given port. Use a higher port number. Terminating")
        else:
            print("Invalid IP address or Port Number. Not able to bind.\nTerminating")
        return

    server_socket.listen(10)
    print(f'Listening on port {port}')

    sock_list = [server_socket]
    write_list = [server_socket]
    client_list = {}
    while sock_list:
        read_sock_list, _, x_list = select.select(sock_list, write_list, sock_list, 0.1)
        for curr_sock in read_sock_list:
            if curr_sock == server_socket:
                client_sock, client_addr = server_socket.accept()
                print(f'Connection established with {client_addr[0]} at port {client_addr[1]}')
                sock_list.append(client_sock)
                client_list[client_sock] = client_addr
            else:
                curr_addr = client_list[curr_sock]
                msg = respond(curr_sock, curr_addr)
                if msg is False:
                    print(f'Connection closed from socket at {client_list[curr_sock][0]} and port {client_list[curr_sock][1]}')
                    sock_list.remove(curr_sock)
                    del client_list[curr_sock]
        
if __name__ == '__main__':
    Main()