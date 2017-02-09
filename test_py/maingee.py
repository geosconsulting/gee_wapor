#!/usr/bin/env

from Tkinter import Tk, BooleanVar, BOTH, RAISED, RIGHT, LEFT, StringVar
from Tkinter import Menu, Checkbutton, Text
from ttk import Frame, Button, Style, Combobox
import tkFileDialog


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("GEE Manage")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)

        self.box_value_operazione = StringVar()
        self.box_operazione = Combobox(frame, textvariable=[])
        self.box_operazione['values'] = ['Upload', 'Delete', 'Cancel']
        self.box_operazione.pack(side=LEFT)

        menubar.add_cascade(label="File", menu=fileMenu)

        submenu = Menu(fileMenu)
        submenu.add_command(label="Crea Metadata")
        submenu.add_command(label="Import Metadata CSV")
        fileMenu.add_cascade(label='Metadata', menu=submenu, underline=0)

        fileMenu.add_separator()

        fileMenu.add_command(label="Help", command=self.onAiuto)
        fileMenu.add_command(label="Exit", command=self.onExit)

        self.var = BooleanVar()
        cb = Checkbutton(self.parent, text="Lunga Transazione",
                         variable=self.var, command=self.onClickLunga)
        cb.select()
        cb.place(x=300, y=350)

        closeButton = Button(self, text="Close",command=self.quit)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT)

        select_file = Button(self.parent, text="Select Directory", command=self.open_file_chooser)
        select_file.pack(side=LEFT)

    def onClickLunga(self):

        if self.var.get() == True:
            iltitolo = self.master.title("GEE Manage -- Long Transaction")


    def onExit(self):
        self.quit()

    def onAiuto(self):
        pass

    def open_file_chooser(self):

        nomeFile = tkFileDialog.askdirectory(parent=self.parent, title='Directory')


def main():

    root = Tk()
    root.geometry("450x450+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
