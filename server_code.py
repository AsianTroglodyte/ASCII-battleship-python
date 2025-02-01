import socket 
import threading


def server_func():
    PORT = 5050
    # gethostname gets name of host. gethostbyname gets IP address using hostname
    SERVER = socket.gethostbyname(socket.gethostname())
    print(socket.gethostname)
    print(SERVER)

    server = socket.socket(socket.AF_INET socket.SOCK_STREAM)
# messages = queue.Queue()
# def server_func():
#     pass

# # other player
# client = []

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server.bind("localhost", 9999)

# def receive():
#     while True:
#         try:
#             message, addr - server.recvfrom(1024)
#         except:
#             pass


# broadcast_thread = "bruh"
# listening_thread = "bruh"