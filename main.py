import csv
from collections import defaultdict


def cargar_fixture(archivo_fixture, fixture):
    with open(archivo_fixture, 'r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fixture.append(fila)


def cargar_resultados(archivo_resultados, resultados):
    with open(archivo_resultados, 'r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            resultados[fila['Match Number']] = {
                'Home Team Goals': fila['Home Team Goals'],
                'Away Team Goals': fila['Away Team Goals']
            }


def actualizar_resultados(fixture, resultados):
    for partido in fixture:
        numero_partido = partido['Match Number']
        if numero_partido in resultados:
            resultado = resultados[numero_partido]
            partido[
                'Result'] = f"{resultado['Home Team Goals']}-{resultado['Away Team Goals']}"


def calcular_posiciones(fixture):
    posiciones = defaultdict(
        lambda: {
            'Puntos': 0,
            'PartidosJugados': 0,
            'Victorias': 0,
            'Empates': 0,
            'Derrotas': 0,
            'GolesAFavor': 0,
            'GolesEnContra': 0
        })

    for partido in fixture:
        resultado = partido.get('Result', '').split('-')
        if resultado:
            local_goals = int(resultado[0])
            visitante_goals = int(resultado[1])
            local_team = partido['Home Team']
            visitante_team = partido['Away Team']

            posiciones[local_team]['PartidosJugados'] += 1
            posiciones[visitante_team]['PartidosJugados'] += 1
            posiciones[local_team]['GolesAFavor'] += local_goals
            posiciones[visitante_team]['GolesAFavor'] += visitante_goals
            posiciones[local_team]['GolesEnContra'] += visitante_goals
            posiciones[visitante_team]['GolesEnContra'] += local_goals

            if local_goals > visitante_goals:
                posiciones[local_team]['Victorias'] += 1
                posiciones[local_team]['Puntos'] += 3
                posiciones[visitante_team]['Derrotas'] += 1
            elif local_goals < visitante_goals:
                posiciones[visitante_team]['Victorias'] += 1
                posiciones[visitante_team]['Puntos'] += 3
                posiciones[local_team]['Derrotas'] += 1
            else:
                posiciones[local_team]['Empates'] += 1
                posiciones[visitante_team]['Empates'] += 1
                posiciones[local_team]['Puntos'] += 1
                posiciones[visitante_team]['Puntos'] += 1

    return posiciones


def mostrar_posiciones(posiciones):
    for equipo, datos in posiciones.items():
        print(f"Equipo: {equipo}")
        print(f"Puntos: {datos['Puntos']}")
        print(f"Partidos Jugados: {datos['PartidosJugados']}")
        print(f"Victorias: {datos['Victorias']}")
        print(f"Empates: {datos['Empates']}")
        print(f"Derrotas: {datos['Derrotas']}")
        print(f"Goles a Favor: {datos['GolesAFavor']}")
        print(f"Goles en Contra: {datos['GolesEnContra']}")
        print()


def generar_informe_final(posiciones, archivo_salida):
    with open(archivo_salida, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "Grupo", "Equipo", "Puntos", "PartidosJugados", "Victorias",
            "Empates", "Derrotas", "GolesAFavor", "GolesEnContra",
            "DiferenciaDeGoles"
        ])
        for equipo, datos in posiciones.items():
            grupo = equipo.split()[-1]
            escritor.writerow([
                grupo, equipo, datos['Puntos'], datos['PartidosJugados'],
                datos['Victorias'], datos['Empates'], datos['Derrotas'],
                datos['GolesAFavor'], datos['GolesEnContra'],
                datos['GolesAFavor'] - datos['GolesEnContra']
            ])


def menu():
    fixture = []
    resultados = {}

    while True:
        print("\nMenú:")
        print("1. Cargar fixture")
        print("2. Cargar resultados")
        print("3. Actualizar resultados")
        print("4. Calcular posiciones")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            archivo_fixture = input(
                "Ingrese el nombre del archivo del fixture: ")
            cargar_fixture(archivo_fixture, fixture)
        elif opcion == '2':
            archivo_resultados = input(
                "Ingrese el nombre del archivo de resultados: ")
            cargar_resultados(archivo_resultados, resultados)
        elif opcion == '3':
            actualizar_resultados(fixture, resultados)
            print("¡Resultados actualizados con éxito!")
        elif opcion == '4':
            posiciones = calcular_posiciones(fixture)
            mostrar_posiciones(posiciones)
        elif opcion == '5':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


# Ejecutar el menú interactivo
if __name__ == "__main__":
    menu()
