import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import queue

# === Lógica de la cola ===
cola = queue.Queue()

# === Variable global para tipo seleccionado ===
selected_type = None

# === Validación según tipo seleccionado ===
def is_valid_input(value):
    try:
        if selected_type == "entero":
            int(value)
        elif selected_type == "float":
            float(value)
        elif selected_type == "vector":
            evaled = eval(value)
            if not isinstance(evaled, (list, tuple)):
                return False
        elif selected_type == "boolean":
            if value not in ["True", "False"]:
                return False
        elif selected_type == "dict":
            evaled = eval(value)
            if not isinstance(evaled, dict):
                return False
        elif selected_type == "char":
            if len(value) != 1:
                return False
        elif selected_type == "real":
            float(value)
        elif selected_type == "everything":
            pass
        else:
            return False
        return True
    except:
        return False

# === Función para lanzar ventana principal ===
def launch_main_window():
    global root, entry, current_list_var, amount_var, first_var, last_var, listbox

    root = tk.Tk()
    root.title("Lógica de Programación I - Simulador de Encolamiento")
    root.iconbitmap(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Berry_principal.ico")

    bg_image = tk.PhotoImage(file=r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\background.png")
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.geometry(f"{bg_image.width()}x{bg_image.height()}")

    # Imagen decorativa
    original_img = Image.open(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Strawberrry.png")
    resized_img = original_img.resize((80, 60), Image.Resampling.LANCZOS)
    strawberry_img = ImageTk.PhotoImage(resized_img)
    tk.Label(root, image=strawberry_img, borderwidth=0).place(x=250, y=0)

    # Entrada
    entry = tk.Entry(root, font=("Arial", 12), width=40)
    entry.place(x=100, y=50)

    # Botones
    tk.Button(root, text="INSERT", bg="green", command=insert_element).place(x=100, y=100)
    tk.Button(root, text="RECORD", bg="blue", fg="white", command=record_element).place(x=200, y=100)
    tk.Button(root, text="CLEAN ELEMENT", bg="lightcoral", command=clean_element).place(x=300, y=100)
    tk.Button(root, text="CLEAN LIST", bg="red", fg="white", command=clean_list).place(x=450, y=100)
    tk.Button(root, text="Volver al selector", command=show_selector_window).place(x=10, y=10)

    # Variables de información
    current_list_var = tk.StringVar()
    amount_var = tk.StringVar()
    first_var = tk.StringVar()
    last_var = tk.StringVar()

    # Visualización
    tk.Label(root, text="CURRENT LIST:", bg="#000000", fg="white").place(x=100, y=170)
    tk.Entry(root, textvariable=current_list_var, width=40, bg="gray20", fg="white").place(x=100, y=190)
    listbox = tk.Listbox(root, width=40, height=8)
    listbox.place(x=100, y=220)

    tk.Label(root, text="ELEMENT AMOUNT:").place(x=350, y=170)
    tk.Entry(root, textvariable=amount_var).place(x=470, y=170)

    tk.Label(root, text="FIRST ELEMENT:").place(x=370, y=210)
    tk.Entry(root, textvariable=first_var).place(x=470, y=210)

    tk.Label(root, text="LAST ELEMENT:").place(x=370, y=250)
    tk.Entry(root, textvariable=last_var).place(x=470, y=250)

    root.mainloop()

# === Acciones ===
def insert_element():
    element = entry.get()
    if is_valid_input(element):
        cola.put(element)  # Encola el elemento
        listbox.insert(tk.END, element)  # Visual
        entry.delete(0, tk.END)
        update_info()
        messagebox.showinfo("Insertado", f"Se ha insertado '{element}'")
    else:
        messagebox.showerror("Error", f"'{element}' no es válido para el tipo '{selected_type}'.")

def record_element():
    if cola.empty():
        messagebox.showinfo("Vacía", "La cola está vacía.")
    else:
        primero = cola.queue[0]
        messagebox.showinfo("Primer elemento", f"El primer elemento es: {primero}")

def clean_element():
    selected = listbox.curselection()
    if selected:
        value = listbox.get(selected)
        listbox.delete(selected)
        # Eliminar manualmente de la cola (no hay método directo)
        elementos = list(cola.queue)
        elementos.remove(value)
        cola.queue.clear()
        for e in elementos:
            cola.put(e)
        update_info()
        messagebox.showinfo("Eliminado", f"Se ha eliminado '{value}'")

def clean_list():
    if messagebox.askyesno("Confirmación", "¿Estás seguro de borrar la lista?"):
        listbox.delete(0, tk.END)
        cola.queue.clear()
        update_info()

def update_info():
    elementos = list(cola.queue)
    amount_var.set(len(elementos))
    first_var.set(elementos[0] if elementos else "")
    last_var.set(elementos[-1] if elementos else "")
    current_list_var.set(f"[{', '.join(elementos)}]")

# === Selector inicial ===
def select_type(tipo):
    global selected_type
    selected_type = tipo
    select_window.destroy()
    launch_main_window()

def show_selector_window():
    global select_window, selected_type
    selected_type = None
    select_window = tk.Tk()
    select_window.title("Selector")
    select_window.iconbitmap(r"C:\Users\juan_\Downloads\Proyecto Final - Lógica\image\Berry_principal.ico")
    select_window.geometry("250x300")
    tk.Label(select_window, text="Selecciona el tipo de elemento").pack(pady=10)
    tipos = ["entero", "float", "vector", "boolean", "dict", "char", "real", "everything"]
    for t in tipos:
        tk.Button(select_window, text=t, width=15, command=lambda tipo=t: select_type(tipo)).pack(pady=3)
    select_window.mainloop()

# Lanzar selector al iniciar
show_selector_window()