import tkinter as tk
from gui.gui_elements import Elements
from functools import partial
from select_cw_tanks import SelectCwTanks
from get_members import getMembers

ELEMENT = Elements()


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Main frame setup:
        self.title("Joinzers clan tool!")
        self.geometry("1650x800")
        self.resizable(True, True)
        self.pack_propagate(1)
        # self.iconphoto(False, tk.PhotoImage(file="lisääkuva"))

        # Creating sidemenu
        _sidemenu = tk.LabelFrame(self, text="Menu", bg="#8AA749", padx=10, pady=10, width=180, height=400)
        ELEMENT.button(_sidemenu, "Home page", lambda: HomePage(self, container), 1, 2, 0, 2)
        ELEMENT.button(_sidemenu, "Setup clan wars vehicles",lambda: TanksFrame(self, container), 2, 2, 0, 2)
        ELEMENT.button(_sidemenu, "Get clan members", lambda: ClanPlayers(self, container), 3, 2, 0, 2)
        _sidemenu.pack_propagate(0)
        _sidemenu.pack(side="left", padx=20, anchor="nw")

        # Creating frame that contains the app frames
        container = tk.Frame(self, bg="#8AA7A9", padx=10, pady=10, width=750, height=600)
        container.pack_propagate(0)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Starting on homepage
        HomePage(self, container)

    def button_placeholder(self) -> None:
        print("moi")
        return None


# ---------------------------------------- HOME PAGE FRAME / CONTAINER ---------------------------------------


class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, width=750, height=500)
        label = tk.Label(self, text="Home Page", font=("Times", "20"))
        label.pack(pady=0, padx=0)
        self.grid(row=0, column=0, sticky="nsew")
        self.tkraise()
        self.pack_propagate(0)


# ---------------------------------------- Selecting cw tanks PAGE FRAME / CONTAINER ------------------------------------------------------------------------


class TanksFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, width=750, height=500)

        confirm_frame = tk.Frame(self, width=750, height=500)
        ELEMENT.label(confirm_frame, "Do you want to select your preferred clan wars tanks", 0, 4, 0, 0, 15,3)
        ELEMENT.button(confirm_frame, "Yes", lambda: self.confirm_yes(confirm_frame), 1, 4, 1, 10)
        ELEMENT.button(confirm_frame, "No", lambda: HomePage(parent, container), 1, 6, 1, 10)
        confirm_frame.pack(pady=50)

        self.grid(row=0, column=0, sticky="nsew")
        self.tkraise()
        self.pack_propagate(0)

    def confirm_yes(self, frame) -> None:
        frame.pack_forget()
        SelectCwTanks(self)
        return None
    

# ---------------------------------------- Getting clan players and sorting their tanks FRAME / CONTAINER ---------------------------------------


class ClanPlayers(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, width=750, height=500)
        label = tk.Label(self, text="Getting clans players", font=("Times", "20"))
        label.pack(pady=0, padx=0)
        self.grid(row=0, column=0, sticky="nsew")
        self.tkraise()
        self.pack_propagate(0)

        confirm_frame = tk.Frame(self, width=750, height=500)
        ELEMENT.label(confirm_frame, "Get clanmembers and sort their tanks?", 0, 4, 0, 0, 15,3)
        ELEMENT.button(confirm_frame, "Yes", lambda: self.confirm_yes(confirm_frame), 1, 4, 1, 10)
        ELEMENT.button(confirm_frame, "No", lambda: HomePage(parent, container), 1, 6, 1, 10)
        confirm_frame.pack(pady=50)

    def confirm_yes(self, frame) -> None:
        frame.pack_forget()
        getMembers(self)
        return None




if __name__ == "__main__":
    app = App()
    app.mainloop()
