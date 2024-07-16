from SearchAlgo.SearchAlgorithm import *
import heapq


class AStar(SearchAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)


    def Try(self):
        queue = [(0, 0, self.start, [])]  # priority queue with cost, node, and path
        visited = set()
        path = []
        while queue:
            (fcost, cost, current, path) = heapq.heappop(queue)
            if current not in visited:
                visited.add(current)
                newPath = path + [current]

                if current == self.end:
                    return newPath
                
                for moveX, moveY in self.directions:
                    newRow, newCol = current[0] + moveX, current[1] + moveY
                    neighbor = (newRow, newCol)
                    if 0 <= newRow < len(self.matrix) and 0 <= newCol < len(self.matrix[0]):
                        if self.matrix[newRow][newCol]!= -1 and neighbor not in visited:
                            newGCost = cost + 1
                            fCost = cost + 1 + manhattan_distance(neighbor, self.end)
                            heapq.heappush(queue, (fCost, newGCost, neighbor, newPath))
        return None  # no path found
        