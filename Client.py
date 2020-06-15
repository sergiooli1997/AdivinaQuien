import speech_recognition as sr
import socket
import os
import time

bufferSize = 1024
ganador = 'no'

r = sr.Recognizer()


def imprimir_tablero(TCPClientSocket):
    for i in range(10):
        for j in range(6):
            data = TCPClientSocket.recv(bufferSize)
            resp = data.decode('utf8')
            print('*' + resp, end='\t\t')
            time.sleep(0.1)
        print('\n')


def actualiza_jugadores(TCPClientSocket):
    pregunta = TCPClientSocket.recv(bufferSize)
    if pregunta.decode('utf8') != "":
        print('Se pregunto' + pregunta.decode('utf8'))
    respuesta = TCPClientSocket.recv(bufferSize)
    if respuesta.decode('utf8') != "":
        print('La respuesta ' + respuesta.decode('utf8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    global ganador
    os.system("cls")
    print('Ingresa direccion del servidor')
    HOST = input()
    print('Ingresa puerto del servidor')
    PORT = int(input())
    TCPClientSocket.connect((HOST, PORT))
    tiempo_inicial = time.time()
    barrier = TCPClientSocket.recv(bufferSize)
    string1 = barrier.decode('utf8')
    print(string1)
    end_barrier = TCPClientSocket.recv(bufferSize)
    string2 = end_barrier.decode('utf8')
    print(string2)
    print('Empezando juego')
    os.system("cls")
    print("---------BIENVENIDO A ADIVINA QUIEN---------")
    imprimir_tablero(TCPClientSocket)
    while True:
        # determinar si hay ganador antes de preguntar
        data = TCPClientSocket.recv(bufferSize)
        ganador = data.decode('utf8')
        if ganador == 'si':
            break
        # espera su turno
        data = TCPClientSocket.recv(bufferSize)
        print(data.decode('utf8'))
        # actualiza
        # actualiza_jugadores(TCPClientSocket)
        res = 'n'
        # recibe pregunta por microfono y confirma
        with sr.Microphone() as source:
            while res != 's':
                print('Lo escucho')
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    text = text.lower()
                    print('Usted dijo: {}'.format(text))
                    print('¿Es correcto? (s/n)')
                    res = input()
                except:
                    print('No se reconocio')
            TCPClientSocket.sendall(bytes(text, 'utf8'))
            # respuesta del servidor
            data = TCPClientSocket.recv(bufferSize)
            resp = data.decode('utf8')
            print(resp)
    #imprime ganador
    data = TCPClientSocket.recv(bufferSize)
    print(data.decode('utf8'))
    #imprime tiemoi de partida
    tiempo_final = time.time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('Duracion de la partida: %.2f segs.' % round(tiempo_ejecucion, 2))
    os.system("pause")
