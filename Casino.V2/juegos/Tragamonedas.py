import random
import time
import sys
from utils.helpers import limpiar_pantalla

def mostrar_carretes(carreteles):
    """Muestra los carretes de la tragamonedas."""
    print(" | ".join(carreteles))

def animacion_carretes():
    """Muestra una animación simple de los carretes girando."""
    simbolos = ['🍒', '🍋', '🍊', '🍏', '🍇', '🔔', '⭐', '💰']
    for _ in range(10):
        carretes = [random.choice(simbolos) for _ in range(3)]
        sys.stdout.write("\r" + " | ".join(carretes))
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def jugar_tragamonedas(saldo_inicial):
    saldo = saldo_inicial
    simbolos = ['🍒', '🍋', '🍊', '🍏', '🍇', '🔔', '⭐', '💰']

    while True:
        limpiar_pantalla()
        print("========================================")
        print("            Bienvenido a la Tragamonedas")
        print("========================================")
        print(f"Saldo actual: ${saldo}")

        # Solicitar apuesta
        while True:
            try:
                apuesta = int(input("Cuanto deseas apostar? $"))
                if 0 < apuesta <= saldo:
                    break
                else:
                    print("La apuesta debe ser mayor que 0 y menor o igual al saldo.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        # Tirar los carretes con animación
        print("\nTirando los carretes...")
        animacion_carretes()
        carretes = [random.choice(simbolos) for _ in range(3)]
        mostrar_carretes(carretes)

        # Comprobar combinaciones ganadoras
        if carretes[0] == carretes[1] == carretes[2]:  # Tres iguales
            ganancia = apuesta * 10
            saldo += ganancia
            print(f"FELICIDADES! Ganaste ${ganancia}!")
        elif (carretes[0] == carretes[1] or 
              carretes[1] == carretes[2] or 
              carretes[0] == carretes[2]):  # Dos iguales
            ganancia = apuesta * 5
            saldo += ganancia
            print(f"¡Buena jugada! Ganaste ${ganancia}!")
        elif '💰' in carretes:  # Jackpot
            ganancia = 50
            saldo += ganancia
            print(f"¡Jackpot! Ganaste ${ganancia}!")
        else:  # No hay ganancia
            saldo -= apuesta
            print(f"Lo siento, perdiste ${apuesta}.")

        print(f"Saldo actual: ${saldo}\n")

        jugar_de_nuevo = input("¿Quieres jugar de nuevo? [S/N]: ").lower()
        if jugar_de_nuevo != 's':
            print("Gracias por jugar. ¡Hasta luego!")
            return saldo

if __name__ == "__main__":
    saldo_inicial = 1000
    saldo_final = jugar_tragamonedas(saldo_inicial)
    print(f"Saldo final: ${saldo_final}")