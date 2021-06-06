import os
from tkinter import *
from tkinter.ttk import Combobox
import psutil
from tkinter import ttk, filedialog
from Injector import Injector
from elevate import elevate

# elevate is optional, we don't typically need elevated privileges to inject into a process
# elevate(show_console=False)


def UpdateLabel(NewText):
    DLLLabel['text'] = NewText


def move_window(event):
    box.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


def Exit():
    window.destroy()

# not really a window lol just the name I decided to use when I made the class
class InjectionWindow:
    def __init__(self):
        self.processesByName = []
        self.processesByPID = []
        self.SelectedDLLPath = ""
        self.SelectedDLLName = ""
        self.DLLSelected = False
        self.ProcessSelected = False
        self.injector = Injector()

    def GetProcesses(self):
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                if "csgo" in processName:
                    self.processesByName.append(processName)
                    self.processesByPID.append(processID)

                # print(processName, ' ::: ', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def SelectDLL(self):
        file_path = filedialog.askopenfilename(filetypes=(("dll files", "*.dll"), ("all files", "*.*")))
        if file_path != "":
            if file_path is not None:
                self.SelectedDLLPath = file_path
                self.SelectedDLLName = os.path.basename(self.SelectedDLLPath)
                UpdateLabel(self.SelectedDLLName)
                self.DLLSelected = True
            else:
                self.DLLSelected = False
        else:
            self.DLLSelected = False

    def CheckProcessSelected(self):
        if ProcessSelector.get() != "":
            self.ProcessSelected = True
        else:
            self.ProcessSelected = False

    def Inject(self):
        if self.DLLSelected:
            self.CheckProcessSelected()
            if self.ProcessSelected:
                i = 0
                for process in self.processesByName:
                    if ProcessSelector.get() == process:
                        self.injector.load_from_pid(self.processesByPID[i])
                        self.injector.inject_dll(self.SelectedDLLPath)
                        self.injector.unload()
                        # inject to processByPID[i]
                        break
                    else:
                        print("wrong process")
                        i += 1

                pass
            else:
                print("No Process Selected")
        else:
            print("No DLL Selected")


myInjector = InjectionWindow()
myInjector.GetProcesses()
window = Tk()
window.attributes('-alpha', 0.0)
window.iconify()
box = Toplevel(window)
box.overrideredirect(1)
window.title('')
box.geometry("250x100+10+20")
box.resizable(False, False)
box['background'] = '#000822'
box.attributes('-topmost', 1)
box.bind('<B1-Motion>', move_window)


# finish window creation

DLLLabel = Label(box, text=".dll", bg='#000822', fg='white')
DLLLabel.place(x=100, y=60)
combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                                      {'configure':
                                           {'selectbackground': 'black',
                                            'fieldbackground': 'black',
                                            'background': 'white'
                                            }}})

combostyle.theme_use('combostyle')
ProcessSelector = Combobox(box, values=myInjector.processesByName)
ProcessSelector.place(x=100, y=30)
ProcessSelector['state'] = 'readonly'

InjectButton = Button(box, text="Inject", bg='black', fg='white', bd=0, activebackground='#4F4F4F', height=1,
                      width=8,
                      command=myInjector.Inject)
InjectButton.place(x=10, y=30)

DLLButton = Button(box, text="Select DLL",
                   bg='black', fg='white', bd=0, activebackground='#4F4F4F', height=1, width=8,
                   command=myInjector.SelectDLL)
DLLButton.place(x=10, y=60)

QuitButton = Button(box, text=" X ", bg='black', fg='white', bd=0, activebackground='#4F4F4F', height=1, width=3,
                   command=Exit)

QuitButton.place(x=225, y=0)


window.mainloop()
