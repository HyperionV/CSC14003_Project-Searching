def readInput(fileName):
    time = 0
    fuel = 0
    agent = []
    goal = []
    station = []
    mat= []
    iFile = open(fileName, 'r')
    _, _, time, fuel = [int(i) for i in iFile.readline().split(' ')]
    for idx, i in enumerate(iFile):
        if any(i) == any(['S', 'G,', 'F']):
            mat.append([])
            for idj, j in enumerate(i.split(' ')):
                if j.__contains__('S'):
                    agent.append((j, (idx, idj)))
                if j.__contains__('G'):
                    goal.append((j, (idx, idj)))
                if j.__contains__('F'):
                    station.append(('F', (idx, idj)))
                mat[idx].append(int(j) if j.isnumeric() or j.__contains__('-') else j)
        else:
            mat.append([int(k) for k in i.split(' ')])
    return time, fuel, mat, agent, goal, station

if __name__ == '__main__':
    time, fuel, mat, agent, goal, station = readInput('input.txt')
    print(time, fuel, mat, agent, goal, station)