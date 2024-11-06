import socket
import threading
import time
import json
import os
import sys
import select
import msvcrt
import random
from utils.helpers import limpiar_pantalla
from juegos.CarrerasCaballos import jugar_carreras_caballos

def jugar_Multijugador(usuario):
    cliente = Cliente()
    
    while True:
        limpiar_pantalla()
        print("========================================")
        print("       CONEXIÓN AL SERVIDOR")
        print("========================================")
        print("1. Conectar a servidor local")
        print("2. Conectar a servidor Render")
        print("3. Conectar a otro servidor remoto")
        print("4. Volver al menú principal")
        print("========================================")
        
        try:
            opcion = int(input("\nSelecciona una opción: "))
            
            if opcion == 1:
                host = 'localhost'
            elif opcion == 2:
                print("\nServidores disponibles:")
                print("1. casino-gib2.onrender.com")
                print("2. 3.75.158.163")
                print("3. 3.125.183.140")
                print("4. 35.157.117.28")
                
                servidor = int(input("\nSelecciona un servidor (1-4): "))
                if servidor == 1:
                    host = 'casino-gib2.onrender.com'
                elif servidor == 2:
                    host = '3.75.158.163'
                elif servidor == 3:
                    host = '3.125.183.140'
                elif servidor == 4:
                    host = '35.157.117.28'
                else:
                    print("\nOpción no válida")
                    time.sleep(2)
                    continue
            elif opcion == 3:
                host = input("\nIngresa la IP del servidor: ")
            elif opcion == 4:
                return usuario
            else:
                print("\nOpción no válida")
                time.sleep(2)
                continue
                
            print("\nConectando al servidor...")
            if cliente.conectar(host):
                print("Conexión exitosa!")
                time.sleep(1)
                break
            else:
                print("\nNo se pudo conectar al servidor")
                time.sleep(2)
                
        except ValueError:
            print("\nPor favor ingresa un número válido")
            time.sleep(2)
    
    while True:
        limpiar_pantalla()
        print("========================================")
        print("          MODO MULTIJUGADOR")
        print("========================================")
        print(f"Usuario: {usuario.nombre}")
        print(f"Saldo: ${usuario.saldo_multi}")
        print("========================================")
        print("1. Crear sala")
        print("2. Unirse a sala")
        print("3. Ver salas disponibles")
        print("4. Volver al menú principal")
        print("========================================")
        
        while True:
            try:
                opcion = int(input("\nSelecciona una opción: "))
                if 1 <= opcion <= 4:
                    break
                print("Opción no válida")
            except ValueError:
                print("Por favor ingresa un número válido")
        
        if opcion == 1:
            crear_sala(cliente, usuario)
        elif opcion == 2:
            id_sala = unirse_sala(cliente, usuario)
            if id_sala:
                gestionar_sala(cliente, usuario, id_sala)
        elif opcion == 3:
            ver_salas_disponibles(cliente)
        elif opcion == 4:
            return usuario
    
    return usuario

class Cliente:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False

    def conectar(self, host, port=10000):
        try:
            self.socket.settimeout(10)
            print(f"\nIntentando conectar a {host}:{port}...")
            self.socket.connect((host, port))
            self.socket.settimeout(None)
            self.conectado = True
            return True
        except socket.timeout:
            print("\nTimeout: El servidor no responde")
            return False
        except socket.gaierror:
            print("\nError: No se puede resolver el nombre del servidor")
            return False
        except ConnectionRefusedError:
            print("\nError: Conexión rechazada por el servidor")
            return False
        except Exception as e:
            print(f"\nError al conectar: {e}")
            return False

    def reconectar(self, host, port=10000, intentos=3):
        for i in range(intentos):
            print(f"\nIntento de reconexión {i+1}/{intentos}")
            if self.conectar(host, port):
                return True
            time.sleep(2)
        return False

    def enviar(self, mensaje):
        try:
            self.socket.send(json.dumps(mensaje).encode('utf-8'))
        except ConnectionError:
            print("\nPérdida de conexión con el servidor")
            self.conectado = False
            raise
        except Exception as e:
            print(f"\nError al enviar mensaje: {e}")
            self.conectado = False
            raise

    def recibir(self):
        try:
            return json.loads(self.socket.recv(2048).decode('utf-8'))
        except ConnectionError:
            print("\nPérdida de conexión con el servidor")
            self.conectado = False
            return None
        except json.JSONDecodeError:
            print("\nError: Datos recibidos inválidos")
            return None
        except Exception as e:
            print(f"\nError al recibir mensaje: {e}")
            self.conectado = False
            return None

    def ping(self):
        try:
            self.enviar({"accion": "ping"})
            response = self.recibir()
            return response and response.get("accion") == "pong"
        except:
            return False

