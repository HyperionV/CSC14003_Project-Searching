import tkinter as tk
from tkinter import Canvas
import random
import copy
from SearchAlgo import UCS, AStar, BFS, GBFS, DFS

class Map:
    def __init__(self, file_name):
        self.time, self.fuel, self.mat, self.agent, self.goal, self.station = self.read_input(file_name)
        self.intrMap = copy.deepcopy(self.mat)
        self.initIntrMap()
        self.steps = self.level2(self.mat, self.time, self.agent['S'], self.goal['G'])
        # self.step3 = self.level3()
        # self.step4 = self.level4()
        
        self.colors = {
            0: "white",
            -1: "LightSkyBlue4",
            1: "SlateGray1",
            'S': "DarkSeaGreen2",
            'G': "RosyBrown1",
            'F': "light goldenrod yellow"
        }
        self.color_mapping = [[(1 if val > 0 else val) if isinstance(val, int) else val[0] for val in row] for row in self.mat]
        self.original_mat = [row[:] for row in self.mat]  
        self.path_color = "DarkSeaGreen2" 
        self.current_step = 0
        self.step4 = self.level4()

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
                        elif j[0] == 'F':
                            station.append((idx, idj, int(j[1:len(j)])))
                            mat[idx].append(j)
                        else:
                            mat[idx].append(int(j))
                    except:
                        print(f"\n\nError occured while reading data: ({idx}, {idj}) - \"{j}\"\n\n")
                        raise SystemExit
        # print('agent:', agent, len(agent))
        # print('goal:', goal, len(goal))
        return time, fuel, mat, agent, goal, station
    
    def level1(self, algorithm, adjacency_matrix, start_node, goal_node):
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

    def level2(self, mat, time, start, end):
        distance_matrix = [[[float('inf') for _ in range(self.time + 10)] for _ in range(len(mat[0]))] for _ in range(len(mat))]
        distance_matrix[start[0]][start[1]][0] = 0
        queue = [(start[0], start[1], 0)] 

        while queue:
            row, col, curr_time = queue.pop(0)
            cur_dis = distance_matrix[row][col][curr_time]

            if curr_time > time:
                continue
            if (row, col) == end:
                path = []
                tmp_time = curr_time
                while (row, col) != start:
                    path.append((row, col))
                    extra_time = 1
                    if isinstance(mat[row][col], int):
                        extra_time = mat[row][col] + 1
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if mat[nr][nc] == -1:
                            continue
                        prv_time = tmp_time - extra_time
                        # print(' prv:', prv_time, mat[nr][nc], '   ', nr, nc)
                        if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and distance_matrix[nr][nc][prv_time] < distance_matrix[row][col][tmp_time]:
                            row, col = nr, nc
                            tmp_time = prv_time
                            break
                path.append(start)
                # print('path:', path)
                return path[::-1]

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and mat[nr][nc] != -1:
                    cell = mat[nr][nc]
                    new_time = curr_time + (0 if cell == 0 or isinstance(cell, str) else cell) + 1
                    if cur_dis + 1 < distance_matrix[nr][nc][new_time]:
                        distance_matrix[nr][nc][new_time] = cur_dis + 1
                        queue.append((nr, nc, new_time))
        return []

    def level3(self):
        # print('lvl3')
        start = self.agent['S']
        end = self.goal['G']
        dis = [[[[1e9 for _ in range(self.fuel + 10)] for _ in range(self.time + 10)] for _ in range(len(self.mat[0]))] for _ in range(len(self.mat))]
        dis[start[0]][start[1]][0][self.fuel] = 0
        queue = []
        queue.append((start[0], start[1], 0, self.fuel))

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while bool(queue):
            row, col, cur_time, cur_fuel = queue.pop(0)
            cur_dis = dis[row][col][cur_time][cur_fuel]
            if cur_fuel < 0:
                continue
            if cur_time > self.time:
                continue

            if (row, col) == end:
                path = []
                tmp_fuel = cur_fuel
                tmp_time = cur_time
                while (row, col) != start:
                    path.append((row, col))
                    extra_time = 1
                    if isinstance(self.mat[row][col], int):
                        extra_time = self.mat[row][col] + 1
                    elif self.mat[row][col][0] == 'F':
                        extra_time = (int(self.mat[row][col][1:len(self.mat[row][col])])) + 1
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(self.mat) and 0 <= nc < len(self.mat[0]):
                            prv_time = tmp_time - extra_time
                            # No station
                            if dis[nr][nc][prv_time][tmp_fuel + 1] < dis[row][col][tmp_time][tmp_fuel]:
                                row, col = nr, nc
                                tmp_fuel = tmp_fuel + 1
                                tmp_time = prv_time
                                break
                            # With station (refuel)
                            elif tmp_fuel == self.fuel:
                                found_path = False
                                for pre_fuel in range(self.fuel):
                                    if dis[nr][nc][prv_time][pre_fuel] < dis[row][col][tmp_time][tmp_fuel]:
                                        found_path = True
                                        tmp_fuel = pre_fuel
                                        row, col = nr, nc
                                        tmp_time = prv_time
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
                    stay_time = max(stay_time, self.mat[next_row][next_col] + 1)
                total_time = cur_time + stay_time + refuel_time
                if cur_dis + 1 < dis[next_row][next_col][total_time][next_fuel]:
                    # time to next cell = current time + stay time (lvl 2) + refuel time (if at station)
                    queue.append((next_row, next_col, total_time, next_fuel))
                    dis[next_row][next_col][total_time][next_fuel] = cur_dis + 1
        return -1

    # for level 4
    def initIntrMap(self):
        for i in range(len(self.intrMap)):
            for j in range(len(self.intrMap[0])):
                if isinstance(self.intrMap[i][j], int):
                    if self.intrMap[i][j] != 0 and self.intrMap[i][j] != -1:
                        self.intrMap[i][j] = 0
                else:
                    if self.intrMap[i][j][0] != 'S':
                        self.intrMap[i][j] = 0
        return
    def revert(self, revList):
        for info in revList:
            i, j, cell = info
            self.intrMap[i][j] = cell
        return
    def findPath(self, start, end, fuel):
        # start = self.agent['S']
        # end = self.goal['G']
        dis = [[[[1e9 for _ in range(self.fuel + 10)] for _ in range(self.time + 10)] for _ in range(len(self.intrMap[0]))] for _ in range(len(self.intrMap))]
        dis[start[0]][start[1]][0][fuel] = 0
        queue = []
        queue.append((start[0], start[1], 0, fuel))
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        tmpWall = []
        for k in range(4):
            if start[0] + dx[k] < 0 or start[1] + dy[k] < 0 or start[0] + dx[k] >= len(self.intrMap) or start[1] + dy[k] >= len(self.intrMap[0]):
                continue
            if isinstance(self.intrMap[start[0] + dx[k]][start[1] + dy[k]], str):
                if self.intrMap[start[0] + dx[k]][start[1] + dy[k]][0] == 'S':
                    tmpWall.append((start[0] + dx[k], start[1] + dy[k], self.intrMap[start[0] + dx[k]][start[1] + dy[k]]))
                    self.intrMap[start[0] + dx[k]][start[1] + dy[k]] = -1

        while bool(queue):
            row, col, cur_time, cur_fuel = queue.pop(0)
            cur_dis = dis[row][col][cur_time][cur_fuel]
            if cur_fuel < 0:
                continue
            if cur_time > self.time:
                continue
            if (row, col) == end:
                path = []
                tmp_fuel = cur_fuel
                tmp_time = cur_time
                # print('    last_time:', tmp_time)
                while (row, col) != start:
                    path.append((row, col))
                    extra_time = 1
                    if isinstance(self.mat[row][col], int):
                        extra_time = self.mat[row][col] + 1
                    elif self.mat[row][col][0] == 'F':
                        extra_time = (int(self.mat[row][col][1:len(self.mat[row][col])])) + 1
                    # print('      extr:', extra_time, 'row, col:', row, col, tmp_time)
                    # if row == 6 and col == 1:
                    #     exit(0)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(self.intrMap) and 0 <= nc < len(self.intrMap[0]):
                            # No station
                            prv_time = tmp_time - extra_time
                            if dis[nr][nc][prv_time][tmp_fuel + 1] < dis[row][col][tmp_time][tmp_fuel]:
                                row, col = nr, nc
                                tmp_fuel = tmp_fuel + 1
                                tmp_time = prv_time
                                break
                            # With station (refuel)
                            elif tmp_fuel == self.fuel:
                                # print('         w/station')
                                found_path = False
                                for pre_fuel in range(self.fuel):
                                    if dis[nr][nc][prv_time][pre_fuel] < dis[row][col][tmp_time][tmp_fuel]:
                                        found_path = True
                                        tmp_fuel = pre_fuel
                                        row, col = nr, nc
                                        tmp_time = prv_time
                                        break
                                if found_path == True:
                                    break
                path.append(start)
                # print('4path:', path)
                self.revert(tmpWall)
                return path[::-1]
            
            for idx in range(4):
                next_row, next_col = row + dx[idx], col + dy[idx]
                if next_row < 0 or next_col < 0 or next_row >= len(self.intrMap) or next_col >= len(self.intrMap[0]):
                    continue
                if self.intrMap[next_row][next_col] == -1:
                    continue
                # print('    fuel:', cur_fuel)
                next_fuel = cur_fuel - 1
                refuel_time = 0
                stay_time = 1
                if isinstance(self.mat[next_row][next_col], str):
                    if self.mat[next_row][next_col][0] == 'F':
                        next_fuel = self.fuel
                        refuel_time = (int(self.mat[next_row][next_col][1:len(self.mat[next_row][next_col])]))
                else:
                    stay_time = max(stay_time, self.mat[next_row][next_col] + 1)
                total_time = cur_time + stay_time + refuel_time
                # if cur_time >= dis[next_row][next_col][next_fuel]:
                #     continue
                if cur_dis + 1 < dis[next_row][next_col][total_time][next_fuel]:
                    queue.append((next_row, next_col, total_time, next_fuel))
                    dis[next_row][next_col][total_time][next_fuel] = cur_time + 1
        self.revert(tmpWall)
        if self.isStation(start[0], start[1]):
            for k in range(4):
                nextRow = start[0] + dx[k]
                nextCol = start[1] + dy[k]
                if self.intrMap[nextRow][nextCol] == 0:
                    path = []
                    path.append(start)
                    path.append((nextRow, nextCol))
                    return path
        return -1
    def findPos(self, cell):
        for i in range(len(self.intrMap)):
            for j in range(len(self.intrMap[0])):
                if self.intrMap[i][j] == cell:
                    return (i, j)
        return -1
    def findGoal(self, cell):
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                if self.mat[i][j] == cell:
                    return (i, j)
        return -1
    def isGoal(self, idx): # S_i reached G_i
        start, goal = 'S', 'G'
        if idx > 0:
            start = str('S' + str(idx))
            goal = str('G' + str(idx))
        for i in range(len(self.intrMap)):
            for j in range(len(self.intrMap[0])):
                if self.intrMap[i][j] == start and self.mat[i][j] == goal:
                    return True
        return False
    def isStation(self, row, col):
        if isinstance(self.mat[row][col], str):
            if self.mat[row][col][0] == 'F':
                return True
        return False
    def goToCell(self, start, goal):
        self.intrMap[start[0]][start[1]], self.intrMap[goal[0]][goal[1]] = self.intrMap[goal[0]][goal[1]], self.intrMap[start[0]][start[1]]
        return
    def generateNewGoal(self, idx):
        cellList = []
        goalLabel = 'G' + str(idx)
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if self.mat[i][j] == 0:
                    cellList.append((i, j))
                if self.mat[i][j] == goalLabel:
                    self.mat[i][j] = 0
        num = random.randint(0, len(cellList) - 1)
        # print('num:', num, cellList[num])
        self.mat[cellList[num][0]][cellList[num][1]] = goalLabel
        return
    def level4(self):
        # wall block goal
        if self.level3() == -1:
            return -1
        path = []
        fuel = [self.fuel for i in range(len(self.agent) + 5)]
        cnt = 0
        while True:
            cnt = cnt + 1
            if fuel[0] == 0:
                path = -1
                break
            if self.isGoal(0):
                break
            path.append((self.agent['S'][0], self.agent['S'][1]))
            for idx in range(len(self.agent)):
                start, goal = (-1, -1), (-1, -1)
                if idx == 0:
                    start = self.findPos('S')
                    goal = self.findGoal('G')
                else:
                    start = self.findPos(str('S' + str(idx)))
                    goal = self.findGoal(str('G' + str(idx)))
                if self.isGoal(idx):
                    continue
                curPath = self.findPath(start, goal, fuel[idx])
                if curPath == -1:
                    continue
                self.goToCell(curPath[0], curPath[1])
                # print('start, goal, fuel:', start, goal, fuel[idx], '  ', idx)
                fuel[idx] = fuel[idx] - 1
                if self.isStation(curPath[1][0], curPath[1][1]):
                    fuel[idx] = self.fuel
                if idx == 0:
                    path.append(curPath[1])
                if self.isGoal(idx):
                    if idx == 0:
                        break
                    self.generateNewGoal(idx)
        #         for row in self.intrMap:
        #             print(row)
        return path

    def create_grid(self, canvas, rows, cols, cell_size):
        for i in range(rows):
            for j in range(cols):
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill="white")

    def draw_map(self, canvas, mat, cell_size):        
        for i, row in enumerate(mat):
            for j, val in enumerate(row):
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=self.colors[self.color_mapping[i][j]])
                if val not in [0, -1]:
                    canvas.create_text(j * cell_size + cell_size/2, i * cell_size + cell_size/2, text=val, fill="black", font=("Helvetica", cell_size//4))

    def next_step(self, canvas, mat, cell_size, steps):
        if self.current_step < len(steps):
            canvas.delete("all")
            self.create_grid(canvas, len(mat), len(mat[0]), cell_size)
            
            if self.current_step > 0:
                prev_row, prev_col = steps[self.current_step - 1]
                mat[prev_row][prev_col] = self.original_mat[prev_row][prev_col]
            
            row, col = steps[self.current_step]
            mat[row][col] = 'S'
            self.color_mapping[row][col] = 'S'
            
            self.draw_map(canvas, mat, cell_size)
            self.current_step += 1

    # def autorun():
    #     root.after(1000, self.next_step, canvas, self.mat, cell_size, self.steps)

    def run(self):
        root = tk.Tk()
        root.title("GUI")

        window_width = 800
        window_height = 600

        rows = len(self.mat)
        cols = len(self.mat[0]) if rows > 0 else 0

        cell_size = min(window_width // cols, window_height // rows)

        canvas = Canvas(root, width=cols * cell_size, height=rows * cell_size)
        canvas.pack(fill="both", expand=True) 

        button_frame = tk.Frame(root)
        button_frame.pack(fill="x")

        autorun_button = tk.Button(button_frame, text="Autorun", command=lambda: (root.after(1000, self.next_step, canvas, self.mat, cell_size, self.steps) for _ in self.steps), width = window_width // 60,height=cell_size // 25, font=("Helvetica", cell_size // 4))
        autorun_button.pack(side=tk.LEFT)

        next_step_button = tk.Button(button_frame, text="Update", command=lambda: self.next_step(canvas, self.mat, cell_size, self.steps), width= window_width//20,height=cell_size // 25, font=("Helvetica", cell_size // 4))
        next_step_button.pack(side=tk.LEFT)

        self.create_grid(canvas, rows, cols, cell_size)
        self.draw_map(canvas, self.mat, cell_size)
        root.mainloop()


if __name__ == '__main__':
    Map = Map('input.txt')
    Map.run()