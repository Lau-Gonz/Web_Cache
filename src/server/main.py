import os
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from env import SERVER_PORT
from utils import response, Sentence

SERVER_STORAGE = "src/server/storage"


def run_commad(sentence: Sentence) -> str:
    match sentence.command:
        case "ls":
            for option in sentence.options:
                match option:
                    case "-l" | "--list":
                        return response(200, "\n".join(os.listdir(SERVER_STORAGE)))
                    case _:
                        return response(404, f'option "{option}" not supported')
            return response(200, ", ".join(os.listdir(SERVER_STORAGE)))
        case "rm":
            for file in sentence.files:
                if not os.path.exists(f"{SERVER_STORAGE}/{file}"):
                    return response(404, f"{file} not found")
            [os.remove(file) for file in sentence.files]
            return response(200, "Ok")
        case "cat":
            file = sentence.files[0]
            if not os.path.exists(f"{SERVER_STORAGE}/{file}"):
                return response(404, "{file} not found")
            with open(f"{SERVER_STORAGE}/{file}") as file:
                content = "".join(file.readlines())
                return response(200, "Ok", len(content), "text/plain", content)
        case _:
            return response(200, get_help())


def get_help(command: str | None = None) -> str:
    match command:
        case "ls":
            return """\
        \nUsage: ls [OPTION]... [FILE]...\n\
        \nOptions:\
        \n-l | --list - Print as a list\
      """
        case "rm":
            return """\
        \nUsage: rm FILE\n
      """
        case "cat":
            return """\
        \nUsage: cat FILE\n
      """
        case "rm-cache":
            return """\
        \nUsage: rm-cache\n
      """
        case _:
            return """\
        \nUsage: command [OPTION]... [FILE]...\n\
        \nCommands:
        \nls - list available files\
        \nrm - remove file\
        \ncat - print content of file\
        \nrm-cache - remove web cache\
        \nhelp - show help\
      """


def handle_request(request: dict[str, dict[str, str]]) -> str:
    sleep(0.250)
    http_request: dict[str, str] = request.get("http") or {}
    match http_request.get("method"):
        case "get":
            return run_commad(Sentence(http_request.get("uri")))
        case _:
            return response(405, "Method not allowed")


def main() -> None:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", SERVER_PORT))
    server_socket.listen(1)
    print("El servidor está listo para recibir mensajes")
    while True:
        socket_connection, ip_client = server_socket.accept()
        print("Conexión establecida con ", ip_client)
        print("Mensaje recibido de ", ip_client)

        payload = str(socket_connection.recv(1024), "utf-8")
        socket_connection.send(bytes(payload, "utf-8"))
        socket_connection.close()
