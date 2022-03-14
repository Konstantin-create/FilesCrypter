#  pyinstaller --onefile --noconsole --hidden-import=pyAesCrypt -i "images/icons/icon.ico" gui.py
import os, sys
import webbrowser as wb
import pyAesCrypt
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from PIL import Image, ImageTk

try:
    os.mkdir("users")
except:
    pass


class App:
    def __init__(self):
        # Create window
        self.root = Tk()
        self.root.iconbitmap("images/icons/icon.ico")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.title("FileLocker")

        # Variabes
        self.font_size = 25
        self.text_size = 22
        self.user_name = ""
        self.true_window = False

        # Authorisation screen
        self.titleLabel = Label(self.root, text="Files Locker", font=("LetterOMatic!", 50), fg="#000")
        self.authorization_layout = Frame(self.root)
        self.user_nameLabel = Label(self.authorization_layout, text="User: ", font=("Century Gothic", 45))
        self.user_nameEntry = Entry(self.authorization_layout, font=("Century Gothic", 40))
        self.user_nameEntry.focus_set()
        self.password_nameLabel = Label(self.authorization_layout, text="Password: ", font=("Century Gothic", 45))
        self.password_nameEntry = Entry(self.authorization_layout, font=("Century Gothic", 40), show="*")
        self.buttons_layout = Frame(self.root)
        self.logInButton = Button(self.buttons_layout, text="Log In", font=("Century Gothic", 40), command=self.login)
        self.signUpButton = Button(self.buttons_layout, text="Sign Up", font=("Century Gothic", 40),
                                   command=self.create_acount)

        # Sign Up screen
        self.registaration_title = Label(self.root, text="Sign Up", font=("LetterOMatic!", 50), fg="#000")
        self.signUpButton2 = Button(self.root, text="Sign Up", font=("Century Gothic", 40),
                                    command=self.signUp)

        # Files system screen
        # Images
        self.addImage = ImageTk.PhotoImage(file="images/add.png")
        self.openImage = ImageTk.PhotoImage(file="images/open.png")
        self.saveImage = ImageTk.PhotoImage(file="images/save.png")
        self.deleteImage = ImageTk.PhotoImage(file="images/trash.png")
        self.infoImage = ImageTk.PhotoImage(file="images/info.png")

        self.file_layout = LabelFrame(self.root, text="Files Locker", font=("LetterOMatic!", 20), fg="#000")
        self.file_list_layout = Frame(self.file_layout)
        self.fileXScroll = Scrollbar(self.file_layout, orient=HORIZONTAL)
        self.fileYScroll = Scrollbar(self.file_list_layout)
        self.fileList = Listbox(self.file_list_layout, font=("Century Gothic", 40), width=10, height=15,
                                xscrollcommand=self.fileXScroll.set,
                                yscrollcommand=self.fileYScroll.set)
        self.fileXScroll.configure(command=self.fileList.xview)
        self.fileYScroll.configure(command=self.fileList.yview)
        self.contentArea = Frame(self.root)
        self.controlArea = Label(self.contentArea)
        self.addButton = Button(self.controlArea, image=self.addImage, command=self.add_file)
        self.openButton = Button(self.controlArea, image=self.openImage, command=self.open_txt_file)
        self.deleteButton = Button(self.controlArea, image=self.deleteImage, command=self.delete_file)
        self.saveButton = Button(self.controlArea, image=self.saveImage, command=self.save_file)
        self.infoButton = Button(self.controlArea, image=self.infoImage, command=self.open_documentation)
        self.contentScroll = Scrollbar(self.contentArea)
        self.contentTextArea = Text(self.contentArea, font=("Century Gothic", self.font_size), bg="#fff", fg="#000",
                                    width=80, height=self.text_size, yscrollcommand=self.contentScroll.set)
        self.contentScroll.configure(command=self.contentTextArea.yview)

        # Images
        self.find_fileImage = ImageTk.PhotoImage(file="images/find.png")

        self.addTitleLabel = Label(self.root, text="Add file", font=("LetterOMatic!", 50), fg="#000")
        self.file_path_layout = Frame(self.root)
        self.file_pathLabel = Label(self.file_path_layout, text="File Path: ", font=("Century Gothic", 45))
        self.file_pathEntry = Entry(self.file_path_layout, font=("Century Gothic", 45), bg="#fff", fg="#000", width=20)
        self.find_fileButton = Button(self.file_path_layout, image=self.find_fileImage, border=0,
                                      command=self.open_file)
        self.file_buttons_layout = Frame(self.root)
        self.protect_fileButton = Button(self.file_buttons_layout, text="Protect file", font=("Century Gothic", 40),
                                         command=self.protect_file)
        self.come_backButton = Button(self.file_buttons_layout, text="Back", font=("Century Gothic", 40),
                                      command=self.file_menu)

    def crypt(self, file):
        password = "pardus"
        bufferSize = 512 * 1024
        pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, bufferSize)
        os.remove(file)

    def decrypt(self, file):
        password = "pardus"
        bufferSize = 512 * 1024
        pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password, bufferSize)
        os.remove(file)

    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        self.file_pathEntry.delete(0, "end")
        self.file_pathEntry.insert(0, file)

    def protect_file(self):
        file_path = str(self.file_pathEntry.get())
        if os.path.exists(file_path):
            if file_path[file_path.rfind("."):] == ".txt":
                with open(f"users/{self.user_name}/file_paths.txt", "a") as file:
                    self.crypt(file_path)
                    file.write(file_path + ".crp" + ";")
                    file.close()
                mb.showinfo("Info", "File was protected")
                self.file_menu()
            else:
                mb.showerror("Error", "Please select .txt file")
        else:
            mb.showerror("Error", "Such a file does not exist")

    def open_txt_file(self):
        try:
            file_path = self.fileList.get(self.fileList.curselection())
            self.file_path_to_save = file_path
            self.decrypt(file_path)
            with open(file_path[:file_path.rfind(".")], "r") as file:
                self.contentTextArea.delete('1.0', END)
                self.contentTextArea.insert(END, file.read())
                file.close()
            self.crypt(file_path[:file_path.rfind(".")])
            mb.showinfo("Info", "The file was open")
        except:
            mb.showerror("Error", "Select file")

    def delete_file(self):
        try:
            file_path = self.fileList.get(self.fileList.curselection())
            with open(f"users/{self.user_name}/file_paths.txt", "r") as file:
                content = file.read()
                file.close()
            with open(f"users//{self.user_name}//file_paths.txt", "w") as file:
                file.write(content.replace(file_path + ";", ""))
                file.close()
            self.decrypt(file_path)
            self.update_file_list()
            self.contentTextArea.delete("1.0", END)
            mb.showinfo("Info", "Protection was removed from the file")
        except Exception as e:
            mb.showerror("Error", f"Select file {e}")

    def save_file(self):
        self.decrypt(self.file_path_to_save)
        with open(self.file_path_to_save[:self.file_path_to_save.rfind(".")], "w") as file:
            file.write(self.contentTextArea.get("1.0", END))
            file.close()
        self.crypt(self.file_path_to_save[:self.file_path_to_save.rfind(".")])

    def open_documentation(self):
        try:
            wb.register('chrome',
                                None,
                                wb.BackgroundBrowser(
                                    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
            print(os.getcwd())
            wb.get('chrome').open(f"{os.getcwd()}\doc\index.html")
        except:
            wb.open_new_tab(f"{os.getcwd()}\doc\index.html")

    def clean(self):
        self.titleLabel.pack_forget()
        self.authorization_layout.pack_forget()
        self.buttons_layout.pack_forget()

        self.registaration_title.pack_forget()
        self.signUpButton2.pack_forget()

        self.file_layout.pack_forget()
        self.contentArea.pack_forget()

        self.addTitleLabel.pack_forget()
        self.file_path_layout.pack_forget()
        self.file_buttons_layout.pack_forget()

    def login(self):
        try:
            with open(f"users\\{str(self.user_nameEntry.get())}\\password.txt", "r") as file:
                if file.read() == str(self.password_nameEntry.get()):
                    self.user_name = str(self.user_nameEntry.get())
                    self.file_menu()
                else:
                    mb.showerror("Error", "Wrong password")
                file.close()
        except Exception as e:
            mb.showerror("Error", f"Wrong user name {e}")

    def signUp(self):
        try:
            os.mkdir(f"users/{str(self.user_nameEntry.get())}")
            with open(f"users/{str(self.user_nameEntry.get())}/password.txt", "w") as file:
                file.write(str(self.password_nameEntry.get()))
                file.close()
        except:
            mb.showerror("Error", "Such a user already exists")
        self.root.update()

    def change_cursor(self, event, item):
        if item == 0:
            self.password_nameEntry.focus_set()
        elif self.true_window:
            if item == 1:
                self.protect_file()
            elif item == 2:
                self.open_file()
            elif item == 3:
                if mb.askyesno("Question", "Do you really want to remove the protection from the file?"):
                    self.delete_file()
            if item == 4:
                if mb.askyesno("Question", "Do you really want to exit?"):
                    try:
                        if self.fileList.get(self.fileList.curselection()) != "":
                            self.save_file()
                    except:
                        pass
                    self.root.destroy()
                    sys.exit()

    def authorization(self):
        self.true_window = False
        self.titleLabel.pack(pady=30)
        self.authorization_layout.pack(pady=75)
        self.user_nameLabel.grid(row=0, column=0)
        self.user_nameEntry.grid(row=0, column=1)
        self.password_nameLabel.grid(row=1, column=0)
        self.password_nameEntry.grid(row=1, column=1)
        self.buttons_layout.pack(pady=50)
        self.logInButton.grid(row=0, column=0, padx=25)
        self.signUpButton.grid(row=0, column=1, padx=25)

    def create_acount(self):
        self.true_window = False
        self.clean()
        self.registaration_title.pack(pady=30)
        self.authorization_layout.pack(pady=75)
        self.user_nameLabel.grid(row=0, column=0)
        self.user_nameEntry.grid(row=0, column=1)
        self.password_nameLabel.grid(row=1, column=0)
        self.password_nameEntry.grid(row=1, column=1)
        self.signUpButton2.pack(side=BOTTOM, pady=100)

    def update_file_list(self):
        self.fileList.delete(0, END)
        with open(f"users/{self.user_name}/file_paths.txt", "r") as file:
            file_path0 = file.read().split(";")
            value = ""
            for i in range(len(file_path0) - 1):
                if os.path.exists(file_path0[i]):
                    value += str(file_path0[i]) + ";"
                else:
                    mb.showerror("Error", f"File {file_path0[i]} does not exists")
            file.close()
        with open(f"users/{self.user_name}/file_paths.txt", "w") as file:
            file.write(value)
            file.close()

        try:
            with open(f"users/{self.user_name}/file_paths.txt") as file:
                file_paths = str(file.read()).split(";")
                for i in range(len(file_paths) - 1):
                    file_path = file_paths[i]
                    self.fileList.insert(0, str(file_path))
                file.close()
        except Exception as e:
            mb.showerror("Error", str(e))

    def file_menu(self):
        self.true_window = True
        self.clean()
        self.update_file_list()

        self.file_layout.pack(side=LEFT, padx=20)
        self.fileList.pack(side=LEFT)
        self.file_list_layout.pack()
        self.fileYScroll.pack(side=LEFT, fill=Y)
        self.fileXScroll.pack(fill=X)
        self.contentArea.pack(side=LEFT, padx=30)
        self.controlArea.pack(fill=X)
        self.addButton.pack(side=LEFT, padx=5)
        self.openButton.pack(side=LEFT, padx=5)
        self.deleteButton.pack(side=LEFT, padx=5)
        self.saveButton.pack(side=LEFT, padx=5)
        self.infoButton.pack(side=LEFT, padx=5)
        self.contentTextArea.pack(side=LEFT, anchor=NW)
        self.contentScroll.pack(side=LEFT, fill=Y)

    def add_file(self):
        self.true_window = False
        self.clean()
        self.addTitleLabel.pack(pady=30)
        self.file_path_layout.pack(pady=175)
        self.file_pathLabel.grid(row=0, column=0)
        self.file_pathEntry.grid(row=0, column=1)
        self.find_fileButton.grid(row=0, column=2)
        self.file_buttons_layout.pack(pady=50)
        self.protect_fileButton.pack(side=LEFT, padx=20)
        self.come_backButton.pack(side=LEFT, padx=20)


app = App()

app.authorization()

# Mainloop
app.user_nameEntry.bind("<Return>", lambda a: app.change_cursor(a, 0))
app.root.bind("<Control-n>", lambda a: app.change_cursor(a, 1))
app.root.bind("<Control-o>", lambda a: app.change_cursor(a, 2))
app.root.bind("<Control-w>", lambda a: app.change_cursor(a, 3))
app.root.bind("<Escape>", lambda a: app.change_cursor(a, 4))
app.root.mainloop()
