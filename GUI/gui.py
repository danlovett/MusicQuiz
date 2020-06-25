import tkinter as tk, webbrowser, random, time
from tkinter import filedialog

rng = ['#23D5AB', '#23A6D5', '#E73C7E', '#EE7752', '#4db11b', '#7315c2']
colorPick = random.choice(rng)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.handle()
        self.navbar()
        self.pack()

    def handle(self):
        root.title('Working on it... | Music Quiz')
        root.geometry('1000x450')
        root.resizable(False, False)
        root.configure(background = colorPick)
        root.iconbitmap('GUI/src/musicCascade.ico')

    def navbar(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Click", command = ''), filemenu.add_separator(), filemenu.add_command(label="Exit", command=root.quit), menubar.add_cascade(label= 'Account', menu=filemenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command = lambda: webbrowser.open_new(r"https://github.com/danlovett/MusicQuiz")), helpmenu.add_command(label="Learn More...", command = lambda: webbrowser.open_new(r"https://github.com/danlovett/MusicQuiz/commits")), menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)

def getFile():
    root.filename = filedialog.askopenfile(initialdir = 'MusicQuiz', initialfile = 'main.py', title = 'Open Main.py', filetype = (('Python Files', '*.py'),('Everything Else', '*.*')))

root = tk.Tk()
app = Application(master=root)
name = tk.Label(root, text = 'MusicQuiz')
status = tk.Label(root, text = 'New content is on it\'s way.')
play = tk.Label(root, text = 'For now, you can play the game in a\nmore basic form below')
o_raw = tk.Button(root, text = 'Open Game')
rdir_aprog = tk.Button(root, text = 'Click here for App Progression')
a_dan = tk.Label(root, text = 'by Daniel Lovett')

name.pack(side = 'top', pady = (30, 0)), name.config(font=("Acumin Pro Bold", 50), bg = colorPick)
status.pack(side = 'top', pady = (0, 20)), status.config(font=("Acumin Pro Regular", 20), bg = colorPick)
play.pack(side = 'top', pady = (10, 15)), play.config(font=("Acumin Pro Bold", 15), fg = "#fff", bg = colorPick)
o_raw.pack(side = 'top', pady = (0, 10)), o_raw.config(command = lambda: getFile(), font=("Acumin Pro Bold", 13), fg = '#fff', bg = colorPick)
rdir_aprog.pack(side = 'top', pady = (30, 10)), rdir_aprog.config(command = lambda: webbrowser.open_new(r"https://github.com/danlovett/MusicQuiz/commits/Dev"), font=("Acumin Pro Regular", 15), bg = colorPick)
a_dan.pack(side = 'bottom', pady = (0, 10)), a_dan.config(font=("Acumin Pro Regular", 10), bg = colorPick)
app.mainloop()