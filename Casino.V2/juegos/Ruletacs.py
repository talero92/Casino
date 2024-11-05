import random
import time
import os

# Colores para la rareza
COLORS = {
    "común": "\033[37m",  # Blanco
    "rara": "\033[34m",   # Azul
    "épica": "\033[35m",  # Morado
    "legendaria": "\033[33m",  # Amarillo
    "reset": "\033[0m"    # Resetear color
}

# Descuentos de venta según la rareza
DISCOUNTS = {
    "común": 0.5,
    "rara": 0.6,
    "épica": 0.7,
    "legendaria": 0.8
}

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_opciones(usuario):
    print("========================================")
    print("              RUEDA DE CS:GO")
    print("========================================")
    print(f"Saldo: ${usuario.saldo_local}")
    print("Opciones de cajas:")
    print("1. Caja Común ($100)")
    print("2. Caja Rara ($300)")
    print("3. Caja Épica ($600)")
    print("4. Caja Legendaria ($1000)")
    print("5. Inventario")
    print("6. Vender arma")
    print("7. Volver al menú principal")
    print("========================================")

def abrir_caja(caja):
    """Función que contiene todas las posibles armas por caja"""
    items = {
        "Caja Común": [
            ("Glock-18", 600, "común"), ("FAMAS", 1100, "común"),
            ("MP5", 1200, "común"), ("USP-S", 800, "común"),
            ("P250", 750, "común"), ("Five-SeveN", 900, "común"),
            ("M4A1", 1600, "rara"), ("AK-47", 2000, "rara"),
            ("AWP | Dragon Lore", 15000, "legendaria")
        ],
        "Caja Rara": [
            ("AWP", 2600, "legendaria"), ("M4A4", 1800, "rara"),
            ("Desert Eagle", 1700, "rara"), ("P90", 2300, "rara"),
            ("AWP | Medusa", 12000, "legendaria"),
            ("M4A1-S", 11000, "legendaria"),
            ("AK-47 | Fire Serpent", 14000, "legendaria")
        ],
        "Caja Épica": [
            ("AWP | Asiimov", 3500, "épica"), ("AK-47 | Vulcan", 3200, "épica"),
            ("M4A4 | Howl", 5000, "épica"), ("Butterfly Knife", 9000, "épica"),
            ("Karambit | Doppler", 11000, "épica")
        ],
        "Caja Legendaria": [
            ("Karambit", 10000, "legendaria"),
            ("Dragon Lore", 15000, "legendaria"),
            ("M9 Bayonet", 12500, "legendaria"),
            ("AWP | Medusa", 12000, "legendaria"),
            ("AK-47 | Fire Serpent", 14000, "legendaria")
        ]
    }
    return random.choice(items[caja])

def mostrar_inventario(usuario):
    if not usuario.inventario_local:
        print("Tu inventario está vacío.")
    else:
        print("Inventario:")
        for item in usuario.inventario_local:
            print(f"{COLORS[item[2]]}{item[0]} (Rareza: {item[2]}, Valor: ${item[1]}){COLORS['reset']}")
    input("Presiona Enter para continuar...")

def vender_arma(usuario):
    if not usuario.inventario_local:
        print("Tu inventario está vacío. No puedes vender armas.")
        input("Presiona Enter para continuar...")
        return
    
    print("Armas en tu inventario:")
    for i, item in enumerate(usuario.inventario_local):
        print(f"{i + 1}. {item[0]} (Rareza: {item[2]}, Valor: ${item[1]})")
    
    try:
        opcion = int(input("Selecciona el número del arma que deseas vender (0 para cancelar): "))
        if opcion == 0:
            return
        if opcion < 1 or opcion > len(usuario.inventario_local):
            print("Opción no válida.")
            input("Presiona Enter para continuar...")
            return
        
        arma_seleccionada = usuario.inventario_local.pop(opcion - 1)
        valor_venta = int(arma_seleccionada[1] * DISCOUNTS[arma_seleccionada[2]])
        usuario.actualizar_saldo_local(valor_venta)
        print(f"Has vendido: {arma_seleccionada[0]} por ${valor_venta}")
        input("Presiona Enter para continuar...")
    except ValueError:
        print("Entrada no válida. Debes ingresar un número.")
        input("Presiona Enter para continuar...")

def mostrar_animacion(caja):
    print(f"Abriendo {caja}...")
    time.sleep(1)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    
    # Simulación de la animación de apertura de caja
    items = abrir_caja(caja)
    for _ in range(10):
        print(f"{items[0]} - {COLORS[items[2]]}{items[2]}{COLORS['reset']}")
        time.sleep(0.2)
        limpiar_pantalla()
    return items

def ruletacs(usuario):
    while True:
        limpiar_pantalla()
        mostrar_opciones(usuario)
        opcion = input("Selecciona una opción: ")
        
        try:
            if opcion == '1':  # Caja Común
                if usuario.saldo_local >= 100:
                    usuario.actualizar_saldo_local(-100)
                    items = mostrar_animacion("Caja Común")
                    usuario.agregar_item_local(items)
                    print(f"¡Obtuviste: {COLORS[items[2]]}{items[0]}{COLORS['reset']}!")
                    input("Presiona Enter para continuar...")
                else:
                    print("No tienes suficiente saldo.")
                    input("Presiona Enter para continuar...")
                    
            elif opcion == '2':  # Caja Rara
                if usuario.saldo_local >= 300:
                    usuario.actualizar_saldo_local(-300)
                    items = mostrar_animacion("Caja Rara")
                    usuario.agregar_item_local(items)
                    print(f"¡Obtuviste: {COLORS[items[2]]}{items[0]}{COLORS['reset']}!")
                    input("Presiona Enter para continuar...")
                else:
                    print("No tienes suficiente saldo.")
                    input("Presiona Enter para continuar...")
                    
            elif opcion == '3':  # Caja Épica
                if usuario.saldo_local >= 600:
                    usuario.actualizar_saldo_local(-600)
                    items = mostrar_animacion("Caja Épica")
                    usuario.agregar_item_local(items)
                    print(f"¡Obtuviste: {COLORS[items[2]]}{items[0]}{COLORS['reset']}!")
                    input("Presiona Enter para continuar...")
                else:
                    print("No tienes suficiente saldo.")
                    input("Presiona Enter para continuar...")

            elif opcion == '4':  # Caja Legendaria
                if usuario.saldo_local >= 1000:
                    usuario.actualizar_saldo_local(-1000)
                    items = mostrar_animacion("Caja Legendaria")
                    usuario.agregar_item_local(items)
                    print(f"¡Obtuviste: {COLORS[items[2]]}{items[0]}{COLORS['reset']}!")
                    input("Presiona Enter para continuar...")
                else:
                    print("No tienes suficiente saldo.")
                    input("Presiona Enter para continuar...")
                    
            elif opcion == '5':  # Ver inventario
                mostrar_inventario(usuario)
                
            elif opcion == '6':  # Vender arma
                vender_arma(usuario)
                
            elif opcion == '7':  # Volver al menú principal
                return usuario
                
            else:
                print("Opción no válida.")
                input("Presiona Enter para continuar...")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    # Prueba del juego de forma independiente
    from data.usuarios import Usuario
    usuario_prueba = Usuario("test")
    usuario_final = ruletacs(usuario_prueba)
    print(f"Saldo final: ${usuario_final.saldo_local}")