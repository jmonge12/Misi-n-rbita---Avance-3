# ============================================================
# Archivo: mision_orbita.py
# Curso: SOFT-01 Principios de Programación 1 - Sección SCV3
# Integrantes: Josue Monge Miranda
# Fecha: 22/11/2026 Versión: 1.0
# Descripción: Sistema integrado Misión Órbita. Administra el ciclo
# completo de una misión espacial (planificación, autorización, viaje,
# exploración, regreso y reporte) y guarda un historial de misiones.
# ============================================================

# --- Declaración de constantes ---
# Datos fijos de la consigna. Van en tuplas porque no deben modificarse.
DESTINOS = (("Luna", 3), ("Marte", 5), ("Europa", 7))
# Cada actividad: (nombre, combustible, energía, provisiones, puntos)
ACTIVIDADES = (("Analizar terreno", 0, 8, 0, 10),
               ("Recolectar muestra", 0, 12, 2, 20),
               ("Realizar observación", 0, 5, 0, 8),
               ("Sobrevolar la zona", 15, 3, 0, 25))
RECURSOS = ("combustible", "oxígeno", "energía", "provisiones")
RECURSOS_VITALES = ("oxígeno", "energía", "provisiones")
RESULTADOS = ("Regreso exitoso", "Regreso interrumpido", "Tripulación varada",
              "No autorizada", "No planificada")

# Columnas de DESTINOS: (nombre, dias)
DES_NOMBRE = 0
DES_DIAS = 1
# Columnas de ACTIVIDADES: (nombre, combustible, energía, provisiones, puntos)
ACT_NOMBRE = 0
ACT_COMBUSTIBLE = 1
ACT_ENERGIA = 2
ACT_PROVISIONES = 3
ACT_PUNTOS = 4
# Posición de cada recurso en las listas recursos, requeridos y consumo
COMBUSTIBLE = 0
OXIGENO = 1
ENERGIA = 2
PROVISIONES = 3
# Posición de cada recurso vital en la lista dias_por_recurso
VIT_OXIGENO = 0
VIT_ENERGIA = 1
VIT_PROVISIONES = 2
# Columnas de la matriz bitacora: [numero, actividad, puntos]
BIT_NUMERO = 0
BIT_ACTIVIDAD = 1
BIT_PUNTOS = 2
# Columnas de la matriz historial: [numero, nombre, destino, resultado, puntos]
MIS_NUMERO = 0
MIS_NOMBRE = 1
MIS_DESTINO = 2
MIS_RESULTADO = 3
MIS_PUNTOS = 4
# Posición de cada resultado dentro de la tupla RESULTADOS
RES_EXITOSO = 0
RES_INTERRUMPIDO = 1
RES_VARADA = 2
RES_NO_AUTORIZADA = 3
RES_NO_PLANIFICADA = 4

# Valores fijos de las fórmulas (los mismos del Avance 1 y 2)
TRAYECTOS = 2                     # ida y regreso
CONSUMO_COMBUSTIBLE_DIA = 8
CONSUMO_OXIGENO_DIA = 2           # por tripulante
CONSUMO_ENERGIA_DIA = 5
CONSUMO_PROVISIONES_DIA = 1       # por tripulante
RESERVA_COMBUSTIBLE = 10
OXIGENO_EMERGENCIA = 5
ENERGIA_EXPLORACION = 10
PROVISIONES_ADICIONALES = 3
MARGEN_MINIMO_COMBUSTIBLE = 10

# Otros valores fijos del sistema
PRIMERA_OPCION = 1                # los menús empiezan a contar desde 1
NOMBRE_MUESTRA = "Recolectar muestra"
DESTINO_NINGUNO = "Ninguno"
OPCION_PLANIFICAR = 1
OPCION_HISTORIAL = 2
OPCION_SALIR = 3


# ============================================================
# Componente A: preparación y autorización
# ============================================================
def mostrar_destinos():
    # Se recorre la tupla para numerar los destinos desde 1.
    print("Destinos disponibles:")
    for i in range(len(DESTINOS)):
        destino = DESTINOS[i]
        print(str(i + PRIMERA_OPCION) + ". " + destino[DES_NOMBRE]
              + " (" + str(destino[DES_DIAS]) + " días)")


