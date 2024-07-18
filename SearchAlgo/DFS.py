from collections import deque
from SearchAlgo.SearchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)
    
    def Try(self):
        visited = set()
        parent = {}
        stack = [self.start]
        
        visited.add(self.start)
        

        while stack:
            current = stack.pop()
            for moveX, moveY in self.directions:
                newRow, newCol = current[0] + moveX, current[1] + moveY
                neighbor = (newRow, newCol)
                if 0 <= newRow < len(self.matrix) and 0 <= newCol < len(self.matrix[0]):
                    if self.matrix[newRow][newCol] != -1 and neighbor not in visited:
                        parent[neighbor] = current
                        if neighbor == self.end:
                            return self.create_path(parent)
                        stack.append(neighbor)
                        visited.add(neighbor)

        
        # Reconstruct the path and calculate the cost
        return None