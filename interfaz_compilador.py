import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu, filedialog, messagebox
from analizador_lexico import lexer, find_column, palabras_reservadas
from analizador_sintactico import parse, obtener_errores
from analizador_semantico import tabla_simbolos

class GrassCodeEditor:
    def __init__(self, notebook, title="Untitled"):
        self.notebook = notebook
        self.frame = ttk.Frame(notebook)
        self.frame.editor_instance = self  # Referencia al propio editor
        notebook.add(self.frame, text=title)
        
        self.file_path = ""
        
        # Tamaño de la fuente predeterminada
        self.font_size = 12
        self.txt_font = ('Roboto', self.font_size)

         # Configurar las filas y columnas para que se expandan
        for i in range(10):
            self.frame.columnconfigure(i, weight=1)

        # Ajustar los pesos de las filas para que txtTerminal no se expanda demasiado
        # Ajustar los pesos de las filas para que solo txtArea y txtNumber se expandan
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=3, minsize=360)  # Más espacio para el área de texto principal
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=0)
        self.frame.rowconfigure(5, weight=1, minsize=100)  # Cambia el minsize según sea necesario
        self.frame.rowconfigure(6, weight=0)

        self.frame.columnconfigure(0, weight=2, pad=400)
        self.frame.columnconfigure(3, weight=1, minsize=465)  # Columna de la tabla de tokens
        self.frame.grid_propagate(False)
        # Componentes
        self.lblTablaTokens = ttk.Label(self.frame, text="Tabla de tokens")
        self.lblTerminalErrores = ttk.Label(self.frame, text="Terminal de salida para errores")
        self.text_frame = tk.Frame(self.frame)
        self.txtNumber = tk.Text(self.text_frame, width=4, padx=4, takefocus=0, border=0,
                                 background='lightgrey', state='disabled', font=self.txt_font)  # Modificación
        self.txtArea = scrolledtext.ScrolledText(self.text_frame, wrap="none", undo=True, font=self.txt_font)
        self.txtNumber.pack(side=tk.LEFT, fill=tk.Y)
        self.txtArea.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text_frame.grid(row=2, column=0, padx=10, pady=2, sticky="nsew")
        # Crear la etiqueta de palabras reservadas
        self.txtArea.tag_configure('reservadas', foreground='blue')
        
        # Vincular el evento de teclado para actualizar los números de línea
        self.txtArea.bind('<KeyRelease>', self.update_line_numbers)
        self.txtArea.bind('<FocusIn>', lambda event: self.resaltar_comentarios())
        self.update_line_numbers()
        self.txtTerminal = tk.Text(self.frame, wrap="word", highlightthickness=0.5, highlightbackground="grey", highlightcolor="grey", state='disabled')  
        self.btnCompilar = ttk.Button(self.frame, text = "Compilar", style = 'Custom.TButton', command=self.compilar)
        
        # Configuración del TreeView (Tabla)
        self.tablaTokens = ttk.Treeview(self.frame, columns=("Token", "Tipo de Token", "Línea/Columna"), show="headings")
        self.tablaTokens.heading("Token", text="Token")
        self.tablaTokens.heading("Tipo de Token", text="Tipo de Token")
        self.tablaTokens.heading("Línea/Columna", text="Línea/Columna")

        self.tablaTokens.column("Token", width=30, anchor='center')
        self.tablaTokens.column("Tipo de Token", width=30, anchor='center')
        self.tablaTokens.column("Línea/Columna", width=30, anchor='center')

        # Posicionamiento de los componentes en la cuadrícula
        self.lblTablaTokens.grid(row=1, column=3, padx=5, pady=2, sticky='w')
        self.tablaTokens.grid(row=2, column=3, columnspan=7, padx=10, pady=2, sticky='nsew')
        self.btnCompilar.grid(row=3, column=0, padx=10, pady=0, sticky='w')
        self.lblTerminalErrores.grid(row=4, column=0, padx=10, pady=(10, 2), sticky='w')
        self.txtTerminal.grid(row=5, column=0, columnspan=10, padx=10, pady=0, sticky='ew')
        self.txtTerminal.update_idletasks()
        
        # Sincronización del scroll
        # Vincular el evento de teclado para cambiar el tamaño de la fuente
        self.txtArea.bind('<Control-MouseWheel>', self.zoom) # Modificación para zoom con Ctrl + Rueda del ratón
        self.txtArea.bind('<MouseWheel>', self.sync_scroll)  # Modificación
        self.txtNumber.bind('<MouseWheel>', self.sync_scroll)  # Modificación

    def update_line_numbers(self, event=None):
        self.txtNumber.config(state=tk.NORMAL)
        self.txtNumber.delete(1.0, tk.END)
        current_lines = self.txtArea.get(1.0, tk.END).split('\n')
        for i in range(1, len(current_lines)):
            self.txtNumber.insert(tk.END, f'{i}\n')
        self.txtNumber.config(state=tk.DISABLED)
        self.sync_scroll()
        self.update_line_numbers_width()
        self.resaltar_palabras_reservadas()
        self.resaltar_comentarios()

    def resaltar_palabras_reservadas(self, event=None):
        self.txtArea.tag_remove('reservadas', '1.0', tk.END)
        codigo = self.txtArea.get("1.0", 'end-1c')
        current_index = 0
        while current_index < len(codigo):
            while current_index < len(codigo) and not codigo[current_index].isalnum():
                current_index += 1
            palabra_inicio = current_index
            while current_index < len(codigo) and codigo[current_index].isalnum():
                current_index += 1
            palabra_final = current_index
            if palabra_inicio < palabra_final:
                palabra = codigo[palabra_inicio:palabra_final]
                if palabra in palabras_reservadas:
                    start = f"1.0 + {palabra_inicio} chars"
                    end = f"1.0 + {palabra_final} chars"
                    self.txtArea.tag_add('reservadas', start, end)

    def resaltar_comentarios(self):
        self.txtArea.tag_remove('comentarios', '1.0', tk.END)
        codigo = self.txtArea.get("1.0", 'end-1c')
        current_index = 0
        while current_index < len(codigo):
            # Busca el inicio de un comentario de línea
            if codigo[current_index:current_index+2] == '//':
                comentario_inicio = current_index
                # Avanza hasta el final de la línea o el final del código
                while current_index < len(codigo) and codigo[current_index] != '\n':
                    current_index += 1
                comentario_final = current_index
                start = f"1.0 + {comentario_inicio} chars"
                end = f"1.0 + {comentario_final} chars"
                self.txtArea.tag_add('comentarios', start, end)
            # Busca el inicio de un comentario de bloque
            elif codigo[current_index:current_index+2] == '/*':
                comentario_inicio = current_index
                # Avanza hasta el final del bloque de comentario o el final del código
                while current_index < len(codigo) and codigo[current_index:current_index+2] != '*/':
                    current_index += 1
                current_index += 2  # Incluir los caracteres '*/'
                comentario_final = current_index
                start = f"1.0 + {comentario_inicio} chars"
                end = f"1.0 + {comentario_final} chars"
                self.txtArea.tag_add('comentarios', start, end)
            else:
                current_index += 1

        # Configura el color verde para la etiqueta 'comentarios'
        self.txtArea.tag_configure('comentarios', foreground='green')


    def update_line_numbers_width(self):
        digits = len(str(self.txtArea.index('end-1c').split('.')[0]))
        self.txtNumber.config(width=digits)

    def update_line_numbers(self, event=None):
        self.txtNumber.config(state=tk.NORMAL)
        self.txtNumber.delete(1.0, tk.END)
        current_lines = self.txtArea.get(1.0, tk.END).split('\n')
        for i in range(1, len(current_lines)):
            self.txtNumber.insert(tk.END, f'{i}\n')
        self.txtNumber.config(state=tk.DISABLED)
        self.sync_scroll()
        self.update_line_numbers_width()  # Modificación
        self.resaltar_palabras_reservadas()  # Llamada a la función para resaltar palabras reservadas
        self.resaltar_comentarios()  # Añadir esta línea para resaltar los comentarios

    def update_line_numbers_width(self):  # Nueva función
        # Calcula el número de dígitos necesarios para el mayor número de línea
        digits = len(str(self.txtArea.index('end-1c').split('.')[0]))
        # Ajusta el ancho de txtNumber basado en el número de dígitos
        self.txtNumber.config(width=digits)

    def sync_scroll(self, event=None):
        self.txtNumber.yview_moveto(self.txtArea.yview()[0])

    def zoom(self, event):
        if event.delta > 0:
            self.font_size += 1
        else:
            self.font_size -= 1
        self.font_size = max(8, min(self.font_size, 24))
        self.txt_font = ('Roboto', self.font_size)
        self.txtArea.config(font=self.txt_font)
        self.txtNumber.config(font=self.txt_font)
        self.update_line_numbers()

    def compilar(self):
        self.txtTerminal.config(state=tk.NORMAL)
        self.txtTerminal.delete("1.0", tk.END)
        codigo = self.txtArea.get("1.0", tk.END)
        lexer.input(codigo)
        self.tablaTokens.delete(*self.tablaTokens.get_children())
        tabla_simbolos.reinicio_clase()
        
        linea = 0
        columna = 0
        while True:
            tok = lexer.token()
            if not tok:
                break
            linea = tok.lineno
            columna = find_column(codigo, tok)
            linea_columna = f"{linea}/{columna}"
            self.tablaTokens.insert("", tk.END, values=(tok.value, tok.type, linea_columna))

        # Realiza el análisis sintáctico
        parse(codigo)
        
        # Obtén los errores y muéstralos en la interfaz
        errores = obtener_errores()
        for error in errores:
            self.txtTerminal.insert(tk.END, f"{error}\n")

        self.txtTerminal.config(state=tk.DISABLED)  # Deshabilita el modo de escritura para que solo sea lectura
        lexer.lineno = 1
        lexer.lexpos = 0


    def run(self, text):
        lexer.input(text)
        tokens = []
        errores = []
        
        for tok in lexer:
            tokens.append(tok)
        
        # Simular valor y error para la demostración
        value = "Compilación exitosa" if not errores else None
        error = None if not errores else "Error de compilación"
        return value, error, tokens
    
    def open_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.txtArea.delete(1.0, tk.END)
                self.txtArea.insert(tk.END, file.read())
                self.file_path = file_path
                self.notebook.tab(self.notebook.index(self.frame), text=file_path.split('/')[-1])
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

    def guardar_archivo(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.txtArea.get(1.0, tk.END))
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
        else:
            self.guardar_como_nuevo()

    def guardar_como_nuevo(self):
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.txtArea.get(1.0, tk.END))
                self.file_path = file_path
                self.notebook.tab(self.notebook.index(self.frame), text=file_path.split('/')[-1])
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

    def close(self):
        self.notebook.forget(self.frame)

    def llenar_tabla(self, tokens = []):
        for item in self.tablaTokens.get_children():
            self.tablaTokens.delete(item)
            
        for token in tokens:
            self.tablaTokens.insert("", tk.END, values=(token.value, token.type))

