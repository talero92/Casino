# modos/Local.py

from juegos.Tragamonedas import jugar_tragamonedas
from juegos.Ruleta import ruleta
from juegos.Ruletacs import ruletacs
from juegos.Bomba import iniciar_juego_bomba
from juegos.ChickenRoad import jugar_chicken_road  # Añade esta línea
from utils.helpers import limpiar_pantalla

def jugar_local(usuario):
    while True:
        limpiar_pantalla()
        print("========================================")
        print("             MODO LOCAL")
        print("========================================")
        print(f"Usuario: {usuario.nombre}")
        print(f"Saldo: ${usuario.saldo_local}")
        print("========================================")
        print("1. Tragamonedas")
        print("2. Ruleta")
        print("3. Ruleta CS:GO")
        print("4. Bomba")
        print("5. Chicken Road")  # Añade esta línea
        print("6. Volver al menú principal")  # Cambia el número
        print("========================================")
        
        opcion = input("Selecciona un juego: ")
        
        if opcion == '1':
            nuevo_saldo = jugar_tragamonedas(usuario.saldo_local)
            usuario.actualizar_saldo_local(nuevo_saldo - usuario.saldo_local)
        elif opcion == '2':
            nuevo_saldo = ruleta(usuario.saldo_local)
            usuario.actualizar_saldo_local(nuevo_saldo - usuario.saldo_local)
        elif opcion == '3':
            usuario = ruletacs(usuario)
        elif opcion == '4':
            nuevo_saldo = iniciar_juego_bomba(usuario.saldo_local)
            usuario.actualizar_saldo_local(nuevo_saldo - usuario.saldo_local)
        elif opcion == '5':  # Añade esta condición
            nuevo_saldo = jugar_chicken_road(usuario.saldo_local)
            usuario.actualizar_saldo_local(nuevo_saldo - usuario.saldo_local)
        elif opcion == '6':  # Cambia el número
            return usuario
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")
    
    return usuario