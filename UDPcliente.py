from socket import *

servidorNombre = "127.0.0.1"
servidorPuerto = 12000
clienteSocket = socket(AF_INET, SOCK_DGRAM)

mensaje = input("Ingrese mensaje:")
clienteSocket.sendto(bytes(mensaje, "utf-8"),(servidorNombre, servidorPuerto))
mensajeRespuesta, servidorDireccion = clienteSocket.recvfrom(2048)
print("Respuesta:\n" + str(mensajeRespuesta))
clienteSocket.close()