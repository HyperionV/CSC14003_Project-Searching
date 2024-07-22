import tkinter as tk
from tkinter import Canvas
import heapq

class Map:
    def __init__(self, file_name):
        self.time, self.fuel, self.mat, self.agent, self.goal, self.station = self.read_input(file_name)
        self.steps = self.level2(self.mat, self.time, self.agent['S'], self.goal['G'])
        self.step3 = self.level3()

    def read_input(self, file_name):
        time = 0
        fuel = 0
        agent = {}
        goal = {}
        station = []
        mat = []
        map_dict = {
            'S': agent,
            'G': goal,
        }
        with open(file_name, 'r') as i_file:
            _, _, time, fuel = [int(i) for i in i_file.readline().split(' ')]
            for idx, i in enumerate(i_file):
                i = i.strip()
                mat.append([])
                for idj, j in enumerate(i.split(' ')):
                    try:
                        if j[0] in ['S', 'G']:
                            map_dict[j[0]][j] = (idx, idj)
                            mat[idx].append(j)
                        if j[0] == 'F':
                            station.append(j)
                            mat[idx].append(j)
                        else:
                            mat[idx].append(int(j))
                    except:
                        print(f"\n\nError occured while reading data: ({idx}, {idj}) - \"{j}\"\n\n")
                        break
        return time, fuel, mat, agent, goal, station

    def level2(self, mat, time, start, end):
        distance_matrix = [[float('inf') for _ in range(len(mat[0]))] for _ in range(len(mat))]
        distance_matrix[start[0]][start[1]] = 0
        queue = [(start[0], start[1], 0)] 

        while queue:
            row, col, curr_time = queue.pop(0)

            if curr_time > time:
                continue
            if (row, col) == end:
                path = []
                while (row, col) != start:
                    path.append((row, col))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and distance_matrix[nr][nc] < distance_matrix[row][col]:
                            row, col = nr, nc
                            break
                return path[::-1]

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and mat[nr][nc] != -1:
                    cell = mat[nr][nc]
                    new_time = curr_time + (1 if cell == 0 or isinstance(cell, str) else cell)

                    if new_time < distance_matrix[nr][nc]:
                        distance_matrix[nr][nc] = new_time
                        queue.append((nr, nc, new_time))
        return []

    def level3(self):
        start = self.agent['S']
        end = self.goal['G']
        dis = [[[1e9 for _ in range(self.fuel + 10)]for _ in range(len(self.mat[0]))] for _ in range(len(self.mat))]
        dis[start[0]][start[1]][self.fuel] = 0
        queue = []
        queue.append((start[0], start[1], 0, self.fuel))

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while bool(queue):
            row, col, cur_time, cur_fuel = queue.pop(0)
            if cur_fuel < 0:
                continue
            if cur_time > self.time:
                continue

            # Trace
            if (row, col) == end:
                path = []
                tmp_fuel = cur_fuel
                while (row, col) != start:
                    path.append((row, col))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(self.mat) and 0 <= nc < len(self.mat[0]):
                            # No station
                            if dis[nr][nc][tmp_fuel + 1] < dis[row][col][tmp_fuel]:
                                row, col = nr, nc
                                tmp_fuel = tmp_fuel + 1
                                break
                            # With station (refuel)
                            elif tmp_fuel == self.fuel:
                                found_path = False
                                for pre_fuel in range(self.fuel):
                                    if dis[nr][nc][pre_fuel] < dis[row][col][tmp_fuel]:
                                        found_path = True
                                        tmp_fuel = pre_fuel
                                        row, col = nr, nc
                                        break
                                if found_path == True:
                                    break

                path.append(start)
                return path[::-1]
            
            for idx in range(4):
                next_row, next_col = row + dx[idx], col + dy[idx]
                if next_row < 0 or next_col < 0 or next_row >= len(self.mat) or next_col >= len(self.mat[0]):
                    continue
                if self.mat[next_row][next_col] == -1:
                    continue
                next_fuel = cur_fuel - 1
                refuel_time = 0
                stay_time = 1
                if isinstance(self.mat[next_row][next_col], str):
                    if self.mat[next_row][next_col][0] == 'F':
                        next_fuel = self.fuel
                        refuel_time = (int(self.mat[next_row][next_col][1:len(self.mat[next_row][next_col])]))
                else:
                    stay_time = max(stay_time, self.mat[next_row][next_col])
                if cur_time >= dis[next_row][next_col][next_fuel]:
                    continue
                if cur_time + 1 < dis[next_row][next_col][next_fuel]:
                    # time to next cell = current time + stay time (lvl 2) + refuel time (if at station)
                    queue.append((next_row, next_col, cur_time + stay_time + refuel_time, next_fuel))
                    dis[next_row][next_col][next_fuel] = cur_time + 1
        return []

    def create_grid(self, canvas, rows, cols, cell_size):
        for i in range(rows):
            for j in range(cols):
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill="white")

    def draw_map(self, canvas, mat, cell_size):
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

    def autorun(self, canvas, mat, cell_size):
        pass

    def next_step(self, canvas, mat, cell_size, steps):
        if not steps:
            return
        canvas.delete("all")
        self.create_grid(canvas, len(mat), len(mat[0]), cell_size)
        row, col = steps.pop(0)
        mat[row][col] = 'S'
        self.draw_map(canvas, mat, cell_size)

    def run(self):
        root = tk.Tk()
        root.title("City Map GUI")

        window_width = 800
        window_height = 600

        rows = len(self.mat)
        cols = len(self.mat[0]) if rows > 0 else 0

        cell_size = min(window_width // cols, window_height // rows)

        canvas = Canvas(root, width=cols * cell_size, height=rows * cell_size)
        canvas.pack(fill="both", expand=True) 

        button_frame = tk.Frame(root)
        button_frame.pack(fill="x")

        autorun_button = tk.Button(button_frame, text="Autorun", command=lambda: self.autorun(canvas, self.mat, cell_size), width = window_width // 60,height=cell_size // 25, font=("Helvetica", cell_size // 4))
        autorun_button.pack(side=tk.LEFT)

        next_step_button = tk.Button(button_frame, text="Update", command=lambda: self.next_step(canvas, self.mat, cell_size, self.steps), width= window_width//20,height=cell_size // 25, font=("Helvetica", cell_size // 4))
        next_step_button.pack(side=tk.LEFT)

        self.create_grid(canvas, rows, cols, cell_size)
        self.draw_map(canvas, self.mat, cell_size)

        root.mainloop()

if __name__ == '__main__':
    city_map = Map('input.txt')
    print(city_map.mat)
    city_map.run()