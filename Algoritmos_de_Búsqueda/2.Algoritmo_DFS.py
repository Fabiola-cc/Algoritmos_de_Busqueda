from algoritmos_busqueda import AlgoritmoBusqueda

class Algoritmo_DFS(AlgoritmoBusqueda):
    """
    Implementación del algoritmo Depth-First Search (DFS).
    """
    
    def solve(self):
        """
        Resuelve el laberinto usando DFS.
        
        Returns:
            Tupla con (search_states, path)
        """
        # Reiniciar estados
        self.search_states = []
        
        # Pila para DFS (usando lista en Python)
        stack = [self.entrance]
        # Diccionario para rastrear nodos visitados y su padre
        visited = {self.entrance: None}
        # Conjuntos para rastrear nodos expandidos y buscados
        expanded = set()
        searched = set([self.entrance])
        
        # Estado inicial
        self.add_state(expanded, searched, self.entrance)
        
        found = False
        
        while stack and not found:
            current = stack.pop()  # Tomar el último elemento (LIFO)
            
            # Si ya está expandido, continuar
            if current in expanded:
                continue
                
            # Marcar como expandido
            expanded.add(current)
            self.add_state(expanded, searched, current)
            
            # Si llegamos a la salida
            if current == self.exit:
                found = True
                break
            
            # Procesar vecinos (en orden inverso para mantener dirección preferida)
            neighbors = self.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited[neighbor] = current
                    searched.add(neighbor)
                    # Estado para mostrar adición a la búsqueda
                    self.add_state(expanded, searched, neighbor)
        
        # Reconstruir camino si se encontró
        path = self.reconstruct_path(visited) if found else []
        
        return self.search_states, path
