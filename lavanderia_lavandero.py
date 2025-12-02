import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

# ====================================================================================================
# --- UTILERÍA ---
# ====================================================================================================

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller."""
    try:
        # Ruta en el entorno empaquetado (PyInstaller)
        base_path = sys._MEIPASS
    except Exception:
        # Ruta en el entorno de desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ====================================================================================================
# --- VISTAS BASE Y DE PÁGINAS ---
# ====================================================================================================

class BaseView(ttk.Frame):
    """Clase base para todas las vistas de contenido."""
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.app_controller = app_controller
        self.config(style="Content.TFrame")
        
        # Diccionario para mantener referencias de ImageTk y evitar que el garbage collector las elimine
        self.imgTk_refs = {} 

    def _load_image(self, filename, size=(200, 200), parent_frame=None, side="top", padding=(10, 10)):
        """Carga una imagen y la coloca en el frame especificado, guardando la referencia local."""
        frame_to_use = parent_frame if parent_frame else self
        try:
            path = resource_path(filename)
            img = Image.open(path) 
            img = img.resize(size) 
            # Guarda la referencia
            self.imgTk_refs[filename] = ImageTk.PhotoImage(img) 
            img_label = tk.Label(frame_to_use, image=self.imgTk_refs[filename], bg=self.app_controller.COLOR_FONDO_PRINCIPAL)
            img_label.pack(side=side, padx=padding[0], pady=padding[1])
            return img_label
        except FileNotFoundError:
            fallback_label = ttk.Label(frame_to_use, text=f"[IMAGEN {filename.upper()}]", font=('Arial', 10, 'italic'), background=self.app_controller.COLOR_FONDO_PRINCIPAL)
            fallback_label.pack(side=side, padx=padding[0], pady=padding[1])
            return fallback_label
        except Exception as e:
            fallback_label = ttk.Label(frame_to_use, text=f"[ERROR CARGA {filename}: {e}]", font=('Arial', 10, 'italic'), background=self.app_controller.COLOR_FONDO_PRINCIPAL)
            fallback_label.pack(side=side, padx=padding[0], pady=padding[1])
            return fallback_label
        
    def destroy(self):
        """Limpia las referencias de imágenes al cerrar la vista."""
        self.imgTk_refs = {} 
        super().destroy()

class LoginView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        self.username = tk.StringVar(value=app_controller.username.get())
        self.password = tk.StringVar(value=app_controller.password.get())
        self.create_widgets()
        
    def create_widgets(self):

        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="left", padx=50, fill="y")
        self._load_image("gerente.png", size=(200, 200), parent_frame=img_frame, side="top", padding=(10, 30)) 
        

        content_frame = ttk.Frame(main_container, style="Content.TFrame", padding=20)
        content_frame.pack(side="left", expand=True, fill="both")
        
        ttk.Label(content_frame, text="🔑 Iniciar Sesión (SOLO GERENTE)", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 30))
        login_frame = ttk.Frame(content_frame, style="Content.TFrame", padding=20)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Usuario:", background=self.app_controller.COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(login_frame, textvariable=self.username, width=30).grid(row=1, column=1, sticky="w", padx=5, pady=10)
        ttk.Label(login_frame, text="Contraseña:", background=self.app_controller.COLOR_FONDO_PRINCIPAL).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(login_frame, textvariable=self.password, show="*", width=30).grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        ttk.Button(login_frame, text="Ingresar", command=lambda: self.app_controller.attempt_login(self.username.get(), self.password.get())).grid(row=3, column=0, columnspan=2, pady=20)


class InicioView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=20, padx=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("lavadoras.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 30)) 
        

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
        
        ttk.Label(text_frame, text="🧼 ¡Bienvenido al Panel de Control Gerencial! 🧺", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 20), anchor="w")
        ttk.Label(text_frame, text=texto_completo_inicio, font=('Arial', 14), foreground="black", background=self.app_controller.COLOR_FONDO_PRINCIPAL, wraplength=550, justify="left").pack(pady=10, padx=20, anchor="w")


class PerfilView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return

        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("gerente.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Por favor, inicie sesión como Gerente.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)
        
    def create_widgets(self):

        main_container = ttk.Frame(self, style="Content.TFrame")
        
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("gerente.png", size=(200, 200), parent_frame=img_frame, side="top", padding=(10, 10)) 

        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")
        
        ttk.Label(content_wrapper, text="⚙️ Perfil de Gerente", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        perfil_frame = ttk.Frame(content_wrapper, style="Content.TFrame", padding=20); perfil_frame.pack(pady=10, anchor="w")
        perfil_data = self.app_controller.profile_data["Gerente"]
        
        r = 0
        for key, value in perfil_data.items():
            ttk.Label(perfil_frame, text=f"{key}:", font=('Arial', 12, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).grid(row=r, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(perfil_frame, text=value, background=self.app_controller.COLOR_FONDO_PRINCIPAL).grid(row=r, column=1, sticky="w", padx=10, pady=5)
            r += 1
        
        config_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); config_frame.pack(pady=20, anchor="w")
        ttk.Button(config_frame, text="✏️ Editar Datos", command=self.app_controller.simulate_edit_data).pack(side="left", padx=10)
        ttk.Button(config_frame, text="🔒 Cambiar Contraseña", command=self.app_controller.simulate_change_password).pack(side="left", padx=10)

        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="👨‍💼 Gestión de Personal", command=lambda: self.app_controller.show_view(GestionPersonalView)).pack(side="left", padx=10)
        ttk.Button(action_frame, text="📈 Reportes Financieros", command=lambda: self.app_controller.show_view(ReportesFinancierosView)).pack(side="left", padx=10)


class GestionPersonalView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return
            
        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("personal.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Solo el Gerente puede acceder a la Gestión de Personal.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)
        
    def create_widgets(self):
        # Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        
        # Frame de Imágenes (Lado Izquierdo)
        img_container = ttk.Frame(main_container, style="Content.TFrame")
        img_container.pack(side="left", padx=30, fill="y")
        self._load_image("personal.png", size=(200, 200), parent_frame=img_container, side="top", padding=(10, 10))
        self._load_image("lavando.png", size=(200, 200), parent_frame=img_container, side="top", padding=(5, 5)) 

        # Frame de Contenido (Lado Derecho)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")
            
        ttk.Label(content_wrapper, text="👨‍💼 Gestión de Personal", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Administración de la plantilla, registro de nuevos empleados y control de asistencia.\n\n"
                     f"**Empleados Activos:** {len(self.app_controller.employees)}\n"
                     "**Faltas en la última semana:** 2 (Ana Ruiz, Juan Salas)\n"
                     "**Próxima Evaluación de Desempeño:** Enero 2026")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450).pack(pady=10, padx=20, anchor="w")
        
        manage_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); manage_frame.pack(pady=20, anchor="w")
        ttk.Button(manage_frame, text="🧑‍💻 Administrar Empleados", command=self.app_controller.simulate_manage_employees).pack(side="top", padx=10)
        

class ReportesFinancierosView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return

        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("estadisticas.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Solo el Gerente puede acceder a los Reportes Financieros.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)

    def create_widgets(self):
        # Contenedor principal para distribución lado a lado
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)
        
        # Frame de Imagen (Lado Derecho)
        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("estadisticas.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 10)) 
        
        # Frame de Contenido (Lado Izquierdo)
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="📈 Reportes Financieros", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Acceda a los datos críticos del negocio para la toma de decisiones.\n\n"
                      "**Ventas de Noviembre (al día):** $85,450.00\n"
                      "**Costo Operativo Mensual:** $45,000.00\n"
                      "**Margen Bruto (Noviembre):** $40,450.00\n\n"
                      "**Gráfico de Rendimiento Mensual (Ventas vs. Costos):**")
        
        info_label = ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450)
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
        ttk.Button(action_frame, text="💵 Reporte de Ventas", command=self.app_controller.simulate_sales_report).pack(side="left", padx=10)
        ttk.Button(action_frame, text="💰 Estado de Resultados", command=self.app_controller.simulate_income_statement).pack(side="left", padx=10)


class InventarioView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return
            
        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("inventario.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Solo el Gerente puede acceder al Inventario.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)
        
    def create_widgets(self):
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("inventario.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 10)) 
        
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="🧺 Gestión de Inventario", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Control total de insumos, químicos y refacciones de equipos.\n\n"
                     "**Nivel de Stock de Detergente Azul:** Bajo (45 unidades)\n"
                     "**Próximo Pedido Programado:** 2025-12-05\n"
                     "**Valor Total de Inventario:** $15,500.00")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450).pack(pady=10, padx=20, anchor="w")
        
        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="📋 Ver Stock Actual", command=self.app_controller.simulate_view_stock).pack(side="left", padx=10)
        ttk.Button(action_frame, text="🛒 Registrar Nuevo Pedido", command=self.app_controller.simulate_make_order).pack(side="left", padx=10)
        ttk.Button(action_frame, text="📦 Seguimiento de Pedidos", command=self.app_controller.simulate_view_orders).pack(side="left", padx=10)


class SucursalesView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return

        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("sucursales.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Solo el Gerente puede acceder a las Sucursales.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)

    def create_widgets(self):
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("sucursales.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 10)) 
        
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="🏢 Gestión de Sucursales", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Monitorea el rendimiento, estado de equipos y capacidad operativa de cada ubicación.\n\n"
                     f"**Sucursales Operativas:** {len([s for s in self.app_controller.sucursales if s['Estado'] == 'Operando'])}\n"
                     "**Última Auditoría de Calidad:** Norte (Aprobada)\n"
                     "**Mantenimientos Pendientes:** 1 (Lavadora Industrial #3 en Centro)")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450).pack(pady=10, padx=20, anchor="w")
        
        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="🔍 Ver Detalle de Rendimiento", command=self.app_controller.simulate_view_sucursales).pack(side="left", padx=10)
        ttk.Button(action_frame, text="🛠️ Solicitar Mantenimiento", command=self.app_controller.simulate_request_maintenance).pack(side="left", padx=10)
        ttk.Button(action_frame, text="➕ Abrir Nueva Sucursal", command=self.app_controller.simulate_open_new_sucursal).pack(side="left", padx=10) 

class ServiciosView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)
        
        if not app_controller.user_logged_in or app_controller.user_role != "Gerente":
            self.show_access_denied()
            return
            
        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("servicios.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Solo el Gerente puede acceder a la Gestión de Servicios.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)
        
    def create_widgets(self):
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("servicios.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 10)) 
        
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="🏷️ Gestión de Servicios y Precios", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Administración centralizada de todos los servicios ofrecidos, tarifas y promociones.\n\n"
                     "**Tarifa Base Actual (por Kg):** $25.00\n"
                     "**Servicio Más Popular:** Lavado Básico\n"
                     "**Promociones Activas:** 2")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450).pack(pady=10, padx=20, anchor="w")
        
        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="📝 Modificar Servicios", command=self.app_controller.simulate_edit_services).pack(side="left", padx=10)
        ttk.Button(action_frame, text="🏷️ Ajustar Precios y Promociones", command=self.app_controller.simulate_adjust_prices).pack(side="left", padx=10)


class ContactoView(BaseView):
    def __init__(self, parent, app_controller, **kwargs):
        super().__init__(parent, app_controller, **kwargs)

        if not app_controller.user_logged_in:
            self.show_access_denied()
            return
            
        self.create_widgets()

    def show_access_denied(self):
        center_frame = ttk.Frame(self, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        self._load_image("contacto.png", size=(200, 200), parent_frame=center_frame, side="top", padding=(30, 30)) 
        ttk.Label(center_frame, text="Acceso Denegado. Por favor, inicie sesión.", font=('Arial', 16, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=30, padx=20)
        
    def create_widgets(self):
        main_container = ttk.Frame(self, style="Content.TFrame")
        main_container.pack(expand=True, fill="both", pady=10, padx=20)

        img_frame = ttk.Frame(main_container, style="Content.TFrame")
        img_frame.pack(side="right", padx=30, fill="y")
        self._load_image("contacto.png", size=(250, 250), parent_frame=img_frame, side="top", padding=(10, 10)) 
        
        content_wrapper = ttk.Frame(main_container, style="Content.TFrame")
        content_wrapper.pack(side="left", expand=True, fill="both")

        ttk.Label(content_wrapper, text="📧 Buzón de Contacto", font=('Arial', 18, 'bold'), background=self.app_controller.COLOR_FONDO_PRINCIPAL).pack(pady=(10, 20), anchor="w")
        
        info_text = ("Revisión de solicitudes de clientes, quejas y consultas internas.\n\n"
                     "**Tickets Pendientes (Gerencia):** 1\n"
                     "**Última Queja:** Demora en la entrega (Cliente: Carla Pérez)\n"
                     "**Tiempo Promedio de Respuesta:** 3 horas")
        
        ttk.Label(content_wrapper, text=info_text, font=('Arial', 14), background=self.app_controller.COLOR_FONDO_PRINCIPAL, justify="left", wraplength=450).pack(pady=10, padx=20, anchor="w")
        
        # Simulación de lista de tickets
        tickets_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); tickets_frame.pack(pady=10, anchor="w")
        ttk.Label(tickets_frame, text="Tickets Pendientes:", font=('Arial', 12, 'bold')).pack(anchor="w")
        
        ticket_list = ttk.Treeview(tickets_frame, columns=("ID", "Asunto", "Estado"), show="headings", height=3)
        ticket_list.heading("ID", text="ID"); ticket_list.column("ID", width=50)
        ticket_list.heading("Asunto", text="Asunto"); ticket_list.column("Asunto", width=250)
        ticket_list.heading("Estado", text="Estado"); ticket_list.column("Estado", width=100)
        
        ticket_list.insert("", tk.END, values=("T1001", "Solicitud de material de limpieza (Centro)", "Pendiente"), tags=('pendiente',))
        ticket_list.insert("", tk.END, values=("T0998", "Fuga en lavadora industrial", "Atendido"))
        
        ticket_list.tag_configure('pendiente', background='#FFFDE7') 
        ticket_list.pack(pady=5)
        
        action_frame = ttk.Frame(content_wrapper, style="Content.TFrame"); action_frame.pack(pady=20, anchor="w")
        ttk.Button(action_frame, text="📧 Abrir Ticket y Responder", command=self.app_controller.simulate_contact_response).pack(side="left", padx=10)


# ====================================================================================================
# --- CLASE PRINCIPAL DE LA APLICACIÓN (CONTROLADOR) ---
# ====================================================================================================

class LavanderosWebApp:
    def __init__(self, root):
        self.root = root
        root.title("Lavandería Lavanderos - Sistema de Gestión (GERENTE)")
        root.geometry("1000x800")
        
        self.user_logged_in = False
        self.user_role = "" 
        self.nav_visible = True
        self.current_view = None 

        self.imgTk_header = None
        
        # Variables de estado de la aplicación
        self.username = tk.StringVar(value="gerente")
        self.password = tk.StringVar(value="1234")
        
        # --- MODELOS DE DATOS DINÁMICOS ---
        self.profile_data = {
            "Gerente": {
                "Nombre": "Andrea Mendoza",
                "Email": "gerencia@lavanderos.com",
                "Teléfono": "55 1234 5678",
                "Rol": "Gerente General",
                "Último Acceso": "2025-12-01 20:30"
            }
        }
        # Lista de empleados para simulación dinámica
        self.employees = [
            {"id": "101", "Nombre": "Luis Pérez", "Puesto": "Lavandero", "Horario": "7:00 - 15:00", "Sucursal": "Centro"},
            {"id": "102", "Nombre": "Ana Ruiz", "Puesto": "Atención Cliente", "Horario": "10:00 - 18:00", "Sucursal": "Norte"},
            {"id": "103", "Nombre": "Javier Cruz", "Puesto": "Repartidor", "Horario": "9:00 - 17:00", "Sucursal": "Sur"},
            {"id": "104", "Nombre": "Sofía Mendoza", "Puesto": "Lavandera", "Horario": "14:00 - 22:00", "Sucursal": "Aeropuerto"}
        ]
        # Lista de sucursales para simulación dinámica
        self.sucursales = [
            {"id": "S01", "Nombre": "Centro", "Estado": "Operando", "Ventas": 22000, "CostoOp": 11500, "Personal": 4},
            {"id": "S02", "Nombre": "Norte", "Estado": "Operando", "Ventas": 25000, "CostoOp": 12000, "Personal": 5},
            {"id": "S03", "Nombre": "Sur", "Estado": "Operando", "Ventas": 18000, "CostoOp": 10000, "Personal": 3},
            {"id": "S04", "Nombre": "Aeropuerto", "Estado": "Operando", "Ventas": 17000, "CostoOp": 9000, "Personal": 3},
        ]
        # Lista de pedidos de inventario
        self.inventory_orders = [
            {"id": "P001", "Insumo": "Detergente Azul", "Cantidad": 100, "Proveedor": "Clean Supplies S.A.", "Estado": "Pendiente"},
            {"id": "P002", "Insumo": "Suavizante", "Cantidad": 50, "Proveedor": "Química Azul Ltda.", "Estado": "Recibido"},
        ]
        
        
        # --- COLORES Y ESTILOS (ttk) ---
        self.COLOR_FONDO_PRINCIPAL = "#E1F5FE"
        self.COLOR_AZUL_BOTON = "#1E88E5" 
        self.COLOR_HEADER = "#091A6F" 
        self.COLOR_NAV_BUTTON = "#5B92E5" 
        self.root.configure(bg=self.COLOR_FONDO_PRINCIPAL)

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
        
        self.style.configure("Footer.TFrame", background=self.COLOR_HEADER) 
        self.style.configure("Footer.TLabel", background=self.COLOR_HEADER, foreground="white", font=('Arial', 10))


        # --- 1. ENCABEZADO (Header) ---
        self.header_frame = ttk.Frame(root, style="Header.TFrame")
        self.header_frame.pack(side="top", fill="x")
        
        try:
            path = resource_path("logo.png")
            img = Image.open(path)
            img = img.resize((50, 50)) 
            self.imgTk_header = ImageTk.PhotoImage(img)
            logo_label = tk.Label(self.header_frame, image=self.imgTk_header, bg=self.COLOR_HEADER)
            logo_label.pack(side="left", padx=10, pady=10)
        except FileNotFoundError:
            ttk.Label(self.header_frame, text="[LOGO]", style="Header.TLabel").pack(side="left", padx=10, pady=10)
            
        ttk.Label(self.header_frame, text="LAVANDEROS", style="Header.TLabel").pack(side="left", padx=10, pady=10)

        self.social_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.social_frame.pack(side="right", padx=10, pady=10)
        self.login_status_label = ttk.Label(self.social_frame, text="HABLA CON NOSOTROS", style="Footer.TLabel")
        self.login_status_label.pack(side="left", padx=5)
        
        # --- 2. CONTENEDOR PRINCIPAL (Nav + Content) ---
        self.main_container = ttk.Frame(root, style="Content.TFrame")
        self.main_container.pack(side="top", fill="both", expand=True) # Este frame va a contener NAV y CONTENT

        # --- 3. BARRA DE NAVEGACIÓN (Nav) ---
        self.nav_frame = ttk.Frame(self.main_container, width=200, style="Nav.TFrame")
        self.nav_frame.pack(side="left", fill="y")
        self.create_nav_buttons()

        # --- 4. CONTENIDO (Content) ---
        self.content_frame = ttk.Frame(self.main_container, style="Content.TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Iniciar con la vista de Login
        self.view_classes = {
            "Inicio": InicioView,
            "Perfil": PerfilView,
            "GestionPersonal": GestionPersonalView,
            "ReportesFinancieros": ReportesFinancierosView,
            "Inventario": InventarioView,
            "Sucursales": SucursalesView,
            "Servicios": ServiciosView,
            "Contacto": ContactoView,
            "Login": LoginView
        }
        self.show_view(LoginView)


    def create_nav_buttons(self):
        """Crea todos los botones de navegación, pero los esconde/muestra según el estado de login."""
        
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        self.nav_buttons = [
            ("🏠 Inicio", InicioView),
            ("⚙️ Perfil", PerfilView, "Gerente"),
            ("👨‍💼 Personal", GestionPersonalView, "Gerente"),
            ("📈 Reportes", ReportesFinancierosView, "Gerente"),
            ("🧺 Inventario", InventarioView, "Gerente"),
            ("🏢 Sucursales", SucursalesView, "Gerente"),
            ("🏷️ Servicios", ServiciosView, "Gerente"),
            ("📧 Contacto", ContactoView, "Cualquiera")
        ]

        for text, view_class, *role in self.nav_buttons:
            role_required = role[0] if role else "Cualquiera"
            
            # Si está logueado y cumple con el rol O si no requiere login
            if self.user_logged_in and (role_required == "Cualquiera" or self.user_role == role_required):
                btn = ttk.Button(self.nav_frame, text=text, command=lambda vc=view_class: self.show_view(vc), style="Nav.TButton")
                btn.pack(fill="x", pady=5, padx=10)
            # Si no está logueado pero la vista es para cualquiera (como Inicio o Contacto sin requerir autenticación)
            elif not self.user_logged_in and role_required == "Cualquiera":
                btn = ttk.Button(self.nav_frame, text=text, command=lambda vc=view_class: self.show_view(vc), style="Nav.TButton")
                btn.pack(fill="x", pady=5, padx=10)

        if self.user_logged_in:
            ttk.Button(self.nav_frame, text="🚪 Cerrar Sesión", command=self.logout, style="Nav.TButton").pack(fill="x", pady=(20, 5), padx=10)


    def show_view(self, view_class):
        """Destruye la vista actual y carga una nueva vista."""
        if self.current_view:
            self.current_view.destroy()

        requires_login = view_class not in [LoginView, InicioView]
        
        if requires_login and not self.user_logged_in:
            messagebox.showerror("Acceso Denegado", "Debe iniciar sesión para acceder a esta vista.")
            view_class = LoginView
            
        self.current_view = view_class(self.content_frame, self)
        self.current_view.pack(expand=True, fill="both")

        self.update_nav_buttons()


    def update_nav_buttons(self):
        """Actualiza el estado de los botones y el mensaje de login en el header."""
        for widget in self.social_frame.winfo_children():
            if widget != self.login_status_label: 
                widget.destroy()

        if self.user_logged_in:
            self.login_status_label.config(text=f"✅ Sesión: {self.user_role}")
        else:
            self.login_status_label.config(text="HABLA CON NOSOTROS")
            
        self.create_nav_buttons()

    # ====================================================================================================
    # --- PIE DE PÁGINA (Funciones) ---
    # ====================================================================================================

    def add_footer_to_toplevel(self, top):
        """Agrega el pie de página estilizado a una ventana Toplevel (modal)."""
        footer_frame = ttk.Frame(top, style="Footer.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        
        footer_frame.grid_columnconfigure(0, weight=1); footer_frame.grid_columnconfigure(1, weight=1) 
        
        footer_info_frame = ttk.Frame(footer_frame, style="Footer.TFrame")
        footer_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        ttk.Label(footer_info_frame, text="🧺", style="Footer.TLabel", font=('Arial', 20, 'bold')).pack(side="left", padx=(0, 10))
        ttk.Label(footer_info_frame, text="Copyright © 2024 Lavandería Lavanderos. Todos los derechos reservados.", 
                  style="Footer.TLabel", justify="left").pack(side="left")
        
        ttk.Label(footer_frame, text="• Políticas de Privacidad", 
                  style="Footer.TLabel", font=('Arial', 10, 'bold'), justify="right").grid(row=0, column=1, padx=20, pady=10, sticky="e")

    def create_footer(self):
        """Crea el pie de página fijo para la ventana principal (self.root)."""
        # Se remueve el main_container para que el footer se quede en el fondo
        self.main_container.pack_forget()
        
        self.footer_frame = ttk.Frame(self.root, style="Footer.TFrame")
        self.footer_frame.pack(side="bottom", fill="x")
        
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=1) 
        
        footer_info_frame = ttk.Frame(self.footer_frame, style="Footer.TFrame")
        footer_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        ttk.Label(footer_info_frame, text="🧺", style="Footer.TLabel", font=('Arial', 20, 'bold')).pack(side="left", padx=(0, 10))
        ttk.Label(footer_info_frame, text="Copyright © 2024 Lavandería Lavanderos. Todos los derechos reservados.", 
                  style="Footer.TLabel", justify="left").pack(side="left")
        
        ttk.Label(self.footer_frame, text="• Políticas de Privacidad", 
                  style="Footer.TLabel", font=('Arial', 10, 'bold'), justify="right").grid(row=0, column=1, padx=20, pady=10, sticky="e")
                  
        # Se vuelve a empacar el main_container para que esté justo arriba del footer
        self.main_container.pack(side="top", fill="both", expand=True)


    # ====================================================================================================
    # --- FUNCIONES DE LOGIN Y AUTENTICACIÓN ---
    # ====================================================================================================

    def attempt_login(self, username, password):
        """Verifica las credenciales del Gerente."""
        if username == "gerente" and password == "1234":
            self.user_logged_in = True
            self.user_role = "Gerente" 
            self.username.set(username); self.password.set(password)
            self.update_nav_buttons()
            self.show_view(ReportesFinancierosView) 
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
        self.show_view(LoginView)
        messagebox.showinfo("Cerrar Sesión", "Has cerrado la sesión correctamente.")
        

    # ====================================================================================================
    # --- SIMULACIONES DE PERFIL ---
    # ====================================================================================================
    
    def simulate_edit_data(self):
        top = tk.Toplevel(self.root)
        top.title("✏️ Editar Datos del Perfil")
        top.geometry("400x400")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Editar Información", font=('Arial', 14, 'bold')).pack(pady=10)
        data = self.profile_data["Gerente"]
        
        ttk.Label(main_content_frame, text="Nombre:").pack(pady=5)
        name_entry = ttk.Entry(main_content_frame, width=40); name_entry.insert(0, data["Nombre"]); name_entry.pack()
        ttk.Label(main_content_frame, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(main_content_frame, width=40); email_entry.insert(0, data["Email"]); email_entry.pack()
        ttk.Label(main_content_frame, text="Teléfono:").pack(pady=5)
        phone_entry = ttk.Entry(main_content_frame, width=40); phone_entry.insert(0, data["Teléfono"]); phone_entry.pack()
        
        def save_data():
            self.profile_data["Gerente"]["Nombre"] = name_entry.get()
            self.profile_data["Gerente"]["Email"] = email_entry.get()
            self.profile_data["Gerente"]["Teléfono"] = phone_entry.get()
            messagebox.showinfo("Guardar", "Datos actualizados exitosamente. Se recargará su perfil.")
            top.destroy(); self.show_view(PerfilView)

        ttk.Button(main_content_frame, text="Guardar Cambios", command=save_data).pack(pady=20)
        self.add_footer_to_toplevel(top)

    def simulate_change_password(self):
        top = tk.Toplevel(self.root)
        top.title("🔒 Cambiar Contraseña")
        top.geometry("350x350")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Cambiar Contraseña", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Contraseña Actual:").pack(pady=5)
        current_pass_entry = ttk.Entry(main_content_frame, show="*", width=30)
        current_pass_entry.pack()
        ttk.Label(main_content_frame, text="Nueva Contraseña:").pack(pady=5)
        new_pass_entry = ttk.Entry(main_content_frame, show="*", width=30)
        new_pass_entry.pack()
        ttk.Label(main_content_frame, text="Confirmar Nueva Contraseña:").pack(pady=5)
        confirm_pass_entry = ttk.Entry(main_content_frame, show="*", width=30)
        confirm_pass_entry.pack()

        def update_password():
            if current_pass_entry.get() != self.password.get():
                messagebox.showerror("Error", "Contraseña actual incorrecta.")
                return
            if new_pass_entry.get() != confirm_pass_entry.get():
                messagebox.showerror("Error", "Las nuevas contraseñas no coinciden.")
                return
            
            self.password.set(new_pass_entry.get())
            messagebox.showinfo("Actualizar", "Contraseña cambiada exitosamente. Debe iniciar sesión de nuevo.")
            self.logout(); top.destroy()

        ttk.Button(main_content_frame, text="Actualizar Contraseña", command=update_password).pack(pady=20)
        self.add_footer_to_toplevel(top)
        
    # ====================================================================================================
    # --- SIMULACIONES DE GESTIÓN DE PERSONAL (DINÁMICAS) ---
    # ====================================================================================================
    
    def simulate_add_employee(self):
        top = tk.Toplevel(self.root)
        top.title("➕ Agregar Nuevo Empleado")
        top.geometry("450x550")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Formulario de Nuevo Empleado", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Nombre Completo:").pack(pady=5)
        name_entry = ttk.Entry(main_content_frame, width=30); name_entry.pack()
        
        ttk.Label(main_content_frame, text="Puesto:").pack(pady=5)
        puesto = ttk.Combobox(main_content_frame, values=["Lavandero", "Repartidor", "Atención Cliente", "Supervisor"], state="readonly", width=30)
        puesto.set("Lavandero"); puesto.pack()
        
        ttk.Label(main_content_frame, text="Sucursal Asignada:").pack(pady=5)
        sucursal = ttk.Combobox(main_content_frame, values=[s['Nombre'] for s in self.sucursales], state="readonly", width=30)
        sucursal.set("Centro"); sucursal.pack()
        
        ttk.Label(main_content_frame, text="Horario (ej. 9:00 - 17:00):").pack(pady=5)
        horario_entry = ttk.Entry(main_content_frame, width=30); horario_entry.insert(0, "9:00 - 17:00"); horario_entry.pack()
        
        ttk.Label(main_content_frame, text="Contraseña Inicial:").pack(pady=5)
        password_entry = ttk.Entry(main_content_frame, show="*", width=30); password_entry.pack()

        def register_employee():
            new_name = name_entry.get()
            new_puesto = puesto.get()
            
            if not new_name or not new_puesto:
                messagebox.showerror("Error", "Debe completar el nombre y el puesto.")
                return

            # Simulación de registro DINÁMICO
            new_id = str(int(self.employees[-1]["id"]) + 1) if self.employees else "101"
            new_employee = {
                "id": new_id,
                "Nombre": new_name,
                "Puesto": new_puesto,
                "Horario": horario_entry.get(),
                "Sucursal": sucursal.get()
            }
            self.employees.append(new_employee)
            
            messagebox.showinfo("Registro", f"¡Nuevo empleado '{new_name}' ({new_puesto}) registrado con ID: {new_id} con éxito!")
            top.destroy()
            
            # Recargar la vista de administración para ver el cambio
            if isinstance(self.current_view, GestionPersonalView):
                 self.show_view(GestionPersonalView) 
            
        ttk.Button(main_content_frame, text="Registrar Empleado", command=register_employee).pack(pady=20)
        self.add_footer_to_toplevel(top)
        
    def simulate_manage_employees(self):
        top = tk.Toplevel(self.root)
        top.title("🧑‍💻 Administrador de Empleados")
        top.geometry("700x550")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")

        ttk.Label(main_content_frame, text="Panel de Gestión de Personal", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(main_content_frame, columns=("ID", "Nombre", "Puesto", "Horario", "Sucursal"), show="headings")
        tree.heading("ID", text="ID"); tree.column("ID", width=50)
        tree.heading("Nombre", text="Nombre"); tree.column("Nombre", width=150)
        tree.heading("Puesto", text="Puesto"); tree.column("Puesto", width=120)
        tree.heading("Horario", text="Horario"); tree.column("Horario", width=120)
        tree.heading("Sucursal", text="Sucursal"); tree.column("Sucursal", width=120)

        # Cargar datos DINÁMICOS
        for emp in self.employees:
            tree.insert("", tk.END, iid=emp["id"], values=(emp["id"], emp["Nombre"], emp["Puesto"], emp["Horario"], emp["Sucursal"]))
        
        tree.pack(fill="both", expand=True, pady=10)
        
        def edit_selected():
            selected_id = tree.focus()
            if selected_id:
                emp_data = next((emp for emp in self.employees if emp["id"] == selected_id), None)
                if emp_data:
                    self.open_edit_employee_window(selected_id, emp_data, tree)
            else:
                messagebox.showerror("Error", "Seleccione un empleado para editar.")

        def delete_selected():
            selected_id = tree.focus()
            if selected_id:
                employee_name = tree.item(selected_id, 'values')[1]
                if messagebox.askyesno("Confirmar Baja", f"¿Está seguro que desea dar de baja a {employee_name} (ID: {selected_id})?"):
                    
                    # Simulación: Eliminación dinámica del modelo
                    nonlocal self
                    self.employees = [emp for emp in self.employees if emp["id"] != selected_id]
                    
                    tree.delete(selected_id)
                    # Recarga la vista de Personal para actualizar el contador de empleados
                    if isinstance(self.current_view, GestionPersonalView):
                        self.show_view(GestionPersonalView)
                        
                    messagebox.showinfo("Baja Exitosa", f"{employee_name} ha sido dado de baja.")
            else:
                messagebox.showerror("Error", "Seleccione un empleado para dar de baja.")

        btn_frame = ttk.Frame(main_content_frame, style="Content.TFrame")
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="➕ Nuevo Empleado", command=self.simulate_add_employee).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="⚙️ Editar Seleccionado", command=edit_selected).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="➖ Dar de Baja", command=delete_selected).pack(side="left", padx=10)
        
        self.add_footer_to_toplevel(top)

    def open_edit_employee_window(self, emp_id, emp_data, parent_tree):
        """Abre una ventana modal para editar los datos de un empleado."""
        top = tk.Toplevel(self.root)
        top.title(f"✏️ Editar Empleado {emp_id}")
        top.geometry("400x450")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text=f"Editando Empleado ID: {emp_id}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        fields = ["Nombre", "Puesto", "Sucursal", "Horario"]
        entries = {}
        
        for field in fields:
            ttk.Label(main_content_frame, text=f"{field}:").pack(pady=5)
            if field == "Puesto":
                entry = ttk.Combobox(main_content_frame, values=["Lavandero", "Repartidor", "Atención Cliente", "Supervisor"], state="readonly", width=30)
            elif field == "Sucursal":
                entry = ttk.Combobox(main_content_frame, values=[s['Nombre'] for s in self.sucursales], state="readonly", width=30)
            else:
                entry = ttk.Entry(main_content_frame, width=30)
            
            entry.insert(0, emp_data[field])
            entry.pack()
            entries[field] = entry
            
        def save_edit():
            # Actualizar datos en el modelo
            for emp in self.employees:
                if emp["id"] == emp_id:
                    emp["Nombre"] = entries["Nombre"].get()
                    emp["Puesto"] = entries["Puesto"].get()
                    emp["Sucursal"] = entries["Sucursal"].get()
                    emp["Horario"] = entries["Horario"].get()
                    break
            
            # Actualizar datos en el Treeview padre
            parent_tree.item(emp_id, values=(emp_id, emp["Nombre"], emp["Puesto"], emp["Horario"], emp["Sucursal"]))
            
            messagebox.showinfo("Guardar", f"Datos del empleado {emp_id} actualizados correctamente.")
            top.destroy()
            # Recarga la vista de Personal para actualizar el contador de empleados
            if isinstance(self.current_view, GestionPersonalView):
                 self.show_view(GestionPersonalView) 
        
        ttk.Button(main_content_frame, text="Guardar Edición", command=save_edit).pack(pady=20)
        self.add_footer_to_toplevel(top)


    # ====================================================================================================
    # --- SIMULACIONES DE INVENTARIO (DINÁMICAS) ---
    # ====================================================================================================

    def simulate_view_stock(self):
        top = tk.Toplevel(self.root)
        top.title("📋 Stock Actual por Insumo")
        top.geometry("600x450")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Inventario de Insumos Críticos", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(main_content_frame, columns=("Insumo", "Unidades", "Ubicación"), show="headings")
        tree.heading("Insumo", text="Insumo"); tree.column("Insumo", width=200)
        tree.heading("Unidades", text="Unidades"); tree.column("Unidades", width=100, anchor="center")
        tree.heading("Ubicación", text="Ubicación"); tree.column("Ubicación", width=150)
        
        tree.insert("", tk.END, values=("Detergente Azul", "45", "Almacén Central"))
        tree.insert("", tk.END, values=("Suavizante Aroma Floral", "120", "Almacén Central"))
        tree.insert("", tk.END, values=("Perchas Metálicas", "15", "Sucursal Centro"), tags=('critico',))
        tree.insert("", tk.END, values=("Lavadora Industrial #5", "1", "Sucursal Norte"))
        
        tree.tag_configure('critico', background='yellow', foreground='red')

        tree.pack(fill="both", expand=True, pady=10)
        
        def start_audit():
            messagebox.showinfo("Inventario", "Iniciando proceso de conteo físico (Auditoría Manual).")
            
        ttk.Button(main_content_frame, text="Hacer Auditoría Manual", command=start_audit).pack(pady=10)
        self.add_footer_to_toplevel(top)

    def simulate_make_order(self):
        top = tk.Toplevel(self.root)
        top.title("🛒 Registrar Pedido de Inventario")
        top.geometry("450x450")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Formulario de Pedido de Insumos", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Proveedor:").pack(pady=5)
        provider = ttk.Combobox(main_content_frame, values=["Clean Supplies S.A.", "Química Azul Ltda."], state="readonly", width=30)
        provider.set("Clean Supplies S.A."); provider.pack()
        
        ttk.Label(main_content_frame, text="Artículo a Pedir:").pack(pady=5)
        item = ttk.Entry(main_content_frame, width=30); item.insert(0, "Detergente Azul"); item.pack()
        
        ttk.Label(main_content_frame, text="Cantidad (Unidades):").pack(pady=5)
        qty = ttk.Entry(main_content_frame, width=30); qty.insert(0, "100"); qty.pack()

        def submit_order():
            new_id = "P" + str(int(self.inventory_orders[-1]["id"].replace('P', '')) + 1).zfill(3) if self.inventory_orders else "P001"
            
            # Validación simple
            if not item.get() or not qty.get().isdigit():
                messagebox.showerror("Error", "Asegúrese de ingresar un artículo y una cantidad válida.")
                return

            new_order = {
                "id": new_id,
                "Insumo": item.get(),
                "Cantidad": int(qty.get()),
                "Proveedor": provider.get(),
                "Estado": "Pendiente"
            }
            self.inventory_orders.append(new_order)

            messagebox.showinfo("Pedido Enviado", f"Pedido {new_id} de {qty.get()} unidades de {item.get()} a {provider.get()} registrado con éxito.")
            top.destroy()

        ttk.Button(main_content_frame, text="Confirmar Pedido", command=submit_order).pack(pady=20)
        self.add_footer_to_toplevel(top)
        
    def simulate_view_orders(self):
        """Nueva ventana para ver y gestionar pedidos de inventario."""
        top = tk.Toplevel(self.root)
        top.title("📦 Seguimiento de Pedidos de Inventario")
        top.geometry("700x500")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Lista de Pedidos Pendientes/En Curso", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(main_content_frame, columns=("ID", "Insumo", "Cantidad", "Proveedor", "Estado"), show="headings")
        tree.heading("ID", text="ID"); tree.column("ID", width=70)
        tree.heading("Insumo", text="Insumo"); tree.column("Insumo", width=150)
        tree.heading("Cantidad", text="Cantidad"); tree.column("Cantidad", width=80, anchor="center")
        tree.heading("Proveedor", text="Proveedor"); tree.column("Proveedor", width=150)
        tree.heading("Estado", text="Estado"); tree.column("Estado", width=100)
        
        # Cargar datos DINÁMICOS
        for order in self.inventory_orders:
            tag = 'pendiente' if order["Estado"] == "Pendiente" else 'recibido'
            tree.insert("", tk.END, iid=order["id"], values=(order["id"], order["Insumo"], order["Cantidad"], order["Proveedor"], order["Estado"]), tags=(tag,))
        
        tree.tag_configure('pendiente', background='#FFFDE7', foreground='#FF7043') 
        tree.tag_configure('recibido', background='#E8F5E9', foreground='#388E3C') 

        tree.pack(fill="both", expand=True, pady=10)
        
        def cancel_order():
            selected_id = tree.focus()
            if selected_id:
                order_state = tree.item(selected_id, 'values')[4]
                if order_state == "Pendiente":
                    if messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro que desea cancelar el pedido {selected_id}?"):
                        # Simulación: Eliminación dinámica del modelo
                        nonlocal self
                        self.inventory_orders = [ord for ord in self.inventory_orders if ord["id"] != selected_id]
                        tree.delete(selected_id)
                        messagebox.showinfo("Cancelación", f"El pedido {selected_id} ha sido cancelado y eliminado de la lista.")
                else:
                    messagebox.showerror("Error", "Solo se pueden cancelar pedidos en estado 'Pendiente'.")
            else:
                messagebox.showerror("Error", "Seleccione un pedido para cancelar.")
                
        def mark_received():
            selected_id = tree.focus()
            if selected_id:
                order_state = tree.item(selected_id, 'values')[4]
                if order_state == "Pendiente":
                    if messagebox.askyesno("Confirmar Recepción", f"¿Confirma que el pedido {selected_id} ha sido recibido y cargado al stock?"):
                        # Simulación: Actualizar estado en el modelo
                        for order in self.inventory_orders:
                            if order["id"] == selected_id:
                                order["Estado"] = "Recibido"
                                break
                        tree.item(selected_id, values=(tree.item(selected_id, 'values')[0], tree.item(selected_id, 'values')[1], tree.item(selected_id, 'values')[2], tree.item(selected_id, 'values')[3], "Recibido"), tags=('recibido',))
                        messagebox.showinfo("Recepción", f"El pedido {selected_id} ha sido marcado como Recibido. (Stock Actualizado: Simulado).")
                else:
                    messagebox.showwarning("Advertencia", "El pedido ya está marcado como Recibido.")
            else:
                messagebox.showerror("Error", "Seleccione un pedido para marcar como Recibido.")


        btn_frame = ttk.Frame(main_content_frame, style="Content.TFrame")
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="❌ Cancelar Pedido", command=cancel_order).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="✅ Marcar como Recibido", command=mark_received).pack(side="left", padx=10)
        
        self.add_footer_to_toplevel(top)


    # ====================================================================================================
    # --- SIMULACIONES DE SUCURSALES (DINÁMICAS) ---
    # ====================================================================================================

    def simulate_view_sucursales(self):
        top = tk.Toplevel(self.root)
        top.title("🔍 Detalle de Rendimiento por Sucursal")
        top.geometry("800x500")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Rendimiento y Estado de Sucursales", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(main_content_frame, columns=("ID", "Sucursal", "Estado", "Ventas", "Costo Op.", "Margen", "Personal"), show="headings")
        tree.heading("ID", text="ID"); tree.column("ID", width=50)
        tree.heading("Sucursal", text="Sucursal"); tree.column("Sucursal", width=120)
        tree.heading("Estado", text="Estado"); tree.column("Estado", width=100)
        tree.heading("Ventas", text="Ventas ($)"); tree.column("Ventas", width=100, anchor="e")
        tree.heading("Costo Op.", text="Costo Op. ($)"); tree.column("Costo Op.", width=100, anchor="e")
        tree.heading("Margen", text="Margen ($)"); tree.column("Margen", width=100, anchor="e")
        tree.heading("Personal", text="Personal"); tree.column("Personal", width=80, anchor="center")
        
        # Cargar datos DINÁMICOS
        for suc in self.sucursales:
            margen = suc["Ventas"] - suc["CostoOp"]
            tag = 'cerrada' if suc["Estado"] == "Cerrada" else ('mejor' if margen > 12000 else 'normal')
            tree.insert("", tk.END, iid=suc["id"], values=(suc["id"], suc["Nombre"], suc["Estado"], f'{suc["Ventas"]:,.0f}', f'{suc["CostoOp"]:,.0f}', f'{margen:,.0f}', suc["Personal"]), tags=(tag,))
        
        tree.tag_configure('mejor', background='#CCFFCC', foreground='green')
        tree.tag_configure('cerrada', background='#FFCCCC', foreground='red')
        tree.tag_configure('normal', background='white', foreground='black')

        tree.pack(fill="both", expand=True, pady=10)
        
        def show_expense_detail():
            messagebox.showinfo("Sucursales", "Abriendo desglose de costos detallado por sucursal (Simulación de reporte).")
        
        def toggle_status():
            selected_id = tree.focus()
            if selected_id:
                suc = next((s for s in self.sucursales if s["id"] == selected_id), None)
                if suc:
                    new_status = "Cerrada" if suc["Estado"] == "Operando" else "Operando"
                    if messagebox.askyesno("Confirmar Cambio", f"¿Desea cambiar el estado de la sucursal {suc['Nombre']} a '{new_status}'?"):
                        suc["Estado"] = new_status
                        
                        # Recargar la ventana actual para mostrar el cambio en el Treeview
                        top.destroy()
                        self.simulate_view_sucursales()
                        
                        # Recargar la vista principal de Sucursales para actualizar el contador
                        if isinstance(self.current_view, SucursalesView):
                            self.show_view(SucursalesView) 
                        
                        messagebox.showinfo("Cambio de Estado", f"Sucursal {suc['Nombre']} marcada como '{new_status}'.")
            else:
                messagebox.showerror("Error", "Seleccione una sucursal para cambiar su estado.")
            
        btn_frame = ttk.Frame(main_content_frame, style="Content.TFrame")
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Detalle de Gastos", command=show_expense_detail).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Abrir/Cerrar Sucursal", command=toggle_status).pack(side="left", padx=10)
        
        self.add_footer_to_toplevel(top)

    def simulate_request_maintenance(self):
        top = tk.Toplevel(self.root)
        top.title("🛠️ Solicitar Mantenimiento")
        top.geometry("450x450")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Formulario de Solicitud de Mantenimiento", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Sucursal:").pack(pady=5)
        sucursal = ttk.Combobox(main_content_frame, values=[s['Nombre'] for s in self.sucursales if s['Estado'] == 'Operando'], state="readonly", width=30)
        sucursal.set("Centro"); sucursal.pack()
        
        ttk.Label(main_content_frame, text="Equipo Afectado:").pack(pady=5)
        equipo = ttk.Entry(main_content_frame, width=30); equipo.insert(0, "Lavadora Industrial #3"); equipo.pack()
        
        ttk.Label(main_content_frame, text="Descripción del Fallo:").pack(pady=5)
        desc = tk.Text(main_content_frame, height=4, width=30); desc.insert("1.0", "Fuga de agua constante al inicio del ciclo de centrifugado.")
        desc.pack()

        def submit_request():
            messagebox.showinfo("Solicitud Enviada", f"Mantenimiento solicitado para {equipo.get()} en {sucursal.get()}. Un técnico será asignado en 24 horas.")
            top.destroy()

        ttk.Button(main_content_frame, text="Enviar Solicitud Urgente", command=submit_request).pack(pady=20)
        self.add_footer_to_toplevel(top)

    def simulate_open_new_sucursal(self):
        top = tk.Toplevel(self.root)
        top.title("➕ Abrir Nueva Sucursal")
        top.geometry("450x400")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Formulario de Apertura de Sucursal", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Nombre de la Nueva Sucursal:").pack(pady=5)
        name_entry = ttk.Entry(main_content_frame, width=30); name_entry.pack()
        
        ttk.Label(main_content_frame, text="Dirección (Simulación):").pack(pady=5)
        address_entry = ttk.Entry(main_content_frame, width=30); address_entry.insert(0, "Calle Inventada #123")
        address_entry.pack()
        
        ttk.Label(main_content_frame, text="Personal Inicial Asignado:").pack(pady=5)
        personal_entry = ttk.Entry(main_content_frame, width=30); personal_entry.insert(0, "3")
        personal_entry.pack()

        def register_sucursal():
            new_name = name_entry.get()
            if not new_name:
                messagebox.showerror("Error", "Debe ingresar el nombre de la sucursal.")
                return
            
            # Simulación: Agregar sucursal al modelo
            new_id = "S" + str(int(self.sucursales[-1]["id"].replace('S', '')) + 1).zfill(2) if self.sucursales else "S01"
            new_sucursal = {
                "id": new_id,
                "Nombre": new_name,
                "Estado": "Operando",
                "Ventas": 0,
                "CostoOp": 0,
                "Personal": int(personal_entry.get() if personal_entry.get().isdigit() else 0)
            }
            self.sucursales.append(new_sucursal)
            
            messagebox.showinfo("Apertura Exitosa", f"¡La nueva sucursal '{new_name}' (ID: {new_id}) ha sido registrada y está 'Operando'!")
            top.destroy()
            
            # Recargar la vista de administración para ver el cambio
            if isinstance(self.current_view, SucursalesView):
                 self.show_view(SucursalesView) 

        ttk.Button(main_content_frame, text="Registrar Apertura", command=register_sucursal).pack(pady=20)
        self.add_footer_to_toplevel(top)


    # ====================================================================================================
    # --- SIMULACIONES DE REPORTES FINANCIEROS ---
    # ====================================================================================================

    def simulate_sales_report(self):
        top = tk.Toplevel(self.root)
        top.title("💵 Reporte de Ventas")
        top.geometry("500x400")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Generador de Reporte de Ventas", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Rango de Fechas:").pack(pady=5)
        date_frame = ttk.Frame(main_content_frame, style="Content.TFrame")
        date_frame.pack()
        start_date = ttk.Entry(date_frame, width=15, justify="center"); start_date.insert(0, "2025-11-01"); start_date.pack(side="left", padx=5)
        ttk.Label(date_frame, text="al", style="TLabel").pack(side="left")
        end_date = ttk.Entry(date_frame, width=15, justify="center"); end_date.insert(0, "2025-11-30"); end_date.pack(side="left", padx=5)
        
        ttk.Label(main_content_frame, text="Tipo de Reporte:").pack(pady=5)
        report_type = ttk.Combobox(main_content_frame, values=["Ventas por Sucursal", "Ventas por Servicio", "Ventas Totales"], state="readonly", width=30)
        report_type.set("Ventas por Sucursal"); report_type.pack()
        
        ttk.Label(main_content_frame, text="Formato de Descarga:").pack(pady=5)
        file_format = ttk.Combobox(main_content_frame, values=["PDF", "CSV", "Excel"], state="readonly", width=30)
        file_format.set("PDF"); file_format.pack()

        def generate_report():
            messagebox.showinfo("Reporte Generado", f"Generando y descargando reporte de {report_type.get()} en formato {file_format.get()} para el rango {start_date.get()} - {end_date.get()}.")
            top.destroy()

        ttk.Button(main_content_frame, text="Generar y Descargar", command=generate_report).pack(pady=20)
        self.add_footer_to_toplevel(top)

    def simulate_income_statement(self):
        top = tk.Toplevel(self.root)
        top.title("💰 Estado de Resultados")
        top.geometry("500x350")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Generador de Estado de Resultados", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Periodo Fiscal:", font=('Arial', 12, 'bold')).pack(pady=5)
        period = ttk.Combobox(main_content_frame, values=["Mensual (Noviembre)", "Trimestral (Q4)", "Anual (2025)"], state="readonly", width=30)
        period.set("Mensual (Noviembre)"); period.pack()
        
        ttk.Label(main_content_frame, text="Seleccione Moneda:").pack(pady=5)
        currency = ttk.Combobox(main_content_frame, values=["MXN - Pesos Mexicanos", "USD - Dólares Americanos"], state="readonly", width=30)
        currency.set("MXN - Pesos Mexicanos"); currency.pack()

        def generate_report():
            messagebox.showinfo("Reporte Generado", f"Generando Estado de Resultados {period.get()} en {currency.get().split(' - ')[0]}. Revisar su carpeta de descargas.")
            top.destroy()

        ttk.Button(main_content_frame, text="Generar Reporte Detallado", command=generate_report).pack(pady=20)
        self.add_footer_to_toplevel(top)
        
    # ====================================================================================================
    # --- SIMULACIONES DE CONTACTO ---
    # ====================================================================================================

    def simulate_contact_response(self):
        top = tk.Toplevel(self.root)
        top.title("📧 Responder Formulario de Contacto")
        top.geometry("550x550")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")

        ttk.Label(main_content_frame, text="Responder Solicitud (Ticket T1001)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Asunto: Solicitud de material de limpieza", font=('Arial', 12, 'italic')).pack(pady=5)
        ttk.Label(main_content_frame, text="Mensaje Original: Necesitamos urgentemente más detergente azul y suavizante para la sucursal Centro.", wraplength=500, justify="left").pack(pady=5)
        
        ttk.Label(main_content_frame, text="Escriba su respuesta:", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        response_text = tk.Text(main_content_frame, height=8, width=60)
        response_text.pack(pady=5)

        def send_response():
            response = response_text.get("1.0", tk.END).strip()
            if response:
                messagebox.showinfo("Respuesta Enviada", f"Respuesta enviada:\n\n'{response[:50]}...'\n\nEl formulario se marcó como 'Atendido'.")
                top.destroy()
            else:
                messagebox.showerror("Error", "Debe escribir una respuesta.")

        ttk.Button(main_content_frame, text="✉️ Enviar Respuesta y Marcar Atendido", command=send_response).pack(pady=20)
        self.add_footer_to_toplevel(top)


    # ====================================================================================================
    # --- SIMULACIONES DE SERVICIOS Y PRECIOS ---
    # ====================================================================================================

    def simulate_edit_services(self):
        top = tk.Toplevel(self.root)
        top.title("📝 Modificar Servicios")
        top.geometry("500x350")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Administración de Servicios", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Servicio Seleccionado:").pack(pady=5)
        service = ttk.Combobox(main_content_frame, values=["Lavado Básico (Kg)", "Secado (Extra)", "Planchado (Unidad)", "Servicio Express"], state="readonly", width=30)
        service.set("Lavado Básico (Kg)"); service.pack()
        
        # Callbacks para los botones internos
        def new_service():
            messagebox.showinfo("Servicios", "Abriendo formulario para añadir nuevo servicio (Simulación: Se abre otra ventana para definir tarifas y descripción).")

        def edit_details():
            messagebox.showinfo("Servicios", f"Abriendo edición de detalles para: {service.get()} (Simulación: Se abre otra ventana para cambiar descripción, nombre, etc.).")

        def deactivate_service():
            if messagebox.askyesno("Confirmar Desactivación", f"¿Está seguro que desea desactivar el servicio '{service.get()}'?"):
                messagebox.showwarning("Servicios", f"El servicio {service.get()} ha sido desactivado. (Simulación: No aparecerá en los pedidos web).")

        btn_frame = ttk.Frame(main_content_frame, style="Content.TFrame"); btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="➕ Nuevo Servicio", command=new_service).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="✏️ Editar Detalles", command=edit_details).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Desactivar Servicio", command=deactivate_service).pack(side="left", padx=10)
        
        self.add_footer_to_toplevel(top)

    def simulate_adjust_prices(self):
        top = tk.Toplevel(self.root)
        top.title("🏷️ Ajustar Precios y Promociones")
        top.geometry("500x380")
        
        main_content_frame = ttk.Frame(top, padding="15", style="Content.TFrame")
        main_content_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_content_frame, text="Ajuste de Precios", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_content_frame, text="Tarifa Base por Kilo (Actual $25.00):").pack(pady=5)
        new_price = ttk.Entry(main_content_frame, width=30); new_price.insert(0, "27.00"); new_price.pack()
        
        ttk.Label(main_content_frame, text="Promoción Activa:").pack(pady=5)
        promo = ttk.Combobox(main_content_frame, values=["10% Express", "20% Estudiantes", "Ninguna"], state="readonly", width=30)
        promo.set("10% Express"); promo.pack()

        def apply_changes():
            messagebox.showinfo("Ajuste Aplicado", f"Precio base actualizado a ${new_price.get()}. Promoción activa: {promo.get()}.")
            top.destroy()
            
        def create_promotion():
            messagebox.showinfo("Promociones", "Abriendo formulario para configurar nueva promoción (Simulación: Se abre otra ventana para establecer reglas).")
            
        ttk.Button(main_content_frame, text="Aplicar Cambio de Precio", command=apply_changes).pack(pady=15)
        ttk.Button(main_content_frame, text="Crear Nueva Promoción", command=create_promotion).pack(pady=5)
        
        self.add_footer_to_toplevel(top)


if __name__ == "__main__":
    # Nota: Los archivos de imagen (gerente.png, lavadoras.png, personal.png, etc.) deben estar en el mismo directorio que el script.
    # Si no tienes las imágenes, el programa usará etiquetas de texto para reemplazarlas.
    root = tk.Tk()
    app = LavanderosWebApp(root)
    
    # Llama a create_footer para asegurar que el pie de página esté en la ventana principal
    app.create_footer() 
    
    root.mainloop()