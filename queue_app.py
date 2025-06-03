import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import BooleanFunction
from PIL import Image, ImageTk
import itertools
import re
import matplotlib

selected_type = None

# === Validación del tipo de entrada según el tipo seleccionado ===
def is_valid_input(value):
    try:
        if selected_type == "entero": # Input example: 33
            int(value)
        elif selected_type == "float": #Input example: 3,14
            float(value)
        elif selected_type == "vector": #Input example [1,3]
            evaled = eval(value)
            if not isinstance(evaled, (list, tuple)):
                return False
        elif selected_type == "boolean": #Input example: True
            if value not in ["True", "False"]:
                return False
        elif selected_type == "dict": #Input example: {"Name": Madeline}
            evaled = eval(value)
            if not isinstance(evaled, dict):
                return False
        elif selected_type == "char": # Input Example: a,b,c,d
            if len(value) != 1:
                return False
        elif selected_type == "real": # Input example: 3/4
            float(value)
        elif selected_type == "everything": #Input Example: 1 , 3,52 , [1,7] , {"Name": Sunset}
            pass
        else:
            return False
        return True
    except:
        return False

# Every choose option validation
def validate_entry_input(value):
    if selected_type == "entero": 
        return value == "" or value.isdigit()
    elif selected_type == "float":
        return re.match(r'^-?\d*(\.\d*)?$', value) is not None
    return True

#------------------------------------------------ PRINCIPAL WINDOW ----------------------------------------------------------#
def launch_main_window():
    # Principal Creation
    global entry
    root = tk.Tk()
    root.title("Lógica de Programación I - Simulador de Encolamiento")
    root.iconbitmap(r"C:\\Users\\juan_\\Downloads\\Proyecto Final - Lógica\\image\\Berry_principal.ico")

    #Background
    bg_image = tk.PhotoImage(file=r"C:\\Users\\juan_\\Downloads\\Proyecto Final - Lógica\\image\\background.png")
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    img_width = bg_image.width()
    img_height = bg_image.height()
    root.geometry(f"{img_width}x{img_height}")

    #Strawberry
    original_img = Image.open(r"C:\\Users\\juan_\\Downloads\\Proyecto Final - Lógica\\image\\Strawberrry.png")
    resized_img = original_img.resize((80, 60), Image.Resampling.LANCZOS)
    strawberry_img = ImageTk.PhotoImage(resized_img)
    strawberry_label = tk.Label(root, image=strawberry_img, borderwidth=0, highlightthickness=0)
    strawberry_label.place(x=250, y=0)

    # Value validation
    vcmd = root.register(validate_entry_input)
    entry = tk.Entry(root, font=("Arial", 12), width=40, validate="key", validatecommand=(vcmd, '%P'))
    entry.place(x=100, y=50)

    #--- Button Functions ---#
    def insert_element():
        element = entry.get()
        if is_valid_input(element):
            listbox.insert(tk.END, element)
            entry.delete(0, tk.END)
            update_info()
        else:
            messagebox.showerror("Invalid input", "The input does not match the selected type.")

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
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to clear the list?")
        if confirm:
            listbox.delete(0, tk.END)
            update_info()

    def update_info():
        elements = listbox.get(0, tk.END)
        amount_var.set(len(elements))
        first_var.set(elements[0] if elements else "")
        last_var.set(elements[-1] if elements else "")
        current_list_var.set(f"[{', '.join(elements)}]")
    
    def back_to_selector(current_window):
        current_window.destroy()  # Cierra la ventana principal
        show_selector_window()    # Vuelve a abrir la de selección
    
    #--- Buttons ---#

    tk.Button(root, text="INSERT", bg="green", fg="black", command=insert_element).place(x=100, y=100)
    tk.Button(root, text="RECORD", bg="blue", fg="white", command=record_element).place(x=200, y=100)
    tk.Button(root, text="CLEAN ELEMENT", bg="lightcoral", command=clean_element).place(x=300, y=100)
    tk.Button(root, text="CLEAN LIST", bg="red", fg="white", command=clean_list).place(x=450, y=100)
    tk.Button(root, text="BACK TO SELECTOR", bg="orange", command=lambda: back_to_selector(root)).place(x=100, y=300)


    tk.Label(root, text="CURRENT LIST:", bg="#000000", fg="white").place(x=100, y=170)
    current_list_var = tk.StringVar()
    tk.Entry(root, textvariable=current_list_var, width=40, bg="gray20", fg="white", insertbackground="white").place(x=100, y=190)
    listbox = tk.Listbox(root, width=40, height=8)
    listbox.place(x=100, y=170)

    #--- Variables ---#
    amount_var = tk.StringVar()
    first_var = tk.StringVar()
    last_var = tk.StringVar()

    tk.Label(root, text="ELEMENT AMOUNT:").place(x=350, y=170)
    tk.Entry(root, textvariable=amount_var).place(x=470, y=170)
    tk.Label(root, text="FIRST ELEMENT:").place(x=370, y=210)
    tk.Entry(root, textvariable=first_var).place(x=470, y=210)
    tk.Label(root, text="LAST ELEMENT:").place(x=370, y=250)
    tk.Entry(root, textvariable=last_var).place(x=470, y=250)


    root.mainloop()


# Selector Window Function
def select_type(tipo):
    global selected_type
    selected_type = tipo
    select_window.destroy()
    launch_main_window()

#------------------------------------------------ SELECTOR ----------------------------------------------------------#
def show_selector_window():
    global select_window
    select_window = tk.Tk()
    select_window.title("Selector")
    select_window.iconbitmap(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Berry_principal.ico")
    select_window.geometry("250x300")

    tk.Label(select_window, text="Selecciona el tipo de elemento").pack(pady=10)

    tipos = ["entero", "float", "vector", "boolean", "dict", "char", "real", "everything"]
    for t in tipos:
        tk.Button(select_window, text=t, width=15, command=lambda tipo=t: select_type(tipo)).pack(pady=3)

    select_window.mainloop()
show_selector_window()
    