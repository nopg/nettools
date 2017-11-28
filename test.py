import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as tkst

#class myTest(tk.Frame):
#    def __init__(self, parent, controller):
#
#        
#        tk.Frame.__init__(self, parent)
#
#        outputLabel = ttk.Label(self, text="Output: ")
#        outputLabel.grid(row=0)
#        outputBox = tkst.ScrolledText(self, width=60, height=30, borderwidth=2, relief=tk.SUNKEN)
#        outputBox.insert(tk.END, "Testing")
#        outputBox.grid(row=1, padx=10)
#
#root = Tk()#

class PopupWindow(object):
    def __init__(self,parent, controller):
        top=self.top=tk.Toplevel(parent)

        self.controller = controller
        #top.grid_rowconfigure(0, weight=1)
        #top.grid_rowconfigure(1, weight=3)
        #top.grid_columnconfigure(0, weight=1)

        outputLabel = ttk.Label(top, text="Output: ")
        outputLabel.grid(row=0)
        outputBox = tkst.ScrolledText(top, width=60, height=30, borderwidth=2, relief=tk.SUNKEN)
        outputBox.insert(tk.END, "Testing")
        outputBox.grid(row=1, padx=10)

        if self.controller.pageFrom == "ApicPage":
            #arc.apic_run_commands(self.controller.apicIP,
            #                     self.controller.apicUser,
            #                     self.controller.apicPass,
            #                     self.controller.apicTag,
            #                     self.controller.deviceUser,
            #                     self.controller.devicePass,
            #                     self.controller.outputPath,
            #                     self.controller.commands)
            x = 1
            while True:
                x += 1
                print(x)
                outputBox.insert(tk.END, x)

        elif self.controller.pageFrom == "FilePage":
            #frc.run_commands(self.controller.deviceList,
            #                self.controller.outputPath,
            #                self.controller.deviceUser,
            #                self.controller.devicePass,
            #                self.controller.commands,
            #                outputBox)
            pass
        elif self.controller.pageFrom == "ManualPage":
            messagebox.showinfo(TITLE, "I told you this was under construction!")
        else:#
            pass