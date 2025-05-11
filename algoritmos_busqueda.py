import numpy as np
from collections import deque
import heapq
from abc import ABC, abstractmethod

class AlgoritmoBusqueda(ABC):
    """
    Clase base abstracta para algoritmos de búsqueda de camino en laberintos.
    """
    
    def __init__(self, maze, entrance, exit):
        """
        Inicializa el algoritmo de búsqueda.
        
        Args:
            maze: La matriz del laberinto (0 = pasillo, 1 = pared)
            entrance: Tupla (fila, columna) del punto de entrada
            exit: Tupla (fila, columna) del punto de salida
        """
        self.maze = maze
        self.entrance = entrance
        self.exit = exit
        self.height, self.width = maze.shape
        self.search_states = []
        
    def get_neighbors(self, position):
        """
        Obtiene los vecinos válidos (pasillos) de una posición.
        
        Args:
            position: Tupla (fila, columna) de la posición actual
            
        Returns:
            Una lista de tuplas (fila, columna) de vecinos válidos
        """
        r, c = position
        neighbors = []
        # Revisar las cuatro direcciones (derecha, abajo, izquierda, arriba)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_r, new_c = r + dr, c + dc
            # Verificar si la posición es válida y es un pasillo (no una pared)
            if (0 <= new_r < self.height and 0 <= new_c < self.width and
                self.maze[new_r, new_c] == 0):
                neighbors.append((new_r, new_c))
        return neighbors
    
    def add_state(self, expanded, searched, current, path=None):
        """
        Añade un estado para visualización.
        
        Args:
            expanded: Conjunto de nodos expandidos
            searched: Conjunto de nodos descubiertos pero no necesariamente expandidos
            current: Nodo actual que se está procesando
            path: Camino parcial (para visualización de reconstrucción)
        """
        if path is None:
            path = []
            
        state = {
            'expanded': set(expanded),
            'searched': set(searched),
            'current': current,
            'path': list(path)
        }
        self.search_states.append(state)
    
    def reconstruct_path(self, visited):
        """
        Reconstruye el camino desde la entrada hasta la salida.
        
        Args:
            visited: Diccionario que mapea nodos a sus padres
            
        Returns:
            Una lista de tuplas formando el camino desde entrada a salida
        """
        path = []
        current = self.exit
        
        # Si no hay camino a la salida
        if self.exit not in visited:
            return []
            
        # Reconstruir camino de salida a entrada
        while current != self.entrance:
            path.append(current)
            current = visited[current]
            if current is None:  # Caso imposible si la salida está en visited
                return []
                
        path.append(self.entrance)
        path.reverse()  # Invertir para obtener camino de entrada a salida
        
        # Añadir estados para visualizar la reconstrucción gradual del camino
        expanded = self.search_states[-1]['expanded']
        searched = self.search_states[-1]['searched']
        
        for i in range(1, len(path) + 1):
            partial_path = path[:i]
            self.add_state(expanded, searched, path[i-1], partial_path)
            
        return path
    
    @abstractmethod
    def solve(self):
        """
        Resuelve el laberinto usando el algoritmo específico.
        
        Returns:
            Tupla con (search_states, path)
        """
        pass

