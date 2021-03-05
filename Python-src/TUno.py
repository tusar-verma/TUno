import tkinter as tk
from tkinter import ttk

def main():
    mainForm = createMainForm()
    
    mainForm.mainloop()


def createMainForm():    
    form = tk.Tk()
    form.title("TUno")
    form.geometry("500x600")

    # Tabs para hostear game y para unirse a un game

    tab_parent = ttk.Notebook(form)

    tabHosting = ttk.Frame(tab_parent)
    tabJoinGame = ttk.Frame(tab_parent)

    tab_parent.add(tabHosting, text= "Host game")
    tab_parent.add(tabJoinGame, text= "Join game")

    tab_parent.pack(expand=1, fill="both")

    return form

if __name__ == "__main__":
    main()