import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib.colors import ListedColormap
from collections import deque
import time

class MazeGenerator:
    def __init__(self, height, width):
        """
        Inicializa el generador de laberintos.
        
        Args:
            height (int): Número de filas (M)
            width (int): Número de columnas (N)
        """
        self.height = height
        self.width = width
        # Matriz para almacenar el laberinto (1 = pared, 0 = pasillo, 2 = celda)
        self.grid = np.ones((2 * height + 1, 2 * width + 1), dtype=np.int8)
        # Para almacenar estados durante la construcción (para visualización)
        self.states = []
        # Posiciones de entrada y salida
        self.entrance = None
        self.exit = None
        
    def _initialize_grid(self):
        """Reinicia la matriz a un estado inicial (todo paredes)"""
        self.grid = np.ones((2 * self.height + 1, 2 * self.width + 1), dtype=np.int8)
        self.states = []
        
        # Marcamos las celdas (no las paredes) como '2' inicialmente para distinguirlas
        # Valor 2 = celdas no visitadas (azul claro en la visualización)
        for i in range(1, 2 * self.height, 2):
            for j in range(1, 2 * self.width, 2):
                self.grid[i, j] = 2
        
        # Guardamos el estado inicial
        self.states.append(np.copy(self.grid))
        
        # Resetear entrada y salida
        self.entrance = None
        self.exit = None
    
    def _get_cell_walls(self, row, col):
        """
        Devuelve las paredes alrededor de una celda como tuplas (pared_r, pared_c, celda_vecina_r, celda_vecina_c)
        """
        walls = []
        # Convertimos índices lógicos a índices de matriz
        r, c = 2*row + 1, 2*col + 1
        
        # Revisar arriba
        if row > 0:
            walls.append((r-1, c, row-1, col))  # (pared_r, pared_c, celda_vecina_r, celda_vecina_c)
        # Revisar abajo
        if row < self.height - 1:
            walls.append((r+1, c, row+1, col))
        # Revisar izquierda
        if col > 0:
            walls.append((r, c-1, row, col-1))
        # Revisar derecha
        if col < self.width - 1:
            walls.append((r, c+1, row, col+1))
            
        return walls
    
    def _get_all_walls(self):
        """Obtiene todas las paredes internas como tuplas (r, c, r1, c1, r2, c2)"""
        walls = []
        
        # Paredes horizontales
        for r in range(1, 2 * self.height, 2):
            for c in range(2, 2 * self.width, 2):
                # Coordenadas lógicas de las celdas a ambos lados de la pared
                cell1_r, cell1_c = (r - 1) // 2, (c - 2) // 2
                cell2_r, cell2_c = (r - 1) // 2, c // 2
                walls.append((r, c, cell1_r, cell1_c, cell2_r, cell2_c))
        
        # Paredes verticales
        for r in range(2, 2 * self.height, 2):
            for c in range(1, 2 * self.width, 2):
                # Coordenadas lógicas de las celdas a ambos lados de la pared
                cell1_r, cell1_c = (r - 2) // 2, (c - 1) // 2
                cell2_r, cell2_c = r // 2, (c - 1) // 2
                walls.append((r, c, cell1_r, cell1_c, cell2_r, cell2_c))
                
        return walls
    
    def generate_kruskal(self):
        """
        Genera un laberinto aleatorio usando el algoritmo de Kruskal.
        """
        self._initialize_grid()
        
        # Inicializar conjuntos disjuntos (cada celda es su propio conjunto)
        sets = {}
        for r in range(self.height):
            for c in range(self.width):
                sets[(r, c)] = (r, c)
        
        # Función para encontrar el representante del conjunto
        def find(cell):
            if sets[cell] != cell:
                sets[cell] = find(sets[cell])  # Compresión de camino
            return sets[cell]
        
        # Función para unir dos conjuntos
        def union(cell1, cell2):
            root1 = find(cell1)
            root2 = find(cell2)
            if root1 != root2:
                sets[root2] = root1
            return root1 != root2
        
        # Obtener todas las paredes internas
        walls = self._get_all_walls()
        # Mezclar las paredes aleatoriamente
        random.shuffle(walls)
        
        # Procesar cada pared
        for wall_r, wall_c, cell1_r, cell1_c, cell2_r, cell2_c in walls:
            cell1 = (cell1_r, cell1_c)
            cell2 = (cell2_r, cell2_c)
            
            # Si las celdas no están en el mismo conjunto, eliminar la pared entre ellas
            if find(cell1) != find(cell2):
                # Eliminar pared
                self.grid[wall_r, wall_c] = 0
                # Unir los conjuntos
                union(cell1, cell2)
                # Guardar estado para visualización
                self.states.append(np.copy(self.grid))
        
        # Convertir todas las celdas (valor 2) en pasillos (valor 0)
        self.grid[self.grid == 2] = 0
        self.states[-1][self.states[-1] == 2] = 0
        
        # Crear entrada y salida
        self._create_entrance_exit()
        self.states.append(np.copy(self.grid))
        
        return self.grid, self.states
    
    def generate_recursive_backtracking(self):
        """
        Genera un laberinto aleatorio usando el algoritmo de Recursive Backtracking.
        """
        self._initialize_grid()
        
        # Comenzamos desde una celda aleatoria
        start_r = random.randint(0, self.height - 1)
        start_c = random.randint(0, self.width - 1)
        
        # Marcar como visitada
        visited = np.zeros((self.height, self.width), dtype=bool)
        visited[start_r, start_c] = True
        
        # La celda inicial es un pasillo
        self.grid[2*start_r + 1, 2*start_c + 1] = 0
        
        # Pila para backtracking
        stack = [(start_r, start_c)]
        
        # Direcciones (arriba, derecha, abajo, izquierda)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        while stack:
            current_r, current_c = stack[-1]
            
            # Buscar vecinos no visitados
            neighbors = []
            for dr, dc in directions:
                next_r, next_c = current_r + dr, current_c + dc
                if (0 <= next_r < self.height and 0 <= next_c < self.width and
                        not visited[next_r, next_c]):
                    neighbors.append((next_r, next_c, dr, dc))
            
            if neighbors:
                # Elegir un vecino aleatorio
                next_r, next_c, dr, dc = random.choice(neighbors)
                
                # Derribar la pared entre celdas
                wall_r = 2*current_r + 1 + dr
                wall_c = 2*current_c + 1 + dc
                if 0 <= next_r < self.height and 0 <= next_c < self.width:
                    self.grid[wall_r, wall_c] = 0  # Eliminar pared
                    self.grid[2*next_r + 1, 2*next_c + 1] = 0  # Marcar celda como pasillo
                    
                    # Marcar como visitada
                    visited[next_r, next_c] = True
                    
                    # Añadir a la pila
                    stack.append((next_r, next_c))
                    
                    # Guardar estado para visualización
                    self.states.append(np.copy(self.grid))
            else:
                # Backtrack
                stack.pop()
        
        # Convertir todas las celdas (valor 2) en pasillos (valor 0)
        self.grid[self.grid == 2] = 0
        self.states[-1][self.states[-1] == 2] = 0
        
        # Crear entrada y salida
        self._create_entrance_exit()
        self.states.append(np.copy(self.grid))
        
        return self.grid, self.states

    def _create_entrance_exit(self):
        """
        Crea una entrada y una salida en el laberinto, en bordes opuestos.
        """
        # Determinar posición de la entrada (pared superior o izquierda)
        entrance_side = random.choice(['top', 'left'])
        
        if entrance_side == 'top':
            # Entrada en la pared superior
            col = random.randint(0, self.width - 1)
            self.entrance = (0, 2*col + 1)
            self.grid[0, 2*col + 1] = 0
            
            # Salida en la pared inferior
            col = random.randint(0, self.width - 1)
            self.exit = (2*self.height, 2*col + 1)
            self.grid[2*self.height, 2*col + 1] = 0
        else:
            # Entrada en la pared izquierda
            row = random.randint(0, self.height - 1)
            self.entrance = (2*row + 1, 0)
            self.grid[2*row + 1, 0] = 0
            
            # Salida en la pared derecha
            row = random.randint(0, self.height - 1)
            self.exit = (2*row + 1, 2*self.width)
            self.grid[2*row + 1, 2*self.width] = 0
    
    def visualize_maze(self, title=None):
        """
        Visualiza el laberinto final.
        """
        plt.figure(figsize=(8, 8))
        # Crear un mapa de colores para el laberinto (0=pasillo, 1=pared, 3=entrada, 4=salida)
        grid_viz = np.copy(self.grid)
        
        # Marcar entrada y salida
        if self.entrance:
            grid_viz[self.entrance] = 3  # Entrada (verde)
        if self.exit:
            grid_viz[self.exit] = 4      # Salida (rojo)
        
        # Crear mapa de colores
        cmap = ListedColormap(['white', 'black', 'lightblue', 'green', 'red'])
        plt.imshow(grid_viz, cmap=cmap)
        
        # Agregar leyenda
        plt.text(0.5, -0.02, 
                "Colores: Negro=Pared, Blanco=Pasillo, Verde=Entrada, Rojo=Salida", 
                transform=plt.gca().transAxes, ha='center', fontsize=10)
        
        plt.axis('off')
        if title:
            plt.title(title)
        plt.tight_layout()
        plt.show()
    
    def animate_construction(self, states, title=None, speed=200):
        """
        Crea una animación del proceso de construcción del laberinto.
        
        Args:
            states: Lista de estados de la matriz del laberinto
            title: Título para la animación
            speed: Velocidad de la animación (ms entre frames)
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Crear mapa de colores personalizado:
        # 0 = pasillo (blanco)
        # 1 = pared (negro)
        # 2 = celda no visitada (azul claro)
        # 3 = entrada (verde)
        # 4 = salida (rojo)
        # 5 = última pared eliminada (amarillo) - para destacar el progreso
        cmap = ListedColormap(['white', 'black', 'lightblue', 'green', 'red', 'yellow'])
        
        # Para rastrear la última pared eliminada
        prev_state = None
        
        # Función de inicialización
        def init():
            ax.clear()
            ax.set_axis_off()
            if title:
                ax.set_title(title)
            ax.text(0.5, -0.05, 
                   "Colores: Negro=Pared, Blanco=Pasillo, Azul=Celda no visitada\nVerde=Entrada, Rojo=Salida, Amarillo=Última modificación", 
                   transform=ax.transAxes, ha='center', fontsize=9)
            return []
        
        # Función de actualización
        def update(frame):
            nonlocal prev_state
            ax.clear()
            
            # Preparar visualización del estado actual
            state_viz = np.copy(states[frame])
            
            # Marcar la última modificación (pared eliminada o entrada/salida añadida)
            if frame > 0 and prev_state is not None:
                # Encontrar las diferencias entre estados
                diff = (state_viz != prev_state)
                # Marcar las diferencias en amarillo (valor 5)
                state_viz[diff] = 5
            
            # Marcar entrada y salida en el último frame
            if frame == len(states) - 1 and self.entrance and self.exit:
                state_viz[self.entrance] = 3  # Entrada (verde)
                state_viz[self.exit] = 4      # Salida (rojo)
            
            # Mostrar laberinto
            ax.imshow(state_viz, cmap=cmap)
            ax.set_axis_off()
            
            # Mostrar título y leyenda
            if title:
                ax.set_title(f"{title} - Paso {frame+1}/{len(states)}")
            
            ax.text(0.5, -0.05, 
                   "Colores: Negro=Pared, Blanco=Pasillo, Azul=Celda no visitada\nVerde=Entrada, Rojo=Salida, Amarillo=Última modificación", 
                   transform=ax.transAxes, ha='center', fontsize=9)
            
            # Actualizar el estado anterior para el próximo frame
            prev_state = np.copy(states[frame])
            
            return []
        
        # Crear animación
        ani = animation.FuncAnimation(fig, update, frames=len(states), 
                                     init_func=init, blit=True, interval=speed)
        plt.close()
        return ani
    
    def save_maze_image(self, filename="maze.png", title=None):
        """
        Guarda una imagen del laberinto actual.

        Args:
            filename (str): Nombre del archivo donde se guardará la imagen.
            title (str): Título opcional para la imagen.
        """
        grid_viz = np.copy(self.grid)
        if self.entrance:
            grid_viz[self.entrance] = 3
        if self.exit:
            grid_viz[self.exit] = 4

        cmap = ListedColormap(['white', 'black', 'lightblue', 'green', 'red'])
        plt.figure(figsize=(8, 8))
        plt.imshow(grid_viz, cmap=cmap)
        plt.axis('off')
        if title:
            plt.title(title)
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()


    def compare_algorithms(self, height, width, save_animation=False):
        """
        Compara los algoritmos de Kruskal y Recursive Backtracking.
        
        Args:
            height: Altura del laberinto
            width: Ancho del laberinto
            save_animation: Si True, guarda las animaciones como archivos GIF
        """
        self.height = height
        self.width = width
        
        # Generar laberinto con Kruskal
        print("Generando laberinto con Kruskal...")
        start_time = time.time()
        kruskal_maze, kruskal_states = self.generate_kruskal()
        kruskal_time = time.time() - start_time
        kruskal_entrance = self.entrance
        kruskal_exit = self.exit
        
        # Guardar el laberinto de Kruskal
        kruskal_final = np.copy(kruskal_maze)
        
        # Resetear atributos para el siguiente laberinto
        self.entrance = None
        self.exit = None
        
        # Generar laberinto con Recursive Backtracking
        print("Generando laberinto con Recursive Backtracking...")
        start_time = time.time()
        rb_maze, rb_states = self.generate_recursive_backtracking()
        rb_time = time.time() - start_time
        rb_entrance = self.entrance
        rb_exit = self.exit
        
        # Guardar el laberinto de Recursive Backtracking
        rb_final = np.copy(rb_maze)
        
        print(f"\n--- Comparación para laberinto de tamaño {height}x{width} ---")
        print(f"Kruskal: {len(kruskal_states)} pasos, {kruskal_time:.4f} segundos")
        print(f"Recursive Backtracking: {len(rb_states)} pasos, {rb_time:.4f} segundos")
        
        print("\nCreando animaciones...")
        
        # Actualizar atributos para las animaciones
        self.entrance = kruskal_entrance
        self.exit = kruskal_exit
        kruskal_ani = self.animate_construction(kruskal_states, "Kruskal", speed=100)
        
        self.entrance = rb_entrance
        self.exit = rb_exit
        rb_ani = self.animate_construction(rb_states, "Recursive Backtracking", speed=100)
        
        # Guardar animaciones si se solicita
        if save_animation:
            print("\nGuardando animaciones como GIF...")
            kruskal_ani.save('./Maze_results/kruskal_maze.gif', writer='pillow', fps=10)
            rb_ani.save('./Maze_results/recursive_backtracking_maze.gif', writer='pillow', fps=10)
            print("Animaciones guardadas como 'kruskal_maze.gif' y 'recursive_backtracking_maze.gif'")

        # Guardar imágenes de los laberintos finales
        print("\nGuardando resultados finales como PNG")
        self.entrance = kruskal_entrance
        self.exit = kruskal_exit
        self.grid = kruskal_final
        self.save_maze_image('./Maze_results/kruskal_maze.png', "Laberinto - Kruskal")

        self.entrance = rb_entrance
        self.exit = rb_exit
        self.grid = rb_final
        self.save_maze_image('./Maze_results/recursive_backtracking_maze.png', "Laberinto - Recursive Backtracking")
        print("Imágenes guardadas como 'kruskal_maze.png' y 'recursive_backtracking_maze.png'")
        
        return kruskal_final, rb_final

# Ejemplo de uso
if __name__ == "__main__":
    # Crear generador de laberintos
    generator = MazeGenerator(10, 10)
    
    kruskal_maze, rb_maze = generator.compare_algorithms(10, 10, save_animation=True)