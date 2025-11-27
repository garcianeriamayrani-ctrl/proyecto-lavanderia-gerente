import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

# La biblioteca PIL (Pillow) es necesaria para manejar imágenes.
# Si aún no la tienes, instala: pip install Pillow

class LavanderosWebApp:
    def __init__(self, root):
        self.root = root
        root.title("Lavandería Lavanderos - Sistema de Gestión (GERENTE)")
        root.geometry("1000x800")
        
        self.user_logged_in = False
        self.user_role = "" 
        self.nav_visible = True
        
        self.imgTk_header = None
        # Usaremos un diccionario para almacenar las referencias de ImageTk de contenido
        # para evitar que sean recolectadas por el garbage collector.
        self.imgTk_content_refs = {} 
        
        # --- COLORES AZULES ESPECIFICADOS ---
        self.COLOR_FONDO_PRINCIPAL = "#E1F5FE"
        self.COLOR_AZUL_BOTON = "#1E88E5" 
        self.COLOR_HEADER = "#091A6F" 
        self.COLOR_NAV_BUTTON = "#5B92E5" 
        self.root.configure(bg=self.COLOR_FONDO_PRINCIPAL)

        # --- ESTILOS (ttk) ---
        self.style = ttk.Style()
        self.style.configure("Content.TFrame", background=self.COLOR_FONDO_PRINCIPAL) 
        self.style.configure("TLabel", background=self.COLOR_FONDO_PRINCIPAL, foreground="black", font=('Arial', 12))
        self.style.configure("Header.TFrame", background=self.COLOR_HEADER)
        self.style.configure("Nav.TFrame", background=self.COLOR_HEADER)
        self.style.configure("Header.TLabel", background=self.COLOR_HEADER, foreground="white", font=('Arial', 28, 'bold'))
        self.style.configure("Nav.TButton", background=self.COLOR_NAV_BUTTON, foreground="#003366", font=('Arial', 12, 'bold'), padding=[20, 10, 20, 10], relief="flat")
        self.style.map("Nav.TButton", background=[('active', '#3A77C8')]) 
        self.style.configure("TButton", background=self.COLOR_AZUL_BOTON, foreground="white", font=('Arial', 12, 'bold'), padding=10)
        self.style.map("TButton", background=[('active', '#1565C0')]) 

        # --- 1. ENCABEZADO (Header) ---
        self.header_frame = ttk.Frame(root, style="Header.TFrame")
        self.header_frame.pack(fill="x", pady=0)
        
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=3)
        self.header_frame.grid_columnconfigure(3, weight=1)
        
        self.menu_button = ttk.Button(self.header_frame, text="☰ Menú", command=self.toggle_nav, style="Nav.TButton")
        self.menu_button.grid(row=0, column=0, padx=(10, 0), pady=15, sticky="nsw")

        self._load_header_image() # Carga lavanderos.png para el logo

        ttk.Label(self.header_frame, text="LAVANDERÍA LAVANDEROS (PANEL GERENTE)", style="Header.TLabel").grid(row=0, column=2, padx=20, pady=15, sticky="w")
        
        search_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        search_frame.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.social_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.social_frame.grid(row=1, column=3, padx=10, pady=5, sticky="e")
        self.login_status_label = ttk.Label(self.social_frame, text="", background=self.COLOR_HEADER, foreground="white", font=('Arial', 10, 'bold'))
        self.login_status_label.pack(side="top", pady=(0, 5))
        
        # --- 2. BARRA DE NAVEGACIÓN ---
        self.nav_frame = ttk.Frame(root, style="Nav.TFrame", height=60)
        self.nav_frame.pack(fill="x", before=None) 
        self.nav_buttons_frame = ttk.Frame(self.nav_frame, style="Nav.TFrame")
        self.nav_buttons_frame.pack(pady=5)
        
        self.create_nav_button(self.nav_buttons_frame, "Inicio", self.show_inicio, side="left")
        self.create_nav_button(self.nav_buttons_frame, "Gestión de Personal", self.show_gestion_personal, side="left") 
        self.create_nav_button(self.nav_buttons_frame, "Reportes Financieros", self.show_reportes_financieros, side="left")
        self.create_nav_button(self.nav_buttons_frame, "Formulario de contacto", self.show_contacto, side="left") 
        self.update_nav_buttons()

        # --- 3. CONTENIDO PRINCIPAL ---
        self.content_frame = ttk.Frame(root, padding=40, style="Content.TFrame") 
        self.content_frame.pack(expand=True, fill="both")

        # Variables y Datos de Perfil 
        self.nombre = tk.StringVar(); self.telefono = tk.StringVar(); self.direccion = tk.StringVar(); self.email_contacto = tk.StringVar()
        self.asunto_contacto = tk.StringVar(); self.username = tk.StringVar(); self.password = tk.StringVar()
        self.profile_data = {
            "Gerente": {
                "Nombre": "García Neri Amayrani", "Puesto": "Gerente General",
                "Email": "gerencia@lavanderos.com", "Teléfono": "55 9876 5432",
                "Sucursal": "Matriz Centro"
            }
        }
        
        self.show_login() 

        # --- 4. FOOTER ---
        self.footer_frame = ttk.Frame(root, style="Header.TFrame")
        self.footer_frame.pack(side="bottom", fill="x", pady=0)
        self.footer_frame.grid_columnconfigure(0, weight=1); self.footer_frame.grid_columnconfigure(1, weight=1) 
        
        footer_info_frame = ttk.Frame(self.footer_frame, style="Header.TFrame")
        footer_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ttk.Label(footer_info_frame, text="🧺", background=self.COLOR_HEADER, foreground="white", font=('Arial', 20, 'bold')).pack(side="left", padx=(0, 10))
        ttk.Label(footer_info_frame, text="Visitas: Inicio | Aviso de Privacidad\nCopyright © 2024 Lavandería Lavanderos.\nTodos los derechos reservados.", 
                  font=('Arial', 10), background=self.COLOR_HEADER, foreground="white", justify="left").pack(side="left")
        
        ttk.Label(self.footer_frame, text="• Políticas de Privacidad\n• Términos y Condiciones", 
                  font=('Arial', 11, 'bold'), background=self.COLOR_HEADER, foreground="white", justify="right").grid(row=0, column=1, padx=20, pady=10, sticky="e")
        

    # ====================================================================================================
    # --- FUNCIONES DE UTILIDAD Y COMPONENTES ---
    # ====================================================================================================

    def _load_header_image(self):
        """Carga y coloca la imagen del logo 'lavanderos.png' en el encabezado (siempre el mismo logo)."""
        try:
            img = Image.open("lavanderos.png") 
            img = img.resize((100, 100))
            self.imgTk_header = ImageTk.PhotoImage(img)
            self.logo_label = tk.Label(self.header_frame, image=self.imgTk_header, bg=self.COLOR_HEADER)
            self.logo_label.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsw")
        except FileNotFoundError:
            self.logo_label = tk.Label(self.header_frame, text="[LOGO]", font=('Arial', 14, 'bold'), bg=self.COLOR_HEADER, fg="white")
            self.logo_label.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsw")

    def _load_content_image(self, parent_frame, filename, size=(200, 200), side="top", padding=(10, 10)):
        """
        Carga y coloca una imagen especificada (por 'filename') en el contenido de una ventana.
        Retorna la etiqueta (Label) creada.
        """
        try:
            img = Image.open(filename) 
            img = img.resize(size) 
            # Guarda la referencia en el diccionario con el nombre del archivo para evitar GC
            self.imgTk_content_refs[filename] = ImageTk.PhotoImage(img) 
            img_label = tk.Label(parent_frame, image=self.imgTk_content_refs[filename], bg=self.COLOR_FONDO_PRINCIPAL)
            img_label.pack(side=side, padx=padding[0], pady=padding[1])
            return img_label
        except FileNotFoundError:
            fallback_label = ttk.Label(parent_frame, text=f"[IMAGEN {filename.upper()}]", font=('Arial', 10, 'italic'), background=self.COLOR_FONDO_PRINCIPAL)
            fallback_label.pack(side=side, padx=padding[0], pady=padding[1])
            return fallback_label
            
    def toggle_nav(self):
        """Oculta o muestra la barra de navegación horizontal (el menú de hamburguesa)."""
        if self.nav_visible:
            self.nav_frame.pack_forget()
            self.menu_button.config(text="☰ Menú (Mostrar)")
        else:
            self.nav_frame.pack(fill="x", before=self.content_frame) 
            self.menu_button.config(text="☰ Menú")
        self.nav_visible = not self.nav_visible

    def create_nav_button(self, parent, text, command, side="left"):
        btn = ttk.Button(parent, text=text, command=command, style="Nav.TButton")
        btn.pack(side=side, padx=10, pady=10) 
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Limpiar referencias de imágenes de contenido
        self.imgTk_content_refs = {}
            
    def update_content_label(self, text, font=('Arial', 14), image_filename="lavanderos.png", image_size=(200, 200)):
        """Utilizado principalmente para mensajes simples o de acceso denegado."""
        self.clear_content()
        
        # Centrar el contenido
        center_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        
        # Colocar imagen más grande en el centro superior
        self._load_content_image(center_frame, image_filename, size=image_size, side="top", padding=(30, 30)) 
        
        new_label = ttk.Label(center_frame, text=text, font=font, background=self.COLOR_FONDO_PRINCIPAL, wraplength=700, justify="center")
        new_label.pack(pady=30, padx=20) 
        
    def update_nav_buttons(self):
        """Actualiza los botones de Perfil/Salir o Login en el social_frame."""
        for widget in self.social_frame.winfo_children():
            if isinstance(widget, ttk.Button): widget.destroy()
        
        self.login_status_label.pack_forget()
        self.login_status_label.pack(side="top", pady=(0, 5))
        
        if self.user_logged_in:
            self.login_status_label.config(text=f"Bienvenido, {self.user_role}")
            btn_perfil = ttk.Button(self.social_frame, text="👤 Perfil", command=self.show_perfil, style="Nav.TButton")
            btn_perfil.pack(side="left", padx=5)
            btn_logout = ttk.Button(self.social_frame, text="❌ Salir", command=self.logout, style="Nav.TButton")
            btn_logout.pack(side="left", padx=5)
        else:
            self.login_status_label.config(text="HABLA CON NOSOTROS")
            btn_login = ttk.Button(self.social_frame, text="🔑 Login", command=self.show_login, style="Nav.TButton")
            btn_login.pack(side="left", padx=5)

    # ====================================================================================================
    # --- FUNCIONES DE LOGIN Y AUTENTICACIÓN (USA gerente.png) ---
    # ====================================================================================================

    def show_login(self):
        self.clear_content()
        
        # 1. Main container for side-by-side layout
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=20)
        
        # 2. Image (Left side) - Más grande (200x200)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="left", padx=50, fill="y")
        self._load_content_image(img_frame, "gerente.png", size=(200, 200), side="top", padding=(10, 30)) 
        
        # 3. Content (Right side)
        content_frame = ttk.Frame(main_container, style="Content.TFrame", padding=20)
        content_frame.pack(side="left", expand=True, fill="both")
        
        ttk.Label(content_frame, text="🔑 Iniciar Sesión (SOLO GERENTE)", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 30))
        login_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=20)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Usuario:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(login_frame, textvariable=self.username, width=30).grid(row=1, column=1, sticky="w", padx=5, pady=10)
        ttk.Label(login_frame, text="Contraseña:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(login_frame, textvariable=self.password, show="*", width=30).grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        ttk.Button(login_frame, text="Ingresar", command=self.attempt_login).grid(row=3, column=0, columnspan=2, pady=20)

    def attempt_login(self):
        """Verifica las credenciales del Gerente."""
        if self.username.get() == "gerente" and self.password.get() == "1234":
            self.user_logged_in = True
            self.user_role = "Gerente" 
            self.update_nav_buttons()
            self.show_reportes_financieros() 
            messagebox.showinfo("Éxito", "Bienvenido, Gerente.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña de Gerente incorrectos.")
            self.password.set("")

    def logout(self):
        """Cierra la sesión y regresa a la pantalla de login."""
        self.user_logged_in = False
        self.user_role = ""
        self.username.set(""); self.password.set("")
        self.update_nav_buttons()
        self.show_login()
        messagebox.showinfo("Cerrar Sesión", "Has cerrado la sesión correctamente.")
        
    # --- Funciones de Simulación de Acciones ---

    def simulate_edit_data(self):
        """Abre una ventana para editar los datos del Gerente."""
        top = tk.Toplevel(self.root)
        top.title("✏️ Editar Datos del Perfil")
        top.geometry("400x300")
        
        frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Editar Información", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        ttk.Entry(frame, width=40).pack()
        ttk.Label(frame, text="Email:").pack(pady=5)
        ttk.Entry(frame, width=40).pack()
        ttk.Label(frame, text="Teléfono:").pack(pady=5)
        ttk.Entry(frame, width=40).pack()
        
        def save_data():
            messagebox.showinfo("Guardar", "Datos actualizados exitosamente.")
            top.destroy()

        ttk.Button(frame, text="Guardar Cambios", command=save_data).pack(pady=20)

    def simulate_change_password(self):
        """Abre una ventana para cambiar la contraseña del Gerente."""
        top = tk.Toplevel(self.root)
        top.title("🔒 Cambiar Contraseña")
        top.geometry("350x250")
        
        frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Cambiar Contraseña", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Contraseña Actual:").pack(pady=5)
        ttk.Entry(frame, show="*", width=30).pack()
        ttk.Label(frame, text="Nueva Contraseña:").pack(pady=5)
        ttk.Entry(frame, show="*", width=30).pack()

        def update_password():
            messagebox.showinfo("Actualizar", "Contraseña cambiada exitosamente. Debe iniciar sesión de nuevo.")
            self.logout()
            top.destroy()

        ttk.Button(frame, text="Actualizar Contraseña", command=update_password).pack(pady=20)


    def simulate_manage_employees(self):
        """Abre una ventana para simular la administración de empleados."""
        top = tk.Toplevel(self.root)
        top.title("🧑‍💻 Administrador de Empleados")
        top.geometry("600x450")
        
        frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Panel de Gestión de Personal", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(frame, columns=("Nombre", "Puesto", "Horario"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Puesto", text="Puesto")
        tree.heading("Horario", text="Horario")
        
        tree.insert("", tk.END, values=("Luis Pérez", "Lavandero", "7:00 - 15:00"))
        tree.insert("", tk.END, values=("Ana Ruiz", "Atención Cliente", "10:00 - 18:00"))
        tree.insert("", tk.END, values=("Javier Cruz", "Repartidor", "9:00 - 17:00"))
        
        tree.pack(fill="both", expand=True, pady=10)
        
        btn_frame = ttk.Frame(frame, style="Content.TFrame")
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="➕ Nuevo Empleado", command=lambda: messagebox.showinfo("Gestión", "Abriendo formulario para nuevo empleado...")).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="⚙️ Editar Seleccionado", command=lambda: messagebox.showinfo("Gestión", "Abriendo ficha para editar datos...")).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="➖ Dar de Baja", command=lambda: messagebox.showwarning("Gestión", "Confirmar baja del empleado...")).pack(side="left", padx=10)

    def simulate_contact_response(self):
        """Abre una ventana para responder un formulario de contacto simulado."""
        top = tk.Toplevel(self.root)
        top.title("📧 Responder Formulario de Contacto")
        top.geometry("550x450")
        
        frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Responder Solicitud", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Asunto: Solicitud de material de limpieza", font=('Arial', 12, 'italic')).pack(pady=5)
        ttk.Label(frame, text="Mensaje Original: Necesitamos urgentemente más detergente azul y suavizante para la sucursal Centro.").pack(pady=5)
        
        ttk.Label(frame, text="Escriba su respuesta:", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        response_text = tk.Text(frame, height=8, width=60)
        response_text.pack(pady=5)

        def send_response():
            response = response_text.get("1.0", tk.END).strip()
            if response:
                messagebox.showinfo("Respuesta Enviada", f"Respuesta enviada:\n\n'{response}'\n\nEl formulario se marcó como 'Atendido'.")
                top.destroy()
            else:
                messagebox.showerror("Error", "Debe escribir una respuesta.")

        ttk.Button(frame, text="✉️ Enviar Respuesta y Marcar Atendido", command=send_response).pack(pady=20)

    # ====================================================================================================
    # --- FUNCIONES DE VISTAS (APLICANDO LAYOUT LADO A LADO) ---
    # ====================================================================================================
        
    def show_inicio(self):
        self.clear_content()
        
        # 1. Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=20, padx=20)
        
        # 2. Frame de Imagen (Lado Derecho) - Imagen más grande (250x250)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_content_image(img_frame, "lavadoras.png", size=(250, 250), side="top", padding=(10, 30)) 
        
        # 3. Frame de Contenido de Texto (Lado Izquierdo)
        text_frame = ttk.Frame(main_container, style="Content.TFrame"); 
        text_frame.pack(side="left", expand=True, fill="both")
        
        texto_completo_inicio = ("Hemos logrado el éxito porque nuestra prioridad es tu tiempo y la calidad " 
                                 "en el cuidado de tu ropa. Nos especializamos en ofrecer un servicio integral a " 
                                 "domicilio: tú agendas la recolección y la entrega a través de nuestra " 
                                 "plataforma, y nosotros nos encargamos del resto.\n\n" 
                                 "Nuestra Misión es ofrecer el mejor servicio de lavandería a domicilio, " 
                                 "garantizando el cuidado de tu ropa con los más altos estándares de calidad.\n\n" 
                                 "Nuestra Visión es ser la lavandería líder en el mercado, reconocida por " 
                                 "la puntualidad en la recolección y entrega, y nuestro compromiso ecológico.")
        
        ttk.Label(text_frame, text="🧼 ¡Bienvenido al Panel de Control Gerencial! 🧺", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 20), anchor="w")
        ttk.Label(text_frame, text=texto_completo_inicio, font=('Arial', 14), foreground="black", background=self.COLOR_FONDO_PRINCIPAL, wraplength=550, justify="left").pack(pady=10, padx=20, anchor="w")


    def show_perfil(self):
        self.clear_content()
        if not self.user_logged_in or self.user_role != "Gerente":
            self.update_content_label("Acceso Denegado. Por favor, inicie sesión como Gerente.", font=('Arial', 16, 'bold'), image_filename="gerente.png", image_size=(200, 200))
            return
        
        # 1. Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)

        # 2. Frame de Imagen (Lado Derecho)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        # *** Uso de la imagen gerente.png para Perfil (200x200) ***
        self._load_content_image(img_frame, "gerente.png", size=(200, 200), side="top", padding=(10, 10)) 
            
        # 3. Frame de Contenido (Lado Izquierdo)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")
        
        ttk.Label(content_wrapper, text="⚙️ Perfil de Gerente", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        perfil_frame = ttk.Frame(content_wrapper, style="Content.TFrame", padding=20); perfil_frame.pack(pady=10, anchor="w")
        perfil_data = self.profile_data["Gerente"]
        
        r = 0
        for key, value in perfil_data.items():
            ttk.Label(perfil_frame, text=f"{key}:", font=('Arial', 12, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).grid(row=r, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(perfil_frame, text=value, background=self.COLOR_FONDO_PRINCIPAL).grid(row=r, column=1, sticky="w", padx=10, pady=5)
            r += 1
        
        config_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); config_frame.pack(pady=20, anchor="w")
        ttk.Button(config_frame, text="✏️ Editar Datos", command=self.simulate_edit_data).pack(side="left", padx=10)
        ttk.Button(config_frame, text="🔒 Cambiar Contraseña", command=self.simulate_change_password).pack(side="left", padx=10)

        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="👨‍💼 Gestión de Personal", command=self.show_gestion_personal).pack(side="left", padx=10)
        ttk.Button(action_frame, text="📈 Reportes Financieros", command=self.show_reportes_financieros).pack(side="left", padx=10)


    def show_gestion_personal(self):
        self.clear_content()
        if not self.user_logged_in or self.user_role != "Gerente":
            self.update_content_label("Acceso Denegado. Solo el Gerente puede acceder a la Gestión de Personal.", font=('Arial', 16, 'bold'), image_filename="personal.png", image_size=(200, 200))
            return
        
        # 1. Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        
        # 2. Frame de Imagen (Lado Izquierdo)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="left", padx=30, fill="y")
        # *** Uso de la imagen personal.png (200x200) ***
        self._load_content_image(img_frame, "personal.png", size=(200, 200), side="top", padding=(10, 10)) 

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="left", padx=20, fill="y")
        # *** Uso de la imagen personal.png (200x200) ***
        self._load_content_image(img_frame, "lavando.png", size=(200, 200), side="top", padding=(5, 5))
            
        # 3. Frame de Contenido (Lado Derecho)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")
            
        info_text = ("👨‍💼 **Gestión de Personal**\n\nAquí puede administrar a los empleados, ver horarios, solicitar altas o bajas, y gestionar nóminas.\n\n"
                      "**Empleados Activos:** 15\n"
                      "**Próxima Nómina:** 2025-11-30\n")
        
        ttk.Label(content_wrapper, text="Panel de Recursos Humanos", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=550).pack(pady=10, padx=20, anchor="w")

        manage_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); manage_frame.pack(pady=20, anchor="w")
        ttk.Button(manage_frame, text="🧑‍💻 Administrar Empleados", command=self.simulate_manage_employees).pack(side="top", padx=10)


    def show_reportes_financieros(self):
        self.clear_content()
        if not self.user_logged_in or self.user_role != "Gerente":
            self.update_content_label("Acceso Denegado. Solo el Gerente puede acceder a los Reportes Financieros.", font=('Arial', 16, 'bold'), image_filename="estadisticas.png", image_size=(200, 200))
            return
            
        # 1. Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        
        # 2. Frame de Imagen (Lado Derecho) - Imagen grande (250x250)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_content_image(img_frame, "estadisticas.png", size=(250, 250), side="top", padding=(10, 10)) 
        
        # 3. Frame de Contenido (Lado Izquierdo)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="📈 Reportes Financieros", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Acceda a los datos críticos del negocio para la toma de decisiones.\n\n"
                      "**Ventas de Noviembre (al día):** $85,450.00\n"
                      "**Costo Operativo Mensual:** $45,000.00\n"
                      "**Margen Bruto (Noviembre):** $40,450.00\n\n"
                      "**Gráfico de Rendimiento Mensual (Ventas vs. Costos):**")
        
        info_label = ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450)
        info_label.pack(pady=10, padx=20, anchor="w")

        # --- SIMULACIÓN DE GRÁFICA MEDIANTE TABLA DE DATOS ---
        graph_frame = ttk.Frame(content_wrapper, style="Content.TFrame")
        graph_frame.pack(pady=10, padx=20, anchor="w")

        data_table = ttk.Treeview(graph_frame, columns=('Mes', 'Ventas', 'Costos'), show='headings', height=6)
        data_table.heading('Mes', text='Mes')
        data_table.heading('Ventas', text='Ventas ($)')
        data_table.heading('Costos', text='Costos ($)')
        data_table.column('Mes', width=100, anchor='center')
        data_table.column('Ventas', width=150, anchor='e')
        data_table.column('Costos', width=150, anchor='e')

        data_table.insert('', 'end', values=('Agosto', '70,000', '40,000'))
        data_table.insert('', 'end', values=('Septiembre', '75,500', '42,000'))
        data_table.insert('', 'end', values=('Octubre', '82,000', '44,500'))
        data_table.insert('', 'end', values=('Noviembre', '85,450', '45,000'))
        
        data_table.pack()

        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=10, anchor="w")
        ttk.Button(action_frame, text="💵 Reporte de Ventas", command=lambda: messagebox.showinfo("Reportes", "Generando Reporte de Ventas...")).pack(side="left", padx=10)
        ttk.Button(action_frame, text="💰 Estado de Resultados", command=lambda: messagebox.showinfo("Reportes", "Generando Estado de Resultados...")).pack(side="left", padx=10)
        
    def show_contacto(self):
        self.clear_content()
        if not self.user_logged_in:
            self.update_content_label("Acceso Denegado. Por favor, inicie sesión.", font=('Arial', 16, 'bold'), image_filename="contacto.png", image_size=(200, 200))
            return

        # 1. Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self.content_frame, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        
        # 2. Frame de Imagen (Lado Izquierdo)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="left", padx=30, fill="y")
        # *** Uso de la imagen contacto.png (200x200) ***
        self._load_content_image(img_frame, "contacto.png", size=(200, 200), side="top", padding=(10, 30)) 
        
        # 3. Frame de Contenido (Lado Derecho)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")
        
        ttk.Label(content_wrapper, text="✉️ Formulario de Contacto (Interno)", font=('Arial', 18, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 20), anchor="w")
        
        info_text = ("Utilice este formulario para comunicarse con el equipo de soporte o administración interna.\n\n"
                      "**Mensajes Pendientes:** 5\n"
                      "**Último Mensaje:** 2025-11-25 10:30 AM (Solicitud de material de limpieza)")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=550).pack(pady=20, padx=20, anchor="w")
        
        contact_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); contact_frame.pack(pady=20, anchor="w")
        ttk.Button(contact_frame, text="✅ Responder / Marcar Atendido", command=self.simulate_contact_response).pack(side="top", padx=10)


if __name__ == "__main__":
    # La siguiente función es un truco para asegurar que tkinter pueda
    # encontrar las imágenes cuando el script se empaqueta como ejecutable.
    def resource_path(relative_path):
        """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Nota: En un entorno de desarrollo normal (sin PyInstaller),
    # las imágenes deben estar en el mismo directorio que este script.
    
    root = tk.Tk()
    app = LavanderosWebApp(root)
    root.mainloop()