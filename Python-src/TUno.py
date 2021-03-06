import tkinter as tk
from tkinter import ttk

def main():
    mainForm = MainForm()
    
    mainForm.form.mainloop()


class MainForm:
    def __init__(self):            
        self.form = tk.Tk()

        self.form.title("TUno")
        self.form.geometry("500x600")      
               
        self.__createTabs()
        
        self.lblInit = tk.Label(self.__tabHosting, text= "TUno is fun")
        self.lblInit.pack()


    # Tabs para hostear game y para unirse a un game
    def __createTabs(self):
        self.__tab_parent = ttk.Notebook(self.form)

        self.__tabHosting = ttk.Frame(self.__tab_parent)
        self.__tabJoinGame = ttk.Frame(self.__tab_parent)
        

        self.__tab_parent.add(self.__tabHosting, text= "Host game")
        self.__tab_parent.add(self.__tabJoinGame, text= "Join game")

        self.__tab_parent.pack(expand=1, fill="both")


if __name__ == "__main__":
    main()