def crear_sala(cliente, usuario):
    limpiar_pantalla()
    print("\n=== Crear Nueva Sala ===")
    
    print("\nSelecciona el tipo de juego:")
    print("1. Ruleta Battle")
    print("2. Poker")
    print("3. Blackjack Multijugador")
    print("4. Carreras de Caballos")
    
    while True:
        try:
            opcion = int(input("\nSelecciona una opción: "))
            if 1 <= opcion <= 4:
                break
            print("Opción no válida")
        except ValueError:
            print("Por favor ingresa un número válido")
    
    tipos_juego = ["Ruleta Battle", "Poker", "Blackjack", "Carreras de Caballos"]
    tipo_juego = tipos_juego[opcion-1]
    
    while True:
        try:
            apuesta = int(input("\nIngresa la apuesta mínima para la sala: $"))
            if apuesta > 0 and apuesta <= usuario.saldo_multi:
                break
            print("La apuesta debe ser mayor a 0 y menor o igual a tu saldo")
        except ValueError:
            print("Por favor ingresa un número válido")
    
    mensaje = {
        "accion": "crear_sala",
        "datos": {
            "tipo_juego": tipo_juego,
            "apuesta_minima": apuesta,
            "creador": usuario.nombre
        }
    }
    
    cliente.enviar(mensaje)
    respuesta = cliente.recibir()
    
    if respuesta and respuesta.get("exito"):
        print("\n¡Sala creada exitosamente!")
        print(f"ID de sala: {respuesta['id_sala ']}")  
        time.sleep(2)  
        gestionar_sala(cliente, usuario, respuesta['id_sala'])  
    else:  
        print("\nError al crear la sala")  
        time.sleep(2)  

def ver_salas_disponibles(cliente):  
    mensaje = {  
        "accion": "obtener_salas"  
    }  
    cliente.enviar(mensaje)  
    respuesta = cliente.recibir()  
    
    if not respuesta or not respuesta.get("salas"):  
        print("\nNo hay salas disponibles")  
        time.sleep(2)  
        return  
    
    salas = respuesta["salas"]  
    print("\n=== Salas Disponibles ===")  
    for sala in salas:  
        print(f"\nSala {sala['id']}:")  
        print(f"Tipo: {sala['tipo_juego']}")  
        print(f"Jugadores: {len(sala['jugadores'])}/4")  
        print(f"Apuesta mínima: ${sala['apuesta_minima']}")  
        print(f"Estado: {sala['estado']}")  
    
    time.sleep(2)  

def unirse_sala(cliente, usuario):  
    mensaje = {  
        "accion": "obtener_salas"  
    }  
    cliente.enviar(mensaje)  
    respuesta = cliente.recibir()  
    
    if not respuesta or not respuesta.get("salas"):  
        print("\nNo hay salas disponibles")  
        time.sleep(2)  
        return None  
    
    salas = respuesta["salas"]  
    print("\n=== Salas Disponibles ===")  
    for sala in salas:  
        print(f"\nSala {sala['id']}:")  
        print(f"Tipo: {sala['tipo_juego']}")  
        print(f"Jugadores: {len(sala['jugadores'])}/4")  
        print(f"Apuesta mínima: ${sala['apuesta_minima']}")  
        print(f"Estado: {sala['estado']}")  
    
    while True:  
        try:  
            id_sala = input("\nIngresa el ID de la sala a la que quieres unirte (0 para volver): ")  
            if id_sala == "0":  
                return None  
            
            mensaje = {  
                "accion": "unirse_sala",  
                "datos": {  
                    "id_sala": int(id_sala),  
                    "jugador": usuario.nombre  
                }  
            }  
            cliente.enviar(mensaje)  
            respuesta = cliente.recibir()  
            
            if respuesta and respuesta.get("exito"):  
                print("\n¡Te has unido a la sala!")  
                time.sleep(2)  
                return int(id_sala)  
            else:  
                print("\nError al unirse a la sala")  
                time.sleep(2)  
        except ValueError:  
            print("Por favor ingresa un número válido")  
            time.sleep(2)  