class MainApplication:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.interfaz.title("GrassCode - Compiler")
        self.notebook = ttk.Notebook(self.interfaz)
        self.notebook.pack(expand=1, fill='both')
        
        # Dimensiones de la ventana
        window_width = 1000
        window_height = 600
        # Obtener el tamaño de la pantalla
        screen_width = self.interfaz.winfo_screenwidth()
        screen_height = self.interfaz.winfo_screenheight()

        # Calcular la posición x, y para centrar la ventana
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Establecer la geometría de la ventana para que esté centrada
        self.interfaz.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        self.create_menu()
        self.new_file()

        # Establecer el estilo personalizado para el encabezado de la tabla
        style = ttk.Style()
        style.theme_use('default')  # Asegurarse de que estás usando el tema predeterminado

    def create_menu(self):
        menubar = Menu(self.interfaz)
        self.interfaz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nuevo", command=self.new_file)
        filemenu.add_command(label="Abrir", command=self.open_file)
        filemenu.add_command(label="Guardar", command=self.guardar_archivo)
        filemenu.add_command(label="Cerrar", command=self.close_file)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.interfaz.quit)

        menubar.add_cascade(label="Archivo", menu=filemenu)

    def new_file(self):
        GrassCodeEditor(self.notebook)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[("Archivos de texto", "*.txt")],
            defaultextension=".txt")
        if file_path:
            new_editor = GrassCodeEditor(self.notebook)
            new_editor.open_file(file_path)

    def guardar_archivo(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.guardar_archivo()

    def close_file(self):
        current_editor = self.get_current_editor()
        if current_editor:
            # Verifica si el contenido del archivo ha sido modificado
            if current_editor.txtArea.edit_modified():
                respuesta = messagebox.askyesnocancel("Cerrar archivo", "El archivo ha sido modificado. ¿Desea guardar los cambios?")
                if respuesta is None:  # Cancelar
                    return
                elif respuesta:  # Sí
                    current_editor.guardar_archivo()
            current_editor.close()

    def get_current_editor(self):
        current_tab = self.notebook.select()
        if current_tab:
            current_frame = self.interfaz.nametowidget(current_tab)
            return current_frame.editor_instance
        return None

#------------------------------------------------------------------------------
if __name__ == "__main__":
    interfaz = tk.Tk()
    app = MainApplication(interfaz)
    interfaz.mainloop()

# Notas:

# TreeView es el equivalente en Python a JTable en Java
# Columns es la propiedad para definir el nombre de las columnas, por defecto se crea una columna 0,
# por eso se oculta en la primera parte de la configuración.

# Propiedades:
# - Wrap word: Propiedad que le indica al componente que debe hacer un salto de línea si la palabra no cabe en el área.
# - Wrap chart: Igual a la de arriba pero en lugar de llevarse toda una palabra la parte y manda el resto a la siguiente línea.
# - Wrap none: Indica que el texto deberá seguir de manera horizontal hasta llegar al punto de desplazarse de manera horizontal.

# - Los componentes se llaman Widgets y la función grid genera una cuadrícula para posicionar
#   dichos Widgets.
# - Row: Propiedad para establecer en cuál renglón quieres ubicar el componente.
# - Column: Propiedad para establecer en cuál columna quieres ubicar el componente.
# - Padx y Pady: Son propiedades para establecer la separación que tiene tu componente con el límite del renglón (Padx) o la columna (Pady).
#   cuando se manda un valor padx (0, 5) defines los píxeles de separación en el eje x, 0 hacia la izquierda y 5 hacia la derecha.
# - Sticky: Indica hacia qué lados se va a ampliar el componente (Norte, Sur, Este u Oeste). Puedes establecer para un solo sentido o varios.
#   Por ejemplo: ns (Norte y Sur) hará que se expanda hacia arriba y hacia abajo; en cambio, colocar n simplemente hará que rellene hacia arriba.