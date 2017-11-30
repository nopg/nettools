import sys
import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext as tkst

import file_run_commands as frc
import apic_run_commands as arc

TITLE = 'net-tools'
MAINWINDOWSIZE = "700x600"

LARGE_FONT = ("Verdana", 18)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

class NetTools(tk.Tk):

    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent

        self.pageFrom = "HomePage"

        self.apicIP = ""
        self.apicUser = ""
        self.apicPass = ""
        self.apicTag = ""
        self.deviceUser = ""
        self.devicePass = ""
        self.outputPath = ""
        self.commands = ""
        self.deviceList = ""

        self.initialize()

    def initialize(self):
        container = tk.Frame(self, background="bisque")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, ApicPage, FilePage, ManualPage, CommandPage):
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
        tk.Frame.__init__(self,parent)

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

class FilePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)#, background="green")
        self.controller = controller
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.showpass = tk.BooleanVar()
        self.outputToFolder = tk.BooleanVar()

        devicelistFrame = tk.Frame(self)#, background="yellow")
        devicelistFrame.grid(row=1,sticky="nsew", padx=10 ,pady=10)

        deviceListLabel = ttk.Label(devicelistFrame, text="Choose device list file (.yml): ", font=LARGE_FONT)
        self.deviceListBox = tk.Text(devicelistFrame, width=45, height=2, wrap=tk.WORD, relief=tk.SUNKEN, border=1)
        self.deviceListBox.bind("<Tab>", controller.focus_next_box)
        deviceListButton = tk.Button(devicelistFrame, text="...", command=self.pickFile)


        credentialsFrame = tk.Frame(self)#, background="red")
        credentialsFrame.grid(row=2,sticky="nsew", padx=10, pady=10)
        credentialsLabel = ttk.Label(credentialsFrame, text="Network Device Credentials: ", font=LARGE_FONT)
        credentialsUserLabel = ttk.Label(credentialsFrame, text="Username: ", font=NORM_FONT)
        self.credentialsUserBox = ttk.Entry(credentialsFrame, width=35)
        self.credentialsUserBox.bind("<Tab>",controller.focus_next_box)
        credentialsPassLabel = ttk.Label(credentialsFrame, text="Password: ", font=NORM_FONT)
        self.credentialsPassBox = ttk.Entry(credentialsFrame, width=35,show="*")
        self.credentialsPassBox.bind("<Tab>", controller.focus_next_box)
        credentialsShowPass = ttk.Checkbutton(credentialsFrame,text="Show Password", variable=self.showpass,
                                                 command=self.show_password)

        outputToFolderFrame = tk.Frame(self)#, background="blue")
        outputToFolderFrame.grid(row=3,sticky="nW", padx=10, pady=10, columnspan=2)
        outputToFolderOption = ttk.Checkbutton(outputToFolderFrame, text="Log output to files?", variable=self.outputToFolder,
                                               command=self.outputToFolderCheck)
        self.outputPathLabel = ttk.Label(outputToFolderFrame, text="Choose output log destination folder: ", font=LARGE_FONT)
        self.outputPathText = tk.Text(outputToFolderFrame, width=45, height=2, wrap=tk.WORD, relief=tk.SUNKEN, border=1)
        self.outputPathText.bind("<Tab>", self.controller.focus_next_box)
        self.directoryButton = tk.Button(outputToFolderFrame, text="...", command=self.pickFolder)

        deviceListLabel.grid(row=1, sticky="W")
        self.deviceListBox.grid(row=2, sticky="W", padx=10,pady=5)
        deviceListButton.grid(row=2,column=1)

        credentialsLabel.grid(row=1, sticky="W")
        credentialsUserLabel.grid(row=2, sticky="W", pady=5)
        self.credentialsUserBox.grid(row=3, sticky="W", padx=10,pady=5)
        credentialsPassLabel.grid(row=4, sticky="W", pady=5)
        self.credentialsPassBox.grid(row=5, sticky="W", padx=10,pady=5)
        credentialsShowPass.grid(row=5,column=1)

        outputToFolderOption.grid(row=0, sticky="W")

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <", command=self.backPage)
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >", command=self.nextPage)
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)

    def show_password(self):
        if self.showpass.get():
            self.credentialsPassBox.config(show="")
        else:
            self.credentialsPassBox.config(show="*")

    def outputToFolderCheck(self):

        if self.outputToFolder.get():
            self.outputPathLabel.grid(row=1, sticky="W", pady=10)
            self.outputPathText.grid(row=2, sticky="W", padx=(10,0),pady=5)
            self.directoryButton.grid(row=2, column = 1, sticky="E", padx=10)
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


    def backPage(self):
        self.deviceListBox.delete(0.0, tk.END)
        self.credentialsUserBox.delete(0, 'end')
        self.credentialsPassBox.delete(0, 'end')
        self.outputPathText.delete(0.0, tk.END)
        self.controller.show_frame(HomePage)

    def nextPage(self):
        self.controller.deviceUser = self.credentialsUserBox.get()
        self.controller.devicePass = self.credentialsPassBox.get()
        self.controller.deviceList = self.deviceListBox.get('1.0', 'end').strip()
        self.controller.outputPath = self.outputPathText.get('1.0', 'end').strip()

        if self.controller.deviceList == "":
            messagebox.showinfo(TITLE, "Please select a device list file!")
        elif self.outputToFolder.get():
            if self.controller.outputPath == "":
                messagebox.showinfo(TITLE, "A folder must be chosen if 'log output' is checked!")
            else:
                self.controller.show_frame(CommandPage)
        else:
            self.controller.show_frame(CommandPage)

class ApicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.showpassApic = tk.BooleanVar()
        self.showpass = tk.BooleanVar()
        self.outputToFolder = tk.BooleanVar()

        apicFrame = tk.Frame(self)
        apicFrame.grid(row=1, sticky="W", padx=10, pady=10)
        apicLabel = ttk.Label(apicFrame, text="APIC-EM Credentials:", font=LARGE_FONT)
        apicIPLabel = ttk.Label(apicFrame, text="IP Address")
        self.apicIPEntry = ttk.Entry(apicFrame, width=15)
        self.apicIPEntry.bind("<Tab>", self.controller.focus_next_box)
        apicUserLabel = ttk.Label(apicFrame, text="Username: ")
        self.apicUserEntry = ttk.Entry(apicFrame, width=35)
        self.apicUserEntry.bind("<Tab>", self.controller.focus_next_box)
        apicPassLabel = ttk.Label(apicFrame, text="Password: ")
        self.apicPassEntry = ttk.Entry(apicFrame, width=35, show="*")
        self.apicPassEntry.bind("<Tab>", self.controller.focus_next_box)
        apicShowPass = ttk.Checkbutton(apicFrame, text="Show Password", variable = self.showpassApic,
                                       command=self.show_password)

        apicTagLabel = ttk.Label(apicFrame, text="Search APIC-EM based on device TAG:\n(Leave blank to find all devices)")
        self.apicTagEntry = ttk.Entry(apicFrame, width=35)
        self.apicTagEntry.bind("<Tab>", self.controller.focus_next_box)


        apicLabel.grid(row=0)
        apicIPLabel.grid(row=1, pady=5)
        self.apicIPEntry.grid(row=1, column=1, sticky="W")
        apicShowPass.grid(row=1, column=1, sticky="E")
        apicUserLabel.grid(row=2, pady=5)
        self.apicUserEntry.grid(row=2, column=1)
        apicPassLabel.grid(row=3, pady=5)
        self.apicPassEntry.grid(row=3, column=1)
        apicTagLabel.grid(row=4, pady=20)
        self.apicTagEntry.grid(row=4, column=1)

        credentialsFrame = tk.Frame(self)
        credentialsFrame.grid(row=2, sticky="W", padx=10, pady=10)
        credentialsLabel = ttk.Label(credentialsFrame, text="Network Device Credentials: ", font=LARGE_FONT)
        credentialsUserLabel = ttk.Label(credentialsFrame, text="Username: ", font=NORM_FONT)
        self.credentialsUserBox = ttk.Entry(credentialsFrame, width=35)
        self.credentialsUserBox.bind("<Tab>", controller.focus_next_box)
        credentialsPassLabel = ttk.Label(credentialsFrame, text="Password: ", font=NORM_FONT)
        self.credentialsPassBox = ttk.Entry(credentialsFrame, width=35, show="*")
        self.credentialsPassBox.bind("<Tab>", controller.focus_next_box)
        credentialsShowPass = ttk.Checkbutton(credentialsFrame, text="Show Password", variable=self.showpass,
                                              command=self.show_password)
        outputToFolderFrame = tk.Frame(self)
        outputToFolderFrame.grid(row=3, sticky="W", padx=10, pady=10)
        outputToFolderOption = ttk.Checkbutton(outputToFolderFrame, text="Log output to files?",
                                               variable=self.outputToFolder,
                                               command=self.outputToFolderCheck)
        self.outputPathLabel = ttk.Label(outputToFolderFrame, text="Choose output log destination folder: ",
                                         font=LARGE_FONT)
        self.outputPathText = tk.Text(outputToFolderFrame, width=45, height=2, wrap=tk.WORD, relief=tk.SUNKEN,
                                      border=1)
        self.outputPathText.bind("<Tab>", self.controller.focus_next_box)
        self.directoryButton = tk.Button(outputToFolderFrame, text="...", command=self.pickFolder)
        credentialsLabel.grid(row=1, sticky="W")
        credentialsUserLabel.grid(row=2, sticky="W", pady=5)
        self.credentialsUserBox.grid(row=3, sticky="W", padx=10, pady=5)
        credentialsPassLabel.grid(row=4, sticky="W", pady=5)
        self.credentialsPassBox.grid(row=5, sticky="W", padx=10, pady=5)
        credentialsShowPass.grid(row=5, column=1)
        outputToFolderOption.grid(row=0, sticky="W")

        # NEXT / BACK BUTTONS
        backButton = ttk.Button(self, text="< Back <", command=self.backPage)
        backButton.grid(row=20, column=1, sticky="se", padx=10, pady=10)
        nextButton = ttk.Button(self, text="> Next >", command=self.nextPage)
        nextButton.grid(row=20, column=2, sticky="se", padx=10, pady=10)

    def show_password(self):
        if self.showpass.get():
            self.credentialsPassBox.config(show="")
        else:
            self.credentialsPassBox.config(show="*")

        if self.showpassApic.get():
            self.apicPassEntry.config(show="")
        else:
            self.apicPassEntry.config(show="*")

    def outputToFolderCheck(self):

        if self.outputToFolder.get():
            self.outputPathLabel.grid(row=1, sticky="W", pady=10)
            self.outputPathText.grid(row=2, sticky="W", padx=10,pady=5)
            self.directoryButton.grid(row=2, sticky="E")
        else:
            self.outputPathLabel.grid_remove()
            self.outputPathText.grid_remove()
            self.directoryButton.grid_remove()
            self.outputPathText.delete(0.0, tk.END)

    def pickFolder(self):
        self.outputPathText.delete(0.0, tk.END)
        outputPath = filedialog.askdirectory()
        self.outputPathText.insert(0.0, outputPath)

    def backPage(self):
        self.apicIPEntry.delete(0, 'end')
        self.apicUserEntry.delete(0, 'end')
        self.apicPassEntry.delete(0, 'end')
        self.apicTagEntry.delete(0, 'end')
        self.credentialsUserBox.delete(0, 'end')
        self.credentialsPassBox.delete(0, 'end')
        self.outputPathText.delete(0.0, tk.END)

        self.controller.show_frame(HomePage)

    def nextPage(self):

        self.controller.apicIP = self.apicIPEntry.get()
        self.controller.apicUser = self.apicUserEntry.get()
        self.controller.apicPass = self.apicPassEntry.get()
        self.controller.apicTag = self.apicTagEntry.get()
        self.controller.deviceUser = self.credentialsUserBox.get()
        self.controller.devicePass = self.credentialsPassBox.get()
        self.controller.outputPath = self.outputPathText.get('1.0', 'end').strip()

        if self.outputToFolder.get():
            if self.controller.outputPath == "":
                messagebox.showinfo(TITLE, "A folder must be chosen if 'log output' is checked!")
        else:
            self.controller.show_frame(CommandPage)


class ManualPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        tempMessage = ttk.Label(self,text="This page is currently under construction.")
        tempMessage.grid()

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <",
                            command=lambda: controller.show_frame(HomePage))
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

        nextButton = ttk.Button(self, text="> Next >",
                            command=lambda: controller.show_frame(CommandPage))
        nextButton.grid(row=20,column=2,sticky="se",padx=10,pady=10)


class CommandPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)

        self.controller = controller
        self.parent = parent

        commandLabel = ttk.Label(self,text="Command(s) to run on devices (one per line): ", font=LARGE_FONT)
        commandLabel.grid(row=0, padx = 10)

        self.commandText = tkst.ScrolledText(self, width=60, height=20, borderwidth=2, relief=tk.SUNKEN)
        self.commandText.grid(row=1, padx=10)

        startButton = ttk.Button(self,text="Push commands to devices (START!)", command=self.start_gather)
        startButton.grid(row=2, pady=30)

        # NEXT / BACK BUTTONS

        backButton = ttk.Button(self, text="< Back <", command=self.backPage)
        backButton.grid(row=20,column=1,sticky="se",padx=10,pady=10)

    def backPage(self):
        if self.controller.pageFrom == "ApicPage":
            self.controller.show_frame(ApicPage)
        elif self.controller.pageFrom == "FilePage":
            self.controller.show_frame(FilePage)
        elif self.controller.pageFrom == "ManualPage":
            self.controller.show_frame(ManualPage)
        return

    def start_gather(self):

        self.controller.commands = self.commandText.get('1.0', 'end').splitlines()

        self.outputWindow = PopupWindow(self.parent, self.controller)
        self.controller.wait_window(self.outputWindow.top)


