from api_handler import ApiHandler
from db_handler import DbHandler, DB_CONN
import tkinter as tk
from gui.gui_elements import Elements


ELEMENT = Elements()


class SelectCwTanks:
    def __init__(self, container) -> None:
        
        #setup
        self.container = container
        self._cw_tanks = {}
        tanks = {}
        keys = {}
        self.tank_classes = ["heavyTank", "mediumTank", "lightTank", "AT-SPG"]
        class_names = ["Heavy tanks", "Medium tanks", "Light tanks", "Tank destroyers"]
        __api_handler = ApiHandler()
        
        #operate
        _label = tk.Label(container, bg="#8AA749", text="Select tanks that you are using in clan wars, and then press next.", font=("arial", 15))
        _label.grid(row=0, column=0, padx=0, pady=5, columnspan=8, sticky="ew")

        #Getting tanks and keys from the api, and sorting them by class
        for tank_class in self.tank_classes:
            tanks[tank_class] = __api_handler.pull_tanks(tank_class)
            print("1.toimi")
            keys[tank_class] = __api_handler.get_keys(tanks[tank_class])
            print("2.toimi")


        #Selecting what tanks are cw tanks
        self.make_tank_selections(tanks, keys, class_names)
        print("3.toimi")

        
        #button to go select tank weights
        confirm_button = tk.Button(self.container, text="Next", command=lambda: self.give_tank_weight(tanks, class_names), padx=12, font="arial", bg="#c4c4c2")
        confirm_button.grid(row=2, column=6, pady=5, padx=5, sticky="e")


        # confirm_button = tk.Button(self.container, text="Next", command=lambda: self.give_tank_weight(tanks, class_names), padx=12, font="arial", bg="#c4c4c2")
        # confirm_button.grid(row=2, column=6, pady=5, padx=5, sticky="e")
        

        
        return None




    def make_tank_selections(self, tanks, keys, class_names) -> list:
        checkbutton_vars = {}
        self.selected_tanks = {}
        column = 0
        col = 0

        def checkbox_click() -> None:
            for item, var in checkbutton_vars.items():
                if var.get():
                    item.config(bg="#23eb3e")
                else:
                    item.config(bg=selection_frame.cget("bg"))

        #Loop to sort tanks by their class and to create checkbox frames for each class
        for count, tank_class in enumerate(self.tank_classes):
            col = 0
            tank_type = tanks[tank_class]
            selection_frame = tk.LabelFrame(self.container, text=class_names[count], font="arial")
            selection_frame.grid(row=1, column=column, sticky="n")

            #Loop to create checkboxes for each tank in their classes frame.
            for row_number, key in enumerate(keys[tank_class]):
                row = row_number
                if row_number > 15:
                    col = 2
                    row -= 16
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(selection_frame, text=tank_type[key]["name"], variable=var, font="arial")
                checkbutton_vars[checkbutton] = var
                self.selected_tanks[key] = [var, tank_class]
                print(key)
                checkbutton.config(command=checkbox_click)
                checkbutton.grid(row=row, column=col, sticky="w")
            column += 2


    def confirm_selections(self, tanks) -> None:
            
            # for key, list in self.selected_tanks.items():
            #     if list[0].get():
            #         print(list)
            #         print(".....")
            # return None
            __db_handler = DbHandler()
            __db_handler.init_tank_database()

            for key, var in self.selected_tanks.items():
                print(key)
                if var[0].get():
                    self._cw_tanks[key] = tanks[var[1]][key]
            print(self._cw_tanks)
            
            __db_handler.add_tanks(self._cw_tanks)
            DB_CONN.close()
            self.container.destroy()


    def give_tank_weight(self, tanks, class_names) -> list[str, bool, int]:

        #remove old widgets from container
        for widgets in self.container.winfo_children():
            widgets.destroy()
        row = 0
        column = 0
        colors = ["#AA00FF", "#0050EF", "#00ABA9", "#008A00", "#F0A30A"]
        label_vars = {}
        entry_list = {}

        #changing the background of the text label on user input
        def text_click(self) -> None:
            for item, var in label_vars.items():
                if var.get() == "":
                    item.config(bg=selection_frame.cget("bg"))
                elif 1 <= int(var.get()) <=5:
                    item.config(bg=colors[int(var.get())-1])

        #check the input is 1-5
        def validate_input(value) -> bool:
            if value == "":
                return True
            elif value.isdigit():
                if 1 <= int(value) <= 5:
                    print(key)
                    return True
            return False

        #Loop to sort tanks by their class and to create checkbox frames for each class
        for count, tank_class in enumerate(self.tank_classes):
            selection_frame = tk.LabelFrame(self.container, text=class_names[count], font="arial")
            selection_frame.grid(row=1, column=column, sticky="n")
            validate = selection_frame.register(validate_input)

            #Loop to create labels and input fields for each tank
            for key, var in self.selected_tanks.items():
                if tank_class != var[1]:
                    continue
                if var[0].get():
                    label = tk.Label(selection_frame, text=tanks[var[1]][key]["name"], font="arial")
                    entry = tk.Entry(selection_frame, validate="key", validatecommand=(validate, '%P'), width=5)
                    entry_list[key] = entry.get() #fix this<--------------------------------------------------------------------------
                    entry.bind("<KeyRelease>", text_click)
                    label_vars[label] = entry
                    label.grid(row=row, column=1, padx=3, pady=3, sticky="w")
                    entry.grid(row=row, column=2, padx=3, pady=3, sticky="w")
                    row += 1

            column += 2
                                                                                                                    #Lisää entryt listaan ja lähetä confirm selectioniin. Siellä listää entry selected tanksiin keyn perusteella.
        newbut = tk.Button(self.container, text="Confirm selections", command= lambda: self.confirm_selections(tanks), padx=12, font="arial", bg="#c4c4c2")
        newbut.grid(row=2, column=6, pady=5, padx=5, sticky="e")

