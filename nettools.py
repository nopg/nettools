import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog

import file_run_commands as fr

TITLE = 'net-tools'
MAINWINDOWSIZE = "900x700"

LARGE_FONT = ("Verdana", 22)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

class NetTools(tk.Tk):

    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.pageFrom = "HomePage"
        self.initialize()

    def initialize(self):
        container = tk.Frame(self, background="bisque")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, ApicPage, FilePage, ManualPage, CommandPage, TestPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def focus_next_box(self,event):
        event.widget.tk_focusNext().focus()
        return("break")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, background="blue")

        self.controller = controller
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.grid_rowconfigure(5,weight=1)
        self.grid_rowconfigure(6,weight=1)

        self.pullFrom = tk.StringVar(value="not selected")

        pullFromLabel = ttk.Label(self, text="Collect devices from:",font=LARGE_FONT)
        pullFromLabel.grid(row=0,column=0,columnspan=2)

        pullFromFrame = tk.Frame(self,relief=tk.SUNKEN)#,borderwidth=1)
        pullFromFrame.grid(row=2,column=0,sticky="ne",padx=20,pady=20)

        apicRadio = tk.Radiobutton(pullFromFrame,text="APIC-EM",variable=self.pullFrom,value="apic-em",
                                   command=self.pullFromChecked)
        apicRadio.grid(sticky="w")

        fileRadio = tk.Radiobutton(pullFromFrame,text="Device File (.yml)",variable=self.pullFrom,value="file",
                                   command=self.pullFromChecked)
        fileRadio.grid(sticky="w")

        manualRadio = tk.Radiobutton(pullFromFrame,text="Manual Entry",variable=self.pullFrom,value="manual",
                                     command=self.pullFromChecked)
        manualRadio.grid(sticky="w")

        # NEXT / BACK BUTTONs

        nextButton = ttk.Button(self, text="> Next >",command=self.nextPage)
        nextButton.grid(row=7,column=1,sticky="se",padx=10,pady=10)

    def pullFromChecked(self):
        self.pullFromVar = self.pullFrom.get()

    def nextPage(self):

        self.pullFromVar = self.pullFrom.get()

        if self.pullFromVar == "apic-em":
            self.controller.pageFrom = "ApicPage"
            self.controller.show_frame(ApicPage)
        elif self.pullFromVar == "file":
            self.controller.pageFrom = "FilePage"
            self.controller.show_frame(FilePage)
        elif self.pullFromVar == "manual":
            self.controller.pageFrom = "ManualPage"
            self.controller.show_frame(ManualPage)
        else:
            messagebox.showinfo(TITLE,"Please choose an option!")
        
class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="gray")

        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.grid_rowconfigure(5,weight=1)
        self.grid_rowconfigure(6,weight=1)

        tlFrame = tk.Frame(self, background="red")
        tlFrame.grid(row=0,column=0, sticky="nsew")

        trFrame = tk.Frame(self, background="blue")
        trFrame.grid(row=0,column=1, sticky="nsew")

        blFrame = tk.Frame(self, background="yellow")
        blFrame.grid(row=1,column=0, sticky="nsew")
        
        brFrame = tk.Frame(self, background="green")
        brFrame.grid(row=1,column=1, sticky="nsew")

        tlFrame.grid_rowconfigure(0, weight=1)
        tlFrame.grid_columnconfigure(0, weight=1)

        brFrame.grid_rowconfigure(0, weight=1)
        brFrame.grid_columnconfigure(0, weight=1)

        spacer1 = ttk.Label(trFrame,text="toprightframe",font=NORM_FONT)
        spacer1.grid(padx=20,pady=20)
        spacer2 = ttk.Label(blFrame,text="bottomleftframe",font=NORM_FONT)
        spacer2.grid(padx=20,pady=20)

        self.label1 = ttk.Label(tlFrame, text="topleftframe", font=NORM_FONT)
        self.label1.grid(padx=20,pady=20)

        label2 = ttk.Label(brFrame, text="bottomrightframe", font=NORM_FONT)
        label2.grid(row = 0, column = 0,padx=20,pady=20)

        button1 = ttk.Button(brFrame, text="< Back <",
                            command=lambda: controller.show_frame(HomePage))
        button1.grid(row=0,column=1,sticky="se",padx=10,pady=10)

        button2 = ttk.Button(brFrame, text="> Next >",
                            command=self.start)
        button2.grid(row=0,column=2,sticky="se",padx=10,pady=10)

    def start(self):
        print("Running start()")
        print("Running gather_configs()")
        teststr = "Testing"
        fr.run_commands(teststr, self.label1)
        print("Finished..")
        return

class FilePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="green")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.grid_rowconfigure(5,weight=1)
        self.grid_rowconfigure(6,weight=1)
        self.grid_rowconfigure(7,weight=1)
        self.grid_rowconfigure(8,weight=1)

        self.showpass = tk.BooleanVar()
        self.outputToFolder = tk.BooleanVar()

        deviceListLabel = ttk.Label(self, text="Choose device list file (.yml): ", font=LARGE_FONT)
        self.deviceListBox = tk.Text(self, width=45,height=2,wrap=tk.WORD,relief=tk.SUNKEN)
        self.deviceListBox.bind("<Tab>", controller.focus_next_box)
        deviceListButton = tk.Button(self, text="...", command=self.pickFile)

        credentialsLabel = ttk.Label(self, text="Network Device Credentials: ", font=LARGE_FONT)
        credentialsUserLabel = ttk.Label(self, text="Username: ", font=NORM_FONT)
        credentialsUserBox = ttk.Entry(self, width=35)
        credentialsUserBox.bind("<Tab>",controller.focus_next_box)
        credentialsPassLabel = ttk.Label(self, text="Password: ", font=NORM_FONT)
        self.credentialsPassBox = ttk.Entry(self, width=35,show="*")
        self.credentialsPassBox.bind("<Tab>", controller.focus_next_box)
        credentialsShowPass = ttk.Checkbutton(self,text="Show Password", variable=self.showpass,
                                                 command=self.show_password)

        outputToFolderOption = ttk.Checkbutton(self, text="Log output to files?", variable=self.outputToFolder,
                                               command=self.outputToFolderCheck)
        self.outputPathLabel = ttk.Label(self, text="Choose output log destination folder: ", font=LARGE_FONT)
        self.outputPathText = tk.Text(self, width=45, height=2, wrap=tk.WORD, relief=tk.SUNKEN, border=1)
        self.outputPathText.bind("<Tab>", self.controller.focus_next_box)
        self.directoryButton = tk.Button(self, text="...", command=self.pickFolder)

        deviceListLabel.grid(row=1, sticky="W", padx=10,pady=10)
        self.deviceListBox.grid(row=2, sticky="W", padx=10,pady=5)
        deviceListButton.grid(row=2,column=1)

        credentialsLabel.grid(row=3, sticky="W", padx=10,pady=5)
        credentialsUserLabel.grid(row=4, sticky="W", padx=10,pady=5)
        credentialsUserBox.grid(row=5, sticky="W", padx=10,pady=5)
        credentialsPassLabel.grid(row=6, sticky="W", padx=10,pady=5)
        self.credentialsPassBox.grid(row=7, sticky="W", padx=10,pady=5)
        credentialsShowPass.grid(row=7,column=1)
        outputToFolderOption.grid(row=8, sticky="W", padx=10,pady=5)

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >",
                            command=lambda: controller.show_frame(CommandPage))
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)

    def show_password(self):
        if self.showpass.get():
            self.credentialsPassBox.config(show="")
        else:
            self.credentialsPassBox.config(show="*")

    def outputToFolderCheck(self):

        if self.outputToFolder.get():
            self.outputPathLabel.grid(row=10, sticky="W", padx=10,pady=5)
            self.outputPathText.grid(row=11, sticky="W", padx=10,pady=5)
            self.directoryButton.grid(row=11, sticky="E")
        else:
            self.outputPathLabel.grid_remove()
            self.outputPathText.grid_remove()
            self.directoryButton.grid_remove()
            self.outputPathText.delete(0.0, tk.END)

    def pickFile(self):
        self.deviceListBox.delete(0.0, tk.END)
        devicelist = filedialog.askopenfilename()
        self.deviceListBox.insert(0.0, devicelist)

    def pickFolder(self):
        self.outputPathText.delete(0.0, tk.END)
        outputPath = filedialog.askdirectory()
        self.outputPathText.insert(0.0, outputPath)

class ApicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >",
                            command=lambda: controller.show_frame(CommandPage))
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)

class ManualPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="grey")


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >",
                            command=lambda: controller.show_frame(CommandPage))
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)


class CommandPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="purple")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.controller = controller

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <", command=self.backPage)
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >",
                            command=lambda: controller.show_frame(HomePage))
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)

    def backPage(self):
        if self.controller.pageFrom == "ApicPage":
            self.controller.show_frame(ApicPage)
        elif self.controller.pageFrom == "FilePage":
            self.controller.show_frame(FilePage)
        elif self.controller.pageFrom == "ManualPage":
            self.controller.show_frame(ManualPage)

if __name__ == "__main__":
    app = NetTools(None)
    app.title(TITLE)
    app.geometry(MAINWINDOWSIZE)
    app.mainloop()