class PopupWindow(object):
    def __init__(self,parent, controller):
        top=self.top=tk.Toplevel(parent)

        self.controller = controller
        self.parent = parent
        top.grid_rowconfigure(1, weight=1)
        top.grid_columnconfigure(0, weight=1)

        outputLabel = ttk.Label(top, text="Output: ")
        self.outputBox = tkst.ScrolledText(top, width=80, height=30, borderwidth=2, relief=tk.SUNKEN)
        self.outputBox.bind_class("Text", "<Button-2>", func=self.nothing)

        buttonFrame = tk.Frame(top)

        doneButton = ttk.Button(buttonFrame, text="Running...", command=self.done)
        doneButton.config(state="disabled")
        cancelLabel = ttk.Label(buttonFrame, text="Use CTRL+C from command line to cancel.", font=SMALL_FONT)

        outputLabel.grid(row=0)
        self.outputBox.grid(row=1, padx=10)

        buttonFrame.grid(row=2)
        doneButton.grid(row=0, pady=10)
        cancelLabel.grid(row=0,column = 1, padx=50, sticky="e")

        if self.controller.pageFrom == "ApicPage":
            arc.apic_run_commands(self.controller.apicIP,
                                 self.controller.apicUser,
                                 self.controller.apicPass,
                                 self.controller.apicTag,
                                 self.controller.deviceUser,
                                 self.controller.devicePass,
                                 self.controller.outputPath,
                                 self.controller.commands,
                                 self.outputBox, parent)

        elif self.controller.pageFrom == "FilePage":
            frc.run_commands(self.controller.deviceList,
                            self.controller.outputPath,
                            self.controller.deviceUser,
                            self.controller.devicePass,
                            self.controller.commands,
                            self.outputBox, parent)

        elif self.controller.pageFrom == "ManualPage":
            messagebox.showinfo(TITLE, "I told you this was under construction!")
        else:#
            pass

        doneButton.config(text="Close")
        doneButton.config(state="normal")

    def nothing(self, pos):
        self.outputBox.selection_clear()
    def done(self):
        self.top.destroy()


if __name__ == "__main__":
    app = NetTools(None)
    app.title(TITLE)
    app.geometry(MAINWINDOWSIZE)
    app.mainloop()