def leer_recursos():
    # Se pide un recurso por cada nombre de RECURSOS para que el orden
    # de la lista sea siempre el mismo.
    disponibles = []
    for recurso in RECURSOS:
        cantidad = int(input("Cantidad disponible de " + recurso + ": "))
        disponibles.append(cantidad)
    return disponibles


def calcular_requeridos(dias_viaje, tripulantes):
    # Fórmulas del Avance 1: el consumo se multiplica por TRAYECTOS
    # porque el viaje es de ida y de regreso.
    requeridos = [0, 0, 0, 0]
    requeridos[COMBUSTIBLE] = (dias_viaje * CONSUMO_COMBUSTIBLE_DIA * TRAYECTOS
                               + RESERVA_COMBUSTIBLE)
    requeridos[OXIGENO] = (dias_viaje * CONSUMO_OXIGENO_DIA * TRAYECTOS * tripulantes
                           + OXIGENO_EMERGENCIA)
    requeridos[ENERGIA] = (dias_viaje * CONSUMO_ENERGIA_DIA * TRAYECTOS
                           + ENERGIA_EXPLORACION)
    requeridos[PROVISIONES] = (dias_viaje * tripulantes * CONSUMO_PROVISIONES_DIA
                               * TRAYECTOS + PROVISIONES_ADICIONALES)
    return requeridos


def mostrar_resumen(nombre_mision, nombre_destino, dias_viaje, tripulantes,
                    disponibles, requeridos):
    print("Misión: " + nombre_mision)
    print("Destino: " + nombre_destino)
    print("Duración del viaje de ida: " + str(dias_viaje) + " días")
    print("Tripulantes: " + str(tripulantes))
    for i in range(len(RECURSOS)):
        print(RECURSOS[i].capitalize() + ": disponible " + str(disponibles[i])
              + " | requerido " + str(requeridos[i]))
    margen = disponibles[COMBUSTIBLE] - requeridos[COMBUSTIBLE]
    print("Margen adicional de combustible: " + str(margen) + " unidades")
    # Con exactamente 10 de margen todavía no se advierte (se usa < y no <=).
    if margen < MARGEN_MINIMO_COMBUSTIBLE:
        print("Advertencia: el margen adicional de combustible es bajo.")


def autorizar_lanzamiento(disponibles, requeridos):
    # Basta con que un recurso no alcance para que no se autorice.
    autorizado = True
    for i in range(len(RECURSOS)):
        if disponibles[i] < requeridos[i]:
            autorizado = False
    return autorizado


# ============================================================
# Componente B: viaje de ida
# ============================================================
def calcular_consumo_diario(tripulantes):
    # El oxígeno y las provisiones dependen de cuántos tripulantes hay.
    consumo = [0, 0, 0, 0]
    consumo[COMBUSTIBLE] = CONSUMO_COMBUSTIBLE_DIA
    consumo[OXIGENO] = CONSUMO_OXIGENO_DIA * tripulantes
    consumo[ENERGIA] = CONSUMO_ENERGIA_DIA
    consumo[PROVISIONES] = CONSUMO_PROVISIONES_DIA * tripulantes
    return consumo


def viajar_al_destino(recursos, dias_viaje, tripulantes):
    # Como la misión ya fue autorizada, se descuenta todo el viaje de una vez.
    consumo = calcular_consumo_diario(tripulantes)
    for i in range(len(RECURSOS)):
        recursos[i] = recursos[i] - consumo[i] * dias_viaje
    return recursos


def recursos_alcanzan(recursos, consumo):
    # Se revisan los cuatro recursos antes de gastar nada.
    alcanzan = True
    for i in range(len(RECURSOS)):
        if recursos[i] < consumo[i]:
            alcanzan = False
    return alcanzan


