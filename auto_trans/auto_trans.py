from auto_trans.main import Main
import tkinter as tk
from tkinter import filedialog, font
import sys, os

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("AutoTrans GUI")
        self.resizable(1,  1)
        icon_file = self.resource_path("icon.png")
        photo = tk.PhotoImage(file = icon_file )
        self.iconphoto(False, photo)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.consonants_filename: str
        self.double_consonants_filename: str
        self.nazalized_consonants_filename: str
        self.double_vowels_filename: str
        self.vowels_filename: str
        self.glides_filename: str
        self.syllable_rules_filename: str
        self.words_filename: str
        self.text_grid_filename: str

        for F in (StartPage, ResultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(relief='groove', borderwidth="2")

        
        self.show_frame(StartPage)	
	

    def resource_path(self, relative_path):
    
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def select_file(self, widget:tk.Button, attr: str):
        filename = filedialog\
        .askopenfilename(title = "Select a File", 
        filetypes = (("All files", "*.*"),("Text files", "*.txt"),("TextGrid files","*.TextGrid")))

        if filename:
            setattr(self, attr, filename)
            widget.configure(text=filename)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
    
    def proccess(self):
        main = Main(self.words_filename, self.consonants_filename, self.double_consonants_filename, self.nazalized_consonants_filename, self.double_vowels_filename, self.vowels_filename, self.glides_filename, self.syllable_rules_filename, self.text_grid_filename)
        main.run()
        self.show_frame(ResultsPage)


class StartPage(tk.Frame):
    def __init__(self, parent, controller: App):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Select the files for processing")
        label.pack(ipadx=10, ipady=10)
    
        words_file = tk.Button(self, command=lambda: controller.select_file(words_file, "words_filename"))
        words_file.configure(borderwidth="2",relief="sunken")
        words_file.configure(text='''Tap to select Words file''')
        words_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        consonants_file = tk.Button(self, command=lambda: controller.select_file(consonants_file,"consonants_filename"))
        consonants_file.configure(borderwidth="2",relief="sunken")
        consonants_file.configure(text='''Tap to select Consonants file''')
        consonants_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        double_consonants_file = tk.Button(self, command=lambda: controller.select_file(double_consonants_file, "double_consonants_filename"))
        double_consonants_file.configure(borderwidth="2", relief="sunken")
        double_consonants_file.configure(text='''Tap to select Double Consonants file''')
        double_consonants_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        vowels_file = tk.Button(self, command=lambda: controller.select_file(vowels_file, "vowels_filename"))
        vowels_file.configure(borderwidth="2", relief="sunken")
        vowels_file.configure(text='''Tap to select Vowels file''')
        vowels_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        double_vowels_file = tk.Button(self, command=lambda: controller.select_file(double_vowels_file, "double_vowels_filename"))
        double_vowels_file.configure(borderwidth="2",relief="sunken")
        double_vowels_file.configure(text='''Tap to select Double Vowels file''')
        double_vowels_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        glides_file = tk.Button(self, command=lambda: controller.select_file(glides_file, "glides_filename"))
        glides_file.configure(borderwidth="2", relief="sunken")
        glides_file.configure(text='''Tap to select Glides file''')
        glides_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        nazalized_consonants_file = tk.Button(self, command=lambda: controller.select_file(nazalized_consonants_file, "nazalized_consonants_filename"))
        nazalized_consonants_file.configure(borderwidth="2", relief="sunken")
        nazalized_consonants_file.configure(text='''Tap to select Nazalized Consonants file''')
        nazalized_consonants_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        syllable_rules_file = tk.Button(self, command=lambda: controller.select_file(syllable_rules_file, "syllable_rules_filename"))
        syllable_rules_file.configure(borderwidth="2",relief="sunken")
        syllable_rules_file.configure(text='''Tap to select Syllable Rules file''')
        syllable_rules_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        text_grid_file = tk.Button(self, command=lambda: controller.select_file(text_grid_file, "text_grid_filename"))
        text_grid_file.configure(borderwidth="2",relief="sunken")
        text_grid_file.configure(text='''Tap to select TextGrid file''')
        text_grid_file.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=5)

        process_btn = tk.Button(self, command=lambda: controller.proccess())
        process_btn.configure(borderwidth="2")
        process_btn.configure(text='''Process''')
        process_btn.pack(padx=10, pady=10, ipadx=10, ipady=10)
    

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        fontStyle = font.Font(family="Lucida Grande", size=100)
        label = tk.Label(self, text="Success!!", font=fontStyle)
        label.pack(padx=10, pady=10)
        start_page = tk.Button(self, text="back", command=lambda:controller.show_frame(StartPage))
        start_page.pack()


def start():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    start()