def gestionar_sala(cliente, usuario, id_sala):  
    while True:  
        limpiar_pantalla()  
        print(f"\n=== Sala {id_sala} ===")  
        
        mensaje = {  
            "accion": "obtener_info_sala",  
            "datos": {  
                "id_sala": id_sala  
            }  
        }  
        cliente.enviar(mensaje)  
        respuesta = cliente.recibir()  
        
        if not respuesta or not respuesta.get("exito"):  
            print("Error al obtener información de la sala")  
            time.sleep(2)  
            return  
        
        info_sala = respuesta["info_sala"]  
        print(f"Tipo de juego: {info_sala['tipo_juego']}")  
        print(f"Apuesta mínima: ${info_sala['apuesta_minima']}")  
        print("\nJugadores en la sala:")  
        for jugador in info_sala['jugadores']:  
            if jugador == info_sala['creador']:  
                print(f"- {jugador} (Creador)")  
            else:  
                print(f"- {jugador}")  
        
        print("\nOpciones:")  
        if usuario.nombre == info_sala['creador']:  
            print("1. Comenzar partida")  
        print("2. Abandonar sala")  
        print("3. Actualizar información")  
        
        print("\nLa información se actualizará automáticamente cada 5 segundos.")  
        print("Selecciona una opción o espera para actualizar...")  
        
        start_time = time.time()  
        while time.time() - start_time < 5:  
            if msvcrt.kbhit():  
                 opcion = msvcrt.getch().decode()  
                break  
        else:  
            continue  

        if opcion == '1' and usuario.nombre == info_sala['creador']:  
            if len(info_sala['jugadores']) > 1:  
                mensaje = {  
                    "accion": "comenzar_partida",  
                    "datos": {  
                        "id_sala": id_sala  
                    }  
                }  
                cliente.enviar(mensaje)  
                respuesta = cliente.recibir()  
                if respuesta and respuesta.get("exito"):  
                    print("\n¡La partida ha comenzado!")  
                    time.sleep(2)  
                    limpiar_pantalla()  
                    print("========================================")  
                    print("         CARRERAS DE CABALLOS")  
                    print("========================================")  
                    
                    caballos = [  
                        "⚡ Relámpago",  
                        "🌟 Estrella Fugaz",  
                        "🔥 Fuego Salvaje",  
                        "💨 Ventisca",  
                        "🌈 Arcoíris"  
                    ]  
                    
                    print("\nCaballos participantes:")  
                    for i, caballo in enumerate(caballos, 1):  
                        print(f"{i}. {caballo}")  
                    
                    while True:  
                        try:  
                            caballo_elegido = int(input("\nElige tu caballo (1-5): ")) - 1  
                            if 0 <= caballo_elegido < len(caballos):  
                                apuesta = int(input(f"¿Cuánto quieres apostar en {caballos[caballo_elegido]}? $"))  
                                if 0 < apuesta <= usuario.saldo_multi:  
                                    break  
                                else:  
                                    print("La apuesta debe ser mayor que 0 y menor o igual a tu saldo.")  
                            else:  
                                print("Por favor, elige un número válido de caballo.")  
                        except ValueError:  
                            print("Por favor, ingresa un número válido.")  
                    
                    mensaje = {  
                        "accion": "realizar_apuesta",  
                        "datos": {  
                            "id_sala": id_sala,  
                            "jugador": usuario.nombre,  
                            "caballo": caballo_elegido,  
                            "cantidad": apuesta  
                        }  
                    }  
                    cliente.enviar(mensaje)  
                    respuesta = cliente.recibir()  
                    
                    if respuesta and respuesta.get("exito"):  
                        print("\n¡Apuesta registrada con éxito!")  
                        print("\nLa carrera comenzará en breve...")  
                        time.sleep(2)  
                        
                        distancia = 20  
                        posiciones = [0] * len(caballos)  
                        
                        while max(posiciones) < distancia:  
                            limpiar_pantalla()  
                            print("\nCarrera en progreso:\n")  
                            for i, caballo in enumerate(caballos):  
                                pista = ["_"] * distancia  
                                if posiciones[i] < distancia:  
                                    pista[posiciones[i]] = caballo.split()[0]  
                                print(f"{caballo}: {''.join(pista)}")  
                                
                                if posiciones[i] < distancia:  
                                    posiciones[i] += random.randint(0, 2)  
                            time.sleep(0.5)  
                        
                        ganador = posiciones.index(max(posiciones))  
                        print(f"\n¡{caballos[ganador]} ha ganado la carrera!")  
                        
                        if ganador == caballo_elegido:  
                            ganancia = apuesta * 2  
                            usuario.actualizar_saldo_multi(ganancia)  
                            print(f"\n¡Felicidades! Has ganado ${ganancia}")  
                        else:  
                            usuario.actualizar_saldo_multi(-apuesta)  
                            print(f"\nLo siento, has perdido ${apuesta}")  
                        
                        print(f"\nSaldo actual: ${usuario.saldo_multi}")  
                        input("\nPresiona Enter para continuar...")  
                    else:  
                        print("\nError al registrar la apuesta")  
                        time.sleep(2)  

                    return  
                else:  
                    print("\nError al comenzar la partida")  
                    time.sleep(2)  
            else:  
                print("\nSe necesitan al menos 2 jugadores para comenzar")  
                time.sleep(2)  
        elif opcion == '2':  
            mensaje = {  
                "accion": "abandonar_sala",  
                "datos": {  
                    "id_sala": id_sala,  
                    "jugador": usuario.nombre  
                }  
            }  
            cliente.enviar(mensaje)  
            respuesta = cliente.recibir()  
            if respuesta and respuesta.get("exito"):  
                print("\nHas abandonado la sala")  
                time ```python
                time.sleep(2)
                return
            else:
                print("\nError al abandonar la sala")
                time.sleep(2)
        elif opcion == '3':
            continue  # Simplemente vuelve al inicio del bucle para actualizar
        else:
            print("\nOpción no válida")
            time.sleep(2)

def jugar_carreras_caballos(cliente, usuario, id_sala):
    limpiar_pantalla()
    print("\n=== Carreras de Caballos ===")
    
    while True:
        mensaje = {
            "accion": "obtener_estado_carrera",
            "datos": {
                "id_sala": id_sala
            }
        }
        cliente.enviar(mensaje)
        respuesta = cliente.recibir()
        
        if not respuesta or not respuesta.get("exito"):
            print("Error al obtener el estado de la carrera")
            time.sleep(2)
            return
        
        estado_carrera = respuesta["estado_carrera"]
        print(f"\nEstado de la carrera: {estado_carrera}")
        
        if estado_carrera == "iniciando":
            print("\nLa carrera está por comenzar...")
            time.sleep(2)
        elif estado_carrera == "en_curso":
            print("\nLa carrera está en curso...")
            time.sleep(2)
        elif estado_carrera == "finalizada":
            print("\nLa carrera ha finalizado")
            print(f"El ganador es: {respuesta['ganador']}")
            time.sleep(2)
            return
        
        mensaje = {
            "accion": "apostar_carrera",
            "datos": {
                "id_sala": id_sala,
                "jugador": usuario.nombre,
                "caballo": input("\nIngresa el nombre del caballo al que quieres apostar: "),
                "cantidad": int(input("Ingresa la cantidad a apostar: $"))
            }
        }
        cliente.enviar(mensaje)
        respuesta = cliente.recibir()
        
        if respuesta and respuesta.get("exito"):
            print("\n¡Apuesta registrada!")
            time.sleep(2)
        else:
            print("\nError al registrar la apuesta")
            time.sleep(2)

        while True:
            mensaje = {
                "accion": "obtener_estado_carrera",
                "datos": {
                    "id_sala": id_sala
                }
            }
            cliente.enviar(mensaje)
            respuesta = cliente.recibir()
            
            if respuesta and respuesta.get("estado_carrera") == "finalizada":
                print("\nLa carrera ha terminado!")
                print(f"El caballo ganador es: {respuesta['ganador']}")
                
                if respuesta.get("ganadores") and usuario.nombre in respuesta["ganadores"]:
                    ganancia = respuesta["ganadores"][usuario.nombre]
                    print(f"\n¡Felicidades! Has ganado ${ganancia}")
                    usuario.actualizar_saldo_multi(ganancia)
                else:
                    print("\nLo siento, no has ganado esta vez.")
                
                print(f"\nTu saldo actual es: ${usuario.saldo_multi}")
                input("\nPresiona Enter para continuar...")
                return

            time.sleep(5)  # Esperar 5 segundos antes de verificar de nuevo

if __name__ == "__main__":
    from data.usuarios import Usuario
    usuario_prueba = Usuario("test")
    jugar_Multijugador(usuario_prueba)