def simular_trayecto(recursos, dias, tripulantes):
    # Se revisa antes de descontar para no consumir un día que no se puede
    # completar. El ciclo termina por su condición, sin cortarlo a la fuerza.
    consumo = calcular_consumo_diario(tripulantes)
    dias_completados = 0
    puede_continuar = True
    while dias_completados < dias and puede_continuar:
        if recursos_alcanzan(recursos, consumo):
            for i in range(len(RECURSOS)):
                recursos[i] = recursos[i] - consumo[i]
            dias_completados = dias_completados + 1
            print("Día " + str(dias_completados)
                  + " | Combustible: " + str(recursos[COMBUSTIBLE])
                  + " | Oxígeno: " + str(recursos[OXIGENO])
                  + " | Energía: " + str(recursos[ENERGIA])
                  + " | Provisiones: " + str(recursos[PROVISIONES]))
        else:
            puede_continuar = False
    return dias_completados


def mostrar_recursos(recursos):
    print("Recursos restantes:")
    for i in range(len(RECURSOS)):
        print("- " + RECURSOS[i].capitalize() + ": " + str(recursos[i]) + " unidades")


# ============================================================
# Componente C: exploración con bitácora
# ============================================================
def mostrar_menu_actividades():
    # La opción de finalizar es siempre la cantidad de actividades + 1.
    for i in range(len(ACTIVIDADES)):
        print(str(i + PRIMERA_OPCION) + ". " + ACTIVIDADES[i][ACT_NOMBRE])
    print(str(len(ACTIVIDADES) + PRIMERA_OPCION) + ". Finalizar exploración")


def explorar(recursos):
    print("=== EXPLORACIÓN ===")
    bitacora = []
    explorando = True
    opcion_finalizar = len(ACTIVIDADES) + PRIMERA_OPCION
    while explorando:
        mostrar_menu_actividades()
        opcion = int(input("Seleccione una actividad: "))
        if opcion >= PRIMERA_OPCION and opcion <= len(ACTIVIDADES):
            actividad = ACTIVIDADES[opcion - PRIMERA_OPCION]
            # La revisión va dentro de la rama porque solo se sabe el costo
            # después de elegir la actividad.
            if (recursos[COMBUSTIBLE] >= actividad[ACT_COMBUSTIBLE]
                    and recursos[ENERGIA] >= actividad[ACT_ENERGIA]
                    and recursos[PROVISIONES] >= actividad[ACT_PROVISIONES]):
                recursos[COMBUSTIBLE] = recursos[COMBUSTIBLE] - actividad[ACT_COMBUSTIBLE]
                recursos[ENERGIA] = recursos[ENERGIA] - actividad[ACT_ENERGIA]
                recursos[PROVISIONES] = recursos[PROVISIONES] - actividad[ACT_PROVISIONES]
                fila = [len(bitacora) + 1, actividad[ACT_NOMBRE], actividad[ACT_PUNTOS]]
                bitacora.append(fila)
                print("Actividad realizada: " + actividad[ACT_NOMBRE]
                      + ". Puntos obtenidos: " + str(actividad[ACT_PUNTOS]))
            else:
                print("Recursos insuficientes para realizar la actividad. La exploración finaliza.")
                explorando = False
        elif opcion == opcion_finalizar:
            print("Exploración finalizada por la tripulación.")
            explorando = False
        else:
            print("Opción no válida.")
    return bitacora


def contar_actividad(bitacora, nombre_actividad):
    # Contador: suma 1 por cada fila cuya actividad tiene ese nombre.
    cantidad = 0
    for fila in bitacora:
        if fila[BIT_ACTIVIDAD] == nombre_actividad:
            cantidad = cantidad + 1
    return cantidad


def calcular_puntos(bitacora):
    # Acumulador de los puntos de todas las filas.
    total = 0
    for fila in bitacora:
        total = total + fila[BIT_PUNTOS]
    return total


def mostrar_resumen_exploracion(bitacora, recursos):
    print("Actividades realizadas: " + str(len(bitacora)))
    print("Muestras recolectadas: " + str(contar_actividad(bitacora, NOMBRE_MUESTRA)))
    print("Puntos científicos: " + str(calcular_puntos(bitacora)))
    mostrar_recursos(recursos)


