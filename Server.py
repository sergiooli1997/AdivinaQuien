import socket
import os
import sys
import threading
import time
from random import randint

bufferSize = 1024
tablero = [['Jose', 'football', 'natacion', 'basketball', 'taekwondo', 'volleyball'],
           ['Paco', 'taekwondo', 'football', 'bailar', 'baseball', 'fotografia'],
           ['Louis', 'teatro', 'kickboxing', 'fotografia', 'pintura', 'cantar'],
           ['Norma', 'piano', 'bailar', 'ciclismo', 'teatro', 'cantar'],
           ['Lola', 'teatro', 'fotografia', 'piano', 'buceo', 'volleyball'],
           ['Maria', 'ciclismo', 'bailar', 'pintura', 'cantar', 'surf'],
           ['Rocio', 'guitarra', 'pintura', 'volleyball', 'piano', 'basketball'],
           ['Frida', 'cantar', 'bailar', 'volleyball', 'teatro', 'guitarra'],
           ['Celeste', 'cantar', 'bailar', 'kickboxing', 'guitarra', 'fotografia'],
           ['Alfredo', 'surf', 'football', 'taekwondo', 'cantar', 'pintura']]

pregunta = ""
respuesta = ""

def imprimir_tablero(Client_conn):
    for i in range(10):
        for j in range(6):
            Client_conn.send(bytes(tablero[i][j], 'utf8'))
            time.sleep(0.3)

def actualiza_jugadores(Client_conn):
    Client_conn.send(bytes(pregunta, 'utf8'))
    Client_conn.send(bytes(respuesta, 'utf8'))
    print('Se actualizo')


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


def jugador_activo(Client_conn, tablero, n):
    global pregunta, respuesta
    Client_conn.send(bytes('Tu turno', 'utf8'))
    data = Client_conn.recv(bufferSize)
    pregunta = data.decode('utf8')
    band = 'no'
    # Comprobar si empata la pregunta con alguna de su personaje
    for i in range(6):
        if pregunta == tablero[n][i].lower():
            band = 'si'
    respuesta = band
    Client_conn.send(bytes(band, 'utf8'))
    # ¿Adivino el nombre del personaje?
    if tablero[n][0].lower() == pregunta:
        return True


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
        # Se asigna personaje aleatorio
        n = randint(0, 9)
        print('Se le asigno a {} {}'.format(threading.current_thread().name, tablero[n][0]))
        imprimir_tablero(Client_conn)
        while True:
            # Lock para determinar turnos
            lock.acquire()
            actualiza_jugadores(Client_conn)
            print('Turno de ' + threading.current_thread().name)
            band = jugador_activo(Client_conn, tablero, n)
            if band:
                print('gano ' + threading.current_thread().name)
                Client_conn.send(bytes('1', 'utf8'))
            else:
                print('Todavia no hay ganador')
                Client_conn.send(bytes('0', 'utf8'))
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
