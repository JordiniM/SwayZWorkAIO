import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter

dirFiles = []
extension = []

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    prefixLength = 0
    directory = ""

    def __init__(self):

        super().__init__()

        # configure window
        self.title("Sway-Z Work AIO v2.0")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("swayzico.ico")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #
        # create listbox
        #
        self.dirlist = ttk.Treeview(self, column=("Filename", "Extension", "Size"), show='headings', height=5, )
        self.dirlist.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.dirlist.column("Filename", anchor=CENTER)
        self.dirlist.heading("Filename", text="Filename")

        self.dirlist.column("Extension", anchor=CENTER, width=100)
        self.dirlist.heading("Extension", text="Extension")

        self.dirlist.column("Size", anchor=CENTER, width=100)
        self.dirlist.heading("Size", text="Size")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Sway-Z Work AIO", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(50, 10))

        self.sidebar_status = True
        self.sidebarControl = customtkinter.CTkButton(self, font=("Times New Roman", 18), text="☰", width=1, hover_color="black", bg_color="transparent",
                                                      fg_color="transparent", text_color=("gray10", "#DCE4EE"), command=self.toggleSidebar)
        self.sidebarControl.grid(row=0, column=0, pady=5, sticky='nw')

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.conversionProgress = customtkinter.CTkProgressBar(self)
        self.conversionProgress.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(30, 30), sticky="nsew")

        self.convertButton = customtkinter.CTkButton(master=self, text="Convert", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                     command=self.convertFiles)
        self.convertButton.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #
        # create tabview for ST01 etc
        #
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, rowspan=2, column=2, padx=(20, 0), pady=(3, 0), sticky="nsew")
        self.tabview.add("Sort")
        self.tabview.tab("Sort").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.sortNameCheck = customtkinter.CTkCheckBox(self.tabview.tab("Sort"), text="# segments in order by name", command=self.enableRenameCombobox)
        self.sortNameCheck.grid(row=0, column=0, padx=0, pady=(20, 10))

        customtkinter.CTkLabel(self.tabview.tab("Sort"), text="Add prefix to numbers:").grid(row=1, column=0, padx=0, pady=(10, 10))

        self.sortNameVar = StringVar()
        self.sortNameVar.trace('w', self.updateList)
        self.sortNameCombobox = customtkinter.CTkComboBox(self.tabview.tab("Sort"), variable=self.sortNameVar, values=["ST", "SN"], state="disabled")
        self.sortNameCombobox.grid(row=2, column=0, padx=0, pady=(10, 10))

        customtkinter.CTkLabel(self.tabview.tab("Sort"), text="Keep first # of characters:").grid(row=3, column=0, padx=0, pady=(10, 10))

        self.sortCharsVar = StringVar(self, "3")
        self.sortCharsVar.trace('w', self.updateList)
        self.sortChars = customtkinter.CTkComboBox(self.tabview.tab("Sort"), variable=self.sortCharsVar, values=["3", "4", "5", "6"], width=75)
        self.sortChars.grid(row=4, column=0, padx=0, pady=(0, 10))

        self.sortConvertButton = customtkinter.CTkButton(self.tabview.tab("Sort"), text="Convert", command=self.replaceConvert)
        self.sortConvertButton.grid(row=5, column=0, padx=0, pady=(10, 10))

        #
        # EXTENSIONS
        #
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.extensionsLabel = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Convert File Extensions", anchor="center")
        self.extensionsLabel.grid(row=0, column=2, columnspan=1, padx=20, pady=10, sticky="")
        self.wavCheckbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text=".wav", command=self.open_dir)
        self.wavCheckbox.grid(row=1, column=2, pady=(20, 0), padx=20)
        self.mp3Checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text=".mp3", command=self.open_dir)
        self.mp3Checkbox.grid(row=2, column=2, pady=(20, 0), padx=20, sticky="n")
        self.oggCheckbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text=".ogg", command=self.open_dir)
        self.oggCheckbox.grid(row=3, column=2, pady=20, padx=20, sticky="n")

        # create radiobutton frame
        self.openPath_frame = customtkinter.CTkFrame(self)
        self.openPath_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.openInExplorerCheckbox = customtkinter.CTkCheckBox(self.openPath_frame, text="Open in File Explorer")
        self.openInExplorerCheckbox.grid(row=0, column=2, padx=20, pady=10, sticky="n")
        self.openInExplorerCheckbox.select()

        self.openFolder = customtkinter.CTkButton(self.openPath_frame, command=self.openFolder, text="Open Folder")
        self.openFolder.grid(row=1, column=2, padx=20, pady=10, sticky="n")

        customtkinter.CTkLabel(self.openPath_frame, text="or enter path:").grid(row=2, column=2, padx=20, pady=10, sticky="n")

        self.enterPathVar = StringVar()
        self.enterPathVar.trace('w', self.updatePath)
        self.enterPath = customtkinter.CTkEntry(self.openPath_frame, textvariable=self.enterPathVar)
        self.enterPath.grid(row=3, column=2, padx=20, pady=0, sticky="n")

        #
        # FILENAME OPTIONS
        #
        self.filename_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filename_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.filename_frame.grid_columnconfigure(0, weight=1)
        self.filename_frame.grid_rowconfigure(4, weight=1)

        self.filenameOptionsLabel = customtkinter.CTkLabel(self.filename_frame, text="Filename Options", anchor="w", font=("Roboto", 16))
        self.filenameOptionsLabel.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.charactersLabel = customtkinter.CTkLabel(self.filename_frame, text="How many characters to keep:")
        self.charactersLabel.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="w")

        self.charactersComboVar = StringVar(self, "4")
        self.charactersComboVar.trace('w', self.updateList)
        self.charactersCombobox = customtkinter.CTkComboBox(self.filename_frame, variable=self.charactersComboVar, values=["4", "5", "6", "ALL"], width=75)
        self.charactersCombobox.grid(row=1, column=0, padx=(200, 0), pady=(0, 0), sticky="w")
        self.enablePrefixCheckbox = customtkinter.CTkCheckBox(self.filename_frame, text="Add prefix to start of files", command=self.activatePrefixCombobox)
        self.enablePrefixCheckbox.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        self.prefixVar = StringVar()
        self.prefixVar.trace('w', self.updateList)
        self.prefixCombobox = customtkinter.CTkComboBox(self.filename_frame, variable=self.prefixVar, values=["PG1", "PG2"], width=150, state="disabled")
        self.prefixCombobox.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky="w")

        # set default values
        self.logo_label.bind("<Button-1>", lambda e: self.aboutSection())
        self.wavCheckbox.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.conversionProgress.set(0)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="white", columnbackground="black", highlightthickness=0, bd=0)
        style.configure("Treeview.Heading", background="#101010", foreground="white", borderwidth=0)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    storedList = []
    prefixName = ""

    def updateList(self, *args):
        index = 0
        self.clearList()
        self.storedList.clear()
        for file in dirFiles:
            if self.sortNameCheck.get():
                self.conversionProgress.set(.25)
                if self.sortCharsVar.get() == '':
                    self.storedList.append(file[:-260] + self.sortNameVar.get() + "{:02d}".format(index))
                else:
                    self.storedList.append(file[:-4][:int(self.sortCharsVar.get())] + self.sortNameVar.get() + "{:02d}".format(index))
            else:
                self.storedList.append(self.prefixVar.get() + file[:int(self.charactersComboVar.get())])
            self.dirlist.insert('', 'end',
                                values=(self.storedList[index], file[-4:], str(round(os.stat(f'{self.directory}\\{file}').st_size / 1024 / 1024, 2)) + " MB"))
            index += 1
        self.conversionProgress.set(.75)

    def enableRenameCombobox(self):
        if self.sortNameCheck.get():
            self.sortNameCombobox.configure(state="normal")
        else:
            self.sortNameCombobox.configure(state="disabled")

    def aboutSection(self):
        about = Toplevel(self)
        about.geometry("500x800")
        about.title("About Section")
        about.configure(bg="#202020")
        customtkinter.CTkLabel(about, text="Changelogs:", font=("Roboto", 24)).pack(pady=20)
        customtkinter.CTkLabel(about, anchor="w", wraplength=500, font=("Roboto", 12),
                               text="9/24/2020 v1.0 (1) -\n• Application released\n\n"
                                    "9/25/2020 v1.1 (4) -\n• Added changelogs\n• Added function for \"PG\" to be added before all filenames\n• Better dark mode functionality\n• Removed unnecessary message boxes when converting files\n\n"
                                    "9/26/2020 v1.2 (12) -\n• Added borders around elements\n• Users can now minimize the application\n• New navigation system, added tabs to give additional room for other content\n• List displays filesize in megabytes instead of kilobytes\n• Changed folder browse dialog window title from \"My Title\" to \"Select Folder for Conversion...\"\n• Replaced browse folder button with Folder Options\n• Added option to choose extensions to convert, and the user can update them in real time\n• Convert button now disabled until user selects directory\n• Users can now re-enter their directory path\n• Added option to open directory after conversion \n• Added \"Table\" tab to the navigation bar.\n• Added option to clear table in the table menu\n\n"
                                    "10/01/2020 v1.3 (14) -\n• Added tooltips to elements around the application\n• Changed element positions to improve visibility\n• Added number of fies under list\n• Added clear button under list as well\n• Disabled clear contents in table menu when previously cleared.\n• Users can now add custom strings / prefixes to the beginning of files.\n• Dark mode implementation drastically improved\n• Improved dark mode functionality\n• File list now refreshes after conversion\n• User can now convert multiple times in a row\n• Updated application icon\n• Added new \"About\" page found in the help menu\n• Changelogs now display the number of features.\n• \"Convert Files\" option added in the file menu.\n\n"
                                    "5/4/2023 v2.0 \n• Completely rewritten from the ground up\n• Written in Python instead of C#\n• Added a numbered sorting functionality (by name)\n• All boxes can take user input\n• Proper dark mode\n• Complete design overhaul\n• Listbox now updates as you use the program\n• Option to scale\n• Can now manually type in path\n• Sidebar (gonna add things in future)").pack()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def updatePath(self, *args):
        self.directory = self.enterPathVar.get()
        try:
            print(self.directory)
            self.open_dir()
        except:
            print("Directory doesn't exist")

    def activatePrefixCombobox(self):
        self.conversionProgress.set(.5)
        if self.enablePrefixCheckbox.get():
            self.prefixCombobox.configure(state="normal")
        else:
            self.prefixCombobox.configure(state="disabled")

    def toggleSidebar(self):
        if self.sidebar_status:
            self.sidebar_frame.grid_forget()
            self.sidebar_status = False
        else:
            self.sidebar_status = True
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

    def clearList(self):
        for item in self.dirlist.get_children():
            self.dirlist.delete(item)

    def openFolder(self):
        self.enterPath.delete(0, END)
        self.directory = filedialog.askdirectory()
        self.enterPath.insert(0, self.directory)
        self.open_dir()

    def open_dir(self):
        self.conversionProgress.set(.25)
        dirFiles.clear()
        extension.clear()
        self.clearList()

        for file in os.listdir(self.directory):
            if self.wavCheckbox.get() == 1 and file.endswith(".wav"):
                dirFiles.append(file)
                extension.append(file[-4:])
                self.dirlist.insert('', 'end', values=(file[:-4], file[-4:], str(round(os.stat(f'{self.directory}\\{file}').st_size / 1024 / 1024, 2)) + " MB"))

            if self.mp3Checkbox.get() == 1 and file.endswith(".mp3"):
                dirFiles.append(file)
                extension.append(file[-4:])
                self.dirlist.insert('', 'end', values=(file[:-4], file[-4:], str(round(os.stat(f'{self.directory}\\{file}').st_size / 1024 / 1024, 2)) + " MB"))

            if self.oggCheckbox.get() == 1 and file.endswith(".ogg"):
                dirFiles.append(file)
                extension.append(file[-4:])
                self.dirlist.insert('', 'end', values=(file[:-4], file[-4:], str(round(os.stat(f'{self.directory}\\{file}').st_size / 1024 / 1024, 2)) + " MB"))

    def convertFiles(self):
        self.conversionProgress.set(1)
        if not dirFiles:
            messagebox.showerror("Conversion Failed...", "Conversion failed! No files to convert.")
        else:
            for ogFile in dirFiles:
                renamedFile = f'{self.prefixCombobox.get()}{ogFile[:int(self.charactersCombobox.get())]}'
                os.rename(f'{self.directory}/{ogFile}', f'{self.directory}/{renamedFile}{ogFile[-4:]}')
                print(f'{self.directory}/{ogFile} to {self.directory}/{renamedFile}{ogFile[-4:]}')  # temp
            if self.openInExplorerCheckbox.get():
                os.system("explorer " + "\"" + self.directory.replace('/', '\\') + "\"")

    def replaceConvert(self):
        self.conversionProgress.set(1)
        nameOrder = 1
        if not dirFiles:
            messagebox.showerror("Conversion Failed...", "Conversion failed! No files to convert.")
        else:
            for ogFile in dirFiles:
                os.rename(f'{self.directory}/{ogFile}',
                          f'{self.directory}/{ogFile[:int(self.sortChars.get())]}{self.sortNameCombobox.get()}{"{:02d}".format(nameOrder)}{ogFile[-4:]}')
                print(f'{self.directory}/{ogFile[:int(self.sortChars.get())]}{self.sortNameCombobox.get()}{"{:02d}".format(nameOrder)}{ogFile[-4:]}')  # temp
                nameOrder += 1

            if self.openInExplorerCheckbox.get():
                os.system("explorer " + "\"" + self.directory.replace('/', '\\') + "\"")


if __name__ == "__main__":
    app = App()
    app.mainloop()
