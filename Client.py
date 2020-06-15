import speech_recognition as sr
import socket
import os
import time

bufferSize = 1024

r = sr.Recognizer()


def imprimir_tablero(TCPClientSocket):
    for i in range(10):
        for j in range(6):
            data = TCPClientSocket.recv(bufferSize)
            resp = data.decode('utf8')
            print('*' + resp, end='\t\t')
            time.sleep(0.1)
        print('\n')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
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
        data = TCPClientSocket.recv(bufferSize)
        print(data.decode('utf8'))
        res = 'n'
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
            # identificar ganador y terminar juego
            data = TCPClientSocket.recv(bufferSize)
            resp = data.decode('utf8')
            if resp == '1':
                print('Ganaste :D')
                break
    tiempo_final = time.time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('Duracion de la partida: %.2f segs.' % round(tiempo_ejecucion, 2))
    os.system("pause")
