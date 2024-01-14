import tkinter as tk
FONT = "arial"

class Elements():
    def __init__(self) -> None:
        pass

    def button(self, container, text: str, command , row: int, col: int, padx: int = 0, pady: int = 0):
        _button = tk.Button(container, text=text, command=command, width=20, font=(FONT))
        _button.grid(row=row, column=col, padx=padx, pady=pady)
        return None
        
    def label(self ,container, text: str, row: int, col: int, padx: int = 0, pady: int = 0, fsize: int = 0, colspan: int = 1):
        _label = tk.Label(container,bg="#8AA749", text=text, font=(FONT, fsize))
        _label.grid(row=row, column = col, padx=padx, pady=pady, columnspan=colspan)
        return None
    
    
    

        
    # class Fbutton(tk.Button):
    #     def __init__(self, container, text, command, row, col, **kwargs):
    #         self.text = text
    #         self.command = command
    #         self.row = row
    #         self.column = col
    #         super().__init__(container)
    #         self["text"] = self.text
    #         self['command'] = self.command
    #         self.grid(row=self.row, column = self.column)
    #         self.config(width=20)
    #         return None

