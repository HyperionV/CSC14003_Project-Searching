from SearchAlgo.SearchAlgorithm import *
import heapq

class GBFS(SearchAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)
    
    def Try(self):
        visited = set()
        parent = {}
        
        # Priority queue to store (heuristic cost, current node)
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start))
        
        while priority_queue:
            _, current = heapq.heappop(priority_queue)
            

            if current in visited:
                continue
            
            visited.add(current)
            

            for moveX, moveY in self.directions:
                newRow, newCol = current[0] + moveX, current[1] + moveY
                neighbor = (newRow, newCol)
                if 0 <= newRow < len(self.matrix) and 0 <= newCol < len(self.matrix[0]):
                    if self.matrix[newRow][newCol]!= -1 and neighbor not in visited:
                        parent[neighbor] = current
                        if neighbor == self.end:
                            return self.create_path(parent)
                        heuristic = manhattan_distance(neighbor, self.end)
                        heapq.heappush(priority_queue, (heuristic, neighbor))
        
        return None  # No path found
