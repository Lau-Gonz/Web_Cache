from socket import socket, AF_INET, SOCK_STREAM
from utils import response
from env import SERVER_NAME, SERVER_PORT


def main() -> None:
    try:
        i = 0
        while i < 10:
            i += 1
            socket_client = socket(AF_INET, SOCK_STREAM)
            socket_client.connect((SERVER_NAME, SERVER_PORT))
            message = input(">> ")
            socket_client.send(bytes(message, "utf-8"))
            res = socket_client.recv(1024)
            print("Respuesta:\n" + str(res, "utf-8"))
            socket_client.close()
    except ConnectionRefusedError:
        print(response(404, "Server Not Found"))
    except ConnectionResetError:
        print(response(999, "Se cerro el servidor we"))


if __name__ == "__main__":
    main()
