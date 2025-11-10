import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Menu, PhotoImage
import os, webbrowser

# ----------------------------------------------------------
# Funciones principales
# ----------------------------------------------------------
def iniciar_editor():
    # Ocultamos el splash en lugar de destruirlo
    splash_frame.pack_forget()
    crear_editor()  # Cargar el editor en la misma raíz

def nuevo():
    texto.delete(1.0, tk.END)
    root.title("Editor de Texto - Sin título")

def abrir():
    archivo = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Archivos Python", "*.py"),
            ("Archivos C++", "*.cpp"),
            ("Archivos C#", "*.cs"),
            ("Todos los archivos", "*.*")
        ]
    )
    if archivo:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
        except:
            with open(archivo, "r", encoding="latin-1") as f:
                contenido = f.read()
        texto.delete(1.0, tk.END)
        texto.insert(tk.END, contenido)
        root.title(f"Editor de Texto - {os.path.basename(archivo)}")
        global archivo_actual
        archivo_actual = archivo

def guardar():
    global archivo_actual
    if not archivo_actual:
        guardar_como()
        return
    contenido = texto.get(1.0, tk.END)
    with open(archivo_actual, "w", encoding="utf-8") as f:
        f.write(contenido)
    messagebox.showinfo("Guardado", f"Archivo guardado correctamente:\n{archivo_actual}")

def guardar_como():
    global archivo_actual
    archivo = filedialog.asksaveasfilename(
        title="Guardar como",
        defaultextension=".txt",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Archivos Python", "*.py"),
            ("Archivos C++", "*.cpp"),
            ("Archivos C#", "*.cs"),
            ("Todos los archivos", "*.*")
        ]
    )
    if archivo:
        contenido = texto.get(1.0, tk.END)
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        archivo_actual = archivo
        root.title(f"Editor de Texto - {os.path.basename(archivo)}")
        messagebox.showinfo("Guardado", f"Archivo guardado como:\n{archivo}")

def buscar():
    ventana = tk.Toplevel(root)
    ventana.title("Buscar texto")
    tk.Label(ventana, text="Buscar:").pack(pady=5)
    entrada = tk.Entry(ventana, width=40)
    entrada.pack(pady=5)
    resultado = tk.Label(ventana, text="")
    resultado.pack()

    def ejecutar_busqueda():
        texto.tag_remove("encontrado", "1.0", tk.END)
        termino = entrada.get()
        if not termino:
            return
        pos = texto.search(termino, "1.0", tk.END, nocase=True)
        contador = 0
        while pos:
            fin = f"{pos}+{len(termino)}c"
            texto.tag_add("encontrado", pos, fin)
            pos = texto.search(termino, fin, tk.END, nocase=True)
            contador += 1
        texto.tag_config("encontrado", background="yellow")
        resultado.config(text=f"{contador} coincidencia(s) encontradas")

    tk.Button(ventana, text="Buscar", command=ejecutar_busqueda).pack(pady=5)
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=5)

def mostrar_info():
    messagebox.showinfo("Información", 
    "Proyecto Final Algoritmos\nEditor de Texto Simplificado\nVersión: 1.0\nLicencia: GPLv3\n\n"
    "Aplicación creada con Python y Tkinter\nAño: 2025")

def abrir_manual():
    webbrowser.open("https://github.com/tu-usuario/tu-repositorio")

def mostrar_integrantes():
    messagebox.showinfo("Integrantes", "Jorge Aaron Reyes Paniagua 7690-25-14222\nAnthony Fernando Jose Pacay Ambrocio 7690-25-19294")

def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar el editor?"):
        root.destroy()

