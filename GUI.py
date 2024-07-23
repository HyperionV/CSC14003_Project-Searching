from collections import defaultdict
from pathlib import Path
from tkinter import *
from tkinter import ttk



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

class GUI:
    # constructor
    def __init__(self):
        self.window = Tk()
        self.window.title("PathFinder")
        self.window.geometry("1200x850")
        self.window.iconbitmap(self.relative_to_assets("icon2.ico"))
        self.window.configure(bg = "#171435")
        self.init()
        self.window.resizable(False, False)
        self.window.mainloop()
        


    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def read_input(self, file_name):
            time = 0
            fuel = 0
            agent = {}
            goal = {}
            station = {}
            mat = []
            map_dict = {
                'S': agent,
                'G': goal,
                'F': station
            }
            # check if can't open file
            try:
                with open(file_name, 'r') as i_file:
                    _, _, time, fuel = [int(i) for i in i_file.readline().split(' ')]
                    for idx, i in enumerate(i_file):
                        i = i.strip()
                        mat.append([])
                        for idj, j in enumerate(i.split(' ')):
                            try:
                                if j[0] in ['S', 'G', 'F']:
                                    map_dict[j[0]][j] = (idx, idj)
                                    mat[idx].append(j)
                                else:
                                    mat[idx].append(int(j))
                            except:
                                print(f"\n\nError occured while reading data: ({idx}, {idj}) - \"{j}\"\n\n")
                                return None, None, None, None, None, None
                                # break
            except FileNotFoundError:
                print("The file was not found.")
                return None, None, None, None, None, None
            except IOError:
                print("An IOError occurred while trying to open the file.")
                return None, None, None, None, None, None
            return time, fuel, mat, agent, goal, station

    def draw_map(self, canvas, mat, cell_size):
        color_mapping = {
            0: "white",
            -1: "LightSkyBlue4",
            'S': "DarkSeaGreen2",
            'G': "RosyBrown1",
            'F': "light goldenrod yellow"
        }
        nrow = len(mat)
        ncol = len(mat[0])
        topMargin = (780 - nrow * cell_size) / 2
        leftMargin = (900 - ncol * cell_size) / 2
        for i, row in enumerate(mat):
            for j, val in enumerate(row):
                color = color_mapping.get(val if isinstance(val, int) else val[0], "SlateGray1")
                canvas.create_rectangle(j * cell_size + leftMargin, i * cell_size + topMargin, (j + 1) * cell_size + leftMargin, (i + 1) * cell_size + topMargin, fill=color)
                if val not in [0, -1]:
                    canvas.create_text(j * cell_size + cell_size/2 + leftMargin, i * cell_size + cell_size/2 + topMargin, text=val, fill="black", font=("Helvetica", cell_size//4))




    def handle_button_press(self, btn_name):
        if(btn_name == "reset"):
            # check maze combobox
            maze = self.maze_option.get()
            if maze == "Read from file":
                path = "input.txt"
            elif maze == "Matrix 1":
                path = "input1.txt"
            elif maze == "Matrix 2":
                path = "input2.txt"
            elif maze == "Matrix 3":
                path = "input3.txt"
            elif maze == "Matrix 4":
                path = "input4.txt"
            elif maze == "Matrix 5":
                path = "input5.txt"
            time, fuel, mat, agent, goal, station = self.read_input(path)
            if(time == None):
                return
            rows, cols = len(mat), len(mat[0])
            cell_size = min(900 // cols, 800 // rows)
            self.draw_map(self.canvas, mat, cell_size)
        elif btn_name == "pauseresume":
            self.pauseresume_button_clicked()
            


    # ~ FUNCTIONS FOR BUTTONS FOR CHANGING TABS ~

        
    def pauseresume_button_clicked(self):
        if (self.pauseresume_button['text']=="Pause"):
                self.pauseresume_button.config(image=self.resume_image,text="Resume")
            

        elif (self.pauseresume_button['text']=="Resume"):
                self.pauseresume_button.config(image=self.pause_image,text="Pause")

    def init(self):
        # window = Tk()
        # window.title("PathFinder")
        # window.geometry("1200x850")
        # window.configure(bg = "#171435")


        self.sidebar = Canvas(
            self.window,
            bg = '#171435',
            height = 950,
            width = 250,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas = Canvas(
            self.window,
            bg = '#171435',
            height = 800,
            width = 900,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )


        self.sidebar.place(x= 0, y= 0)
        self.canvas.place(x = 270, y = 30)
        time, fuel, mat, agent, goal, station = self.read_input("input.txt")
        rows, cols = len(mat), len(mat[0])
        cell_size = min(900 // cols, 800 // rows)
        self.draw_map(self.canvas, mat, cell_size)


        self.sidebar.create_text(
            38.0,
            125.0,
            anchor="nw",
            text="Maze",
            fill="#FFFFFF",
            font=("Montserrat-Bold", 12 * -1)
        )
        self.maze_option= ttk.Combobox(
            values=["Read from file", "Matrix 1", "Matrix 2", "Matrix 3", "Matrix 4", "Matrix 5"],
            state="readonly",
            justify="center",
            font=("Montserrat-Bold", 14 * -1)
        )
        self.maze_option.current(0) # For Setting the Standard Video as Default
                            # Though i know this won't work Correctly
                            # will be changed in Future Commits
        self.maze_option.place(
            x=38.0,
            y=147.0,
            width=182.0,
            height=34.0
        )

        self.sidebar.create_text(
            38.0,
            210.0,
            anchor="nw",
            text="Level",
            fill="#FFFFFF",
            font=("Montserrat-Bold", 12 * -1)
        )
        self.level_option= ttk.Combobox(
            values=["Level 1", "Level 2", "Level 3", "Level 4"],
            state="readonly",
            justify="center",
            font=("Montserrat-Bold", 14 * -1)
        )
        self.level_option.current(0) # For Setting the Standard Video as Default
                            # Though i know this won't work Correctly
                            # will be changed in Future Commits
        self.level_option.place(
            x=38.0,
            y=232.0,
            width=182.0,
            height=34.0
        )


        self.sidebar.create_text(
            38.0,
            300.0,
            anchor="nw",
            text="Graph",
            fill="#FFFFFF",
            font=("Montserrat-Bold", 12 * -1)
        )
        self.graph_option= ttk.Combobox(
            values=["Depth First Search", "Breadth First Search", "Greedy Best First Search", "Uniform Cost Search", "A*"],
            state="readonly",
            justify="center",
            font=("Montserrat-Bold", 12 * -1)
        )
        self.graph_option.current(0) # For Setting the Standard Video as Default
                            # Though i know this won't work Correctly
                            # will be changed in Future Commits
        self.graph_option.place(
            x=38.0,
            y=320.0,
            width=182.0,
            height=34.0
        )

        self.sidebar.create_text(
            38.0,
            390.0,
            anchor="nw",
            text="Autorun speed",
            fill="#FFFFFF",
            font=("Montserrat-Bold", 12 * -1)
        )
        self.speed_option= ttk.Combobox(
            values=["Slow", "Medium", "Fast"],
            state="readonly",
            justify="center",
            font=("Montserrat-Bold", 14 * -1)
        )
        self.speed_option.current(0) # For Setting the Standard Video as Default
                            # Though i know this won't work Correctly
                            # will be changed in Future Commits
        self.speed_option.place(
            x=38.0,
            y=410.0,
            width=182.0,
            height=34.0
        )


        self.reset_button = Button(
                    self.sidebar, 
                    background= '#C67FFC',
                    height= 1,
                    foreground= "#171435",
                    highlightthickness= 2,
                    highlightbackground= '#f5267b',
                    highlightcolor= "WHITE",
                    activebackground= "WHITE", 
                    activeforeground= 'BLACK',
                    border= 0,
                    text= 'Update maze/ reset',
                    font= ("Montserrat-Bold", 14 * -1),
                    command= lambda: self.handle_button_press("reset")
                )

        self.reset_button.place(
            x=38.0,
            y=490.0,
            width=182.0,
            height=34.0
        )

        ######## PREVIOUS-PAUSERESUME-FORWARD BUTTONS #######

        ######## (i) PAUSE-RESUME BUTTON #######
        self.pause_image = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.resume_image = PhotoImage(
            file=self.relative_to_assets("button_3.png"))

        self.pauseresume_button = Button(
            image=self.pause_image,
            borderwidth=0,
            bg="#171435",
            highlightthickness=0,
            command=lambda: self.handle_button_press("pauseresume"),
            relief="flat",
            text=str("Pause"),
            activebackground="#171435",
            activeforeground="#171435"
        )
        self.pauseresume_button.place(
            x=107.0,
            y=580.0,
            width=40.18182373046875,
            height=40.436981201171875
        )
        ########################################

        ######## (ii)  FORWARD BUTTON ##########
        self.Forward_button_image = PhotoImage(
            file=self.relative_to_assets("button_5.png"))
        self.Forward_button = Button(
            image=self.Forward_button_image,
            borderwidth=0,
            bg="#171435",
            highlightthickness=0,
            command=lambda: None,
            relief="flat"
        )
        self.Forward_button.place(
            x=180.0,
            y=580.0,
            width=40.18182373046875,
            height=40.0
        )
        ########################################

        ###### (iii)  PREVIOUS BUTTON ##########
        self.Previous_button_image = PhotoImage(
            file=self.relative_to_assets("button_6.png"))
        self.Previous_button = Button(
            image=self.Previous_button_image,
            borderwidth=0,
            bg="#171435",
            highlightthickness=0,
            command=lambda: None,
            relief="flat"
        )
        self.Previous_button.place(
            x=35.0,
            y=580.0,
            width=40.18182373046875,
            height=40.0
        )


        self.sidebar.create_text(             
            30.0,
            25.0,
            anchor="nw",
            text="PathFinder",
            fill="#FFFFFF",
            font=("Montserrat-Bold", 32 * -1)
        )
        self.sidebar.create_text(             
            17.0,
            820.0,
            anchor="nw",
            text="10Cent",
            fill="yellow",
            font=("Montserrat-Bold", 9)
        )


# newGui = GUI()