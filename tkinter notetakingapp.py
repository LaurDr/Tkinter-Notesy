import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import json

class NewprojectApp:
    def __init__(self, master=None):
        self.localPath=os.path.dirname(__file__)        # setting the localpath for the application
        self.notesFolder = self.localPath+'/Notes'      # The notes folder gets generated and consists of the default note+the config.json file
        self.note= self.notesFolder+'/Notepad.txt'      
        self.config = self.notesFolder + '/config.json' 
        self.Setup()

        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel1.minsize(230, 200)
        self.toplevel1.resizable(True, True)
        self.toplevel1.title("Notepad")

        self.icon = tk.PhotoImage(file=self.localPath+'/Icons/icon.png')    # setting the icons for the application, when using pyinstaller must be added again manually 
        self.toplevel1.iconbitmap("@icon.png")
        self.toplevel1.iconphoto(True, self.icon)

        # self.toplevel1.update()
        self.toplevel1.attributes('-alpha',0.9)         #transparency
        self.toplevel1.overrideredirect(True)           #top bar deactivate

        menubar = tk.Menu(self.toplevel1)               # create menubar so i dont get the python/ tkinter/ tcl default menubar.
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.toplevel1.quit)
        menubar.add_cascade(label="App", menu=filemenu)
        self.toplevel1.config(menu=menubar)


        self.frame1 = ttk.Frame(self.toplevel1)
        self.text1 = tk.Text(self.frame1)
        self.text1.configure(
            font="{Apple Braille} 13 {}",
            highlightbackground="#1e1e1e",              # tk.text has weird highlight colors. Used a neutral color so it cant be seen
            highlightcolor="#1e1e1e",                      
            tabs=30,
            undo="true",
            wrap="word",
        )
        self.text1.pack(expand=True,fill="both")
        self.text1.bind("<Mod2-BackSpace>",self.OptDelete)

        self.Read()                                     # first read here because text1 wasnt created yet

        self.frame1.pack(expand="true", fill="both", side="top")
        self.frame1.pack_propagate(0)

        self.frame2 = ttk.Frame(self.toplevel1)
        self.frame2.place(anchor="se", relx=1.0, rely=1.0, x=0, y=0)    

        self.label1 = ttk.Label(self.frame2)
        self.label1.configure(text="❌")
        self.label1.grid(column=0, row=0)
        self.label1.bind("<ButtonPress>", self.Quit, add="")

        self.label2 = ttk.Label(self.frame2)
        self.label2.configure(text="✅")
        self.label2.grid(column=0, row=1)
        self.label2.bind("<ButtonPress>", self.Save, add="")

        self.label3 = ttk.Label(self.frame2)
        self.label3.configure(text="📂")
        self.label3.grid(column=0, row=2)
        self.label3.bind("<ButtonPress>", self.Open, add="")

        # self.label4 = ttk.Label(self.frame2)                  # not used anymore, might come later
        # self.label4.configure(text="🗒")
        # self.label4.grid(column=0, row=3)
        # self.label4.bind("<ButtonPress>", self.OpenWindow, add="")

        self.label5 = ttk.Label(self.frame2)
        self.label5.configure(text="🔄")
        self.label5.grid(column=0, row=4)
        self.label5.bind("<ButtonPress>", self.Revert, add="")

        self.label6 = ttk.Label(self.frame2)
        self.label6.configure(text="↘️")
        self.label6.grid(column=0, row=5)
        self.label6.bind("<B1-Motion>", self.Resize, add="")
        self.label6.bind("<Button-1>", self.SaveLastClickPos, add="")

        self.label7 = ttk.Label(self.frame2)
        self.label7.configure(text="✋")
        self.label7.grid()
        self.label7.bind("<B1-Motion>", self.Dragging, add="")
        self.label7.bind("<Button-1>", self.SaveLastClickPos, add="")     
        

        self.toplevel1.attributes('-topmost', True)                 # stay on top. Must be here because otherwise it doesnt stay on top, dk why
        
        # Main widget
        self.mainwindow = self.toplevel1
    
    def Setup(self):                                                # looks if the note dir, notepad.txt and config.json exist, and if note creates them 
        if (os.path.exists(self.notesFolder) == False):
            try: os.mkdir(self.notesFolder)
            except: print("couldnt create"+self.notesFolder)
        if (os.path.exists(self.note)==False):
            try: 
                open(self.note,'w')
            except:print('couldnt create'+self.note)
        if (os.path.exists(self.config)==False):
            try:
                with open(self.config,'w') as f:
                    json.dump({'currentNote':'%s' % (self.note)},f)
                    f.close()
            except:print('couldnt create'+self.config)                               
        try:                                                    # every startup config.json has to be read once so the current note from last session can be retrieved.              
            with open(self.config,'r') as f:                    # if something goes wrong
                self.currentNote=json.load(f)['currentNote']            
                f.close()
        except:                                                 # if something goes wrong reading the config.json
            print("something went wrong reading the currentnote")
            with open(self.config,'w') as f: 
                json.dump({'currentNote':'%s' % (self.note)},f)
                f.close()
            with open(self.config,'r') as f:                    
                self.currentNote=json.load(f)['currentNote']            
                f.close()
        print("setup done")

    def ChangeCurrentNote(self,path):                               # takes in a path as a parameter and updates self.currentnote AND config.json
        self.currentNote = path
        config = {'currentNote':'%s' % (self.currentNote)}
        with open(self.config,'w') as f:
            json.dump(config,f)
            f.close()
        print("changed current note to: "+self.currentNote)

    def OptDelete(self,event=None):                                 # cannot use opt+backspace in tk.text. workaround is by creating the event of holding shift, opt and going left every time i press opt+backspace.
        self.text1.event_generate('<Shift-Mod2-Left>')

    def run(self):
        self.mainwindow.mainloop()

    def Read(self,event=None):                                      # reads the self.current note   
        with open(self.currentNote,'r') as f:                       # reading the .txt file and making the array output.
            output=f.readlines()
            f.close()
        self.text1.delete('1.0','end-1c')                           # deleting what text was there before
        for x in range(0,len(output)):                              # filling the text1 
            self.text1.insert('%s.0'%(x+1),output[x])               
        print("read")
        pass

    def Revert(self,event=None):                                    # simply reverts to the defualt note
        self.Save()
        self.ChangeCurrentNote(path=self.note)
        self.Read()

    def OpenFleDialog(self):                                        # file dialog to choose a new txt file to read and edit. Returns the chosen path
        self.toplevel1.overrideredirect(False)                      # the file dialof of tkinter is bugged. It intervenes with accessing the text1 module. Deactivating overridirrect shortly fixes it
        currentNote = filedialog.askopenfilename(
            title="Select your .txt file",
            initialdir=self.localPath+'/../../..',
            filetypes=(("text files","*.txt"),))                    # only .txt files selectable
        if (currentNote==''): currentNote= self.note                # if nothing is chose, the default note is set t the current path
        print("opened file dialog")
        return currentNote
        
    def Open(self,event=None):                                      # executes OpenFileDialog 
        self.Save() 
        self.ChangeCurrentNote(path=self.OpenFleDialog())           

        self.toplevel1.focus_force()                                #   
        self.toplevel1.overrideredirect(True)                       #
        self.toplevel1.attributes('-topmost', True)                 # all 3 lines needed to combat filedialog issues

        self.Read()
        print("opened")
        pass

    def Save(self,event=None):
        with open(self.currentNote,'w+') as f:                      
            f.writelines(self.text1.get("1.0","end-1c"))
            f.close()
        print("saved")
        pass
    
    def OpenWindow(self,event=None):                                # under development. No real use yet
        window = tk.Toplevel()
        window.minsize(230, 200)
        x,y=self.toplevel1.winfo_x(),self.toplevel1.winfo_y()
        window.geometry("+%s+%s" % ( x - self.toplevel1.winfo_width(), y ))
        window.resizable(True, True)
        window.title("Notepad")
        window.attributes('-topmost', True) 

        frame1 = ttk.Frame(window)
        frame1.configure(height=200, width=200)
        text1 = tk.Text(frame1)
        text1.configure(
            font="{Apple Braille} 13 {}",
            highlightbackground="#1e1e1e",
            highlightcolor="#1e1e1e",
            tabs=30,
            undo="true",
            wrap="word",
        )
        text1.pack(expand="true", fill="both", side="top")
        frame1.pack(expand="true", fill="both", side="top")
        frame1.pack_propagate(0)
        pass

    def Quit(self,event):                                           # quits. Tries to save.
        try: self.Save()
        finally: self.toplevel1.quit()
    
    def SaveLastClickPos(self,event):                               # needed so the step between clicking and dragging doesnt have a ?pixel jump?                
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def Dragging(self,event):
        x, y = event.x - lastClickX + self.toplevel1.winfo_x(), event.y - lastClickY + self.toplevel1.winfo_y()
        self.toplevel1.geometry("+%s+%s" % (x , y))
    
    def Resize(self,event):
        x, y = event.x - lastClickX + self.toplevel1.winfo_width(), event.y - lastClickY + self.toplevel1.winfo_height()
        self.toplevel1.geometry("%sx%s" % (x , y))


if __name__ == "__main__":
    app = NewprojectApp()
    app.run()

