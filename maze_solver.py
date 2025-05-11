import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import os

# Importamos la clase MazeGenerator y nuestros algoritmos
from MazeGenerator import MazeGenerator
from Algoritmos_de_Búsqueda import Algoritmo_BFS
from Algoritmos_de_Búsqueda import Algoritmo_DFS
from Algoritmos_de_Búsqueda import Algoritmo_Dijkstra
from Algoritmos_de_Búsqueda import Algoritmo_AStar
from Algoritmos_de_Búsqueda import Algoritmo_Greedy

def visualize_maze_with_path(generator, expanded, searched, path, title="Visualización de Búsqueda de Camino"):
    """
    Crea una visualización del laberinto con los resultados de la búsqueda de camino.
    
    Args:
        generator: Instancia de MazeGenerator con el laberinto
        expanded: Conjunto de nodos expandidos
        searched: Conjunto de nodos buscados
        path: Lista de nodos que forman el camino
        title: Título para la visualización
    """
    # Crear una copia de la matriz del laberinto para visualización
    viz_grid = np.copy(generator.grid)
    
    # Crear un mapa de colores similar a la imagen original
    # 0: Celda/Pasillo (blanco)
    # 1: Pared (negro)
    # 2: Inicio/Entrada (rojo)
    # 3: Fin/Salida (verde)
    # 4: Búsqueda (amarillo)
    # 5: Expandido (naranja)
    # 6: Camino (morado)
    
    # Marcar área de búsqueda (amarillo)
    for r, c in searched:
        if (r, c) not in [generator.entrance, generator.exit]:
            viz_grid[r, c] = 4
    
    # Marcar nodos expandidos (naranja)
    for r, c in expanded:
        if (r, c) not in [generator.entrance, generator.exit]:
            viz_grid[r, c] = 5
    
    # Marcar camino (morado)
    for r, c in path:
        if (r, c) not in [generator.entrance, generator.exit]:
            viz_grid[r, c] = 6
    
    # Marcar entrada (rojo) y salida (verde)
    viz_grid[generator.entrance] = 2
    viz_grid[generator.exit] = 3
    
    # Crear figura
    plt.figure(figsize=(12, 8))
    
    # Definir colores para la visualización
    colors = ['white', 'black', 'red', 'lime', 'yellow', 'orange', 'purple']
    cmap = ListedColormap(colors)
    
    # Mostrar el laberinto
    plt.imshow(viz_grid, cmap=cmap)
    
    # Crear leyenda
    legend_elements = [
        mpatches.Patch(color='black', label='Pared'),
        mpatches.Patch(color='white', label='Celda'),
        mpatches.Patch(color='red', label='Inicio'),
        mpatches.Patch(color='lime', label='Fin'),
        mpatches.Patch(color='yellow', label='Búsqueda'),
        mpatches.Patch(color='orange', label='Expandido'),
        mpatches.Patch(color='purple', label='Camino')
    ]
    
    # Añadir leyenda a la derecha
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), 
               loc='upper left', title='Leyenda del Laberinto')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    
    return plt.gcf()  # Devolver la figura actual para posible guardado

