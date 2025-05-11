import heapq
from matplotlib import colors
import matplotlib.pyplot as plt
import os


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_maze_a_star(maze, start, end):
    height, width = maze.shape

    # Si el destino es una pared, buscar una celda libre adyacente
    if maze[end] != 0:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = end[0] + dx, end[1] + dy
            if 0 <= nx < height and 0 <= ny < width and maze[nx, ny] == 0:
                end = (nx, ny)
                break
        else:
            print("No se encontró una celda adyacente libre para el destino.")
            return [], []

    # Inicializar estructuras
    frontier = [(0 + manhattan(start, end), 0, start)]  # (f_score, g_score, nodo)
    came_from = {}
    g_scores = {start: 0}
    explored = set()
    searched = set([start])
    search_states = []

    found = False

    while frontier and not found:
        _, g_score, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)
        search_states.append((set(explored), set(searched), current))

        if current == end:
            found = True
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if 0 <= nx < height and 0 <= ny < width and maze[nx, ny] == 0:
                new_g = g_score + 1
                if neighbor not in g_scores or new_g < g_scores[neighbor]:
                    g_scores[neighbor] = new_g
                    f_score = new_g + manhattan(neighbor, end)
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (f_score, new_g, neighbor))
                    searched.add(neighbor)
                    search_states.append((set(explored), set(searched), neighbor))

    # Reconstruir camino
    path = []
    if found:
        current = end
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

    return list(explored), path




def visualize_solution(maze, explored, path, start, end, title="Solución A*", filename="solucion.png"):
    # Crear carpeta si no existe
    os.makedirs("Maze_results", exist_ok=True)

    cmap = colors.ListedColormap(['white', 'black', 'lightblue', 'green', 'red', 'orange'])
    norm = colors.BoundaryNorm([0, 0.5, 1.5, 2.5, 3.5, 4.5, 6], cmap.N)

    display_maze = maze.copy()
    for x, y in explored:
        if (x, y) not in [start, end]:
            display_maze[x, y] = 2  # Azul claro
    for x, y in path:
        if (x, y) not in [start, end]:
            display_maze[x, y] = 3  # Verde
    display_maze[start] = 4      # Rojo
    display_maze[end] = 5        # Verde oscuro

    plt.figure(figsize=(10, 10))
    plt.imshow(display_maze, cmap=cmap, norm=norm)
    plt.title(title)
    plt.axis('off')

    # Guardar imagen
    save_path = os.path.join("Maze_results", filename)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

    print(f"🔹 Longitud del camino: {len(path)}")
    print(f"🔹 Celdas exploradas: {len(explored)}")
    print(f"📸 Imagen guardada como: {save_path}")


