import heapq
from algoritmos_busqueda import AlgoritmoBusqueda

class Algoritmo_Dijkstra(AlgoritmoBusqueda):
    """
    Implementación del algoritmo de Dijkstra.
    En un laberinto tradicional, todos los pasos tienen el mismo costo (1).
    """
    
    def solve(self):
        """
        Resuelve el laberinto usando Dijkstra.
        
        Returns:
            Tupla con (search_states, path)
        """
        # Reiniciar estados
        self.search_states = []
        
        # Cola de prioridad para Dijkstra
        # Formato: (distancia, nodo)
        priority_queue = [(0, self.entrance)]
        
        # Diccionario para rastrear nodos visitados y su padre
        visited = {}
        # Distancias conocidas a cada nodo
        distances = {self.entrance: 0}
        # Conjuntos para rastrear nodos expandidos y buscados
        expanded = set()
        searched = set([self.entrance])
        
        # Estado inicial
        self.add_state(expanded, searched, self.entrance)
        
        found = False
        
        while priority_queue and not found:
            # Obtener nodo con menor distancia
            dist, current = heapq.heappop(priority_queue)
            
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
            
            # Procesar vecinos
            for neighbor in self.get_neighbors(current):
                # Costo siempre es 1 en un laberinto tradicional
                new_dist = dist + 1
                
                # Si encontramos un camino mejor
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    visited[neighbor] = current
                    heapq.heappush(priority_queue, (new_dist, neighbor))
                    searched.add(neighbor)
                    # Estado para mostrar adición a la búsqueda
                    self.add_state(expanded, searched, neighbor)
        
        # Reconstruir camino si se encontró
        path = self.reconstruct_path(visited) if found else []
        
        return self.search_states, path
