from socket import *

servidorPuerto = 12000
servidorSocket = socket(AF_INET, SOCK_DGRAM)
servidorSocket.bind(('', servidorPuerto))

print("El servidor está listo para recibir mensajes")
while 1:
    mensaje, clienteDireccion = servidorSocket.recvfrom(2048)
    print("Mensaje recibido de ", clienteDireccion)
    print(mensaje)
    mensajeRespuesta = mensaje.upper()
    print(mensajeRespuesta)
    servidorSocket.sendto(mensajeRespuesta, clienteDireccion)