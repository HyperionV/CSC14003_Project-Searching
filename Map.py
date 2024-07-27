import random
import copy
from SearchAlgo import UCS, AStar, BFS, GBFS, DFS
from tkinter import PhotoImage

class Map:
    def __init__(self, canvas):
        self.path = None
        self.goalList = None
        self.isForward = True
        self.canvas = canvas
        self.colors = {
            0: "white",
            -1: "LightSkyBlue4",
            1: "SlateGray1",
            'S': "DarkSeaGreen2",
            'G': "RosyBrown1",
            'F': "light goldenrod yellow"
        }
        self.path_color = "DarkSeaGreen2" 

        
    def getPath(self, level, algorithm_name = None):
        if(level == "Level 1"):
            self.path =  self.level1(algorithm_name)
        elif(level == "Level 2"):
            self.path =  self.level2()
        elif(level == "Level 3"):
            self.path =  self.level3()
        elif(level == "Level 4"):
            self.path, self.goalList =  self.level4()
            return self.path, self.goalList
        return self.path
        
    def load(self, path):
        self.path = None
        self.goalList = None
        self.isForward = True
        self.getMaze(path)
        self.color_mapping = [[(1 if val > 0 else val) if isinstance(val, int) else val[0] for val in row] for row in self.mat]
        self.intrMap = copy.deepcopy(self.mat)
        self.initIntrMap()
        self.original_mat = [row[:] for row in self.mat]  
        self.current_step = 0
        self.drawMap()

    
    def getMaze(self, file_name):
        self.time, self.fuel, self.mat, self.agent, self.goal, self.station = self.readInput(file_name)

    def readInput(self, file_name):
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
    
    def level1(self, algorithm):
        adjacency_matrix = self.mat
        start_node = self.agent['S']
        goal_node = self.goal['G']
        algorithms = {
            "Depth First Search": DFS.DFS,
            "Uniform Cost Search": UCS.UCS,
            "A*": AStar.AStar,
            "Breadth First Search": BFS.BFS,
            "Greedy Best First Search": GBFS.GBFS
        }
        try:
            return algorithms[algorithm](adjacency_matrix, start_node, goal_node).Try()
        except:
            raise ValueError("Invalid algorithm name")

    def level2(self):
        mat = self.mat
        time = self.time
        start = self.agent['S']
        end = self.goal['G']
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
                        prv_time = tmp_time - extra_time
                        if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and distance_matrix[nr][nc][prv_time] < distance_matrix[row][col][tmp_time]:                          
                            if mat[nr][nc] == -1:
                                continue
                            row, col = nr, nc
                            tmp_time = prv_time
                            break
                return path[::-1]

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(mat) and 0 <= nc < len(mat[0]) and mat[nr][nc] != -1:
                    cell = mat[nr][nc]
                    new_time = curr_time + (0 if cell == 0 or isinstance(cell, str) else cell) + 1
                    if cur_dis + 1 < distance_matrix[nr][nc][new_time]:
                        distance_matrix[nr][nc][new_time] = cur_dis + 1
                        queue.append((nr, nc, new_time))
        return -1

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
        dis = [[[[1e9 for _ in range(self.fuel + 10)] for _ in range(self.time + 10)] for _ in range(len(self.intrMap[0]))] for _ in range(len(self.intrMap))]
        # print('fuel:', fuel, self.fuel)
        dis[start[0]][start[1]][0][fuel] = 0
        queue = []
        queue.append((start[0], start[1], 0, fuel))
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        tmpWall = []
        for k in range(4):
            next_row = start[0] + dx[k]
            next_col = start[1] + dy[k]
            if next_row < 0 or next_col < 0 or next_row >= len(self.intrMap) or next_col >= len(self.intrMap[0]):
                continue
            if isinstance(self.intrMap[next_row][next_col], str):
                if self.intrMap[next_row][next_col][0] == 'S':
                    tmpWall.append((next_row, next_col, self.intrMap[next_row][next_col]))
                    self.intrMap[next_row][next_col] = -1
        # for row in self.intrMap:
        #     print(row)
        # print('start:', start)
        # print('\n')
        while bool(queue):
            row, col, cur_time, cur_fuel = queue.pop(0)
            cur_dis = dis[row][col][cur_time][cur_fuel]
            if cur_fuel < 0:
                continue
            if cur_time > self.time:
                continue
            # print('expand:', row, col, '   time:', cur_time)
            if (row, col) == end:
                path = []
                tmp_fuel = cur_fuel
                tmp_time = cur_time
                # print('    last_time:', tmp_time)
                cnt = 0
                while (row, col) != start:
                    cnt += 1
                    path.append((row, col))
                    extra_time = 1
                    if isinstance(self.mat[row][col], int):
                        extra_time = self.mat[row][col] + 1
                    elif self.mat[row][col][0] == 'F':
                        extra_time = (int(self.mat[row][col][1:len(self.mat[row][col])])) + 1
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(self.intrMap) and 0 <= nc < len(self.intrMap[0]):
                            # No station
                            prv_time = tmp_time - extra_time
                            if self.mat[nr][nc] == -1:
                                continue
                            # print('   nr, nc:', nr, nc, self.mat[nr][nc], prv_time, tmp_fuel, dis[nr][nc][prv_time][tmp_fuel + 1])
                            if dis[nr][nc][prv_time][tmp_fuel + 1] < dis[row][col][tmp_time][tmp_fuel]:
                                # print('    case1:', dis[nr][nc][prv_time][tmp_fuel + 1], dis[row][col][tmp_time][tmp_fuel], '   ', nr, nc, self.mat[nr][nc])
                                row, col = nr, nc
                                tmp_fuel = tmp_fuel + 1
                                tmp_time = prv_time
                                break
                            elif tmp_fuel == self.fuel:
                                # print('    case2')
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
                self.revert(tmpWall)
                return path[::-1]
            
            for idx in range(4):
                next_row, next_col = row + dx[idx], col + dy[idx]
                if next_row < 0 or next_col < 0 or next_row >= len(self.intrMap) or next_col >= len(self.intrMap[0]):
                    continue
                if self.intrMap[next_row][next_col] == -1:
                    # print('  -1', next_row, next_col, self.intrMap[next_row][next_col])
                    continue
                # print('  consider:', next_row, next_col)
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
                if total_time > self.time: 
                    continue
                if cur_dis + 1 < dis[next_row][next_col][total_time][next_fuel]:
                    queue.append((next_row, next_col, total_time, next_fuel))
                    dis[next_row][next_col][total_time][next_fuel] = cur_time + 1
                    # print('  reach:', next_row, next_col, total_time, next_fuel)
                    # if next_row == 11 and next_col == 1:
                    #     print('dis:', total_time, next_fuel, dis[next_row][next_col][total_time][next_fuel])
        
        # if self.isStation(start[0], start[1]):
        validCell = []
        for k in range(4):
            nextRow = start[0] + dx[k]
            nextCol = start[1] + dy[k]
            if nextRow >= 0 and nextRow < len(self.mat) and nextCol >= 0 and nextCol < len(self.mat[0]):
                if self.intrMap[nextRow][nextCol] == -1:
                    continue
                if isinstance(self.mat[nextRow][nextCol], int):
                    validCell.append((nextRow, nextCol))
        # num = random.randint(0, len(validCell) - 1)
        self.revert(tmpWall)
        if len(validCell) > 0:
            path = []
            path.append(start)
            path.append(validCell[0])
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
    
    def isGoal(self, idx):
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
        self.mat[cellList[num][0]][cellList[num][1]] = goalLabel
        return
    
    def level4(self):
        if self.level3() == -1:
            return (-1, -1)
        path = [[] for _ in range(len(self.agent))]
        fuel = [self.fuel for i in range(len(self.agent) + 5)]
        goalList = []
        for i in range(len(self.agent)):
            pos = self.agent['S']
            if i > 0:
                pos = self.agent['S' + str(i)]
            path[i].append(pos)
        cnt = 0
        goalIdx = 0
        while True:
            # print('cnt:', cnt)
            for idx in range(len(self.agent)):
                print(path[idx][len(path[idx]) - 1], ' ', end = '')
            print('\n')

            if fuel[0] == 0:
                path, goalList = -1, -1
                break
            if self.isGoal(0):
                break
            # print('grid:')
            # for row in self.intrMap:
            #     print(row)
            for idx in range(len(self.agent)):
                # print('\n idx:', idx)

                cnt = cnt + 1
                start, goal = (-1, -1), (-1, -1)
                if idx == 0:
                    start = self.findPos('S')
                    goal = self.findGoal('G')
                else:
                    start = self.findPos(str('S' + str(idx)))
                    goal = self.findGoal(str('G' + str(idx)))
                if fuel[idx] == 0:
                    path[idx].append(path[idx][len(path[idx]) - 1])
                    continue
                # print('idx:', idx)
                curPath = self.findPath(start, goal, fuel[idx])
                if curPath == -1:
                    path[idx].append(path[idx][len(path[idx]) - 1])
                    
                    goalList.append([])
                    for j in range(len(self.agent)):
                        if j > 0:
                            goalList[goalIdx].append((j, self.findGoal('G' + str(j))))
                        else:
                            goalList[goalIdx].append((j, self.findGoal('G')))
                    goalIdx = goalIdx + 1
                    continue
                self.goToCell(curPath[0], curPath[1])
                # print('start, goal, fuel:', start, goal, fuel[idx], '  ', idx)
                # print(' dec ', idx)
                fuel[idx] = fuel[idx] - 1
                if self.isStation(curPath[1][0], curPath[1][1]):
                    fuel[idx] = self.fuel
                path[idx].append(curPath[1])
                if self.isGoal(idx):
                    if idx == 0:
                        break
                    self.generateNewGoal(idx)
                goalList.append([])
                for j in range(len(self.agent)):
                    if j > 0:
                        goalList[goalIdx].append((j, self.findGoal('G' + str(j))))
                    else:
                        goalList[goalIdx].append((j, self.findGoal('G')))
                goalIdx = goalIdx + 1
        #         for row in self.intrMap:
        #             print(row)
        # print('path:', path)
        for i in range(len(path)):
            print('path:', i, ' ' , len(path[i]))
            for j in range(len(path[i])):
                print(path[i][j], end = ' ')
        # for lists in goalList:
        #     print(lists)

        return (path, goalList)

    def create_grid(self, canvas, rows, cols, cell_size):
        for i in range(rows):
            for j in range(cols):
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill="white")

    def createGrid(self):
        rows, cols = len(self.mat), len(self.mat[0])
        topMargin = (780 - rows * cell_size) / 2
        leftMargin = (900 - cols * cell_size) / 2
        cell_size = min(900 // cols, 800 // rows)
        for i in range(rows):
            for j in range(cols):
                self.canvas.create_rectangle(j * cell_size + leftMargin, i * cell_size + topMargin, (j + 1) * cell_size + leftMargin, (i + 1) * cell_size  + topMargin, fill="white")

    def drawMap(self):
        self.canvas.delete("all")
        rows, cols = len(self.mat), len(self.mat[0])
        cell_size = min(900 // cols, 800 // rows)
        nrow = len(self.mat)
        ncol = len(self.mat[0])
        topMargin = (780 - nrow * cell_size) / 2
        leftMargin = (900 - ncol * cell_size) / 2
        for i, row in enumerate(self.mat):
            for j, val in enumerate(row):
                color = self.colors.get(val if isinstance(val, int) else val[0], "SlateGray1")
                self.canvas.create_rectangle(j * cell_size + leftMargin, i * cell_size + topMargin, (j + 1) * cell_size + leftMargin, (i + 1) * cell_size + topMargin, fill=color)
                if val not in [0, -1]:
                    self.canvas.create_text(j * cell_size + cell_size/2 + leftMargin, i * cell_size + cell_size/2 + topMargin, text=val, fill="black", font=("Helvetica", cell_size//4))

    def nextStep(self):
        if self.current_step < len(self.path):
            self.canvas.delete("all")
            if(not self.isForward):
                
                row, col = self.path[self.current_step + 1]
                self.mat[row][col] = 'S'
                self.color_mapping[row][col] = 'S'
                self.current_step += 2
                self.isForward = True
            else:   
                    row, col = self.path[self.current_step]
                    self.mat[row][col] = 'S'
                    self.color_mapping[row][col] = 'S'
                    self.current_step += 1
            self.drawMap()


    def previousStep(self):
        if self.current_step >= 0:
            self.canvas.delete("all")
            if(self.isForward):
                row, col = self.path[self.current_step - 1]
                self.mat[row][col] = self.original_mat[row][col]
                self.color_mapping[row][col] = self.mat[row][col]
                self.current_step -= 2
                self.isForward = False
                
            else:
                    row, col = self.path[self.current_step]
                    self.mat[row][col] = self.original_mat[row][col]
                    self.color_mapping[row][col] = self.mat[row][col]
                    self.current_step -= 1
            self.drawMap()
    
    def loadMatrixState(self, curStep):
        print('curStep:', curStep)
        total_steps = 0
        for i in range(len(self.path)):
            total_steps += len(self.path[i])
        if(curStep >= 0 and curStep <= total_steps):
            for i in range(len(self.mat)):
                for j in range(len(self.mat[0])):
                    # check if cell not start or goal
                    if 'S' not in str(self.original_mat[i][j]) and 'G' not in str(self.original_mat[i][j]):
                        self.mat[i][j] = self.original_mat[i][j]
                    else:
                        self.mat[i][j] = 0

            for i in range (0, curStep):
                S_index = int(i / len(self.path))
                S_turn = i % len(self.path)
                # print('S_index:', S_index, '  S_turn:', S_turn, 'len: ', len(self.path[S_turn]))

                if(S_turn == 0):
                    self.mat[self.path[S_turn][S_index][0]][self.path[S_turn][S_index][1]] = 'S' 
                else:
                    self.mat[self.path[S_turn][S_index][0]][self.path[S_turn][S_index][1]] = 'S' + str(S_turn)
            currStep = min(len(self.goalList) + 5, curStep)
            currStep -= 6
            if(currStep < 0):
                currStep = 0
            for j in range(len(self.goalList[0])):
                goal = self.goalList[currStep][j][1]
                if(j == 0):
                    self.mat[goal[0]][goal[1]] = 'G'
                else:
                    self.mat[goal[0]][goal[1]] = 'G' + str(j)
        return

        
    def nextSteplvl4(self, toalSteps):
        if(self.current_step == 0):
            self.current_step = 6
        if self.current_step <= toalSteps:
            self.canvas.delete("all")
            if(not self.isForward):
                self.loadMatrixState(self.current_step + 2)
                self.current_step += 2
                self.isForward = True
            else:
                self.loadMatrixState(self.current_step)
            self.current_step += 1
            self.drawMap()

    def previousSteplvl4(self):
        if self.current_step >= 5:
            self.canvas.delete("all")
            if(self.isForward):
                self.loadMatrixState(self.current_step - 2)
                self.current_step -= 2
                self.isForward = False
            else:
                self.loadMatrixState(self.current_step)
            self.current_step -= 1
            self.drawMap()

    def autoRun(self, speed):
        if(self.current_step >= len(self.path) or self.path is None):
            return
        self.nextStep()
        self.canvas.after(speed, self.autoRun, speed)
    
    def autoRunlvl4(self, speed, totalSteps):
        if(self.current_step > totalSteps or self.path is None):
            return
        self.nextSteplvl4(totalSteps)
        self.canvas.after(speed, self.autoRunlvl4, speed, totalSteps)

    def getCurrentStep(self):
        return self.current_step
