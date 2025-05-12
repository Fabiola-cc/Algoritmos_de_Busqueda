'''
Proyecto #2 IA

Archivo para ejecutar el proceso completo
'''
from MazeGenerator import MazeGenerator
from MazeSolver import solve_maze_a_star, visualize_solution

# Crear generador de laberintos
generator = MazeGenerator(10, 10)

# Generar y comparar los laberintos
kruskal_maze, rb_maze = generator.compare_algorithms(10, 10, True)

generator2 = MazeGenerator(60, 80)

kruskal_maze, rb_maze = generator2.compare_algorithms(60, 80, False)

start = (1,1)
end = (60,80)

explored, path = solve_maze_a_star(kruskal_maze, start, end)
explored2, path2 = solve_maze_a_star(rb_maze, start, end)

print("\nSolución A* a laberinto kruskal\n")
visualize_solution(kruskal_maze, explored, path, start, end, title="Ruta A*", filename="solucion_kruskal.png")
print("\nSolución A* a laberinto RB\n")
visualize_solution(rb_maze, explored2, path2, start, end, title="Ruta A*", filename="solucion_rb.png")