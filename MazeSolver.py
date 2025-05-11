import heapq
from matplotlib import colors
import matplotlib.pyplot as plt
import os


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_maze_a_star(maze, start, end):
    height, width = maze.shape

    # Verifica si el end es una pared
    if maze[end] != 0:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = end[0] + dx, end[1] + dy
            if 0 <= nx < height and 0 <= ny < width and maze[nx, ny] == 0:
                end = (nx, ny)
                break
        else:
            print(" No se encontró una celda adyacente libre para el punto de llegada.")
            return [], []

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = []

    while frontier:
        _, current = heapq.heappop(frontier)
        explored.append(current)

        if current == end:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            next_cell = (nx, ny)

            if 0 <= nx < height and 0 <= ny < width and maze[nx, ny] == 0:
                new_cost = cost_so_far[current] + 1
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + manhattan(next_cell, end)
                    heapq.heappush(frontier, (priority, next_cell))
                    came_from[next_cell] = current

    # Reconstruir camino
    path = []
    if end in came_from:
        current = end
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

    return explored, path



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


