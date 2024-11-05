import os
import sys
import traceback
import time
from modos.Local import jugar_local
from modos.Multijugador import jugar_Multijugador
from utils.helpers import limpiar_pantalla
from data.usuarios import Usuario
from data.db_manager import cargar_usuario, guardar_usuario

def mostrar_menu():
    limpiar_pantalla()
    print("========================================")
    print("           CASINO VIRTUAL")
    print("========================================")
    print("1. Jugar modo Local")
    print("2. Jugar modo Multijugador")
    print("3. Ver saldo")
    print("4. Salir")
    print("========================================")

def iniciar_casino(usuario):
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            usuario = jugar_local(usuario)
            guardar_usuario(usuario)  # Guardar después de cada juego
        elif opcion == '2':
            usuario = jugar_Multijugador(usuario)
            guardar_usuario(usuario)  # Guardar después de cada juego
        elif opcion == '3':
            print(f"Saldo local: ${usuario.saldo_local}")
            print(f"Saldo multijugador: ${usuario.saldo_multi}")
            input("Presiona Enter para continuar...")
            guardar_usuario(usuario)
        elif opcion == '4':
            print("Gracias por jugar. ¡Hasta luego!")
            guardar_usuario(usuario)  # Guardar antes de salir
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            time.sleep(2)

if __name__ == "__main__":
    try:
        nombre_usuario = input("Ingresa tu nombre de usuario: ")
        usuario = cargar_usuario(nombre_usuario)
        
        if usuario is None:
            usuario = Usuario(nombre_usuario)
            guardar_usuario(usuario)
            print(f"Bienvenido, {nombre_usuario}! Se ha creado una nueva cuenta para ti.")
        else:
            print(f"Bienvenido de vuelta, {nombre_usuario}!")
            print(f"Saldo local actual: ${usuario.saldo_local}")
            print(f"Saldo multijugador actual: ${usuario.saldo_multi}")
        
        input("\nPresiona Enter para entrar al casino...")
        
        iniciar_casino(usuario)
        
    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        print("\nDetalles del error:")
        print(traceback.format_exc())
    
    input("\nPresiona Enter para salir...")