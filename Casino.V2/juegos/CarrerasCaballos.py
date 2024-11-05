import random
import time
import os
import sys

class Caballo:
    def __init__(self, nombre, probabilidad):
        self.nombre = nombre
        self.probabilidad = probabilidad
        self.posicion = 0

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_pista(caballos, distancia=50):
    limpiar_pantalla()
    print("=" * (distancia + 10))
    for caballo in caballos:
        pista = ["-"] * distancia
        if caballo.posicion < distancia:
            pista[caballo.posicion] = "🐎"
        else:
            pista[-1] = "🏁"
        print(f"{caballo.nombre.ljust(10)} {''.join(pista)}")
    print("=" * (distancia + 10))
    sys.stdout.flush()

def simular_carrera(caballos, distancia=50):
    while True:
        for caballo in caballos:
            avance = random.randint(0, 2)
            caballo.posicion += avance
            if caballo.posicion >= distancia:
                return caballo
        mostrar_pista(caballos, distancia)
        time.sleep(0.2)

def mostrar_caballos(caballos):
    print("\nCaballos disponibles:")
    for i, caballo in enumerate(caballos, 1):
        print(f"{i}. {caballo.nombre} (Probabilidad: {caballo.probabilidad})")

def obtener_apuesta(jugador, caballos, saldo):
    while True:
        try:
            mostrar_caballos(caballos)
            caballo_elegido = int(input(f"\n{jugador}, elige un caballo (1-{len(caballos)}): ")) - 1
            if 0 <= caballo_elegido < len(caballos):
                cantidad = int(input(f"¿Cuánto quieres apostar? (Saldo: ${saldo}): "))
                if 0 < cantidad <= saldo:
                    return caballos[caballo_elegido].nombre, cantidad
                else:
                    print("Cantidad inválida.")
            else:
                print("Selección inválida.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def jugar_carreras_caballos(jugadores):
    caballos = [
        Caballo("Relámpago", 1.2),
        Caballo("Tormenta", 1.0),
        Caballo("Veloz", 0.9),
        Caballo("Trueno", 1.1),
        Caballo("Rayo", 1.0)
    ]
    
    apuestas = {}
    for nombre, jugador in jugadores.items():
        apuesta = obtener_apuesta(nombre, caballos, jugador.saldo_multi)
        apuestas[nombre] = apuesta
        jugador.saldo_multi -= apuesta[1]
    
    input("\nPresiona Enter para comenzar la carrera...")
    
    print("\n¡Comienza la carrera!")
    ganador = simular_carrera(caballos)
    print(f"\n¡El ganador es {ganador.nombre}!")
    
    for jugador, (caballo_apostado, cantidad) in apuestas.items():
        if caballo_apostado == ganador.nombre:
            ganancia = int(cantidad * ganador.probabilidad * 2)
            jugadores[jugador].saldo_multi += ganancia
            print(f"{jugador} gana ${ganancia}!")
        else:
            print(f"{jugador} pierde ${cantidad}")
    
    for jugador in jugadores.values():
        print(f"\nSaldo de {jugador.nombre}: ${jugador.saldo_multi}")
    
    return jugadores

if __name__ == "__main__":
    # Código de prueba
    from collections import namedtuple
    JugadorPrueba = namedtuple('JugadorPrueba', ['nombre', 'saldo_multi'])
    jugadores_prueba = {
        "Jugador1": JugadorPrueba("Jugador1", 1000),
        "Jugador2": JugadorPrueba("Jugador2", 1000)
    }
    jugar_carreras_caballos(jugadores_prueba)