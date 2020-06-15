import socket
import os
import sys
import threading
import time
from random import randint

bufferSize = 1024
n = 0
tablero = [['Jose', 'ojos azules', ' delgado', 'car3', 'car4', 'car5'],
           ['Juan', 'ojos cafes', 'delgado', 'car3', 'car4', 'car5'],
           ['Louis', 'ojos verdes', 'delgado', 'car3', 'car4', 'car5'],
           ['Norma', 'ojos azules', 'delgado', 'car3', 'car4', 'car5'],
           ['Lola', 'ojos cafes', 'delgado', 'car3', 'car4', 'car5'],
           ['Maria', 'ojos cafes', 'delgado', 'car3', 'car4', 'car5'],
           ['Rocio', 'ojos cafes', 'delgado', 'car3', 'car4', 'car5'],
           ['Frida', 'ojos azules', 'delgado', 'car3', 'car4', 'car5'],
           ['Celeste', 'ojos verdes', 'delgado', 'car3', 'car4', 'car5'],
           ['Alfredo', 'ojos cafes', 'delgado', 'car3', 'car4', 'car5']]


def imprimir_tablero(Client_conn):
    for i in range(10):
        for j in range(6):
            Client_conn.send(bytes(tablero[i][j], 'utf8'))


def servirPorSiempre(socketTcp, listaconexiones):
    barrier = threading.Barrier(int(numConn))
    lock = threading.Lock()
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, barrier, lock])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)


def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def jugador_activo(Client_conn, tablero):
    Client_conn.send(bytes('Tu turno', 'utf8'))
    data = Client_conn.recv(bufferSize)
    pregunta = data.decode('utf8')
    band = 'no'
    for i in range(6):
        if pregunta == tablero[n][i]:
            band = 'si'
        Client_conn.send(bytes(band, 'utf8'))


def recibir_datos(Client_conn, addr, barrier, lock):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        # Barrera que espera que se conecte los jugadores
        print(threading.current_thread().name,
              'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
        mensaje = 'Faltan {} jugadores para comenzar'.format(int(numConn) - (barrier.n_waiting + 1))
        Client_conn.send(bytes(mensaje, 'utf8'))
        jugador = barrier.wait()
        # Despues de la barrera
        print(threading.current_thread().name, 'Después de la barrera', jugador)
        time.sleep(1)
        Client_conn.send(bytes('Todos los jugadores se han conectado', 'utf8'))
        n = randint(0, 9)
        print('Se le asigno a {} {}'.format(threading.current_thread().name, tablero[n][0]))
        while True:
            # Lock para determinar turnos
            lock.acquire()
            print('Turno de ' + threading.current_thread().name)
            jugador_activo(Client_conn, tablero)
            lock.release()
            time.sleep(2)
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()


listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket, listaConexiones)
