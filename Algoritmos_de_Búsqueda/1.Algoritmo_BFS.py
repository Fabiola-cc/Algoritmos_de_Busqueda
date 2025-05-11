from collections import deque
from algoritmos_busqueda import AlgoritmoBusqueda

class Algoritmo_BFS(AlgoritmoBusqueda):
    """
    Implementación del algoritmo Breadth-First Search (BFS).
    """
    
    def solve(self):
        """
        Resuelve el laberinto usando BFS.
        
        Returns:
            Tupla con (search_states, path)
        """
        # Reiniciar estados
        self.search_states = []
        
        # Cola para BFS
        queue = deque([self.entrance])
        # Diccionario para rastrear nodos visitados y su padre
        visited = {self.entrance: None}
        # Conjuntos para rastrear nodos expandidos y buscados
        expanded = set()
        searched = set([self.entrance])
        
        # Estado inicial
        self.add_state(expanded, searched, self.entrance)
        
        found = False
        
        while queue and not found:
            current = queue.popleft()
            
            # Marcar como expandido
            expanded.add(current)
            self.add_state(expanded, searched, current)
            
            # Si llegamos a la salida
            if current == self.exit:
                found = True
                break
            
            # Procesar vecinos
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = current
                    searched.add(neighbor)
                    # Estado para mostrar adición a la búsqueda
                    self.add_state(expanded, searched, neighbor)
        
        # Reconstruir camino si se encontró
        path = self.reconstruct_path(visited) if found else []
        
        return self.search_states, path