def create_search_animation(generator, search_states, algorithm_name="", save_path=None):
    """
    Crea una animación del proceso de búsqueda en el laberinto.
    
    Args:
        generator: Instancia de MazeGenerator con el laberinto
        search_states: Lista de estados de búsqueda
        algorithm_name: Nombre del algoritmo para el título
        save_path: Ruta opcional para guardar la animación como GIF
        
    Returns:
        ani: Objeto de animación
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Definir colores para la visualización
    colors = ['white', 'black', 'red', 'lime', 'yellow', 'orange', 'purple']
    cmap = ListedColormap(colors)
    
    # Crear leyenda
    legend_elements = [
        mpatches.Patch(color='black', label='Pared'),
        mpatches.Patch(color='white', label='Celda'),
        mpatches.Patch(color='red', label='Inicio'),
        mpatches.Patch(color='lime', label='Fin'),
        mpatches.Patch(color='yellow', label='Búsqueda'),
        mpatches.Patch(color='orange', label='Expandido'),
        mpatches.Patch(color='purple', label='Camino')
    ]
    
    def init():
        ax.clear()
        ax.set_axis_off()
        return []
    
    def update(frame_idx):
        ax.clear()
        
        # Obtener el estado actual
        state = search_states[frame_idx]
        
        # Crear una copia del laberinto para visualización
        viz_grid = np.copy(generator.grid)
        
        # Marcar área de búsqueda (amarillo)
        for r, c in state['searched']:
            if (r, c) not in [generator.entrance, generator.exit]:
                viz_grid[r, c] = 4
                
        # Marcar nodos expandidos (naranja)
        for r, c in state['expanded']:
            if (r, c) not in [generator.entrance, generator.exit]:
                viz_grid[r, c] = 5
                
        # Marcar el camino (morado)
        for r, c in state['path']:
            if (r, c) not in [generator.entrance, generator.exit]:
                viz_grid[r, c] = 6
                
        # Marcar entrada (rojo) y salida (verde)
        viz_grid[generator.entrance] = 2
        viz_grid[generator.exit] = 3
        
        # Mostrar el laberinto
        ax.imshow(viz_grid, cmap=cmap)
        
        # Añadir leyenda a la derecha
        ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), 
                loc='upper left', title='Leyenda del Laberinto')
        
        # Determinar etapa del progreso
        progress_stage = ""
        if len(state['path']) == 0:
            progress_stage = "Búsqueda"
        else:
            progress_stage = "Construcción de camino"
            
        ax.set_title(f'{algorithm_name} - {progress_stage} - Paso {frame_idx+1}/{len(search_states)}')
        ax.axis('off')
        
        return []
    
    ani = animation.FuncAnimation(fig, update, frames=len(search_states),
                                 init_func=init, blit=True, interval=200)
    
    # Guardar la animación si se solicita
    if save_path:
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        ani.save(save_path, writer='pillow', fps=5)
        print(f"Animación guardada en: {save_path}")
        
    return ani

def compare_algorithms(generator, save_path=None):
    """
    Compara diferentes algoritmos de búsqueda de camino en el mismo laberinto.
    
    Args:
        generator: Instancia de MazeGenerator con el laberinto ya generado
        save_path: Directorio opcional para guardar resultados
    """
    maze = generator.grid
    entrance = generator.entrance
    exit = generator.exit
    
    # Crear directorio para resultados si se especifica
    if save_path:
        os.makedirs(save_path, exist_ok=True)
    
    # Lista de algoritmos a comparar
    algorithms = [
        ("BFS (Breadth-First Search)", Algoritmo_BFS(maze, entrance, exit)),
        ("DFS (Depth-First Search)", Algoritmo_DFS(maze, entrance, exit)),
        ("Dijkstra", Algoritmo_Dijkstra(maze, entrance, exit)),
        ("A* (A-Star)", Algoritmo_AStar(maze, entrance, exit)),
        ("Greedy Best-First", Algoritmo_Greedy(maze, entrance, exit))
    ]
    
    results = {}
    
    # Ejecutar cada algoritmo
    for name, algorithm in algorithms:
        print(f"Ejecutando algoritmo: {name}")
        search_states, path = algorithm.solve()
        
        results[name] = {
            "estados": len(search_states),
            "longitud_camino": len(path),
            "search_states": search_states,
            "path": path
        }
        
        print(f"  - Estados generados: {len(search_states)}")
        print(f"  - Longitud del camino: {len(path)}")
        
        # Visualizar resultado final
        final_state = search_states[-1]
        fig = visualize_maze_with_path(
            generator, 
            final_state['expanded'],
            final_state['searched'],
            path,
            title=f"Resultado: {name}"
        )
        
        # Guardar imagen final si se especifica ruta
        if save_path:
            fig.savefig(f"{save_path}/{name.replace(' ', '_')}_final.png", 
                       bbox_inches='tight')
            
        # Generar animación si se especifica ruta
        if save_path:
            ani = create_search_animation(
                generator,
                search_states,
                algorithm_name=name,
                save_path=f"{save_path}/{name.replace(' ', '_')}_animation.gif"
            )
    
    # Mostrar tabla comparativa
    print("\n=== Comparación de Algoritmos ===")
    print(f"{'Algoritmo':<20} {'Estados':<10} {'Longitud':<10}")
    print("-" * 40)
    for name, data in results.items():
        print(f"{name:<20} {data['estados']:<10} {data['longitud_camino']:<10}")
    
    return results

# Función para resolver con un algoritmo específico
def solve_maze(generator, algorithm_class, animation=True, save_path=None):
    """
    Resuelve un laberinto con un algoritmo específico.
    
    Args:
        generator: Instancia de MazeGenerator con el laberinto ya generado
        algorithm_class: Clase del algoritmo a utilizar
        animation: Si True, muestra la animación del proceso
        save_path: Ruta opcional para guardar resultados
        
    Returns:
        Tupla con (search_states, path)
    """
    maze = generator.grid
    entrance = generator.entrance
    exit = generator.exit
    
    # Crear instancia del algoritmo
    algorithm = algorithm_class(maze, entrance, exit)
    
    # Nombre del algoritmo para visualización
    algorithm_name = algorithm.__class__.__name__.replace('Algoritmo_', '')
    
    # Resolver el laberinto
    search_states, path = algorithm.solve()
    
    # Obtener estado final
    final_state = search_states[-1]
    expanded = final_state['expanded']
    searched = final_state['searched']
    
    # Visualizar resultado
    visualize_maze_with_path(
        generator, 
        expanded,
        searched,
        path,
        title=f"Resultado: {algorithm_name}"
    )
    
    # Crear animación si se solicita
    if animation:
        ani = create_search_animation(
            generator,
            search_states,
            algorithm_name=algorithm_name,
            save_path=save_path
        )
        plt.show()
    
    return search_states, path

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un generador de laberintos
    height, width = 15, 25
    generator = MazeGenerator(height, width)
    
    # Generar un laberinto
    maze, _ = generator.generate_recursive_backtracking()
    
    # Visualizar el laberinto original
    generator.visualize_maze(title="Laberinto Original")
    
    # Opción 1: Resolver con un algoritmo específico
    # Descomentar la línea del algoritmo deseado
    
    # solve_maze(generator, Algoritmo_BFS)
    # solve_maze(generator, Algoritmo_DFS)
    # solve_maze(generator, Algoritmo_Dijkstra)
    # solve_maze(generator, Algoritmo_AStar)
    # solve_maze(generator, Algoritmo_Greedy)
    
    # Opción 2: Comparar todos los algoritmos
    # Descomentar la siguiente línea para ejecutar la comparación
    
    # compare_algorithms(generator, save_path="./Maze_results")
    
    # Por defecto, ejecutamos BFS para este ejemplo
    solve_maze(generator, Algoritmo_BFS)
    
    plt.show()