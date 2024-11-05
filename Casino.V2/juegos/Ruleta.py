import random
import time
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_ruleta(numero_actual, numeros_colores):
    print("========================================")
    print("                RULETA ")
    print("========================================")
    
    # Mostrar los números con sus colores
    fila = ""
    for numero, color in numeros_colores:
        if numero == numero_actual:
            fila += f" > {numero} {color} < "
        else:
            fila += f" {numero} {color} "
        if numero % 6 == 0:
            print(fila.center(80))
            fila = ""
    if fila:
        print(fila.center(80))
    print("========================================")
    print()

def generar_numero_ganador(numeros_colores):
    return random.choice(numeros_colores)

def girar_ruleta(numeros_colores):
    for _ in range(10):  # Girar 10 veces
        numero_ganador = generar_numero_ganador(numeros_colores)
        limpiar_pantalla()
        mostrar_ruleta(numero_ganador[0], numeros_colores)
        time.sleep(0.2)
    return generar_numero_ganador(numeros_colores)

def solicitar_apuesta(saldo):
    while True:
        try:
            apuesta = int(input("Cuanto deseas apostar? $"))
            if 0 < apuesta <= saldo:
                return apuesta
            else:
                print("La apuesta debe ser mayor que 0 y menor o igual al saldo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def solicitar_tipo_apuesta():
    print("Elige el tipo de apuesta:")
    print("1. Número")
    print("2. Color (rojo/negro/verde)")
    print("3. Par/Impar")
    while True:
        tipo_apuesta = input("Selecciona una opción (1, 2, o 3): ")
        if tipo_apuesta in ['1', '2', '3']:
            return tipo_apuesta
        else:
            print("Opción no válida. Por favor, selecciona 1, 2, o 3.")

def solicitar_numero():
    while True:
        try:
            numero = int(input("Elige un número entre 0 y 36: "))
            if 0 <= numero <= 36:
                return numero
            else:
                print("El número debe estar entre 0 y 36.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def solicitar_color():
    while True:
        color = input("Elige un color (rojo/negro/verde): ").lower()
        if color in ['rojo', 'negro', 'verde']:
            return color
        else:
            print("El color debe ser 'rojo', 'negro' o 'verde'.")

def solicitar_par_impar():
    while True:
        par_impar = input("Elige par o impar: ").lower()
        if par_impar in ['par', 'impar']:
            return par_impar
        else:
            print("Debes elegir 'par' o 'impar'.")

def mostrar_resultado(numero_ganador, color_ganador, tipo_apuesta, apuesta, resultado_apuesta, ganancia, saldo):
    limpiar_pantalla()
    print("========================================")
    print("                GANADOR")
    print("========================================")
    print(f"\n           {numero_ganador} ({color_ganador})\n")
    print("========================================")
    if tipo_apuesta == '1':
        print(f"Tu apuesta fue al número: {apuesta}\n")
    elif tipo_apuesta == '2':
        print(f"Tu apuesta fue al color: {apuesta}\n")
    else:
        print(f"Tu apuesta fue a: {apuesta}\n")
    
    if resultado_apuesta:
        print(f"FELICIDADES! Ganaste ${ganancia}!")
    else:
        print(f"Lo siento, perdiste ${-ganancia}.")
    print(f"Saldo actual: ${saldo}\n")

def ruleta(saldo_inicial):
    saldo = saldo_inicial
    numeros_colores = [(i, "Rojo" if i % 2 else "Negro") for i in range(1, 37)]
    numeros_colores.insert(0, (0, "Verde"))
    
    while True:
        limpiar_pantalla()
        print("========================================")
        print("            Bienvenido a la Ruleta")
        print("========================================")
        print("Reglas del juego:")
        print("1. Puedes apostar a un número, color o par/impar.")
        print("2. La apuesta mínima es de $1.")
        print("3. Si apuestas a un número y aciertas, ganas 35 veces tu apuesta.")
        print("4. Si apuestas a un color y aciertas, ganas 2 veces tu apuesta.")
        print("5. Si apuestas a par/impar y aciertas, ganas 2 veces tu apuesta.")
        print("========================================")
        print(f"Saldo actual: ${saldo}")
        
        if saldo <= 0:
            print("Te has quedado sin saldo. Has perdido.")
            return saldo
        
        apuesta = solicitar_apuesta(saldo)
        tipo_apuesta = solicitar_tipo_apuesta()
        
        if tipo_apuesta == '1':
            apuesta_detalle = solicitar_numero()
        elif tipo_apuesta == '2':
            apuesta_detalle = solicitar_color()
        else:
            apuesta_detalle = solicitar_par_impar()

        print("\n========================================")
        print("              Girando la ruleta...")
        time.sleep(1)
        numero_ganador, color_ganador = girar_ruleta(numeros_colores)
        color_ganador = color_ganador.lower()

        resultado_apuesta = False
        ganancia = 0

        if tipo_apuesta == '1' and apuesta_detalle == numero_ganador:
            resultado_apuesta = True
            ganancia = apuesta * 35
        elif tipo_apuesta == '2' and apuesta_detalle == color_ganador:
            resultado_apuesta = True
            ganancia = apuesta * 2
        elif tipo_apuesta == '3' and ((apuesta_detalle == 'par' and numero_ganador % 2 == 0) or (apuesta_detalle == 'impar' and numero_ganador % 2 != 0)):
            resultado_apuesta = True
            ganancia = apuesta * 2
        else:
            ganancia = -apuesta
        
        saldo += ganancia
        mostrar_resultado(numero_ganador, color_ganador, tipo_apuesta, apuesta_detalle, resultado_apuesta, ganancia, saldo)

        if input("¿Quieres jugar de nuevo? [S/N]: ").lower() != 's':
            print("Gracias por jugar. ¡Hasta luego!")
            return saldo

if __name__ == "__main__":
    saldo_inicial = 1000
    saldo_final = ruleta(saldo_inicial)
    print(f"Saldo final: ${saldo_final}")