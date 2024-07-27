from pathlib import Path
from tkinter import *
from tkinter import ttk
import pyglet
from Map import Map


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("fonts/Montserrat-Bold.ttf")

class GUI:
    # constructor
    def __init__(self):
        self.path = None
        self.goalList = None
        self.level = "Level 1"
        self.window = Tk()
        self.window.title("PathFinder")
        self.window.geometry("1200x850")
        self.window.iconbitmap(self.relative_to_assets("icon2.ico"))
        self.window.configure(bg = "#171435")
        self.init()
        self.window.resizable(False, False)
        self.window.mainloop()
        self.currLevel = "Level 1"
        
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)


    def handle_button_press(self, btn_name):
        if btn_name == "pauseresume":
            self.pauseresume_button_clicked()
        elif btn_name == "update":
            self.updateButtonClicked()
        elif btn_name == "previous":
            self.previousButtonClicked()
        elif btn_name == "forward":
            self.forwardButtonClicked()
        
    def handleLevel4(self, isForward):
        if isForward:
            totalStep = 0
            for i in range (len(self.path)):
                totalStep += len(self.path[i])
            self.map.nextSteplvl4(totalStep)
        else:
            self.map.previousSteplvl4()
        
    def forwardButtonClicked(self):
        if(self.path is not None):
            if self.level != "Level 4":    
                self.map.nextStep()
            else:
                self.handleLevel4(True)
        
    def previousButtonClicked(self):
        if(self.path is not None):
            if self.level != "Level 4":
                self.map.previousStep()
                currentStep = self.map.getCurrentStep()
                if(currentStep < 6):
                        self.changePauseresumeState("pause")
            else:
                self.handleLevel4(False)
                currentStep = self.map.getCurrentStep()
                if(currentStep < 0):
                        self.changePauseresumeState("pause")  
            
            
    def updateButtonClicked(self):
        print(self.level)
        # self.hidePathInfo()
        self.path = None
        self.goalList = None
        self.changePauseresumeState("pause")
        filePath = self.getMazeOption()
        self.map.load(filePath)
        self.level = self.level_option.get()
        graph = self.graph_option.get()
        if self.level != "Level 4":
            self.path = self.map.getPath(self.level, graph)
        else:
            print("before")
            self.path, self.goalList = self.map.getPath(self.level, graph)
            print("after")
        
        self.showPathInfo()

        
    def getMazeOption(self):
        pre = ''.join(self.level.split(' ')).lower() + '.txt'
        maze = self.maze_option.get()
        path = {
            "Matrix 1": "input1_",
            "Matrix 2": "input2_",
            "Matrix 3": "input3_",
            "Matrix 4": "input4_",
            "Matrix 5": "input5_",
            "Read from file": "input.txt"
        }
        return path.get(maze) + pre if maze != "Read from file" else path.get(maze)
        
    # ~ FUNCTIONS FOR BUTTONS FOR CHANGING TABS ~
    def changePauseresumeState(self, state):
        if state == "pause":
            self.pauseresume_button.config(image=self.pause_image,text="Pause")
        elif state == "resume":
            self.pauseresume_button.config(image=self.resume_image,text="Resume")
        
    def pauseresume_button_clicked(self):
        if(self.level == "Level 4"):
            if(self.map.getCurrentStep() > 5):
                return
        else:    
            if(self.map.getCurrentStep() > 0  or self.path is None):
                return

        
        speed = self.speed_option.get()
        autoSpeed = 1000
        if(speed == "Medium"):
            autoSpeed = 600
        elif(speed == "Fast"):
            autoSpeed = 200
        self.pauseresume_button.config(image=self.resume_image,text="Resume") 
        if(self.level == "Level 4"):
            totalStep = 0
            for i in range (len(self.path)):
                totalStep += len(self.path[i])
            self.map.autoRunlvl4(autoSpeed, totalStep)
        else:
            self.map.autoRun(autoSpeed)
        # self.showPathInfo(12, 13, 14)
        

    def showPathInfo(self):
        self.info.delete("all")
        informMessage = "Path found!"
        if self.path == -1:
            informMessage = "Path not found!"
        self.info.create_text(
            33,
            0,
            anchor="nw",
            text="Result: " + informMessage,
            fill="#FFFFFF",
            font=("Montserrat-Bold", 12 * -1)
        )
        
    
    def hidePathInfo(self):
        self.info.delete("all")


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
        self.info = Canvas(
            self.window,
            bg = '#171435',
            height = 150,
            width = 250,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        self.info.place(x = 0, y = 650)
        self.sidebar.place(x= 0, y= 0)
        self.canvas.place(x = 270, y = 30)
        self.map = Map(self.canvas)
        self.map.load('input.txt')


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
        self.maze_option.current(0)
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


        self.update_button = Button(
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
                    text= 'Update',
                    font= ("Montserrat-Bold", 14 * -1),
                    command= lambda: self.handle_button_press("update")
                )

        self.update_button.place(
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
            command= lambda: self.handle_button_press("forward"),
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
            command= lambda: self.handle_button_press("previous"),
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

        