# ----------------------------------------------------------
# Interfaz principal (editor)
# ----------------------------------------------------------
def crear_editor():
    global texto, archivo_actual
    archivo_actual = None

    # Frame contenedor del editor
    editor_frame = tk.Frame(root, bg="#112d4d")
    editor_frame.pack(fill=tk.BOTH, expand=True)

    # Área de texto
    texto = scrolledtext.ScrolledText(editor_frame, undo=True, font=("Consolas", 11), fg="#112d4d", bg="#d8dce7")
    texto.pack(fill=tk.BOTH, expand=True)

    # Menú principal
    menubar = Menu(root)
    root.config(menu=menubar)

    # Menú Archivo
    menu_archivo = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Nuevo", command=nuevo)
    menu_archivo.add_command(label="Abrir", command=abrir)
    menu_archivo.add_command(label="Guardar", command=guardar)
    menu_archivo.add_command(label="Guardar como...", command=guardar_como)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Buscar", command=buscar)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=salir)

    # Menú Editar
    menu_editar = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Editar", menu=menu_editar)
    menu_editar.add_command(label="Deshacer", command=lambda: texto.edit_undo())
    menu_editar.add_command(label="Rehacer", command=lambda: texto.edit_redo())
    menu_editar.add_separator()
    menu_editar.add_command(label="Copiar", command=lambda: texto.event_generate("<<Copy>>"))
    menu_editar.add_command(label="Cortar", command=lambda: texto.event_generate("<<Cut>>"))
    menu_editar.add_command(label="Pegar", command=lambda: texto.event_generate("<<Paste>>"))
    menu_editar.add_separator()
    menu_editar.add_command(label="Seleccionar todo", command=lambda: texto.event_generate("<<SelectAll>>"))

    # Menú Ayuda
    menu_ayuda = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Información", command=mostrar_info)
    menu_ayuda.add_command(label="Manual de usuario", command=abrir_manual)
    menu_ayuda.add_command(label="Integrantes", command=mostrar_integrantes)

    # Aplicar estilo a los submenús
    for submenu in [menu_archivo, menu_editar, menu_ayuda]:
        submenu.config(
            bg="#101a29",
            fg="#d8dce7",
            activebackground="#163e68",
            activeforeground="white",
            font=("Segoe UI", 10)
        )

# ----------------------------------------------------------
# Pantalla de inicio (splash)
# ----------------------------------------------------------
root = tk.Tk()
root.title("Bienvenido")

# Centrar ventana
ancho, alto = 800, 600
pant_ancho = root.winfo_screenwidth()
pant_alto = root.winfo_screenheight()
x = (pant_ancho // 2) - (ancho // 2)
y = (pant_alto // 2) - (alto // 2)
root.geometry(f"{ancho}x{alto}+{x}+{y}")
root.configure(bg="#112d4d")

# Splash como Frame dentro del root
splash_frame = tk.Frame(root, bg="#112d4d")
splash_frame.pack(fill="both", expand=True)

# Elementos del splash
etiqueta = tk.Label(splash_frame, text="Jorge Aaron Reyes Paniagua y Anthony Fernando Pacay Ambrocio", bg="#101a29", font=("Times New Roman", 12), fg="#d8dce7")
etiqueta.pack(fill=tk.X, side=tk.BOTTOM, ipady=10)

try:
    logo = PhotoImage(file="logoumg.png")
    logo = logo.subsample(2, 2)
    tk.Label(splash_frame, image=logo, bg="#112d4d").pack(pady=(120,5))
except Exception:
    tk.Label(splash_frame, text="[Logo no encontrado]", bg="#112d4d", fg="white", font=("Arial", 14)).pack(pady=120)

tk.Label(splash_frame, text="Presiona el botón para acceder\n al editor de texto", fg="#d8dce7", font=("Times New Roman", 18, "bold"), bg="#112d4d").pack(pady=5)
tk.Button(
    splash_frame,
    text="Acceder",
    font=("Segoe UI", 12, "bold"),
    width=15,
    bg="#101a29",
    fg="#d8dce7",
    activebackground="#112d4d",
    activeforeground="#d8dce7",
    relief="flat",
    cursor="hand2",
    command=iniciar_editor
).pack(pady=10)



root.mainloop()
