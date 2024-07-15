import tkinter as tk
from tkinter import Canvas

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
            color = color_mapping.get(val if isinstance(val, int) else val[0], "white")
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
            if isinstance(val, str):
                canvas.create_text(j * cell_size + cell_size/2, i * cell_size + cell_size/2, text=val, fill="black", font=("Helvetica", cell_size//4))

def update_matrix(mat):
    pass

def next_step(canvas, mat, cell_size):
    canvas.delete("all")
    mat = update_matrix(mat)
    create_grid(canvas, len(mat), len(mat[0]), cell_size)
    draw_map(canvas, mat, cell_size)

def autorun(canvas, mat, cell_size):
    # while True:
    #     next_step(canvas, mat, cell_size)
    #     canvas.update()
    #     canvas.after(1000)  
    pass

def main(fileName):
    time, fuel, mat, agent, goal, station = readInput(fileName)
    print(time, fuel, mat, agent, goal, station)

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

    next_step_button = tk.Button(button_frame, text="Update", command=lambda: next_step(canvas, mat, cell_size), width= window_width//20 ,height=cell_size // 25, font=("Helvetica", cell_size // 4))
    next_step_button.pack(side=tk.LEFT)

    create_grid(canvas, rows, cols, cell_size)
    draw_map(canvas, mat, cell_size)

    root.mainloop()

if __name__ == '__main__':
    main('input.txt')