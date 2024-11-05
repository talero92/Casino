import random
import time
import sys
from utils.helpers import limpiar_pantalla

def jugar_chicken_road(saldo):
    distancia = 0
    while True:
        limpiar_pantalla()
        print("========================================")
        print("           CHICKEN ROAD")
        print("========================================")
        print(f"Saldo actual: ${saldo}")
        print("\nAyuda al pollo a cruzar la carretera!")
        print("Elige una línea (1-3) para que el pollo cruce.")
        print("Si el pollo cruza con éxito, ¡ganas!")
        
        apuesta = solicitar_apuesta(saldo)
        if apuesta is None:
            return saldo

        while True:
            linea_elegida = elegir_linea()
            resultado = cruzar_carretera(linea_elegida)
            distancia += 1

            if resultado:
                ganancia = apuesta * distancia
                saldo += ganancia
                print(f"\n¡El pollo cruzó con éxito! Ganaste ${ganancia}")
            else:
                saldo -= apuesta
                print(f"\n¡Oh no! El pollo no logró cruzar. Perdiste ${apuesta}")
                distancia = 0
                animacion_calavera()
                break
            
            print(f"\nSaldo actual: ${saldo}")
            
            if saldo <= 0:
                print("\n¡Te has quedado sin saldo!")
                return saldo
            
            if not jugar_de_nuevo():
                return saldo

def solicitar_apuesta(saldo):
    while True:
        try:
            apuesta = int(input("\n¿Cuánto quieres apostar? $"))
            if 0 < apuesta <= saldo:
                return apuesta
            else:
                print("La apuesta debe ser mayor que 0 y menor o igual a tu saldo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")
        
        if input("¿Quieres salir? (s/n): ").lower() == 's':
            return None

def elegir_linea():
    while True:
        try:
            linea = int(input("\nElige una línea (1-3): "))
            if 1 <= linea <= 3:
                return linea
            else:
                print("Por favor, elige una línea entre 1 y 3.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def cruzar_carretera(linea_elegida):
    print("\nEl pollo intenta cruzar...")
    time.sleep(1)
    return random.choice([True, False])

def animacion_pollito():
    frames = [
        "🐥   |   |   |",
        "   🐥|   |   |",
        "   |🐥  |   |",
        "   |   |🐥  |",
        "   |   |   |🐥",
    ]
    for _ in range(2):
        for frame in frames:
            sys.stdout.write("\r" + frame)
            sys.stdout.flush()
            time.sleep(0.3)
    print()

def animacion_calavera():
    print("\n¡Oh no! El pollo no logró cruzar...")
    time.sleep(1)
    print("☠️  ☠️  ☠️  ☠️  ☠️")
    time.sleep(1)

def jugar_de_nuevo():
    animacion_pollito()
    return input("\n¿Quieres jugar de nuevo? (s/n): ").lower() == 's'

if __name__ == "__main__":
    # Prueba del juego
    saldo_inicial = 1000
    saldo_final = jugar_chicken_road(saldo_inicial)
    print(f"\nJuego terminado. Saldo final: ${saldo_final}")