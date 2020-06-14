import speech_recognition as sr
import socket
import os
import time

bufferSize = 1024

r = sr.Recognizer()

tablero = []


def imprimir_tablero(tablero, n):
    a = ""
    if n == 3:
        print('\t0' + '\t1' + '\t2')
    if n == 5:
        print('\t0' + '\t1' + '\t2' + '\t3' + '\t4')
    for i in range(n):
        print(i, end="\t")
        for j in range(n):
            a += str(tablero[i][j]) + '\t'
        print(a)
        a = ""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    os.system("cls")
    print('Ingresa direccion del servidor')
    HOST = input()
    print('Ingresa puerto del servidor')
    PORT = int(input())
    TCPClientSocket.connect((HOST, PORT))
    tiempo_inicial = time.time()
    print("---------BIENVENIDO A ADIVINA QUIEN---------")
    os.system("cls")
    barrier = TCPClientSocket.recv(bufferSize)
    string1 = barrier.decode('utf8')
    print(string1)
    end_barrier = TCPClientSocket.recv(bufferSize)
    string2 = end_barrier.decode('utf8')
    print(string2)
    os.system("cls")
    print('Empezando juego')
    while True:
        os.system("cls")
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
            if text == 'Adios':
                break
            # print("Elige casilla")
            # x = int(input())
            # TCPClientSocket.sendall(bytes([x]))
    tiempo_final = time.time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('Duracion de la partida: %.2f segs.' % round(tiempo_ejecucion, 2))
    os.system("pause")
