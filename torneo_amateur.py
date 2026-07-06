# ==========================================
# SISTEMA DE GESTIÓN DE TORNEO AMATEUR
# Trabajo Final Integrador
# ==========================================

equipos = []
historial_partidos = []
partidos_jugados = 0


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def buscar_equipo(nombre):
    """Busca un equipo por nombre."""
    for equipo in equipos:
        if equipo["nombre"].lower() == nombre.lower():
            return equipo
    return None


def calcular_diferencia(equipo):
    """Calcula la diferencia de goles."""
    equipo["dg"] = equipo["gf"] - equipo["gc"]


def partido_ya_jugado(local, visitante):
    """Verifica si el partido ya fue cargado."""

    for partido in historial_partidos:

        if (
            (partido["local"] == local["nombre"] and
             partido["visitante"] == visitante["nombre"])

            or

            (partido["local"] == visitante["nombre"] and
             partido["visitante"] == local["nombre"])
        ):

            return True

    return False


# ==========================================
# REGISTRO DE EQUIPOS
# ==========================================

def registrar_equipos():

    try:

        cantidad = int(input("\n¿Cuántos equipos desea registrar?: "))

        if cantidad <= 0:
            print("La cantidad debe ser mayor a cero.")
            return

    except ValueError:
        print("Debe ingresar un número.")
        return

    for i in range(cantidad):

        while True:

            nombre = input(f"Nombre del equipo {i+1}: ").strip()

            if nombre == "":
                print("El nombre no puede estar vacío.")
                continue

            if buscar_equipo(nombre):
                print("Ese equipo ya existe.")
                continue

            equipo = {
                "nombre": nombre,
                "pj": 0,
                "pg": 0,
                "pe": 0,
                "pp": 0,
                "gf": 0,
                "gc": 0,
                "dg": 0,
                "pts": 0
            }

            equipos.append(equipo)
            break

    print("\nEquipos registrados correctamente.")


# ==========================================
# MOSTRAR EQUIPOS
# ==========================================

def mostrar_equipos():

    if len(equipos) == 0:
        print("\nNo hay equipos registrados.")
        return

    print("\n========== EQUIPOS ==========")

    for i, equipo in enumerate(equipos, start=1):
        print(f"{i}. {equipo['nombre']}")


# ==========================================
# CARGAR RESULTADO
# ==========================================

def cargar_resultado():

    global partidos_jugados

    if len(equipos) < 2:
        print("\nDebe registrar al menos dos equipos.")
        return

    print("\n========== EQUIPOS ==========")

    for i, equipo in enumerate(equipos, start=1):
        print(f"{i}. {equipo['nombre']}")

    # -------------------------
    # Equipo local
    # -------------------------

    dato_local = input(
        "\nIngrese el número o nombre del equipo local: "
    )

    if dato_local.isdigit():

        indice = int(dato_local) - 1

        if indice < 0 or indice >= len(equipos):
            print("Equipo inexistente.")
            return

        local = equipos[indice]

    else:

        local = buscar_equipo(dato_local)

        if local is None:
            print("Equipo inexistente.")
            return

    # -------------------------
    # Equipo visitante
    # -------------------------

    dato_visitante = input(
        "Ingrese el número o nombre del equipo visitante: "
    )

    if dato_visitante.isdigit():

        indice = int(dato_visitante) - 1

        if indice < 0 or indice >= len(equipos):
            print("Equipo inexistente.")
            return

        visitante = equipos[indice]

    else:

        visitante = buscar_equipo(dato_visitante)

        if visitante is None:
            print("Equipo inexistente.")
            return

    if local == visitante:
        print("\nUn equipo no puede jugar contra sí mismo.")
        return

    if partido_ya_jugado(local, visitante):
        print("\nEse partido ya fue cargado.")
        return

    try:

        goles_local = int(
            input(f"Goles de {local['nombre']}: ")
        )

        goles_visitante = int(
            input(f"Goles de {visitante['nombre']}: ")
        )

        if goles_local < 0 or goles_visitante < 0:
            print("Los goles no pueden ser negativos.")
            return

    except ValueError:
        print("Debe ingresar números enteros.")
        return
        # ---------------------------------
    # ACTUALIZAR ESTADÍSTICAS
    # ---------------------------------

    partidos_jugados += 1

    local["pj"] += 1
    visitante["pj"] += 1

    local["gf"] += goles_local
    local["gc"] += goles_visitante

    visitante["gf"] += goles_visitante
    visitante["gc"] += goles_local

    if goles_local > goles_visitante:

        local["pg"] += 1
        local["pts"] += 3

        visitante["pp"] += 1

    elif goles_local < goles_visitante:

        visitante["pg"] += 1
        visitante["pts"] += 3

        local["pp"] += 1

    else:

        local["pe"] += 1
        visitante["pe"] += 1

        local["pts"] += 1
        visitante["pts"] += 1

    calcular_diferencia(local)
    calcular_diferencia(visitante)

    historial_partidos.append({
        "local": local["nombre"],
        "visitante": visitante["nombre"],
        "goles_local": goles_local,
        "goles_visitante": goles_visitante
    })

    print("\nResultado cargado correctamente.")


