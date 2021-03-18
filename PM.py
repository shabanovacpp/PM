import tkinter as tk
import tkinter.messagebox
import os

def fTtM(name): #from text to mp3
    os.rename(name, os.path.splitext(name)[0] + '.mp3')
def fMtT(name): #from mp3 to text
    os.rename(name, os.path.splitext(name)[0] + '.txt')

    
passwords = {}
PATHm = "C:\pass\da.mp3"
PATHt = "C:\pass\da.txt"

if os.path.exists(PATHm):
    fMtT(PATHm)
    lines = 0
    file = open(PATHt)
    with open(PATHt) as f:
        for line in f:
            lines += 1
    for i in range (lines):
        s = file.readline()
        passwords[s[0:s.find(':')]] = s[s.find(':') + 1:s.find('\n'):]
    file.close()
    fTtM(PATHt)
else:
    if (os.access("C:\pass", os.F_OK)) == False:
        os.mkdir("C:\pass")
    f = open(PATHt, 'a')
    f.close()
    fTtM(PATHt)

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder=None):
        super().__init__(master)

        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = '#DAD9C6'
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


class AddFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self['bg'] = '#2D2D2D'
        self.nameEnt = EntryWithPlaceholder(self, 'name')
        self.nameEnt['bg'] = 'grey'
        self.nameEnt.pack(pady = 1)
        self.passwordEnt = EntryWithPlaceholder(self, 'password')
        self.passwordEnt['bg'] = 'grey'
        self.passwordEnt.pack(pady = 1)
        self.addBtn = tk.Button(self, text = 'add', width = 5, bg = '#DAD9C6', command = self.addNew, activebackground='#DAD9C6', relief = 'flat')
        self.addBtn.pack(pady = 5)

    def addNew(self):
        passwords[self.nameEnt.get()] = self.passwordEnt.get()
        fMtT(PATHm)
        fileP = open("C:\pass\da.txt", 'a+')
        if self.nameEnt.get() != 'name' and self.passwordEnt.get() != 'password' and self.nameEnt.get() != '' and self.passwordEnt.get() != '':
             fileP.write(self.nameEnt.get() + ':' + self.passwordEnt.get() + '\n')
             tkinter.messagebox.showinfo('','password was added')
        fileP.close()
        fTtM(PATHt)
        self.nameEnt.delete(0, 'end')
        self.nameEnt.focus_out()
        
        self.passwordEnt.delete(0, 'end')
        self.passwordEnt.focus_out()
        


class GetFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self['bg'] = '#2D2D2D'
        self.nameEnt = EntryWithPlaceholder(self, 'name')
        self.nameEnt['bg'] = 'grey'
        self.nameEnt.pack()
        self.getBtn = tk.Button(self, text = 'copy', width = 5, bg = '#DAD9C6', activebackground='#DAD9C6', relief = 'flat', command = self.cop)
        self.getBtn.pack(pady = 5)

        self.listOfNames = tk.Listbox(self, relief = 'flat', bg = 'grey', fg = '#DAD9C6', selectbackground = 'grey', \
                                      highlightthickness = 0, highlightcolor = 'grey', height = 4, justify='center')
        self.listOfNames.yview_scroll(1, 'units')
        self.listOfNames.pack(pady = 30)
        
        self.listOfNames.insert(1, 'your passwords:')
        self.listOfNames.itemconfig('end', background = '#2D2D2D')
        for i in range (len(list(passwords.keys()))):
            self.listOfNames.insert(i+2, list(passwords.keys())[i])

    def cop(self):
        if self.nameEnt.get() != 'name':
            if self.nameEnt.get() in passwords:
                pas = passwords[self.nameEnt.get()]
                clip = tk.Tk()
                clip.withdraw()
                clip.clipboard_clear()
                clip.clipboard_append(pas) 
                clip.destroy()
            else:
                tkinter.messagebox.showinfo('','there is no that password')
    

class DelFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self['bg'] = '#2D2D2D'
        self.nameEnt = EntryWithPlaceholder(self, 'name')
        self.nameEnt['bg'] = 'grey'
        self.nameEnt.pack()
        self.getBtn = tk.Button(self, text = 'delete', width = 5, bg = '#DAD9C6', activebackground='#DAD9C6', relief = 'flat', command = self.dell)
        self.getBtn.pack(pady = 5)

        self.listOfNames = tk.Listbox(self, relief = 'flat', bg = 'grey', fg = '#DAD9C6', selectbackground = 'grey', \
                                      highlightthickness = 0, highlightcolor = 'grey', height = 4, justify='center')
        self.listOfNames.pack(pady = 30)

        self.listOfNames.insert(1, 'your passwords:')
        self.listOfNames.itemconfig(0, background = '#2D2D2D')
        for i in range (len(list(passwords.keys()))):
            self.listOfNames.insert(i+2, list(passwords.keys())[i])

    def dell(self):
        if self.nameEnt.get() != 'name':
            if self.nameEnt.get() in passwords:
                fMtT(PATHm)
                f = open("C:\pass\da.txt")
                lines = f.readlines()
                f.close()
                f = open("C:\pass\da.txt", "w")
                for line in lines:
                    if line!=self.nameEnt.get()+":"+passwords[self.nameEnt.get()]+"\n":
                        f.write(line)
                f.close()
                fTtM(PATHt)
                del passwords[self.nameEnt.get()]
                self.listOfNames.delete(0,'end')
                for i in range (len(list(passwords.keys()))):
                    self.listOfNames.insert(i+1, list(passwords.keys())[i])
                tkinter.messagebox.showinfo('','password was deleted')
            else:
                tkinter.messagebox.showinfo('','there is no that password')

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title('PM')
        if os.path.exists('PM.ico'):
            self.iconbitmap('PM.ico')
        self.geometry('600x300+%d+%d'%(screen_width/2 - 320, screen_height/2 - 150))
        self.config(bg = '#2D2D2D')
        self.resizable(width = False, height = False)
        
        self.addBtn = tk.Button(self, text = 'add new password', width = 80, command = self.showAdd, bg = '#DAD9C6', activebackground='#DAD9C6', relief = 'flat')
        self.getBtn = tk.Button(self, text = 'get password', width = 80, command = self.showGet, bg = '#DAD9C6', activebackground='#DAD9C6', relief = 'flat')
        self.delBtn = tk.Button(self, text = 'delete password', width = 15, command = self.showDel, bg = '#DAD9C6', activebackground='#DAD9C6', relief = 'flat')
        self.addBtn.pack(side = 'top', pady = 7)
        self.getBtn.pack(side = 'top')
        self.delBtn.pack(side = 'top', pady = 7)

        self.frame_add = AddFrame()
        self.frame_add.destroy()

        self.frame_get = GetFrame()
        self.frame_get.destroy()

        self.frame_del = DelFrame()
        self.frame_del.destroy()
        
    def showAdd(self):
        if self.frame_add.winfo_exists() == False:
            self.frame_add = AddFrame()
            self.frame_add.pack(pady = 20)
        if self.frame_get.winfo_exists():
            self.frame_get.destroy()
        if self.frame_del.winfo_exists():
            self.frame_del.destroy()
    def showGet(self):
        if self.frame_get.winfo_exists() == False:
            self.frame_get = GetFrame()
            self.frame_get.pack(pady = 20)
        if self.frame_add.winfo_exists():
            self.frame_add.destroy()
        if self.frame_del.winfo_exists():
            self.frame_del.destroy()
    def showDel(self):
        if self.frame_del.winfo_exists() == False:
            self.frame_del = DelFrame()
            self.frame_del.pack(pady = 20)
        if self.frame_get.winfo_exists():
            self.frame_get.destroy()
        if self.frame_add.winfo_exists():
            self.frame_add.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
