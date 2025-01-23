import tkinter as tk
class AppGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("AniPY")

        self.nav_bar=tk.Frame(self.root,background="#101424", width=400)
        self.nav_bar.pack(side="left", fill="y")
        self.main_panel=tk.Frame(self.root,background="#182434")
        self.main_panel.pack(side="right", fill="both",expand=True)

        self.menu_options = ["Strona Główna", "Szukaj", "Profil", "Zaloguj Się"]
        for option in self.menu_options:
            button=tk.Button(self.nav_bar,text=option)
            button.pack(fill="x")
        self.change_main_panel(self.menu_options[0])

        self.root.mainloop()

    def change_main_panel(self, option):
        for widget in self.main_panel.winfo_children():
            widget.destroy()

AppGUI()