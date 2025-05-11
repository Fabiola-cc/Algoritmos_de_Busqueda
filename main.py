'''
Proyecto #2 IA

Archivo para ejecutar el proceso completo
'''
from MazeGenerator import MazeGenerator
from MazeSolver import solve_maze_a_star, visualize_solution

# Crear generador de laberintos
generator = MazeGenerator(60, 80)

# Generar y comparar los laberintos
kruskal_maze, rb_maze = generator.compare_algorithms(60, 80, False)

def logical_to_maze_coords(logical_coord):
    return (2 * logical_coord[0] + 1, 2 * logical_coord[1] + 1)

# Automático: usa inicio en (0,0) lógico y fin en (M-1,N-1) lógico
def get_start_end_from_maze_shape(maze):
    logical_height = (maze.shape[0] - 1) // 2
    logical_width = (maze.shape[1] - 1) // 2
    start = logical_to_maze_coords((0, 0))
    end = logical_to_maze_coords((logical_height - 1, logical_width - 1))
    return start, end

start, end = get_start_end_from_maze_shape(kruskal_maze)

explored, path = solve_maze_a_star(kruskal_maze, start, end)
explored2, path2 = solve_maze_a_star(rb_maze, start, end)

visualize_solution(kruskal_maze, explored, path, start, end)
visualize_solution(rb_maze, explored2, path2, start, end)
