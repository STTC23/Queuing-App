import tkinter as tk #Windows library
from tkinter import messagebox #Verification and confirmation tool
from PIL import Image, ImageTk #Images tools
import queue #Importing FiFO Python queue
import re #Chains functions
import os

# --- Global path configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Script base directory
IMAGE_DIR = os.path.join(BASE_DIR, "image")  # Image folder path

# FIFO Queue logic
cola = queue.Queue()  # FIFO queue to store the inserted elements

selected_type = None #Save the select type on the selector window

# All element verification and selection
def is_valid_input(value):
    try: # Mistakes structures
        if selected_type == "entero": # Input example: 33
            int(value) #Int definition
        elif selected_type == "float": #Input example: 3,14
            float(value) #Float definition
        elif selected_type == "vector": #Input example [1,3]
            evaled = eval(value) #vector definition
            if not isinstance(evaled, (list, tuple)):
                return False
        elif selected_type == "boolean": #Input example: True
            if value not in ["True", "False"]: #Boolean definition
                return False
        elif selected_type == "dict": #Input example: {"Name": Madeline}
            evaled = eval(value) #dictinonary definition
            if not isinstance(evaled, dict):
                return False
        elif selected_type == "char": # Input Example: a,b,c,d
            if len(value) != 1:  #Char definition
                return False
        elif selected_type == "real": # Input example: 3/4
            float(value) #float because its global
        elif selected_type == "everything": #Input Example: 1 , 3,52 , [1,7] , {"Name": Sunset}
            pass #Always valid, no actions to do
        else:
            return False
        return True
    except: #Mistakes structure
        return False

# Every choose option validation
def validate_entry_input(value):
    if selected_type == "entero": #if the user select integer
        return value == "" or value.isdigit() #only numbers
    elif selected_type == "float":
        return re.match(r'^-?\d*(\.\d*)?$', value) is not None #The program will be avoid to write those symbols
    return True

