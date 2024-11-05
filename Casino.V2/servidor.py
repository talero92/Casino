import socket
import threading
import json
import random
import time

class Servidor:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clientes = []
        self.salas = {}
        self.jugadores_conectados = set()
        self.carreras_activas = {}

    def iniciar(self):
        self.server.listen()
        print(f"Servidor iniciado en {self.host}:{self.port}")
        while True:
            cliente, direccion = self.server.accept()
            thread = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            thread.start()

    def manejar_cliente(self, cliente):
        nombre_jugador = None
        while True:
            try:
                mensaje = json.loads(cliente.recv(2048).decode('utf-8'))
                
                if 'nombre_jugador' in mensaje:
                    nombre_jugador = mensaje['nombre_jugador']
                    if nombre_jugador in self.jugadores_conectados:
                        respuesta = {
                            'exito': False,
                            'mensaje': 'Este jugador ya está conectado'
                        }
                        cliente.send(json.dumps(respuesta).encode('utf-8'))
                        cliente.close()
                        return
                    self.jugadores_conectados.add(nombre_jugador)
                    self.clientes.append(cliente)
                    print(f"Jugador {nombre_jugador} conectado")
                    continue

                if mensaje['accion'] == 'crear_sala':
                    self.crear_sala(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'unirse_sala':
                    self.unirse_sala(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'obtener_salas':
                    self.enviar_salas(cliente)
                elif mensaje['accion'] == 'obtener_info_sala':
                    self.obtener_info_sala(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'comenzar_partida':
                    self.comenzar_partida(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'abandonar_sala':
                    self.abandonar_sala(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'apostar_carrera':
                    self.procesar_apuesta_carrera(cliente, mensaje['datos'])
                elif mensaje['accion'] == 'actualizar_carrera':
                    self.actualizar_carrera(mensaje['datos'])
                elif mensaje['accion'] == 'desconectar':
                    self.desconectar_cliente(cliente, nombre_jugador)
                    break

            except Exception as e:
                print(f"Error: {e}")
                self.desconectar_cliente(cliente, nombre_jugador)
                break

    def crear_sala(self, cliente, datos):
        id_sala = len(self.salas) + 1
        nueva_sala = {
            'id': id_sala,
            'tipo_juego': datos['tipo_juego'],
            'apuesta_minima': datos['apuesta_minima'],
            'jugadores': [datos['creador']],
            'estado': 'esperando',
            'creador': datos['creador']
        }
        
        if datos['tipo_juego'] == "Carreras de Caballos":
            nueva_sala['apuestas'] = {}
            nueva_sala['caballos'] = []
            nueva_sala['estado_carrera'] = 'esperando'
        
        self.salas[id_sala] = nueva_sala
        respuesta = {
            'exito': True,
            'id_sala': id_sala,
            'mensaje': 'Sala creada exitosamente'
        }
        cliente.send(json.dumps(respuesta).encode('utf-8'))

    def obtener_info_sala(self, cliente, datos):
        id_sala = int(datos['id_sala'])
        if id_sala in self.salas:
            respuesta = {
                'exito': True,
                'info_sala': self.salas[id_sala]
            }
        else:
            respuesta = {
                'exito': False,
                'mensaje': 'La sala no existe'
            }
        cliente.send(json.dumps(respuesta).encode('utf-8'))

    def comenzar_partida(self, cliente, datos):
        id_sala = int(datos['id_sala'])
        if id_sala in self.salas:
            sala = self.salas[id_sala]
            if len(sala['jugadores']) > 1:
                sala['estado'] = 'en_curso'
                
                if sala['tipo_juego'] == "Carreras de Caballos":
                    self.iniciar_carrera_caballos(id_sala)
                
                respuesta = {
                    'exito': True,
                    'mensaje': 'Partida iniciada'
                }
            else:
                respuesta = {
                    'exito': False,
                    'mensaje': 'Se necesitan al menos 2 jugadores para comenzar'
                }
        else:
            respuesta = {
                'exito': False,
                'mensaje': 'La sala no existe'
            }
        cliente.send(json.dumps(respuesta).encode('utf-8'))
        def iniciar_carrera_caballos(self, id_sala):
            sala = self.salas[id_sala]
        caballos = [
            {"nombre": "Relámpago", "probabilidad": 1.2, "posicion": 0},
            {"nombre": "Tormenta", "probabilidad": 1.0, "posicion": 0},
            {"nombre": "Veloz", "probabilidad": 0.9, "posicion": 0},
            {"nombre": "Trueno", "probabilidad": 1.1, "posicion": 0},
            {"nombre": "Rayo", "probabilidad": 1.0, "posicion": 0}
        ]
        sala['caballos'] = caballos
        sala['estado_carrera'] = 'iniciando'
        self.carreras_activas[id_sala] = {
            'estado': 'iniciando',
            'caballos': caballos,
            'apuestas': {},
            'ganador': None,
            'distancia_meta': 50
        }
        self.notificar_inicio_carrera(id_sala)

    def actualizar_carrera(self, datos):
        id_sala = datos['id_sala']
        if id_sala in self.carreras_activas:
            carrera = self.carreras_activas[id_sala]
            if carrera['estado'] == 'en_curso':
                ganador = None
                for caballo in carrera['caballos']:
                    avance = random.randint(0, 2) * caballo['probabilidad']
                    caballo['posicion'] += avance
                    if caballo['posicion'] >= carrera['distancia_meta']:
                        ganador = caballo
                        break
                
                if ganador:
                    self.finalizar_carrera(id_sala, ganador)
                else:
                    self.notificar_estado_carrera(id_sala)

    def finalizar_carrera(self, id_sala, caballo_ganador):
        carrera = self.carreras_activas[id_sala]
        carrera['estado'] = 'finalizada'
        carrera['ganador'] = caballo_ganador
        
        # Procesar apuestas y distribuir ganancias
        for jugador, apuesta in carrera[' apuestas'].items():
            if apuesta['caballo'] == caballo_ganador['nombre']:
                # Distribuir ganancias
                pass
        
        self.notificar_fin_carrera(id_sala)

    def notificar_inicio_carrera(self, id_sala):
        mensaje = {
            'accion': 'inicio_carrera',
            'datos': {
                'id_sala': id_sala,
                'caballos': self.carreras_activas[id_sala]['caballos']
            }
        }
        self.enviar_mensaje_sala(id_sala, mensaje)

    def notificar_estado_carrera(self, id_sala):
        mensaje = {
            'accion': 'estado_carrera',
            'datos': {
                'id_sala': id_sala,
                'caballos': self.carreras_activas[id_sala]['caballos']
            }
        }
        self.enviar_mensaje_sala(id_sala, mensaje)

    def notificar_fin_carrera(self, id_sala):
        mensaje = {
            'accion': 'fin_carrera',
            'datos': {
                'id_sala': id_sala,
                'ganador': self.carreras_activas[id_sala]['ganador']
            }
        }
        self.enviar_mensaje_sala(id_sala, mensaje)

    def procesar_apuesta_carrera(self, cliente, datos):
        id_sala = datos['id_sala']
        jugador = datos['jugador']
        caballo = datos['caballo']
        cantidad = datos['cantidad']

        if id_sala in self.carreras_activas:
            carrera = self.carreras_activas[id_sala]
            if carrera['estado'] == 'iniciando':
                carrera['apuestas'][jugador] = {
                    'caballo': caballo,
                    'cantidad': cantidad
                }
                respuesta = {
                    'exito': True,
                    'mensaje': 'Apuesta registrada'
                }
            else:
                respuesta = {
                    'exito': False,
                    'mensaje': 'La carrera ya comenzó'
                }
        else:
            respuesta = {
                'exito': False,
                'mensaje': 'La carrera no existe'
            }
        cliente.send(json.dumps(respuesta).encode('utf-8'))

    def enviar_mensaje_sala(self, id_sala, mensaje):
        if id_sala in self.salas:
            mensaje_codificado = json.dumps(mensaje).encode('utf-8')
            for jugador in self.salas[id_sala]['jugadores']:
                for cliente in self.clientes:
                    try:
                        cliente.send(mensaje_codificado)
                    except Exception as e:
                        print(f"Error al enviar mensaje: {e}")

    def desconectar_cliente(self, cliente, nombre_jugador):
        if cliente in self.clientes:
            self.clientes.remove(cliente)
        
        if nombre_jugador:
            if nombre_jugador in self.jugadores_conectados:
                self.jugadores_conectados.remove(nombre_jugador)
            
            for id_sala in list(self.salas.keys()):
                if nombre_jugador in self.salas[id_sala]['jugadores']:
                    self.abandonar_sala(cliente, {
                        'id_sala': id_sala,
                        'jugador': nombre_jugador
                    })
        
        cliente.close()
        print(f"Cliente desconectado: {nombre_jugador}")

    def cerrar_servidor(self):
        for cliente in self.clientes:
            cliente.close()
        self.server.close()
        print("Servidor cerrado")

if __name__ == "__main__":
    servidor = Servidor()
    try:
        servidor.iniciar()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        servidor.cerrar_servidor()
    except Exception as e:
        print(f"Error en el servidor: {e}")
        servidor.cerrar_servidor()