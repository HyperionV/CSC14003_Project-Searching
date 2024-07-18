from SearchAlgo.supportiveFunctions import manhattan_distance
class SearchAlgorithm:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.start = start
        self.end = end
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def create_path(self, parent):
        path = []
        current = self.end
        
        while True:
            path.append(current)
            if(next_node := parent.get(current)) is None:
                break
            next_node = parent[current]
            current = next_node
            
        path.reverse()
        
        if path[0] != self.start:  # If start node is not in the path, no path exists
            return None
    
        return path

    def Try(self):
        pass


    