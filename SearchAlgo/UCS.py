import heapq
from SearchAlgo.SearchAlgorithm import SearchAlgorithm


class UCS(SearchAlgorithm):
    def __init__(self, matrix, start, end):
        super().__init__(matrix, start, end)

    def Try(self):
        queue = [(0, self.start, [])]  # priority queue with cost, node, and path
        visited = set()
        while queue:
            (cost, current, path) = heapq.heappop(queue)
            if current not in visited:
                visited.add(current)
                newPath = path + [current]

                if current == self.end:
                    return newPath
                
                for moveX, moveY in self.directions:
                    newRow, newCol = current[0] + moveX, current[1] + moveY
                    neighbor = (newRow, newCol)
                    if 0 <= newRow < len(self.matrix) and 0 <= newCol < len(self.matrix[0]):
                        if self.matrix[newRow][newCol] != -1 and neighbor not in visited:
                            heapq.heappush(queue, (cost + 1, neighbor, newPath))
        return None # no path found