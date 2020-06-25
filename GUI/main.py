import tkinter as tk
import webbrowser

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.navbar()
        self.handle()

    def handle(self):
        root.geometry('1000x400')
        root.title('Music Quiz | by Daniel Lovett')
        root.iconphoto(False, tk.PhotoImage(file = 'GUI/src/winIcon1.png'))

    def navbar(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Login | Sign Up  ", command = ''), filemenu.add_separator(), filemenu.add_command(label="Exit", command=root.quit), menubar.add_cascade(label= 'Account', menu=filemenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command = ''), helpmenu.add_command(label="Learn More...", command = ''), menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)

root = tk.Tk()
app = Application(master=root)

tk.Label(root, text = 'Music Quiz', font=("Acumin Pro Bold", 50)).pack(side = 'top')
tk.Label(root, text = 'A Game Made by Daniel Lovett', font=("Acumin Pro Regular", 20)).pack(side = 'top')
tk.Label(root, text = 'Please wait for more content to be added', font=("Acumin Pro Regular", 15)).pack(side = 'bottom')
tk.Button(root, text = 'Click here for App Progression', font=("Acumin Pro Regular", 15), command = lambda: webbrowser.open_new(r"http://www.google.com")).pack(side = 'bottom')

app.mainloop()