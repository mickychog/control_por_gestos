import tkinter as tk
from tkinter import ttk, PhotoImage
import threading
import queue 
import sys
import os
from datetime import datetime
from PIL import Image, ImageTk 


try:
    from src.gesture_controller import GestureController
except ImportError as e:
    print(f"Error al importar GestureController: {e}")
    print(".")
    print("También verifica las importaciones internas de gesture_controller.py ( .enums, .config).")
    sys.exit(1)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control por Gestos")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.detection_thread = None
        self.stop_event = threading.Event()
        self.gesture_queue = queue.Queue() 

        # Pasamos la cola al GestureController
        self.gesture_controller = GestureController(stop_event=self.stop_event, gesture_queue=self.gesture_queue)

        self.create_widgets()
        self.after_id = None # Para almacenar el ID del método after
        self.process_queue() # Iniciar el procesamiento de la cola

    def create_widgets(self):
        # Frame superior para el título y la imagen
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        # Título del proyecto
        title_label = ttk.Label(top_frame, text="CONTROL POR GESTOS", font=("Arial", 20, "bold"))
        title_label.pack(side=tk.LEFT, padx=20)

        # Campo para la imagen de la universidad
        image_path = "escudoUSFX.png" # Cambia esto a la ruta de tu imagen
        try:
            img = Image.open(image_path)
            # Redimensionar la imagen para que encaje bien (ej. 100 píxeles de ancho)
            aspect_ratio = img.height / img.width
            new_width = 100
            new_height = int(new_width * aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.uni_logo = ImageTk.PhotoImage(img)

            uni_logo_label = ttk.Label(top_frame, image=self.uni_logo)
            uni_logo_label.pack(side=tk.RIGHT, padx=20)
        except FileNotFoundError:
            print(f"Error: La imagen '{image_path}' no se encontró. Asegúrate de que la ruta sea correcta.")
            no_image_label = ttk.Label(top_frame, text="[Imagen no encontrada]", font=("Arial", 10))
            no_image_label.pack(side=tk.RIGHT, padx=20)
        except Exception as e:
            print(f"Error al cargar o procesar la imagen '{image_path}': {e}")
            no_image_label = ttk.Label(top_frame, text="[Error de imagen]", font=("Arial", 10))
            no_image_label.pack(side=tk.RIGHT, padx=20)


        # Botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(
            button_frame,
            text="Iniciar Detección",
            command=self.start_detection,
            style="Green.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(
            button_frame,
            text="Detener Detección",
            command=self.stop_detection,
            style="Red.TButton"
        )
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        # Estilos para los botones
        style = ttk.Style()
        style.configure("Green.TButton", background="#4CAF50", foreground="black", font=("Arial", 12))
        style.map("Green.TButton",
                background=[('active', '#4CAF50'), ('!disabled', '#66BB6A')])
        style.configure("Red.TButton", background="#f44336", foreground="black", font=("Arial", 12))
        style.map("Red.TButton",
                background=[('active', '#f44336'), ('!disabled', '#ef5350')])

        # Consola de gestos
        console_frame = ttk.LabelFrame(self.root, text="Gestos Detectados")
        console_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.console_text = tk.Text(console_frame, wrap=tk.WORD, state=tk.DISABLED,
                                    height=10, bg="#2b2b2b", fg="#00FF00", font=("Consolas", 10))
        self.console_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Scrollbar para la consola
        console_scrollbar = ttk.Scrollbar(self.console_text, command=self.console_text.yview)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console_text.config(yscrollcommand=console_scrollbar.set)

        # Estado inicial de los botones
        self.update_button_states(False)

    def update_button_states(self, is_running):
        if is_running:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def append_to_console(self, message):
        """Añade un mensaje a la consola de gestos."""
        self.console_text.config(state=tk.NORMAL) # Habilitar para escribir
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END) # Auto-scroll al final
        self.console_text.config(state=tk.DISABLED) # Deshabilitar de nuevo

    def process_queue(self):
        """
        Lee los mensajes de la cola y los muestra en la consola de la GUI.
        Se llama periódicamente usando `after`.
        """
        try:
            while True:
                message = self.gesture_queue.get_nowait()
                # print(f"DEBUG: Mensaje recibido de la cola: {message}") # Debug
                self.append_to_console(message)
        except queue.Empty:
            pass # No hay mensajes en la cola

        # Llamar a este método de nuevo después de 100 ms
        self.after_id = self.root.after(100, self.process_queue)


    def start_detection(self):
        if self.detection_thread is None or not self.detection_thread.is_alive():
            self.append_to_console("Iniciando detección...")
            self.stop_event.clear()
            self.detection_thread = threading.Thread(target=self.gesture_controller.start_detection)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            self.update_button_states(True)
        else:
            self.append_to_console("La detección ya está en curso.")

    def stop_detection(self):
        if self.detection_thread and self.detection_thread.is_alive():
            self.append_to_console("Deteniendo detección...")
            self.gesture_controller.stop_detection()
            # No actualizamos el estado de los botones a "detenido" inmediatamente aquí,
            # ya que el hilo aún puede estar limpiando recursos.
            # El mensaje "Detección detenida." se enviará a la cola cuando el hilo termine,
            # lo cual es una mejor señal para el usuario.
            self.root.after(500, lambda: self.update_button_states(False)) # Retrasar la actualización un poco
        else:
            self.append_to_console("La detección no está en curso.")
            self.update_button_states(False)

    def on_closing(self):
        print("Cerrando la aplicación GUI.")
        if self.after_id:
            self.root.after_cancel(self.after_id) # Detener el loop de after
        self.stop_detection()
        if self.detection_thread and self.detection_thread.is_alive():
            print("Esperando que el hilo de detección termine...")
            self.detection_thread.join(timeout=2) # Esperar un poco más
            if self.detection_thread.is_alive():
                print("Advertencia: El hilo de detección no se detuvo a tiempo al cerrar.")
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()