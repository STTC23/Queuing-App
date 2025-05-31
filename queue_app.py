import tkinter as tk #GUI library
from tkinter import messagebox
from tkinter import PhotoImage #Using images
from tkinter import ttk #Windows GUi options
from sympy.parsing.sympy_parser import parse_expr #Logic maths library
from sympy.logic.boolalg import BooleanFunction #Booleans logic
from PIL import Image, ImageTk
import itertools #iterations library
import re #chars library
import matplotlib #Vector library



# Funciones de los botones
def insert_element():
    element = entry.get()
    if element:
        listbox.insert(tk.END, element)
        entry.delete(0, tk.END)
        update_info()


def record_element():
    selected = listbox.curselection()
    if selected:
        entry.delete(0, tk.END)
        entry.insert(0, listbox.get(selected))

def clean_element():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected)
        update_info()

def clean_list():
    listbox.delete(0, tk.END)
    update_info()

# Clean Element Verification
def clean_list():
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to clear the list?")
    if confirm:
        listbox.delete(0, tk.END)
        update_info()

def update_info():
    elements = listbox.get(0, tk.END)
    amount_var.set(len(elements)) #Select amount of element
    first_var.set(elements[0] if elements else "") #First element always in 0
    last_var.set(elements[-1] if elements else "") #Last element always in -1 cause is the alst



# Principal Window
root = tk.Tk()
root.title("Lógica de Programación I - Simulador de Encolamiento") #Title window
root.iconbitmap(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Berry_principal.ico") #Icon
root.geometry("600x350")

bg_image = tk.PhotoImage(file=r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\background.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

img_width = bg_image.width()
img_height = bg_image.height()
root.geometry(f"{img_width}x{img_height}")


# Starwberry Image
original_img = Image.open(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Strawberrry.png")
resized_img = original_img.resize((80, 60), Image.Resampling.LANCZOS)
strawberry_img = ImageTk.PhotoImage(resized_img)
strawberry_label = tk.Label(root, image=strawberry_img, borderwidth=0, highlightthickness=0)
strawberry_label.place(x=250, y=0)  


# Text font
entry = tk.Entry(root, font=("Arial", 12), width=40)
entry.place(x=100, y=50)

# Text buttons
tk.Button(root, text="INSERT", bg="green", fg="black", command=insert_element).place(x=100, y=100)
tk.Button(root, text="RECORD", bg="blue", fg="white", command=record_element).place(x=200, y=100)
tk.Button(root, text="CLEAN ELEMENT", bg="lightcoral", command=clean_element).place(x=300, y=100)
tk.Button(root, text="CLEAN LIST", bg="red", fg="white", command=clean_list).place(x=450, y=100)


# Current List
tk.Label(root, text="CURRENT LIST:").place(x=100, y=150)
listbox = tk.Listbox(root, width=40, height=8)
listbox.place(x=100, y=170)

# Elements information
tk.Label(root, text="ELEMENT AMOUNT:").place(x=350, y=170) #Amount of elements on a list
amount_var = tk.StringVar()
tk.Entry(root, textvariable=amount_var).place(x=470, y=170) #Square

tk.Label(root, text="FIRST ELEMENT:").place(x=370, y=210) #First element
first_var = tk.StringVar()
tk.Entry(root, textvariable=first_var).place(x=470, y=210) #Square

tk.Label(root, text="LAST ELEMENT:").place(x=370, y=250) #Last Element 
last_var = tk.StringVar()
tk.Entry(root, textvariable=last_var).place(x=470, y=250) #Square

# Close Windows
tk.Button(root, text="X", bg="lightcoral", command=root.quit).place(x=570, y=0)


root.mainloop()