#------------------------------------------------ PRINCIPAL WINDOW ----------------------------------------------------------#
def launch_main_window():
    global entry, current_list_var

    root = tk.Tk() #Creates the principal program
    root.title("Lógica de Programación I - Simulador de Encolamiento") #Principal windows title
    root.iconbitmap(os.path.join(IMAGE_DIR, "Berry_principal.ico"))   #principal windows icon

    bg_image = tk.PhotoImage(file=os.path.join(IMAGE_DIR, "background.png")) #image localitation
    background_label = tk.Label(root, image=bg_image) #Location 
    background_label.place(x=0, y=0, relwidth=1, relheight=1) #Position
    img_width = bg_image.width() #width size
    img_height = bg_image.height() #hegiht size
    root.geometry(f"{img_width}x{img_height}") # Final image size

    original_img = Image.open(os.path.join(IMAGE_DIR, "Strawberrry.png")) #Image localitation
    resized_img = original_img.resize((80, 60), Image.Resampling.LANCZOS) #Resized the image
    strawberry_img = ImageTk.PhotoImage(resized_img) # resized image
    strawberry_label = tk.Label(root, image=strawberry_img, borderwidth=0, highlightthickness=0) #Size configuration
    strawberry_label.place(x=250, y=0) #Position

    vcmd = root.register(validate_entry_input) #Values every type of element
    entry = tk.Entry(root, font=("Arial", 12), width=40, validate="key", validatecommand=(vcmd, '%P'))
    entry.place(x=100, y=50)

    #--- Variables ---#
    amount_var = tk.StringVar() #Amount variable and gives tk.Stringvar the value
    first_var = tk.StringVar() #Amount frist var
    last_var = tk.StringVar() #Amount last var
    history = []
    current_list_var = tk.StringVar()

    #--- Button Functions ---#
    def insert_element():
        element = entry.get()
        if element:
            if is_valid_input(element):
                listbox.insert(tk.END, element) #Insert Definiction
                entry.delete(0, tk.END)
                cola.put(element)  # Add to FIFO queue
                update_info() #Update save every actions in every function
                history.append(f"The following element has been inserted {element}") #Record fucntion
            else:
                messagebox.showerror("Invalid input", f"The valor '{element}' isn't right '{selected_type}'") #Error message

    def record_element():
        if history:
            historial_texto = "\n".join(history)
        else:
            historial_texto = "There is not register actions" #Record function
        messagebox.showinfo("Record: ", historial_texto)  #Error message

    def clean_element():
        selected = listbox.curselection()
        if selected:
            removed = listbox.get(selected)
            listbox.delete(selected) #Delected definition
            update_info()
            history.append(f"The following element has been removed {removed}") #Record function

    def clean_list():
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to clear the list?") #Confirmation function
        if confirm:
            listbox.delete(0, tk.END) #Delecte every element in the list
            with cola.mutex: # Queue access
                cola.queue.clear()  # Clear FIFO queue
            update_info()
            history.append("The list has been cleaned")

    def update_info(): #This function saves every action in the list
        elements = listbox.get(0, tk.END)
        amount_var.set(len(elements))
        first_var.set(elements[0] if elements else "") #Every elements its olways in 0 position
        last_var.set(elements[-1] if elements else "") #Every last element its always in -1 last position
        current_list_var.set(f"[{', '.join(elements)}]") #Show the elements on the list
    
    def back_to_selector(current_window):
        current_window.destroy()  # Close main window
        show_selector_window()    # Show selector window

    #--- Buttons ---#
    tk.Button(root, text="INSERT", bg="green", fg="black", command=insert_element).place(x=100, y=100) #Insert Button
    tk.Button(root, text="RECORD", bg="blue", fg="white", command=record_element).place(x=200, y=100) #Record Button
    tk.Button(root, text="CLEAN ELEMENT", bg="lightcoral", command=clean_element).place(x=300, y=100) #Clean Element button
    tk.Button(root, text="CLEAN LIST", bg="red", fg="white", command=clean_list).place(x=450, y=100) #Clean list button
    tk.Button(root, text="BACK TO SELECTOR", bg="orange", command=lambda: back_to_selector(root)).place(x=100, y=20) #Back to selector button

    #--- Labels and Entry fields ---#
    tk.Label(root, text="CURRENT LIST:", bg="#000000", fg="white").place(x=100, y=140) #Current list label
    tk.Entry(root, textvariable=current_list_var, width=40, bg="gray20", fg="white", insertbackground="white").place(x=100, y=160)

    listbox = tk.Listbox(root, width=40, height=8)
    listbox.place(x=100, y=190)

    tk.Label(root, text="ELEMENT AMOUNT:").place(x=350, y=170) #Element amoutn label
    tk.Entry(root, textvariable=amount_var).place(x=470, y=170)
    tk.Label(root, text="FIRST ELEMENT:").place(x=370, y=210) #First element label
    tk.Entry(root, textvariable=first_var).place(x=470, y=210)
    tk.Label(root, text="LAST ELEMENT:").place(x=370, y=250) #Last element label
    tk.Entry(root, textvariable=last_var).place(x=470, y=250)

    root.mainloop() #Keep the windows open

#---------------------------------------------------------------------------------------------------------------------#
# Selector Window Function
def select_type(tipo):
    global selected_type #Variable has so many types of element
    selected_type = tipo
    select_window.destroy() #Close selector windows when the user selects a type
    launch_main_window() #Goes to the main window

#------------------------------------------------ SELECTOR ----------------------------------------------------------#
def show_selector_window():
    global select_window
    select_window = tk.Tk()
    select_window.title("Selector")
    select_window.iconbitmap(os.path.join(IMAGE_DIR, "Berry_principal.ico"))
    select_window.geometry("250x300")

    tk.Label(select_window, text="Please, select a type of element").pack(pady=10)

    tipos = ["entero", "float", "vector", "boolean", "dict", "char", "real", "everything"]
    for t in tipos:
        tk.Button(select_window, text=t, width=15, command=lambda tipo=t: select_type(tipo)).pack(pady=3)

    select_window.mainloop() #Keeps select windows open

show_selector_window() #Go tothe selector when push the back to selector option
