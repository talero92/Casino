from flask import Flask, request, jsonify
import json
import random
import time

app = Flask(__name__)

class Sala:
    def __init__(self, id, tipo_juego, apuesta_minima, creador):
        self.id = id
        self.tipo_juego = tipo_juego
        self.apuesta_minima = apuesta_minima
        self.creador = creador
        self.jugadores = [creador]
        self.estado = "esperando"
        self.apuestas = {}
        self.ganador = None

class Servidor:
    def __init__(self):
        self.salas = {}
        self.id_sala_actual = 1

    def crear_sala(self, datos):
        sala = Sala(self.id_sala_actual, datos['tipo_juego'], datos['apuesta_minima'], datos['creador'])
        self.salas[self.id_sala_actual] = sala
        self.id_sala_actual += 1
        return {'exito': True, 'id_sala': sala.id}

    def unirse_sala(self, datos):
        sala = self.salas.get(datos['id_sala'])
        if sala and len(sala.jugadores) < 4 and sala.estado == "esperando":
            sala.jugadores.append(datos['jugador'])
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se puede unir a la sala'}

    def obtener_salas(self):
        salas_info = [{
            'id': s.id, 
            'tipo_juego': s.tipo_juego, 
            'jugadores': s.jugadores, 
            'apuesta_minima': s.apuesta_minima, 
            'estado': s.estado
        } for s in self.salas.values()]
        return {'salas': salas_info}

    def abandonar_sala(self, datos):
        sala = self.salas.get(datos['id_sala'])
        if sala and datos['jugador'] in sala.jugadores:
            sala.jugadores.remove(datos['jugador'])
            if len(sala.jugadores) == 0:
                del self.salas[datos['id_sala']]
            elif datos['jugador'] == sala.creador and len(sala.jugadores) > 0:
                sala.creador = sala.jugadores[0]
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se puede abandonar la sala'}

    def comenzar_partida(self, datos):
        sala = self.salas.get(datos['id_sala'])
        if sala and sala.estado == "esperando" and len(sala.jugadores) > 1:
            sala.estado = "en_curso"
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se puede comenzar la partida'}

    def realizar_apuesta(self, datos):
        sala = self.salas.get(datos['id_sala'])
        if sala and sala.estado == "en_curso":
            sala.apuestas[datos['jugador']] = {
                'caballo': datos['caballo'], 
                'cantidad': datos['cantidad']
            }
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se puede realizar la apuesta'}

    def obtener_estado_carrera(self, id_sala):
        sala = self.salas.get(id_sala)
        if sala:
            return {
                'estado': sala.estado,
                'ganador': sala.ganador if sala.estado == "finalizada" else None
            }
        return {'exito': False, 'mensaje': 'Sala no encontrada'}

# Initialize servidor
servidor = Servidor()

# Flask routes
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/crear_sala', methods=['POST'])
def crear_sala():
    datos = request.get_json()
    response = servidor.crear_sala(datos)
    return jsonify(response)

@app.route('/unirse_sala', methods=['POST'])
def unirse_sala():
    datos = request.get_json()
    response = servidor.unirse_sala(datos)
    return jsonify(response)

@app.route('/obtener_salas', methods=['GET'])
def obtener_salas():
    response = servidor.obtener_salas()
    return jsonify(response)

@app.route('/abandonar_sala', methods=['POST'])
def abandonar_sala():
    datos = request.get_json()
    response = servidor.abandonar_sala(datos)
    return jsonify(response)

@app.route('/comenzar_partida', methods=['POST'])
def comenzar_partida():
    datos = request.get_json()
    response = servidor.comenzar_partida(datos)
    return jsonify(response)

@app.route('/realizar_apuesta', methods=['POST'])
def realizar_apuesta():
    datos = request.get_json()
    response = servidor.realizar_apuesta(datos)
    return jsonify(response)

@app.route('/estado_carrera/<int:id_sala>', methods=['GET'])
def estado_carrera(id_sala):
    response = servidor.obtener_estado_carrera(id_sala)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