# ============================================================
# Componente D: regreso y supervivencia
# ============================================================
def puede_regresar(recursos, dias_viaje):
    # Aquí no se suma la reserva de 10 unidades, como en el Avance 2.
    puede = recursos[COMBUSTIBLE] >= dias_viaje * CONSUMO_COMBUSTIBLE_DIA
    return puede


def calcular_supervivencia(recursos, tripulantes):
    # División entera: solo cuentan los días completos.
    dias_por_recurso = []
    dias_por_recurso.append(recursos[OXIGENO] // (tripulantes * CONSUMO_OXIGENO_DIA))
    dias_por_recurso.append(recursos[ENERGIA] // CONSUMO_ENERGIA_DIA)
    dias_por_recurso.append(recursos[PROVISIONES] // (tripulantes * CONSUMO_PROVISIONES_DIA))
    return dias_por_recurso


def obtener_limitantes(dias_por_recurso, minimo):
    # Si hay empate se agregan varios nombres, siempre en el orden de
    # RECURSOS_VITALES.
    limitantes = []
    for i in range(len(dias_por_recurso)):
        if dias_por_recurso[i] == minimo:
            limitantes.append(RECURSOS_VITALES[i])
    return limitantes


def regresar(recursos, dias_viaje, tripulantes):
    print("=== REGRESO ===")
    if puede_regresar(recursos, dias_viaje):
        # Caso A: alcanza el combustible, se simula día por día.
        dias_completados = simular_trayecto(recursos, dias_viaje, tripulantes)
        if dias_completados == dias_viaje:
            print("La tripulación regresó exitosamente a la Tierra.")
            mostrar_recursos(recursos)
            resultado = RESULTADOS[RES_EXITOSO]
        else:
            print("El regreso se interrumpió en el día "
                  + str(dias_completados + 1) + ".")
            # El combustible nunca sale aquí porque puede_regresar ya
            # comprobó que alcanza.
            consumo = calcular_consumo_diario(tripulantes)
            for i in range(len(RECURSOS)):
                if recursos[i] < consumo[i]:
                    print("Recurso insuficiente: " + RECURSOS[i])
            print("La tripulación no completó el regreso.")
            resultado = RESULTADOS[RES_INTERRUMPIDO]
    else:
        # Caso B: no hay combustible, la tripulación queda varada.
        print("La tripulación quedó varada en el destino.")
        dias_por_recurso = calcular_supervivencia(recursos, tripulantes)
        for i in range(len(RECURSOS_VITALES)):
            print("Días por " + RECURSOS_VITALES[i] + ": " + str(dias_por_recurso[i]))
        minimo = min(dias_por_recurso)
        limitantes = obtener_limitantes(dias_por_recurso, minimo)
        print("Supervivencia estimada: " + str(minimo) + " días")
        print("Recurso(s) limitante(s): " + ", ".join(limitantes))
        resultado = RESULTADOS[RES_VARADA]
    return resultado


# ============================================================
# Componente E: reporte final ordenado
# ============================================================
def obtener_puntos_actividad(fila):
    # sorted() llama a esta función con cada fila para saber por qué ordenar.
    return fila[BIT_PUNTOS]


def ordenar_bitacora(bitacora):
    # sorted() devuelve una lista nueva y es estable: con el mismo puntaje
    # queda primero la fila de número menor.
    ordenada = sorted(bitacora, key=obtener_puntos_actividad, reverse=True)
    return ordenada


def mostrar_reporte(mision, bitacora):
    print("=== REPORTE FINAL ===")
    print("Misión: " + mision[MIS_NOMBRE])
    print("Destino: " + mision[MIS_DESTINO])
    print("Resultado: " + mision[MIS_RESULTADO])
    print("Puntos científicos: " + str(mision[MIS_PUNTOS]))
    print("Bitácora de exploración (de mayor a menor puntaje):")
    if len(bitacora) == 0:
        print("Sin actividades registradas.")
    else:
        ordenada = ordenar_bitacora(bitacora)
        for fila in ordenada:
            print("#" + str(fila[BIT_NUMERO]) + " " + fila[BIT_ACTIVIDAD]
                  + " - " + str(fila[BIT_PUNTOS]) + " puntos")


def ejecutar_mision(numero):
    # Cada misión termina siempre en el reporte final, por cualquier causa.
    print("=== PLANIFICACIÓN ===")
    nombre_mision = input("Nombre de la misión: ")
    tripulantes = int(input("Cantidad de tripulantes: "))
    mostrar_destinos()
    opcion = int(input("Seleccione un destino: "))
    bitacora = []
    if opcion < PRIMERA_OPCION or opcion > len(DESTINOS):
        print("Opción de destino no válida. La misión no puede planificarse.")
        nombre_destino = DESTINO_NINGUNO
        resultado = RESULTADOS[RES_NO_PLANIFICADA]
    else:
        destino = DESTINOS[opcion - PRIMERA_OPCION]
        nombre_destino = destino[DES_NOMBRE]
        dias_viaje = destino[DES_DIAS]
        recursos = leer_recursos()
        requeridos = calcular_requeridos(dias_viaje, tripulantes)
        mostrar_resumen(nombre_mision, nombre_destino, dias_viaje, tripulantes,
                        recursos, requeridos)
        if autorizar_lanzamiento(recursos, requeridos):
            print("Lanzamiento autorizado.")
            print("=== VIAJE DE IDA ===")
            recursos = viajar_al_destino(recursos, dias_viaje, tripulantes)
            print("La nave llegó a " + nombre_destino + " en "
                  + str(dias_viaje) + " días.")
            mostrar_recursos(recursos)
            bitacora = explorar(recursos)
            mostrar_resumen_exploracion(bitacora, recursos)
            resultado = regresar(recursos, dias_viaje, tripulantes)
        else:
            print("Lanzamiento no autorizado. La misión debe ser revisada.")
            resultado = RESULTADOS[RES_NO_AUTORIZADA]
    puntos = calcular_puntos(bitacora)
    mision = [numero, nombre_mision, nombre_destino, resultado, puntos]
    mostrar_reporte(mision, bitacora)
    return mision


# ============================================================
# Componente F: menú principal e historial de misiones
# ============================================================
def mostrar_menu_principal():
    print("===== MISIÓN ÓRBITA =====")
    print("1. Planificar y ejecutar una misión")
    print("2. Ver historial de misiones")
    print("3. Salir")


def obtener_puntos_mision(mision):
    return mision[MIS_PUNTOS]


def ordenar_historial(historial):
    # Igual que la bitácora: lista nueva, de mayor a menor puntaje y sin
    # tocar el historial original.
    ordenado = sorted(historial, key=obtener_puntos_mision, reverse=True)
    return ordenado


def linea_mision(mision):
    texto = ("#" + str(mision[MIS_NUMERO]) + " " + mision[MIS_NOMBRE] + " | "
             + mision[MIS_DESTINO] + " | " + mision[MIS_RESULTADO] + " | "
             + str(mision[MIS_PUNTOS]) + " puntos")
    return texto


def mostrar_historial(historial):
    print("=== HISTORIAL DE MISIONES ===")
    if len(historial) == 0:
        print("No hay misiones registradas.")
    else:
        ordenado = ordenar_historial(historial)
        for mision in ordenado:
            print(linea_mision(mision))


def main():
    historial = []
    ejecutando = True
    while ejecutando:
        mostrar_menu_principal()
        opcion = int(input("Seleccione una opción: "))
        if opcion == OPCION_PLANIFICAR:
            mision = ejecutar_mision(len(historial) + 1)
            historial.append(mision)
        elif opcion == OPCION_HISTORIAL:
            mostrar_historial(historial)
        elif opcion == OPCION_SALIR:
            ejecutando = False
        else:
            print("Opción no válida.")
    print("Fin del sistema Misión Órbita.")


main()
