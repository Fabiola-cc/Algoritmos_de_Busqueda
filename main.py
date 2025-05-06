'''
Proyecto #2 IA

Archivo para ejecutar el proceso completo
'''
from MazeGenerator import MazeGenerator

# Crear generador de laberintos
generator = MazeGenerator(10, 10)

# Generar y comparar los laberintos
kruskal_maze, rb_maze = generator.compare_algorithms(10, 10, save_animation=True)
