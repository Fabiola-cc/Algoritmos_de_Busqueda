"""
Proyecto #2 IA - Comparación de algoritmos de búsqueda

Este script genera 25 laberintos aleatorios de tamaño 45x55 usando el algoritmo de Kruskal,
ejecuta 4 algoritmos de búsqueda (BFS, DFS, Dijkstra, A*) en cada uno, y registra las estadísticas
de desempeño en un archivo CSV y un archivo de texto consolidado.
"""
import numpy as np
import time
import csv
import os
import random
from collections import deque

# Importar generador de laberintos
from MazeGenerator import MazeGenerator

# Importar la clase base de algoritmos de búsqueda
from algoritmos_busqueda import AlgoritmoBusqueda

from Algoritmo_BFS import Algoritmo_BFS
from Algoritmo_DFS import Algoritmo_DFS
from Algoritmo_Dijkstra import Algoritmo_Dijkstra
from Algoritmo_AStar import Algoritmo_AStar

def manhattan_distance(point1, point2):
    """Calcula la distancia Manhattan entre dos puntos."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def logical_to_maze_coords(logical_coord):
    """Convierte coordenadas lógicas a coordenadas del laberinto."""
    return (2 * logical_coord[0] + 1, 2 * logical_coord[1] + 1)

def generate_distant_points(maze, min_distance=10):
    """
    Genera dos puntos A y B en el laberinto con una distancia Manhattan mínima.
    
    Args:
        maze: Matriz del laberinto
        min_distance: Distancia Manhattan mínima requerida
        
    Returns:
        Tupla (punto_A, punto_B) donde cada punto es (fila, columna)
    """
    height, width = maze.shape
    logical_height = (height - 1) // 2
    logical_width = (width - 1) // 2
    
    # Generar puntos aleatorios hasta encontrar dos con la distancia requerida
    max_attempts = 100
    for _ in range(max_attempts):
        # Generar coordenadas lógicas aleatorias
        logical_a = (random.randint(0, logical_height-1), random.randint(0, logical_width-1))
        logical_b = (random.randint(0, logical_height-1), random.randint(0, logical_width-1))
        
        # Convertir a coordenadas del laberinto
        point_a = logical_to_maze_coords(logical_a)
        point_b = logical_to_maze_coords(logical_b)
        
        # Verificar distancia Manhattan y que ambos puntos sean pasillos (valor 0)
        distance = manhattan_distance(logical_a, logical_b)
        if distance >= min_distance and maze[point_a] == 0 and maze[point_b] == 0:
            return point_a, point_b
    
    # Si no se encuentran puntos con la distancia requerida, usar extremos del laberinto
    point_a = (1, 1)  # Esquina superior izquierda
    point_b = (height-2, width-2)  # Esquina inferior derecha
    return point_a, point_b

def run_algorithm(algorithm_class, maze, start, end):
    """
    Ejecuta un algoritmo de búsqueda y mide su desempeño.
    
    Args:
        algorithm_class: Clase del algoritmo a utilizar
        maze: Matriz del laberinto
        start: Punto de inicio (fila, columna)
        end: Punto final (fila, columna)
        
    Returns:
        Diccionario con estadísticas de desempeño
    """
    # Crear instancia del algoritmo
    algorithm = algorithm_class(maze, start, end)
    
    # Medir tiempo
    start_time = time.time()
    
    # Ejecutar algoritmo
    search_states, path = algorithm.solve()
    
    # Calcular tiempo transcurrido
    elapsed_time = time.time() - start_time
    
    # Obtener estadísticas
    expanded_nodes = len(search_states[-1]['expanded']) if search_states else 0
    path_length = len(path)
    
    return {
        'tiempo_ejecucion': elapsed_time,
        'nodos_explorados': expanded_nodes,
        'longitud_ruta': path_length
    }

def compare_algorithms_on_maze(maze, start, end):
    """
    Compara los 4 algoritmos en un laberinto específico.
    
    Args:
        maze: Matriz del laberinto
        start: Punto de inicio
        end: Punto final
        
    Returns:
        Diccionario con resultados por algoritmo
    """
    algorithms = [
        ('BFS', Algoritmo_BFS),
        ('DFS', Algoritmo_DFS),
        ('Dijkstra', Algoritmo_Dijkstra),
        ('A*', Algoritmo_AStar)
    ]
    
    results = {}
    
    for name, algorithm_class in algorithms:
        print(f"Ejecutando {name}...")
        stats = run_algorithm(algorithm_class, maze, start, end)
        results[name] = stats
        print(f"  Tiempo: {stats['tiempo_ejecucion']:.4f}s, "
              f"Nodos: {stats['nodos_explorados']}, "
              f"Long. Ruta: {stats['longitud_ruta']}")
    
    return results

def main():
    """Función principal del script."""
    # Parámetros
    num_laberintos = 25
    altura = 45
    ancho = 55
    min_distance = 10
    output_file = "resultados_algoritmos.csv"
    
    # Crear directorio para resultados si no existe
    os.makedirs("resultados", exist_ok=True)
    
    # Preparar archivo CSV para resultados
    with open(os.path.join("resultados", output_file), 'w', newline='') as csvfile:
        fieldnames = [
            'laberinto', 'algoritmo', 'tiempo_ejecucion', 
            'nodos_explorados', 'longitud_ruta'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Preparar archivo TXT consolidado para resultados detallados
        with open(os.path.join("resultados", "todos_laberintos_resultados.txt"), 'w') as txt_file:
            txt_file.write("=== RESULTADOS DETALLADOS POR LABERINTO ===\n\n")
            
            # Generar y procesar cada laberinto
            for i in range(num_laberintos):
                print(f"\n=== Laberinto {i+1}/{num_laberintos} ===")
                
                # Crear generador y laberinto
                generator = MazeGenerator(altura, ancho)
                maze, _ = generator.generate_kruskal()
                
                # Generar puntos A y B
                start, end = generate_distant_points(maze, min_distance)
                
                # Calcular distancia Manhattan para versión lógica (coordenadas en la cuadrícula)
                logical_start = ((start[0] - 1) // 2, (start[1] - 1) // 2)
                logical_end = ((end[0] - 1) // 2, (end[1] - 1) // 2)
                logical_distance = manhattan_distance(logical_start, logical_end)
                
                print(f"Puntos A={start}, B={end}, Distancia Manhattan lógica: {logical_distance}")
                
                # Comparar algoritmos
                results = compare_algorithms_on_maze(maze, start, end)
                
                # Guardar resultados en CSV
                for algo_name, stats in results.items():
                    writer.writerow({
                        'laberinto': i+1,
                        'algoritmo': algo_name,
                        'tiempo_ejecucion': stats['tiempo_ejecucion'],
                        'nodos_explorados': stats['nodos_explorados'],
                        'longitud_ruta': stats['longitud_ruta']
                    })
                
                # Añadir resultados de este laberinto al archivo de texto consolidado
                txt_file.write(f"{'='*50}\n")
                txt_file.write(f"=== Laberinto {i+1} ===\n")
                txt_file.write(f"Dimensiones: {altura}x{ancho}\n")
                txt_file.write(f"Puntos: A={start}, B={end}\n")
                txt_file.write(f"Distancia Manhattan lógica: {logical_distance}\n\n")
                
                txt_file.write("Resultados por algoritmo:\n")
                for algo_name, stats in results.items():
                    txt_file.write(f"{algo_name}:\n")
                    txt_file.write(f"  Tiempo de ejecución: {stats['tiempo_ejecucion']:.6f} segundos\n")
                    txt_file.write(f"  Nodos explorados: {stats['nodos_explorados']}\n")
                    txt_file.write(f"  Longitud de ruta: {stats['longitud_ruta']}\n\n")
                
                txt_file.write("\n")
    
    print("\n=== Proceso completado ===")
    print(f"Los resultados se han guardado en la carpeta 'resultados'")
    
    # Crear resumen final con promedios
    create_summary_table()

def create_summary_table():
    """Crea una tabla resumen con los promedios de los 25 laberintos."""
    # Leer datos del CSV
    data = []
    with open(os.path.join("resultados", "resultados_algoritmos.csv"), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'laberinto': int(row['laberinto']),
                'algoritmo': row['algoritmo'],
                'tiempo_ejecucion': float(row['tiempo_ejecucion']),
                'nodos_explorados': int(row['nodos_explorados']),
                'longitud_ruta': int(row['longitud_ruta'])
            })
    
    # Calcular promedios por algoritmo
    algoritmos = ['BFS', 'DFS', 'Dijkstra', 'A*']
    promedios = {algo: {'tiempo': 0, 'nodos': 0, 'longitud': 0} for algo in algoritmos}
    
    for row in data:
        algo = row['algoritmo']
        promedios[algo]['tiempo'] += row['tiempo_ejecucion']
        promedios[algo]['nodos'] += row['nodos_explorados']
        promedios[algo]['longitud'] += row['longitud_ruta']
    
    num_laberintos = max(row['laberinto'] for row in data)
    for algo in algoritmos:
        for key in promedios[algo]:
            promedios[algo][key] /= num_laberintos
    
    # Crear rankings para cada métrica
    metrics = [
        ('tiempo', 'tiempo_ejecucion', 'Tiempo de ejecución (s)'),
        ('nodos', 'nodos_explorados', 'Nodos explorados'),
        ('longitud', 'longitud_ruta', 'Longitud de ruta')
    ]
    
    rankings = {metric[0]: {} for metric in metrics}
    
    for metric_key, _, _ in metrics:
        # Ordenar algoritmos por la métrica (menor es mejor)
        sorted_algos = sorted(algoritmos, key=lambda x: promedios[x][metric_key])
        for rank, algo in enumerate(sorted_algos, 1):
            rankings[metric_key][algo] = rank
    
    # Calcular ranking promedio
    avg_rankings = {algo: sum(rankings[m[0]][algo] for m in metrics) / len(metrics) for algo in algoritmos}
    
    # Guardar resumen en archivo
    with open(os.path.join("resultados", "resumen_final.txt"), 'w') as f:
        f.write("=== RESUMEN DE COMPARACIÓN DE ALGORITMOS ===\n")
        f.write(f"Basado en {num_laberintos} laberintos de tamaño 45x55\n\n")
        
        f.write("PROMEDIOS POR ALGORITMO:\n")
        f.write(f"{'Algoritmo':<10} {'Tiempo (s)':<15} {'Nodos':<15} {'Longitud':<15}\n")
        f.write("-" * 55 + "\n")
        for algo in algoritmos:
            f.write(f"{algo:<10} {promedios[algo]['tiempo']:<15.6f} {promedios[algo]['nodos']:<15.1f} {promedios[algo]['longitud']:<15.1f}\n")
        
        f.write("\nRANKING POR MÉTRICA (1 = mejor, 4 = peor):\n")
        f.write(f"{'Algoritmo':<10} {'Tiempo':<10} {'Nodos':<10} {'Longitud':<10} {'Promedio':<10}\n")
        f.write("-" * 50 + "\n")
        
        # Ordenar por ranking promedio
        sorted_by_avg = sorted(algoritmos, key=lambda x: avg_rankings[x])
        for algo in sorted_by_avg:
            f.write(f"{algo:<10} {rankings['tiempo'][algo]:<10} {rankings['nodos'][algo]:<10} {rankings['longitud'][algo]:<10} {avg_rankings[algo]:<10.2f}\n")
        
        f.write("\nRANKING FINAL (de mejor a peor):\n")
        for rank, algo in enumerate(sorted_by_avg, 1):
            f.write(f"{rank}. {algo}\n")

if __name__ == "__main__":
    main()