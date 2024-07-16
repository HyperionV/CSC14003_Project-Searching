import tkinter as tk
from tkinter import Canvas
from SearchAlgo.supportiveFunctions import *
from SearchAlgo import DFS, UCS, BFS, AStar, GBFS


def readInput(fileName):
    time = 0
    fuel = 0
    agent = {}
    goal = {}
    station = {}
    mat= []
    mapDict = {
        'S': agent,
        'G': goal,
        'F': station
    }
    iFile = open(fileName, 'r')

    _, _, time, fuel = [int(i) for i in iFile.readline().split(' ')]
    for idx, i in enumerate(iFile):
        i = i.strip()
        mat.append([])
        for idj, j in enumerate(i.split(' ')):
            try:
                if j[0] in ['S', 'G', 'F']:
                    mapDict[j[0]][j] = (idx, idj)
                    mat[idx].append(j)
                else:
                        mat[idx].append(int(j))
            except:
                print(f"\n\nError occured while reading data: ({idx}, {idj}) - \"{j}\"\n\n")
                break
    return time, fuel, mat, agent, goal, station

def level1(algorithm, adjacency_matrix, start_node, goal_node):
    if algorithm == "DFS":
        search_algo = DFS.DFS(adjacency_matrix, start_node, goal_node)
    elif algorithm == "UCS":
        search_algo = UCS.UCS(adjacency_matrix, start_node, goal_node)
    elif algorithm == "AStar":
        search_algo = AStar.AStar(adjacency_matrix, start_node, goal_node)
    elif algorithm == "BFS":
        search_algo = BFS.BFS(adjacency_matrix, start_node, goal_node)
    elif algorithm == "GBFS":
        search_algo = GBFS.GBFS(adjacency_matrix, start_node, goal_node)
    else:
        raise ValueError("Invalid algorithm name")
    
    return search_algo.Try()

def level2(mat, time, start, end):
    distance_matrix = [[float('inf') for _ in range(len(mat[0]))] for _ in range(len(mat))]
    distance_matrix[start[0]][start[1]] = 0
    queue = [(start[0], start[1], 0)]  # (row, col, time)

    while queue:
        row, col, curr_time = queue.pop(0)
        if curr_time > time:
            continue
        if (row, col) == end:
            path = []
            while (row, col)!= start:
                path.append((row, col))
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and distance_matrix[nr][nc] < distance_matrix[row][col]:
                        row, col = nr, nc
                        break
            path.append(start)
            return path[::-1]

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and mat[nr][nc]!= -1:
                new_time = curr_time + 1

                if new_time < distance_matrix[nr][nc]:
                    distance_matrix[nr][nc] = new_time
                    queue.append((nr, nc, new_time))
    return []

def create_grid(canvas, rows, cols, cell_size):
    for i in range(rows):
        for j in range(cols):
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill="white")

def draw_map(canvas, mat, cell_size):
    color_mapping = {
        0: "white",
        -1: "LightSkyBlue4",
        'S': "DarkSeaGreen2",
        'G': "RosyBrown1",
        'F': "light goldenrod yellow"
    }
    
    for i, row in enumerate(mat):
        for j, val in enumerate(row):
            color = color_mapping.get(val if isinstance(val, int) else val[0], "SlateGray1")
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
            if val not in [0, -1]:
                canvas.create_text(j * cell_size + cell_size/2, i * cell_size + cell_size/2, text=val, fill="black", font=("Helvetica", cell_size//4))

def update_matrix(mat):
    pass

def autorun(canvas, mat, cell_size):
    # while True:
    #     next_step(canvas, mat, cell_size)
    #     canvas.update()
    #     canvas.after(1000)  
    pass    

def next_step(canvas, mat, cell_size, path):
    if not path:
        return
    print(path)
    draw_paths(canvas, path, cell_size)
    

def draw_paths(canvas, path, cell_size):
    color = 'green'
    for i in range(len(path) - 1):
        y1, x1 = path[i]
        y2, x2 = path[i + 1]
        canvas.create_line(
            (x1 + 0.5) * cell_size, (y1 + 0.5) * cell_size,
            (x2 + 0.5) * cell_size, (y2 + 0.5) * cell_size,
            fill=color, width=3
            )
        
def main(fileName):
    time, fuel, mat, agent, goal, station = readInput(fileName)
    steps = level1("AStar", mat, agent['S'], goal['G'])

    root = tk.Tk()
    root.title("City Map GUI")

    window_width = 800
    window_height = 600

    rows = len(mat)
    cols = len(mat[0]) if rows > 0 else 0

    cell_size = min(window_width // cols, window_height // rows)

    canvas = Canvas(root, width=cols * cell_size, height=rows * cell_size)
    canvas.pack(fill="both", expand=True) 

    button_frame = tk.Frame(root)
    button_frame.pack(fill="x")

    autorun_button = tk.Button(button_frame, text="Autorun", command=lambda: autorun(canvas, mat, cell_size), width = window_width // 60,height=cell_size // 25, font=("Helvetica", cell_size // 4))
    autorun_button.pack(side=tk.LEFT)

    next_step_button = tk.Button(button_frame, text="Update", command=lambda: next_step(canvas, mat, cell_size, steps), width= window_width//20 ,height=cell_size // 25, font=("Helvetica", cell_size // 4))
    next_step_button.pack(side=tk.LEFT)

    create_grid(canvas, rows, cols, cell_size)
    draw_map(canvas, mat, cell_size)

    root.mainloop()



if __name__ == '__main__':
    main('input.txt')