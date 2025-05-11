import heapq
from algoritmos_busqueda import AlgoritmoBusqueda

class Algoritmo_AStar(AlgoritmoBusqueda):
    """
    Implementación del algoritmo A* con heurística de distancia Manhattan.
    """
    
    def heuristic(self, node):
        """
        Calcula la heurística (distancia Manhattan) desde el nodo hasta la salida.
        
        Args:
            node: Tupla (fila, columna) del nodo
            
        Returns:
            Distancia Manhattan al nodo de salida
        """
        r1, c1 = node
        r2, c2 = self.exit
        return abs(r1 - r2) + abs(c1 - c2)
    
    def solve(self):
        """
        Resuelve el laberinto usando A*.
        
        Returns:
            Tupla con (search_states, path)
        """
        # Reiniciar estados
        self.search_states = []
        
        # Cola de prioridad para A*
        # Formato: (f_score, g_score, nodo)
        # f_score = g_score + heurística (estimación del costo total)
        # g_score = costo actual desde inicio
        start_h = self.heuristic(self.entrance)
        priority_queue = [(start_h, 0, self.entrance)]
        
        # Diccionario para rastrear nodos visitados y su padre
        visited = {}
        # Costo actual desde inicio (g_score)
        g_scores = {self.entrance: 0}
        # Conjuntos para rastrear nodos expandidos y buscados
        expanded = set()
        searched = set([self.entrance])
        
        # Estado inicial
        self.add_state(expanded, searched, self.entrance)
        
        found = False
        
        while priority_queue and not found:
            # Obtener nodo con menor f_score
            _, g_score, current = heapq.heappop(priority_queue)
            
            # Si ya está expandido, continuar (posibles duplicados en la cola)
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
                new_g = g_score + 1
                
                # Si encontramos un camino mejor
                if neighbor not in g_scores or new_g < g_scores[neighbor]:
                    g_scores[neighbor] = new_g
                    f_score = new_g + self.heuristic(neighbor)
                    visited[neighbor] = current
                    heapq.heappush(priority_queue, (f_score, new_g, neighbor))
                    searched.add(neighbor)
                    # Estado para mostrar adición a la búsqueda
                    self.add_state(expanded, searched, neighbor)
        
        # Reconstruir camino si se encontró
        path = self.reconstruct_path(visited) if found else []
        
        return self.search_states, path

