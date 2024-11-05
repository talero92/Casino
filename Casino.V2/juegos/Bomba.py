import random

import time

import os


def limpiar_pantalla():

    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_instrucciones():

    """Muestra las instrucciones del juego."""

    print("========================================")

    print("         Juego de la Bomba")

    print("========================================")

    print("Adivina la palabra relacionada con la informática o la electricidad.")

    print("Tienes 10 segundos para adivinar. ¡Buena suerte!")

    print("========================================")


def elegir_palabra_y_pista():

    """Elige una palabra aleatoria de la lista junto con su pista."""

    palabras_y_pistas = {

        'computadora': "Dispositivo que usas para trabajar o jugar.",

        'teclado': "Dispositivo que usas para escribir.",

        'ratón': "Dispositivo que controla el cursor en la pantalla.",

        'pantalla': "Superficie donde ves la información.",

        'software': "Programas que hacen que la computadora funcione.",

        'hardware': "Partes físicas de la computadora.",

        'circuito': "Ruta por donde fluye la electricidad.",

        'batería': "Fuente de energía que almacena electricidad.",

        'voltaje': "Fuerza que empuja la corriente eléctrica.",

        'internet': "Red global que conecta computadoras en todo el mundo.",

        'servidor': "Computadora que proporciona recursos a otras computadoras.",

        'código': "Instrucciones escritas para que la computadora realice tareas.",

        'virus': "Programa dañino que puede afectar a la computadora.",

        'router': "Dispositivo que dirige el tráfico de datos en una red.",

        'cable': "Conductor que transporta electricidad o datos.",

        'chip': "Pequeño circuito que realiza funciones específicas.",

        'datos': "Información procesada o almacenada.",

        'byte': "Unidad básica de información en computación.",

    }

    palabra = random.choice(list(palabras_y_pistas.keys()))

    pista = palabras_y_pistas[palabra]

    return palabra, pista


def mostrar_bomba(tiempo_restante):

    """Muestra una bomba en ASCII con el tiempo restante."""

    bomba_ascii = f"""

        ██████████████████

        ████  ██████  ████

        ████  ██████  ████

        ████  ██████  ████

        ██████████████████

        ██              ██

        ██  Tiempo: {tiempo_restante:2d} seg  ██

        ██              ██

        ██████████████████

        ████  ██████  ████

        ████  ██████  ████

        ████  ██████  ████

        ██████████████████

    """

    print(bomba_ascii)


def jugar_bomba(saldo):

    """Inicia el juego."""

    limpiar_pantalla()

    mostrar_instrucciones()

    palabra, pista = elegir_palabra_y_pista()

    

    while True:

        print(f"\nLa pista es: {pista}")

        print(f"Saldo actual: ${saldo}")

        

        # Solicitar apuesta

        while True:

            try:

                apuesta = int(input("\n¿Cuánto quieres apostar? $"))

                if 0 < apuesta <= saldo:

                    break

                else:

                    print("La apuesta debe ser mayor que 0 y menor o igual a tu saldo.")

            except ValueError:

                print("Por favor, ingresa un número válido.")


        tiempo_inicio = time.time()

        

        while True:

            tiempo_actual = time.time()

            tiempo_transcurrido = tiempo_actual - tiempo_inicio

            tiempo_restante = max(0, int(10 - tiempo_transcurrido))

            

            limpiar_pantalla()

            print(f"La pista es: {pista}")

            mostrar_bomba(tiempo_restante)

            

            if tiempo_restante == 0:

                print(f"\n¡BOOM! Se acabó el tiempo. La palabra era: {palabra}")

                saldo -= apuesta

                break

                

            respuesta = input("\n¿Cuál es la palabra? ").lower()

            

            if respuesta == palabra:

                print("\n¡FELICIDADES! ¡Has desactivado la bomba!")

                ganancia = apuesta * 2

                saldo += ganancia

                print(f"Has ganado ${ganancia}!")

                break

        

        print(f"\nSaldo actual: ${saldo}")

        

        if saldo <= 0:

            print("\n¡Te has quedado sin saldo!")

            return saldo

            

        jugar_de_nuevo = input("\n¿Quieres jugar otra vez? (s/n): ").lower()

        if jugar_de_nuevo != 's':

            return saldo

            

        palabra, pista = elegir_palabra_y_pista()


def iniciar_juego_bomba(saldo_inicial):

    """Función principal para iniciar el juego desde el casino."""

    return jugar_bomba(saldo_inicial)


if __name__ == "__main__":

    # Prueba del juego de forma independiente

    saldo_inicial = 1000

    saldo_final = iniciar_juego_bomba(saldo_inicial)

    print(f"\nJuego terminado. Saldo final: ${saldo_final}")