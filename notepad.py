import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

def CodeText (S, Key):
    SS = ""
    for i in range(len(S)):
        C = S[i]
        K = ord(C) ^ Key
        CC = chr(K)
        SS = SS + CC
    return (SS)

class Notepad:
    __form = Tk()
    __thisWidth = 300
    __thisHeight = 300
    __keyS = 19
    __keyP = 13
    __thisTextArea = Text(__form,  wrap=NONE)
    __thisMenuBar = Menu(__form)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=False)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=False)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=False)
    __heightScrollBar = Scrollbar(__thisTextArea)
    __widthScrollBar = Scrollbar(__thisTextArea, orient=HORIZONTAL)
    __file = None
    __emptyBar = Label(__form, text=" ", bd=1, relief=SUNKEN, anchor=W)
    __cursorBar = Label(__form, text="Стр 1, стлб 1", bd=1, relief=SUNKEN, anchor=W)
    __percentBar = Label(__form, text="100%", bd=1, relief=SUNKEN, anchor=W)
    __systemBar = Label(__form, text="Windows(CRLF)", bd=1, relief=SUNKEN, anchor=W)
    __encodingBar = Label(__form, text="UTF-8", bd=1, relief=SUNKEN, anchor=W)

    def __init__(self, **kwargs):
        try:
            self.__form.wm_iconbitmap("Notepad.ico")
        except:
            pass
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass
        self.__form.title("Безымянный - Блокнот")
        screenWidth = self.__form.winfo_screenwidth()
        screenHeight = self.__form.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__form.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))
        self.__form.grid_rowconfigure(0, weight=1)
        self.__form.grid_columnconfigure(0, weight=1)
        self.__thisTextArea.grid(sticky=NSEW, columnspan=5)
        self.__emptyBar.grid(row=1, column=0, columnspan=1, sticky=W+E)
        self.__cursorBar.grid(row=1, column=1, columnspan=1, sticky=W+E)
        self.__percentBar.grid(row=1, column=2, columnspan=1, sticky=W+E)
        self.__systemBar.grid(row=1, column=3, columnspan=1, sticky=W+E)
        self.__encodingBar.grid(row=1, column=4, columnspan=1, sticky=W+E)
        self.__form.grid_columnconfigure(0, weight=7)
        self.__form.grid_columnconfigure(1, weight=1)
        self.__form.grid_columnconfigure(2, weight=1)
        self.__form.grid_columnconfigure(3, weight=1)
        self.__form.grid_columnconfigure(4, weight=2)
        self.__form.config(menu=self.__thisMenuBar)
        self.__thisMenuBar.add_cascade(label="Файл", menu=self.__thisFileMenu)
        self.__thisFileMenu.add_command(label="Новый", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Открыть...", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Сохранить", command=self.__saveFile)
        self.__thisFileMenu.add_command(label="Сохранить как...", command=self.__saveFileAs)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Выход", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="Правка", menu=self.__thisEditMenu)
        self.__thisEditMenu.add_command(label="Вырезать", command=self.__cut)
        self.__thisEditMenu.add_command(label="Копировать", command=self.__copy)
        self.__thisEditMenu.add_command(label="Вставить", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Справка", menu=self.__thisHelpMenu)
        self.__thisHelpMenu.add_command(label="Содержание", command=self.__contents)
        self.__thisHelpMenu.add_separator()
        self.__thisHelpMenu.add_command(label="О программе...", command=self.__showAbout)
        self.__heightScrollBar.pack(side=RIGHT, fill=Y)
        self.__widthScrollBar.pack(side=BOTTOM, fill=X)
        self.__heightScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__heightScrollBar.set)
        self.__widthScrollBar.config(command=self.__thisTextArea.xview)
        self.__thisTextArea.config(xscrollcommand=self.__widthScrollBar.set)
        self.__update_label()

    def __update_label(self):
        row, col = self.__thisTextArea.index('insert').split('.')
        self.__cursorBar.config(text=f'Стр {row}, стлб {str(int(col)+1)}')
        self.__form.after(100, self.__update_label)

    def __quitApplication(self):
        self.__form.destroy()

    def __showAbout(self):
        showinfo("О программе", "Программа для 'прозрачного шифрования'")

    def __contents(self):
        def content_close():
            form_ref.destroy()
        form_ref = Tk()
        form_ref.resizable(False, False)
        form_ref.title('Справка')
        try:
            form_ref.wm_iconbitmap("info.ico")
        except:
            pass
        form_ref.geometry("400x150+150+100")
        label1 = Label(form_ref,
                       text="Приложение с графическим интерфейсом \"Блокнот TCD\" (файл приложения: TCD). Позволяет: создавать / открывать / сохранять зашифрованный текстовый файл, предусмотрены ввод и сохранение личного ключа, вывод не модальной формы \"Справка\", вывод модальной формы \"О программе\"",
                       wraplength=400, justify=LEFT)
        label1.place(relx=0.5, rely=0.3, anchor='center')
        button_close = Button(form_ref, text="Закрыть", command=content_close)
        button_close.place(x=320, y=100, width=60, height=30)

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if self.__file == "":
            self.__file = None
        else:
            self.__form.title(os.path.basename(self.__file) + ' - Блокнот')
            self.__thisTextArea.delete(1.0, END)
            with open(self.__file, mode='r', encoding="utf-8") as F:
                S = F.read()
                Slines = S.splitlines()
                Key = int(Slines[1].replace('Key=', ''))*self.__keyS
                Slines = Slines[2:]
                it='\n'
                S = it.join(Slines)
            S = CodeText(S, Key)
            self.__thisTextArea.insert(1.0, S)

    def __newFile(self):
        self.__form.title("Безымянный - Блокнот")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):
        if self.__file is None:
            self.__saveFileAs()
        else:
            Key = self.__keyP*self.__keyS
            S = CodeText(self.__thisTextArea.get(1.0, END), Key)
            with open(self.__file, mode='w', encoding="utf-8") as F:
                F.write("[main]\nKey="+str(self.__keyP)+"\n"+S)

    def __saveFileAs(self):
        self.__file = asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if self.__file == "":
            self.__file = None
        else:
            Key = self.__keyP * self.__keyS
            S = CodeText(self.__thisTextArea.get(1.0, END), Key)
            with open(self.__file, mode='w', encoding="utf-8") as F:
                F.write("[main]\nKey="+str(self.__keyP)+"\n"+S)
            self.__form.title(os.path.basename(self.__file) + ' - Блокнот')

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__form.mainloop()


notepad = Notepad(width=600, height=400)
notepad.run()