# ==========================================
# TABLA DE POSICIONES
# ==========================================

def mostrar_tabla():

    if len(equipos) == 0:
        print("\nNo hay equipos registrados.")
        return

    tabla = sorted(
        equipos,
        key=lambda e: (e["pts"], e["dg"], e["gf"]),
        reverse=True
    )

    print("\n================ TABLA DE POSICIONES ================")

    print(
        f"{'POS':<5}"
        f"{'EQUIPO':<20}"
        f"{'PJ':<5}"
        f"{'PG':<5}"
        f"{'PE':<5}"
        f"{'PP':<5}"
        f"{'GF':<5}"
        f"{'GC':<5}"
        f"{'DG':<5}"
        f"{'PTS':<5}"
    )

    print("-" * 70)

    for posicion, equipo in enumerate(tabla, start=1):

        print(
            f"{posicion:<5}"
            f"{equipo['nombre']:<20}"
            f"{equipo['pj']:<5}"
            f"{equipo['pg']:<5}"
            f"{equipo['pe']:<5}"
            f"{equipo['pp']:<5}"
            f"{equipo['gf']:<5}"
            f"{equipo['gc']:<5}"
            f"{equipo['dg']:<5}"
            f"{equipo['pts']:<5}"
        )


# ==========================================
# HISTORIAL DE PARTIDOS
# ==========================================

def mostrar_historial():

    if len(historial_partidos) == 0:
        print("\nTodavía no se jugaron partidos.")
        return

    print("\n============= HISTORIAL DE PARTIDOS =============")

    for i, partido in enumerate(historial_partidos, start=1):

        print(
            f"{i}. "
            f"{partido['local']} "
            f"{partido['goles_local']} - "
            f"{partido['goles_visitante']} "
            f"{partido['visitante']}"
        )


# ==========================================
# ESTADÍSTICAS
# ==========================================

def mostrar_estadisticas():

    if len(equipos) == 0:
        print("\nNo hay equipos registrados.")
        return

    total_goles = 0

    for equipo in equipos:
        total_goles += equipo["gf"]

    promedio = 0

    if partidos_jugados > 0:
        promedio = total_goles / partidos_jugados

    goleador = max(equipos, key=lambda e: e["gf"])
    campeon = max(equipos, key=lambda e: (e["pts"], e["dg"], e["gf"]))

    print("\n================ ESTADÍSTICAS ================")

    print(f"Equipos registrados : {len(equipos)}")
    print(f"Partidos jugados    : {partidos_jugados}")
    print(f"Total de goles      : {total_goles}")
    print(f"Promedio de goles   : {promedio:.2f}")

    print("\n🏆 Campeón actual:")
    print(f"{campeon['nombre']} - {campeon['pts']} puntos")

    print("\n⚽ Equipo más goleador:")
    print(f"{goleador['nombre']} ({goleador['gf']} goles)")
    # ==========================================
# ELIMINAR EQUIPO
# ==========================================

def eliminar_equipo():

    if len(equipos) == 0:
        print("\nNo hay equipos registrados.")
        return

    mostrar_equipos()

    dato = input("\nIngrese el número o nombre del equipo a eliminar: ")

    if dato.isdigit():

        indice = int(dato) - 1

        if indice < 0 or indice >= len(equipos):
            print("Equipo inexistente.")
            return

        eliminado = equipos.pop(indice)

    else:

        eliminado = buscar_equipo(dato)

        if eliminado is None:
            print("Equipo inexistente.")
            return

        equipos.remove(eliminado)

    print(f"\nEl equipo {eliminado['nombre']} fue eliminado correctamente.")


# ==========================================
# REINICIAR TORNEO
# ==========================================

def reiniciar_torneo():

    global partidos_jugados

    confirmacion = input(
        "\n¿Está seguro de reiniciar el torneo? (S/N): "
    ).strip().upper()

    if confirmacion not in ("S", "SI"):
        print("Operación cancelada.")
        return

    equipos.clear()
    historial_partidos.clear()
    partidos_jugados = 0

    print("\nEl torneo fue reiniciado correctamente.")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def menu():

    while True:

        print("\n======================================")
        print("     GESTIÓN DE TORNEO AMATEUR")
        print("======================================")
        print("1. Registrar equipos")
        print("2. Mostrar equipos")
        print("3. Cargar resultado")
        print("4. Tabla de posiciones")
        print("5. Estadísticas")
        print("6. Historial de partidos")
        print("7. Eliminar equipo")
        print("8. Reiniciar torneo")
        print("9. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":

            registrar_equipos()

        elif opcion == "2":

            mostrar_equipos()

        elif opcion == "3":

            cargar_resultado()

        elif opcion == "4":

            mostrar_tabla()

        elif opcion == "5":

            mostrar_estadisticas()

        elif opcion == "6":

            mostrar_historial()

        elif opcion == "7":

            eliminar_equipo()

        elif opcion == "8":

            reiniciar_torneo()

        elif opcion == "9":

            print("\nGracias por utilizar el sistema.")
            print("Hasta luego.")
            break

        else:

            print("\nOpción inválida.")



# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

print("=" * 45)
print("   SISTEMA DE GESTIÓN DE TORNEO")
print("=" * 45)

menu()