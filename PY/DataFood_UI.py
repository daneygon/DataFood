import tkinter as tk
from tkinter import ttk, messagebox as msg, filedialog
from datetime import datetime
from tkinter import messagebox as msg  
import pyodbc                           
from PIL import Image, ImageTk
import io
import mimetypes



def conectar():
    """Conexión a SQL Server (ajusta SERVER si lo necesitas)."""
    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.;"                       # . = instancia local
            "DATABASE=DataFood2;"
            "Trusted_Connection=yes;"
        )
        print("Conexión establecida con SQL Server (DataFood2)")
        return conexion
    except Exception as e:
        msg.showerror("Error de conexión", f"No se pudo conectar a la BD:\n{e}")
        raise
class RestauranteUI(tk.Tk):
    LEFT_PANEL_WIDTH = 260

    # 1. MODIFICAR EL __init__ PARA MANTENER EL PANEL DERECHO
   # 1. MODIFICAR EL __init__ - PANEL DERECHO MÁS ANCHO
    def __init__(self):
        super().__init__()

        # ---------- Ventana principal ---------------
        self.title("Sistema de Gestión de Restaurante - DataFood")
        self.geometry("1200x700")
        self.configure(bg="#F5F1E8")

        # --------------- Estilo ------------------
        self._apply_style()
        self.left_panel_width = 260

        # --------------- Encabezado ------------------
        header = tk.Frame(self, bg="#C8B88A", height=50)
        header.pack(side="top", fill="x")

        self.header_title = tk.Label(
            header,
            text="  DataFood  | sistema para la gestión de insumos y ventas de un comedor(COMEDOR RAQUEL)",
            bg="#C8B88A",
            fg="#ffffff",
            font=("Segoe UI", 15, "bold")
        )
        self.header_title.pack(side="left", pady=5, padx=10)

        self.time_label = tk.Label(
            header,
            text="",
            bg="#C8B88A",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold")
        )
        self.time_label.pack(side="right", pady=5, padx=15)

        self._actualizar_hora()

        # --------------- CONTENEDOR PRINCIPAL (3 COLUMNAS) ------------------
        main_content = tk.Frame(self, bg="#F5F1E8")
        main_content.pack(expand=True, fill="both", padx=10, pady=10)

        # ------------------ COLUMNA IZQUIERDA (SIDEBAR) ---------------------
        self.sidebar = tk.Frame(main_content, bg="#C8B88A", width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="DataFood",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            justify="left"
        ).pack(padx=15, pady=(20, 10), anchor="w")

        tk.Label(
            self.sidebar,
            text="INICIO",
            bg="#C8B88A",
            fg="#FDF7EA",
            font=("Segoe UI", 10)
        ).pack(padx=15, anchor="w")

        tk.Label(
            self.sidebar,
            text="────────────",
            bg="#C8B88A",
            fg="#FDF7EA"
        ).pack(padx=15, pady=(5, 10), anchor="w")

        inicio_btn = ttk.Button(
            self.sidebar,
            text="Inicio",
            command=self._mostrar_dashboard_inicial
        )
        inicio_btn.pack(fill="x", padx=15, pady=(5, 5))

        gestion_btn = ttk.Button(
            self.sidebar,
            text="Gestión",
            command=self._abrir_ventana_gestion
        )
        gestion_btn.pack(fill="x", padx=15, pady=(10, 5))

        ttk.Button(self.sidebar, text="Reportes (próximamente)").pack(
            fill="x", padx=15, pady=5
        )
        ttk.Button(self.sidebar, text="Ajustes (próximamente)").pack(
            fill="x", padx=15, pady=5
        )

        # ------------------ ZONA CENTRAL DINÁMICA ----------------
        self.center_frame = tk.Frame(main_content, bg="#FFFFFF")
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # ------------------ COLUMNA DERECHA (MÁS ANCHA) ----------------
        self.right_panel = tk.Frame(main_content, bg="#F5F1E8", width=320)
        self.right_panel.pack(side="left", fill="y")
        self.right_panel.pack_propagate(False)

        tk.Label(
            self.right_panel,
            text="Panel derecho\n(próximas funciones)",
            bg="#F5F1E8",
            fg="#444444",
            font=("Segoe UI", 11, "bold"),
            justify="center"
        ).pack(padx=10, pady=20)

        tk.Label(
            self.right_panel,
            text="no se que poner pero algo voy a poner\n"
                "- Detalle del pedido actual\n"
                "- Resumen de venta\n"
                "- Métodos de pago, etc.",
            bg="#F5F1E8",
            fg="#666666",
            font=("Segoe UI", 9),
            justify="left"
        ).pack(padx=15, pady=5)

        # estado de paneles
        self.sidebar_visible = True
        self.right_panel_visible = True

        # Inicializar atributos para el menú
        self.current_menu_window = None
        self.canvas_platos = None
        self.canvas_bebidas = None
        self.frame_preview_platos = None
        self.frame_preview_bebidas = None
        self.btn_left_platos = None
        self.btn_right_platos = None
        self.btn_left_bebidas = None
        self.btn_right_bebidas = None

        # al iniciar, mostramos el "Menú de Platos y Bebidas"
        self._mostrar_dashboard_inicial()

        
    def _mostrar_dashboard_inicial(self):
        """Muestra el dashboard inicial con menús desplazables"""
        
        # Cerrar ventana de menú completo si está abierta
        if hasattr(self, 'current_menu_window') and self.current_menu_window:
            try:
                self.current_menu_window.destroy()
            except:
                pass
            self.current_menu_window = None
        
        # Mostrar panel derecho si está oculto
        if not getattr(self, "right_panel_visible", False):
            self.right_panel.pack(side="left", fill="y")
            self.right_panel.pack_propagate(False)
            self.right_panel_visible = True

        # limpiar contenido central
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        # ====== CONTENEDOR PRINCIPAL CON SCROLL VERTICAL ======
        # Crear un Canvas con Scrollbar vertical
        canvas_container = tk.Canvas(self.center_frame, bg="#FFFFFF", highlightthickness=0)
        canvas_container.pack(side="left", fill="both", expand=True)
        
        # Scrollbar VERTICAL para el dashboard
        v_scrollbar = tk.Scrollbar(
            self.center_frame, 
            orient="vertical", 
            command=canvas_container.yview,
            width=12,
            bg="#C8B88A",
            troughcolor="#F5F1E8"
        )
        v_scrollbar.pack(side="right", fill="y")
        
        canvas_container.configure(yscrollcommand=v_scrollbar.set)
        
        # Frame interior que contendrá TODO el dashboard
        scrollable_frame = tk.Frame(canvas_container, bg="#FFFFFF")
        canvas_container.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_configure(event):
            # Actualizar región de scroll cuando el contenido cambie de tamaño
            canvas_container.configure(scrollregion=canvas_container.bbox("all"))
            # Ajustar ancho del canvas
            canvas_container.config(width=scrollable_frame.winfo_reqwidth())
        
        scrollable_frame.bind("<Configure>", on_configure)
        
        # ---------------------------------------------------------
        #                     PLATOS (todo el contenido de antes)
        # ---------------------------------------------------------
        frame_platos = tk.LabelFrame(
            scrollable_frame,
            text="Menú de Platos",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )
        frame_platos.pack(side="top", fill="x", pady=(0, 20))
        
        tk.Label(
            frame_platos,
            text="(Vista previa de platos recientes)",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor="w", padx=5, pady=(0, 10))
        
        # --- CONTENEDOR CON FLECHAS Y TARJETAS ---
        platos_container = tk.Frame(frame_platos, bg="#FFFFFF")
        platos_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Flecha izquierda
        self.btn_left_platos = tk.Button(
            platos_container,
            text="◀",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            width=2,
            height=8
        )
        self.btn_left_platos.pack(side="left", fill="y", padx=(15, 5))
        
        # Canvas para scroll horizontal (esto es solo para las tarjetas)
        self.canvas_platos = tk.Canvas(
            platos_container, 
            bg="#FFFFFF", 
            height=200,
            highlightthickness=0
        )
        self.canvas_platos.pack(side="left", fill="both", expand=True)
        
        # Frame interior para las tarjetas (solo horizontal)
        self.frame_preview_platos = tk.Frame(self.canvas_platos, bg="#FFFFFF")
        self.canvas_platos.create_window((0, 0), window=self.frame_preview_platos, anchor="nw")
        
        # Flecha derecha
        self.btn_right_platos = tk.Button(
            platos_container,
            text="▶",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            width=2,
            height=8
        )
        self.btn_right_platos.pack(side="right", fill="y", padx=(5, 15))
        
        # ---------------------------------------------------------
        #                     BEBIDAS
        # ---------------------------------------------------------
        frame_bebidas = tk.LabelFrame(
            scrollable_frame,
            text="Menú de Bebidas",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )
        frame_bebidas.pack(side="top", fill="x", pady=(0, 20))
        
        tk.Label(
            frame_bebidas,
            text="(Vista previa de bebidas recientes)",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor="w", padx=5, pady=(0, 10))
        
        # --- CONTENEDOR CON FLECHAS Y TARJETAS ---
        bebidas_container = tk.Frame(frame_bebidas, bg="#FFFFFF")
        bebidas_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Flecha izquierda
        self.btn_left_bebidas = tk.Button(
            bebidas_container,
            text="◀",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            width=2,
            height=8
        )
        self.btn_left_bebidas.pack(side="left", fill="y", padx=(15, 5))
        
        # Canvas para scroll horizontal
        self.canvas_bebidas = tk.Canvas(
            bebidas_container, 
            bg="#FFFFFF", 
            height=200,
            highlightthickness=0
        )
        self.canvas_bebidas.pack(side="left", fill="both", expand=True)
        
        # Frame interior para las tarjetas
        self.frame_preview_bebidas = tk.Frame(self.canvas_bebidas, bg="#FFFFFF")
        self.canvas_bebidas.create_window((0, 0), window=self.frame_preview_bebidas, anchor="nw")
        
        # Flecha derecha
        self.btn_right_bebidas = tk.Button(
            bebidas_container,
            text="▶",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            width=2,
            height=8
        )
        self.btn_right_bebidas.pack(side="right", fill="y", padx=(5, 15))
        
        # ---------------------------------------------------------
        # Botones "Ver menú completo" (ESTOS AHORA SERÁN VISIBLES)
        # ---------------------------------------------------------
        # Marco para botones
        btn_container = tk.Frame(scrollable_frame, bg="#E6F2FF", height=70)
        btn_container.pack(side="top", fill="x", pady=(15, 5))
        btn_container.pack_propagate(False)
        
        # Marco interior para centrar
        btn_frame = tk.Frame(btn_container, bg="#E6F2FF")
        btn_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_platos = tk.Button(
            btn_frame,
            text="📋 Ver menú completo de Platos",
            bg="#C8B88A",
            fg="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=25,
            pady=12,
            command=lambda: self._abrir_ventana_menu_completo("Plato")
        )
        btn_platos.pack(side="left", padx=(0, 20))
        
        btn_bebidas = tk.Button(
            btn_frame,
            text="🥤 Ver menú completo de Bebidas",
            bg="#C8B88A",
            fg="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=25,
            pady=12,
            command=lambda: self._abrir_ventana_menu_completo("Bebida")
        )
        btn_bebidas.pack(side="left")
        
        # ---------------------------------------------------------
        # Espacio al final para que se vea mejor
        # ---------------------------------------------------------
        tk.Frame(scrollable_frame, bg="#FFFFFF", height=20).pack(side="top", fill="x")
        
        # ---------------------------------------------------------
        # Cargar preview de platos y bebidas
        # ---------------------------------------------------------
        self._cargar_vista_previa_menu()
        
    def _cargar_vista_previa_menu(self):
        
        if not self.frame_preview_platos or not self.frame_preview_bebidas:
            return
        
        # Limpiar contenido previo
        for w in self.frame_preview_platos.winfo_children():
            w.destroy()
        for w in self.frame_preview_bebidas.winfo_children():
            w.destroy()

        conexion = conectar()
        cursor = conexion.cursor()

        # ============================================================
        # ---------------------  PREVIEW PLATOS  ----------------------
        # ============================================================
        cursor.execute("""
            SELECT 
                P.IDProduccion,
                COALESCE(P.NombrePlato, '—') AS Nombre,
                COALESCE(CP.NombreCategoria, '—') AS Categoria,
                ISNULL(P.CostoPorPlato, 0) AS Precio,
                P.Imagen
            FROM Produccion P
            LEFT JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
            LEFT JOIN CategoriaPlatos CP ON CP.IDCategoriaPlatos = MP.IDCategoriaPlatos
            WHERE P.NombrePlato IS NOT NULL
            AND ISNULL(P.CantidadDePlatos,0) > 0
            ORDER BY P.NombrePlato;
        """)
        platos = cursor.fetchall()

        # Función para crear tarjeta
        def crear_tarjeta(parent, idp, nombre, categoria, precio, img_bytes):
            card = tk.Frame(
                parent, 
                bg="#F8F5EE", 
                bd=2, 
                relief="ridge",
                width=220,
                height=200
            )
            card.pack_propagate(False)
            
            # CONTENEDOR PARA LA IMAGEN
            img_container = tk.Frame(card, bg="#FFFFFF", width=100, height=100)
            img_container.pack(pady=(10, 5))
            img_container.pack_propagate(False)
            
            lbl_img = tk.Label(img_container, bg="#FFFFFF")
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")
            
            if img_bytes:
                try:
                    from PIL import Image, ImageTk
                    from io import BytesIO
                    img = Image.open(BytesIO(img_bytes))
                    
                    img.thumbnail((90, 90), Image.Resampling.LANCZOS)
                    
                    if img.size[0] != img.size[1]:
                        background = Image.new('RGB', (100, 100), color='white')
                        offset = ((100 - img.size[0]) // 2, (100 - img.size[1]) // 2)
                        background.paste(img, offset)
                        img = background
                    
                    photo = ImageTk.PhotoImage(img)
                    lbl_img.config(image=photo)
                    lbl_img.image = photo
                except Exception as e:
                    print(f"Error cargando imagen: {e}")
                    lbl_img.config(text="🖼️", fg="#999", font=("Segoe UI", 24))
            else:
                lbl_img.config(text="📷", fg="#999", font=("Segoe UI", 24))
            
            # NOMBRE
            nombre_display = str(nombre)[:18] + ("..." if len(str(nombre)) > 18 else "")
            tk.Label(
                card,
                text=nombre_display,
                bg="#F8F5EE",
                fg="#222222",
                font=("Segoe UI", 10, "bold"),
                wraplength=180,
                justify="center"
            ).pack(pady=(0, 3))
            
            # CATEGORÍA
            cat_display = str(categoria)[:20] + ("..." if len(str(categoria)) > 20 else "")
            tk.Label(
                card,
                text=cat_display,
                bg="#F8F5EE",
                fg="#555555",
                font=("Segoe UI", 9),
                wraplength=180,
                justify="center"
            ).pack(pady=(0, 5))
            
            # PRECIO
            try:
                precio_num = float(precio) if precio else 0.0
                precio_text = f"C$ {precio_num:.2f}"
            except (ValueError, TypeError):
                precio_text = "C$ 0.00"
            
            precio_frame = tk.Frame(card, bg="#F8F5EE", height=30)
            precio_frame.pack(fill="x", pady=(5, 10))
            precio_frame.pack_propagate(False)
            
            tk.Label(
                precio_frame,
                text=precio_text,
                bg="#F8F5EE",
                fg="#157347",
                font=("Segoe UI", 11, "bold")
            ).pack(expand=True)
            
            return card

        # Crear tarjetas de platos
        col = 0
        for idp, nombre, categoria, precio, img_bytes in platos:
            card = crear_tarjeta(self.frame_preview_platos, idp, nombre, categoria, precio, img_bytes)
            card.grid(row=0, column=col, padx=12, pady=5, sticky="nw")
            col += 1

        # ============================================================
        # ---------------------  PREVIEW BEBIDAS  ---------------------
        # ============================================================
        cursor.execute("""
            SELECT 
                P.IDProduccion,
                COALESCE(P.NombreBebida, '—') AS Nombre,
                COALESCE(CB.NombreCategoria, '—') AS Categoria,
                ISNULL(P.CostoPorBebida, 0) AS Precio,
                P.Imagen
            FROM Produccion P
            LEFT JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
            LEFT JOIN CategoriaBebidas CB ON CB.IDCategoriaBebidas = MB.IDCategoriaBebidas
            WHERE P.NombreBebida IS NOT NULL
            AND ISNULL(P.CantidadDeBebidas,0) > 0
            ORDER BY P.NombreBebida;
        """)
        bebidas = cursor.fetchall()

        # Crear tarjetas de bebidas
        col = 0
        for idp, nombre, categoria, precio, img_bytes in bebidas:
            card = crear_tarjeta(self.frame_preview_bebidas, idp, nombre, categoria, precio, img_bytes)
            card.grid(row=0, column=col, padx=12, pady=5, sticky="nw")
            col += 1

        conexion.close()

        # Configurar scroll después de crear todas las tarjetas
        self._configurar_scroll()


    def _configurar_scroll(self):    
        def update_scrollregion(canvas, inner_frame):
            canvas.configure(scrollregion=canvas.bbox("all"))
            inner_frame.update_idletasks()
            canvas_width = inner_frame.winfo_width()
            
            # Configurar canvas width
            if canvas_width > 600:
                canvas.config(width=600)
                
                # 🔥 ELIMINAR ESTO - NO CREAR SCROLLBAR HORIZONTAL 🔥
                # Remover scrollbar si existe
                if hasattr(canvas, 'h_scrollbar') and canvas.h_scrollbar:
                    canvas.h_scrollbar.destroy()
                    canvas.h_scrollbar = None
                canvas.configure(xscrollcommand=lambda *args: None)
            else:
                canvas.config(width=canvas_width + 20)
                # Remover scrollbar si existe
                if hasattr(canvas, 'h_scrollbar') and canvas.h_scrollbar:
                    canvas.h_scrollbar.destroy()
                    canvas.h_scrollbar = None
                canvas.configure(xscrollcommand=lambda *args: None)
        
        # Para platos
        if self.frame_preview_platos:
            self.frame_preview_platos.update_idletasks()
            update_scrollregion(self.canvas_platos, self.frame_preview_platos)
            
            def scroll_platos_left():
                self.canvas_platos.xview_scroll(-3, "units")
            
            def scroll_platos_right():
                self.canvas_platos.xview_scroll(3, "units")
            
            if self.btn_left_platos:
                self.btn_left_platos.config(command=scroll_platos_left)
            if self.btn_right_platos:
                self.btn_right_platos.config(command=scroll_platos_right)
        
        # Para bebidas
        if self.frame_preview_bebidas:
            self.frame_preview_bebidas.update_idletasks()
            update_scrollregion(self.canvas_bebidas, self.frame_preview_bebidas)
            
            def scroll_bebidas_left():
                self.canvas_bebidas.xview_scroll(-3, "units")
            
            def scroll_bebidas_right():
                self.canvas_bebidas.xview_scroll(3, "units")
            
            if self.btn_left_bebidas:
                self.btn_left_bebidas.config(command=scroll_bebidas_left)
            if self.btn_right_bebidas:
                self.btn_right_bebidas.config(command=scroll_bebidas_right)

                

    def _abrir_ventana_menu_completo(self, tipo_menu):
        """Abre ventana con TODO el menú y oculta el dashboard"""
        
        # Cerrar cualquier ventana de menú anterior
        if hasattr(self, 'current_menu_window') and self.current_menu_window:
            try:
                self.current_menu_window.destroy()
            except:
                pass
        
        # Ocultar panel derecho
        if getattr(self, "right_panel_visible", False):
            self.right_panel.pack_forget()
            self.right_panel_visible = False
        
        # Limpiar contenido central
        for widget in self.center_frame.winfo_children():
            widget.destroy()
        
        # Crear barra superior con flecha para volver
        top_bar = tk.Frame(self.center_frame, bg="#FFFFFF")
        top_bar.pack(fill="x", pady=(10, 5))
        
        # Flecha para volver al dashboard
        arrow_btn = tk.Button(
            top_bar,
            text="← Volver al Inicio",
            bg="#FFFFFF",
            fg="#C8B88A",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            command=self._mostrar_dashboard_inicial
        )
        arrow_btn.pack(side="left", padx=(5, 15))
        
        # Título
        titulo = "Menú completo de Platos" if tipo_menu == "Plato" else "Menú completo de Bebidas"
        tk.Label(
            top_bar,
            text=titulo,
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=5)
        
        # Contenedor para el menú completo
        cont = tk.Frame(self.center_frame, bg="#F5F1E8")
        cont.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas con scroll
        canvas = tk.Canvas(cont, bg="#F5F1E8", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        vsb = ttk.Scrollbar(cont, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)
        
        inner = tk.Frame(canvas, bg="#F5F1E8")
        canvas.create_window((0, 0), window=inner, anchor="nw")
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", on_configure)
        
        # Cargar datos
        conexion = conectar()
        cursor = conexion.cursor()
        
        if tipo_menu == "Plato":
            cursor.execute("""
                SELECT 
                    COALESCE(P.NombrePlato, '—') AS Nombre,
                    COALESCE(CP.NombreCategoria, '—') AS Categoria,
                    ISNULL(P.CostoPorPlato, 0) AS Precio,
                    P.Imagen
                FROM Produccion P
                LEFT JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
                LEFT JOIN CategoriaPlatos CP ON CP.IDCategoriaPlatos = MP.IDCategoriaPlatos
                WHERE P.NombrePlato IS NOT NULL
                    AND ISNULL(P.CantidadDePlatos,0) > 0
                ORDER BY Categoria, Nombre;
            """)
        else:
            cursor.execute("""
                SELECT 
                    COALESCE(P.NombreBebida, '—') AS Nombre,
                    COALESCE(CB.NombreCategoria, '—') AS Categoria,
                    ISNULL(P.CostoPorBebida, 0) AS Precio,
                    P.Imagen
                FROM Produccion P
                LEFT JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
                LEFT JOIN CategoriaBebidas CB ON CB.IDCategoriaBebidas = MB.IDCategoriaBebidas
                WHERE P.NombreBebida IS NOT NULL
                    AND ISNULL(P.CantidadDeBebidas,0) > 0
                ORDER BY Categoria, Nombre;
            """)
        
        filas = cursor.fetchall()
        
        # Organizar por categorías
        categorias = {}
        for nombre, categoria, precio, img_bytes in filas:
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append((nombre, precio, img_bytes))
        
        # Mostrar por categorías
        row_idx = 0
        for categoria, productos in categorias.items():
            # Título de categoría
            cat_frame = tk.LabelFrame(
                inner,
                text=f"  {categoria}  ",
                bg="#FFFFFF",
                fg="#333333",
                font=("Segoe UI", 11, "bold"),
                padx=15,
                pady=10
            )
            cat_frame.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=(0, 15))
            cat_frame.columnconfigure(0, weight=1)
            row_idx += 1
            
            # Crear grid de productos (4 por fila)
            productos_frame = tk.Frame(cat_frame, bg="#FFFFFF")
            productos_frame.grid(row=0, column=0, sticky="ew")
            
            for idx, (nombre, precio, img_bytes) in enumerate(productos):
                col = idx % 4
                row = idx // 4
                
                # TARJETA CON TAMAÑO FIJO PARA LA IMAGEN
                card = tk.Frame(
                    productos_frame,
                    bg="#F8F5EE",
                    bd=2,
                    relief="ridge",
                    width=200,  # Ancho fijo
                    height=200  # Alto fijo
                )
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
                card.grid_propagate(False)  # Mantener tamaño fijo
                
                # CONTENEDOR PARA IMAGEN CON TAMAÑO FIJO
                img_container = tk.Frame(card, bg="#FFFFFF", width=120, height=120)
                img_container.pack(pady=(15, 8))
                img_container.pack_propagate(False)  # Mantener tamaño fijo del contenedor
                
                # Label para mostrar la imagen centrada
                lbl_img = tk.Label(img_container, bg="#FFFFFF")
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")  # Centrar imagen
                
                if img_bytes:
                    try:
                        from io import BytesIO
                        from PIL import Image, ImageTk
                        img = Image.open(BytesIO(img_bytes))
                        
                        # Redimensionar imagen a tamaño fijo (100x100)
                        img = img.resize((100, 100), Image.Resampling.LANCZOS)
                        
                        # Si la imagen no es cuadrada, crear fondo blanco
                        if img.size[0] != img.size[1]:
                            # Crear imagen cuadrada con fondo blanco
                            background = Image.new('RGB', (100, 100), color='white')
                            # Calcular posición para centrar
                            offset = ((100 - img.size[0]) // 2, (100 - img.size[1]) // 2)
                            background.paste(img, offset)
                            img = background
                        
                        photo = ImageTk.PhotoImage(img)
                        lbl_img.config(image=photo)
                        lbl_img.image = photo  # Mantener referencia
                    except Exception as e:
                        print(f"Error cargando imagen: {e}")
                        lbl_img.config(text="🖼️", fg="#999", font=("Segoe UI", 24))
                else:
                    lbl_img.config(text="📷", fg="#999", font=("Segoe UI", 24))
                
                # Nombre
                nombre_display = str(nombre)[:22] + ("..." if len(str(nombre)) > 22 else "")
                tk.Label(
                    card,
                    text=nombre_display,
                    bg="#F8F5EE",
                    fg="#222222",
                    font=("Segoe UI", 9, "bold"),
                    wraplength=180,
                    justify="center"
                ).pack()
                
                # Precio
                tk.Label(
                    card,
                    text=f"C$ {float(precio):.2f}",
                    bg="#F8F5EE",
                    fg="#157347",
                    font=("Segoe UI", 10, "bold")
                ).pack(pady=(8, 15))
        
        conexion.close()
        
        # Guardar referencia a la ventana actual
        self.current_menu_window = inner


    def _actualizar_vistas_menu(self):
        """
        Actualiza todas las vistas del menú después de cambios en categorías.
        Esto incluye las vistas previas y los combos en producción.
        """
        try:
            # 1. Recargar categorías en producción
            if hasattr(self, 'recargar_categorias'):
                self.recargar_categorias()
            
            # 2. Recargar vista previa del dashboard
            if hasattr(self, '_cargar_vista_previa_menu'):
                self._cargar_vista_previa_menu()
            
            # 3. Actualizar combos en producción si existen
            if hasattr(self, 'cmb_categoria') and hasattr(self, 'cmb_tipo'):
                try:
                    if self.cmb_categoria.winfo_exists() and self.cmb_tipo.winfo_exists():
                        tipo_actual = self.cmb_tipo.get()
                        if tipo_actual == "Plato" and hasattr(self, 'cat_platos_nombres'):
                            self.cmb_categoria["values"] = self.cat_platos_nombres
                        elif tipo_actual == "Bebida" and hasattr(self, 'cat_bebidas_nombres'):
                            self.cmb_categoria["values"] = self.cat_bebidas_nombres
                except tk.TclError:
                    # Widgets no existen (ventana cerrada)
                    pass
            
            # 4. Recargar producción en treeview
            if hasattr(self, 'cargar_produccion'):
                self.cargar_produccion()
                
        except Exception as e:
            print(f"Error actualizando vistas del menú: {e}")
            # Continuar sin fallar
        # ------------------------------------------------------------------
    # VENTANA DE GESTIÓN (CRUDs) + FLECHA PARA OCULTAR PANEL LATERAL
    # ------------------------------------------------------------------
    def _abrir_ventana_gestion(self):
        """Muestra el notebook de CRUDs dentro del centro (misma ventana)."""

        # 🔹 OCULTAR panel derecho mientras se está en los CRUDs
        if getattr(self, "right_panel_visible", False):
            self.right_panel.pack_forget()
            self.right_panel_visible = False

        # limpiar contenido central
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        # contenedor para todo el CRUD
        container = tk.Frame(self.center_frame, bg="#FFFFFF")
        container.pack(fill="both", expand=True)

        # barra superior con flecha + título
        top_bar = tk.Frame(container, bg="#FFFFFF")
        top_bar.pack(fill="x", pady=(10, 5))

        self.arrow_btn = tk.Button(
            top_bar,
            text="◀",              # triangulito hacia la izquierda
            bg="#FFFFFF",
            bd=0,
            font=("Segoe UI", 12, "bold"),
            command=self._toggle_sidebar
        )
        self.arrow_btn.pack(side="left", padx=(5, 5))

        tk.Label(
            top_bar,
            text="Gestión de Datos  |  CRUD DataFood",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=5)

        # Notebook de CRUDs
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # pestañas CRUD
        self._create_tab_proveedores(notebook)
        self._create_tab_insumos(notebook)
        self._create_tab_produccion(notebook)
        self._create_tab_clientes(notebook)
        self._create_tab_ventas(notebook)

        self.sidebar_visible = True

    # hora
    def _actualizar_hora(self):
        ahora = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=ahora)
        # vuelve a llamarse dentro de 1000 ms (1 segundo)
        self.after(1000, self._actualizar_hora)

    # ------------------------------------------------------------------
    # TOGGLE DEL PANEL LATERAL (SOLO SIDEBAR, SIN PANEL DERECHO)
    # ------------------------------------------------------------------
    def _toggle_sidebar(self):
        """Oculta o muestra el panel lateral cuando se pulsa la flecha."""
        if self.sidebar_visible:
            # ocultar sidebar → el Treeview se expande
            self.sidebar.pack_forget()
            self.center_frame.pack_forget()
            self.center_frame.pack(
                side="left", fill="both", expand=True, padx=10, pady=5
            )

            self.sidebar_visible = False
            if hasattr(self, "arrow_btn"):
                self.arrow_btn.config(text="▶")   # flecha hacia la derecha
        else:
            # volver a mostrar sidebar
            self.center_frame.pack_forget()
            self.sidebar.pack(side="left", fill="y")
            self.center_frame.pack(
                side="left", fill="both", expand=True, padx=10, pady=5
            )

            self.sidebar_visible = True
            if hasattr(self, "arrow_btn"):
                self.arrow_btn.config(text="◀")   # flecha hacia la izquierda

    # ------------------------- UI --------------------------------

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TNotebook", background="#F5F1E8")
        style.configure("TNotebook.Tab", background="#E9E2D0", padding=6)
        style.map("TNotebook.Tab", background=[("selected", "#C8B88A")])

        style.configure("TFrame", background="#F5F1E8")
        style.configure("TLabel", background="#F5F1E8", font=("Segoe UI", 10))
        style.configure("TEntry", padding=4, font=("Segoe UI", 10))

        style.configure(
            "TButton", padding=6, font=("Segoe UI", 10, "bold"), background="#FFFFFF"
        )

        # TreeView
        style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            foreground="black",
            rowheight=24,
        )

        style.configure(
            "Treeview.Heading",
            background="#C8B88A",
            foreground="black",
            font=("Segoe UI", 10, "bold"),
        )

    # ----------------------------------------------------------------------------------- FUNCIÓN TREEVIEW ---------------------

    def _create_treeview(self, parent, columns):
        frame = tk.Frame(parent, bg="#F5F1E8")
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        # Scrollbars
        scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.pack(fill="both", expand=True)
        return tree

    # --------------------------------------------------------------------------------- CREATE TABS -----------------------------------
    
    # ---------------------------------------------------------------------------------
    def _create_tab_content(self, parent, title, labels, tree_columns, special_widgets=None):
        
        # Frame que va dentro del tab del Notebook
        frame_tab = ttk.Frame(parent)
        frame_tab.pack(fill="both", expand=True)

        # Frame principal interno
        main_frame = tk.Frame(frame_tab, bg="#F5F1E8")
        main_frame.pack(fill="both", expand=True)

        # ---------- PANEL IZQUIERDO CON SCROLL (FORMULARIO) ----------
        left_container = tk.Frame(
            main_frame, bg="#E9E2D0", width=self.LEFT_PANEL_WIDTH
        )
        left_container.pack(side="left", fill="y")
        left_container.pack_propagate(False)


        canvas = tk.Canvas(left_container, bg="#E9E2D0", highlightthickness=0)

        # ⬇️ Scrollbar VISIBLE, igual que la del Treeview
        scrollbar_left = tk.Scrollbar(
            left_container,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar_left.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar_left.set)


        # Frame interior real donde van labels, entries y botones
        left = tk.Frame(canvas, bg="#E9E2D0", padx=15, pady=15)
        canvas.create_window((0, 0), window=left, anchor="nw")

        def on_left_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        left.bind("<Configure>", on_left_configure)

        # ---------- CONTENIDO DEL FORM ----------
        tk.Label(
            left,
            text=f"📦 {title}",
            bg="#E9E2D0",
            font=("Segoe UI", 12, "bold"),
            fg="#6A4E23",
        ).pack(pady=(0, 10), anchor="w")

        entries = {}
        for lbl in labels:
            tk.Label(
                left,
                text=lbl + ":",
                bg="#E9E2D0",
                font=("Segoe UI", 10),
            ).pack(anchor="w")

            # Si hay un widget especial para este campo, úsalo
            if special_widgets and lbl in special_widgets:
                widget = special_widgets[lbl](left)
            else:
                widget = ttk.Entry(left)

            widget.pack(fill="x", pady=2)
            entries[lbl] = widget

        # ---------- BOTONES CRUD ----------
        btn_frame = tk.Frame(left, bg="#E9E2D0")
        btn_frame.pack(pady=10, fill="x")

        btn_agregar = ttk.Button(btn_frame, text="Agregar")
        btn_editar = ttk.Button(btn_frame, text="Editar")
        btn_eliminar = ttk.Button(btn_frame, text="Eliminar")
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar")

        btn_agregar.pack(fill="x", pady=2)
        btn_editar.pack(fill="x", pady=2)
        btn_eliminar.pack(fill="x", pady=2)
        btn_limpiar.pack(fill="x", pady=2)

        # ---------- FLECHITA ENTRE FORM Y TABLA ----------
        middle_bar = tk.Frame(main_frame, bg="#F5F1E8", width=12)
        middle_bar.pack(side="left", fill="y")

        # ---------- TREEVIEW A LA DERECHA ----------
        right = ttk.Frame(main_frame)
        right.pack(side="left", fill="both", expand=True)

        tree = self._create_treeview(right, tree_columns)

        form_visible = True  # estado interno de este TAB (no global)

        def toggle_form():
            nonlocal form_visible
            if form_visible:
                # Ocultar SOLO el panel izquierdo → Treeview ocupa más
                left_container.pack_forget()
                form_visible = False
                arrow_btn.config(text="▶")  # apunta a la derecha
            else:
                # Para restaurar el orden correcto: left | middle_bar | right
                right.pack_forget()
                middle_bar.pack_forget()

                left_container.pack(side="left", fill="y")
                middle_bar.pack(side="left", fill="y")
                right.pack(side="left", fill="both", expand=True)

                form_visible = True
                arrow_btn.config(text="◀")  # apunta a la izquierda

        arrow_btn = tk.Button(
            middle_bar,
            text="◀",
            bg="#F5F1E8",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            command=toggle_form,
        )
        arrow_btn.pack(padx=0, pady=0, fill="y")

        # devolvemos todo lo que necesita cada tab
        return entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar



# --------------------------------------proveedores global----------------------------------------------
    def cargar_proveedores_global(self):
        """Carga la lista de proveedores y, si el combo de Insumos existe y está vivo, lo actualiza."""
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT IDProveedor, NombreProveedor
                FROM Proveedores
                ORDER BY NombreProveedor
            """)
            # Guardamos la lista como atributo de la clase
            self.lista_proveedores = cursor.fetchall()

            # Intentar actualizar el combobox de Insumos solo si existe y NO está destruido
            if hasattr(self, "combo_proveedores_insumos"):
                try:
                    # winfo_exists() devuelve 1 si el widget sigue vivo en Tk
                    if self.combo_proveedores_insumos.winfo_exists():
                        self.combo_proveedores_insumos["values"] = [
                            fila[1] for fila in self.lista_proveedores
                        ]
                except tk.TclError:
                    # El widget ya no existe (por cambiar de pantalla, etc.), lo ignoramos
                    pass

            conexion.close()

        except Exception as e:
            # Aquí solo entramos si hay un problema REAL con la conexión/consulta
            msg.showerror(
                "Error de BD",
                f"No se pudieron cargar los proveedores globales desde la base de datos:\n{e}"
            )
            self.lista_proveedores = []



    # ---------------- ------------------------------------------------------------------------TAB PROVEEDORES ----------------
 
    def _create_tab_proveedores(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Proveedores")

        # Crear sección con widgets
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = self._create_tab_content(
            frame,
            "Gestión de Proveedores",
            ["Nombre Proveedor", "Teléfono"],
            ["IDProveedor", "Nombre Proveedor", "Teléfono"]
        )

        conexion = conectar()
        cursor = conexion.cursor()

        # -------------------------------------------------
        # Función para limpiar valores raros (', ) etc.
        # -------------------------------------------------
        def limpiar_valor(v):
            if v is None:
                return ""
            v = str(v)
            return v.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()

        # -------------------------------------------------
        # CARGAR PROVEEDORES EN EL TREEVIEW
        # -------------------------------------------------
        def cargar_proveedores():
            for fila in tree.get_children():
                tree.delete(fila)

            cursor.execute("""
                SELECT 
                    P.IDProveedor,
                    P.NombreProveedor,
                    T.Telefono
                FROM Proveedores P
                INNER JOIN TelefonoProveedores T
                    ON P.IDTelefonoProveedores = T.IDTelefonoProveedores
                ORDER BY P.IDProveedor
            """)

            for row in cursor.fetchall():
                limpio = [limpiar_valor(x) for x in row]
                tree.insert("", "end", values=limpio)

      
            self.cargar_proveedores_global()

        # -------------------------------------------------
        # AGREGAR PROVEEDOR
        # -------------------------------------------------
        def agregar_proveedor():
            try:
                nombre = entries["Nombre Proveedor"].get().strip()
                telefono = entries["Teléfono"].get().strip()

                if not nombre:
                    return msg.showwarning("Atención", "Debe ingresar el nombre del proveedor.")
                if not telefono:
                    return msg.showwarning("Atención", "Debe ingresar un número de teléfono.")

                # Insertar teléfono → obtener ID
                cursor.execute("""
                    INSERT INTO TelefonoProveedores (Telefono)
                    OUTPUT INSERTED.IDTelefonoProveedores
                    VALUES (?);
                """, (telefono,))
                id_tel = cursor.fetchone()[0]

                # Insertar proveedor
                cursor.execute("""
                    INSERT INTO Proveedores (NombreProveedor, IDTelefonoProveedores)
                    VALUES (?, ?)
                """, (nombre, id_tel))

                conexion.commit()
                msg.showinfo("Éxito", "Proveedor agregado correctamente.")

                cargar_proveedores()
                limpiar()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar:\n{e}")

        # -------------------------------------------------
        # ELIMINAR PROVEEDOR
        # -------------------------------------------------
        def eliminar_proveedor():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un proveedor para eliminar.")

                fila = tree.item(sel)["values"]
                id_prov = int(limpiar_valor(fila[0]))

                # Obtener IDTel antes de eliminar
                cursor.execute("SELECT IDTelefonoProveedores FROM Proveedores WHERE IDProveedor=?", (id_prov,))
                id_tel = cursor.fetchone()[0]

                # Borrar proveedor
                cursor.execute("DELETE FROM Proveedores WHERE IDProveedor=?", (id_prov,))
                cursor.execute("DELETE FROM TelefonoProveedores WHERE IDTelefonoProveedores=?", (id_tel,))

                conexion.commit()
                msg.showinfo("Éxito", "Proveedor eliminado correctamente.")

                cargar_proveedores()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")

        # -------------------------------------------------
        # EDITAR PROVEEDOR
        # -------------------------------------------------
        def editar_proveedor():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un proveedor para editar.")

                fila = tree.item(sel)["values"]
                id_prov = int(limpiar_valor(fila[0]))

                nombre = entries["Nombre Proveedor"].get().strip()
                telefono = entries["Teléfono"].get().strip()

                if not nombre:
                    return msg.showwarning("Atención", "El proveedor debe tener nombre.")
                if not telefono:
                    return msg.showwarning("Atención", "Debe ingresar un teléfono.")

                # Obtener ID teléfono
                cursor.execute("""
                    SELECT IDTelefonoProveedores 
                    FROM Proveedores
                    WHERE IDProveedor=?
                """, (id_prov,))
                id_tel = cursor.fetchone()[0]

                # Actualizar proveedor
                cursor.execute("""
                    UPDATE Proveedores
                    SET NombreProveedor=?
                    WHERE IDProveedor=?
                """, (nombre, id_prov))

                # Actualizar teléfono
                cursor.execute("""
                    UPDATE TelefonoProveedores
                    SET Telefono=?
                    WHERE IDTelefonoProveedores=?
                """, (telefono, id_tel))

                conexion.commit()
                msg.showinfo("Éxito", "Proveedor actualizado correctamente.")

                cargar_proveedores()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar:\n{e}")

        # -------------------------------------------------
        # LIMPIAR CAMPOS
        # -------------------------------------------------
        def limpiar():
            for e in entries.values():
                e.delete(0, tk.END)



                # -------------------------------------------------
        # DETALLE AL HACER DOBLE CLIC (IGUAL QUE INSUMOS)
        # -------------------------------------------------
        def mostrar_detalle_proveedor(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            id_prov, nombre, telefono = vals

            def safe(v):
                return "—" if v in (None, "", "—") else v

            # ---------- VENTANA ----------
            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle del proveedor #{safe(id_prov)}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 460
            alto_ventana = 260
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")
            detalle.minsize(420, 240)

            detalle.update_idletasks()
            sw = detalle.winfo_screenwidth()
            sh = detalle.winfo_screenheight()
            ww = detalle.winfo_width()
            wh = detalle.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            detalle.geometry(f"{ww}x{wh}+{x}+{y}")

            container = tk.Frame(detalle, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            card = tk.Frame(
                container,
                bg="#FDF7EA",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(fill="both", expand=True)

            canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
            canvas_d.pack(side="left", fill="both", expand=True)

            scrollbar_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
            scrollbar_d.pack(side="right", fill="y")

            canvas_d.configure(yscrollcommand=scrollbar_d.set)

            content = tk.Frame(canvas_d, bg="#FDF7EA")
            canvas_d.create_window((0, 0), window=content, anchor="nw")

            def on_configure(event):
                canvas_d.configure(scrollregion=canvas_d.bbox("all"))

            content.bind("<Configure>", on_configure)

            # ----- título -----
            tk.Label(
                content,
                text=f"Proveedor: {safe(nombre)}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(content, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            # ----- datos -----
            datos = [
                ("ID Proveedor", safe(id_prov)),
                ("Nombre", safe(nombre)),
                ("Teléfono", safe(telefono)),
            ]

            for i, (label_txt, valor) in enumerate(datos, start=2):
                tk.Label(
                    content,
                    text=label_txt + ":",
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 10, "bold"),
                ).grid(row=i, column=0, sticky="w", padx=10, pady=3)

                tk.Label(
                    content,
                    text=str(valor),
                    bg="#FDF7EA",
                    fg="#222222",
                    font=("Segoe UI", 10),
                ).grid(row=i, column=1, sticky="w", padx=5, pady=3)

            last_row = len(datos) + 2

            ttk.Separator(content, orient="horizontal").grid(
                row=last_row, column=0, columnspan=2, sticky="ew", padx=5, pady=(8, 5)
            )

            # ----- botón EDITAR (rellena formulario de la izquierda) -----
            def preparar_edicion():
                entries["Nombre Proveedor"].delete(0, tk.END)
                entries["Nombre Proveedor"].insert(
                    0, "" if safe(nombre) == "—" else nombre
                )

                entries["Teléfono"].delete(0, tk.END)
                entries["Teléfono"].insert(
                    0, "" if safe(telefono) == "—" else telefono
                )

                detalle.destroy()

            btn_editar_detalle = ttk.Button(
                content, text="Editar", command=preparar_edicion
            )
            btn_editar_detalle.grid(
                row=last_row + 1, column=0, padx=10, pady=(5, 10), sticky="w"
            )

            btn_cerrar = ttk.Button(content, text="Cerrar", command=detalle.destroy)
            btn_cerrar.grid(
                row=last_row + 1, column=1, padx=10, pady=(5, 10), sticky="e"
            )

            detalle.transient(self)
            detalle.grab_set()

        # doble clic → abrir detalle
        tree.bind("<Double-1>", mostrar_detalle_proveedor)

     
         # -------------------------------------------------
        # ASIGNAR BOTONES
        # -------------------------------------------------
        btn_agregar.config(command=agregar_proveedor)
        btn_eliminar.config(command=eliminar_proveedor)

        # Igual que en INSUMOS: este botón SOLO guarda cambios
        btn_editar.config(text="Guardar cambios", command=editar_proveedor)

        btn_limpiar.config(command=limpiar)

        cargar_proveedores()





     # ---------------- ------------------------------------------------------------------TAB INSUMOS ----------------
  
    def _create_tab_insumos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Insumos")

        conexion = conectar()
        cursor = conexion.cursor()

        # --------- Campos del formulario (sin fecha manual) ---------
        labels = [
            "Categoría",
            "Nombre del Insumo",
            "Cantidad Disponible",
            "Cantidad Dañada",
            "Proveedor",
            "Precio Compra",
            "Cantidad Comprada",
        ]

        columns = [
            "ID", "Categoría", "Nombre", "Disponible",
            "Dañada", "Proveedor", "Precio Compra",
            "Cantidad Comprada", "Fecha"
        ]

        # Fábrica Combobox
        def make_combo(parent):
            return ttk.Combobox(parent, state="readonly")

        special = {
            "Categoría": make_combo,
            "Nombre del Insumo": make_combo,
            "Proveedor": make_combo,
        }

        # Usamos el molde genérico
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = (
            self._create_tab_content(
                frame,
                "Gestión de Insumos",
                labels,
                columns,
                special_widgets=special,
            )
        )

        # Referencias rápidas
        combo_categoria = entries["Categoría"]
        cmb_nombre_insumo = entries["Nombre del Insumo"]
        self.combo_proveedores_insumos = entries["Proveedor"]

        # Ocultar algunas columnas si quieres menos info visible
        for col in ("Dañada", "Proveedor", "Precio Compra", "Cantidad Comprada", "Fecha"):
            tree.column(col, width=0, stretch=False)

        # ========== CARGAR DATOS PARA COMBOS DESDE BD ==========
        # Categorías de insumos
        cursor.execute("""
            SELECT IDCategoriaInsumos, NombreCategoria
            FROM CategoriaInsumos
            ORDER BY NombreCategoria;
        """)
        categorias_ins = cursor.fetchall()
        nombres_categorias_ins = [c[1] for c in categorias_ins]
        id_cat_por_nombre = {c[1]: c[0] for c in categorias_ins}
        combo_categoria["values"] = nombres_categorias_ins

        # Proveedores (usa tu función global)
        self.cargar_proveedores_global()
        self.combo_proveedores_insumos["values"] = [p[1] for p in self.lista_proveedores]

        # -------- Combobox de nombres de insumos según categoría --------
        def cargar_nombres_insumo(*_):
            categoria = combo_categoria.get()
            if not categoria or categoria not in id_cat_por_nombre:
                cmb_nombre_insumo["values"] = ()
                cmb_nombre_insumo.set("")
                return

            id_cat = id_cat_por_nombre[categoria]
            cursor.execute("""
                SELECT DISTINCT NombreInsumo
                FROM Insumos
                WHERE IDCategoriaInsumos = ?
                ORDER BY NombreInsumo;
            """, (id_cat,))
            nombres = [r[0] for r in cursor.fetchall()]

            cmb_nombre_insumo["values"] = nombres
            if nombres:
                cmb_nombre_insumo.set(nombres[0])
            else:
                cmb_nombre_insumo.set("")

        combo_categoria.bind("<<ComboboxSelected>>", cargar_nombres_insumo)

        # ===================== FILTROS (como en producción) =====================

        filtro_texto = {"texto": ""}
        filtro_categoria = {"categoria": None}

        # Frame que contiene el Treeview (viene de _create_tab_content)
        cont_tabla = tree.master

        barra_filtros = tk.Frame(cont_tabla, bg="#FDF7EA")
        barra_filtros.pack(fill="x", padx=3, pady=(0,4), before=tree)

        # ---- Filtro categoría ----
        tk.Label(
            barra_filtros,
            text="Categoría:",
            bg="#FDF7EA",
            fg="#333333",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(4,4))

        cmb_filtro_cat = ttk.Combobox(
            barra_filtros, 
            state="readonly", 
            width=18
        )
        cmb_filtro_cat.pack(side="left", padx=(0,10))

        cmb_filtro_cat["values"] = ["Todas"] + nombres_categorias_ins
        cmb_filtro_cat.set("Todas")

        # ---- Filtro texto ----
        tk.Label(
            barra_filtros,
            text="Buscar:",
            bg="#FDF7EA",
            fg="#333333",
        ).pack(side="left")

        txt_buscar_ins = tk.Entry(barra_filtros, width=20)
        txt_buscar_ins.pack(side="left", padx=(4,6))

        # ---- Botón limpiar ----
        btn_limpiar_filtro = tk.Button(
            barra_filtros,
            text="Limpiar",
            bg="#E5D8B4",
            fg="#333333",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            command=lambda: limpiar_filtros_insumos()
        )
        btn_limpiar_filtro.pack(side="left", padx=4)

        # ============================================================
        # FUNCIONES DE FILTRADO
        # ============================================================
        def cargar_insumos():
            tree.delete(*tree.get_children())

            texto = filtro_texto["texto"]
            cat_sel = filtro_categoria["categoria"]

            cursor.execute("""
                WITH UltimaCompra AS (
                    SELECT
                        PI.IDInsumos,
                        PI.IDProveedor,
                        PI.PrecioCompra,
                        PI.CantidadComprada,
                        PI.Dia,
                        PI.Mes,
                        PI.Ano,
                        ROW_NUMBER() OVER (
                            PARTITION BY PI.IDInsumos
                            ORDER BY PI.Ano DESC, PI.Mes DESC, PI.Dia DESC
                        ) AS rn
                FROM ProveedoresInsumos PI
                )
                SELECT 
                    I.IDInsumos,
                    C.NombreCategoria,
                    I.NombreInsumo,
                    I.CantidadDisponible,
                    I.CantidadDañada,
                    P.NombreProveedor,
                    UC.PrecioCompra,
                    UC.CantidadComprada,
                    UC.Dia,
                    UC.Mes,
                    UC.Ano
                FROM Insumos I
                JOIN CategoriaInsumos C 
                    ON C.IDCategoriaInsumos = I.IDCategoriaInsumos
                LEFT JOIN UltimaCompra UC
                    ON UC.IDInsumos = I.IDInsumos AND UC.rn = 1
                LEFT JOIN Proveedores P ON P.IDProveedor = UC.IDProveedor
                ORDER BY I.IDInsumos ASC;
            """)

            for row in cursor.fetchall():
                (id_in, cat, nombre, disp, danio, prov, precio, compr, dia, mes, ano) = row
                
                # FILTRO CATEGORÍA
                if cat_sel and cat_sel != cat:
                    continue
                
                # FILTRO TEXTO
                if texto and texto not in nombre.lower():
                    continue
                
                fecha = f"{dia}/{mes}/{ano}" if dia and mes and ano else "—"

                tree.insert(
                    "",
                    "end",
                    values=[
                        id_in, cat, nombre, disp, danio, prov or "—",
                        precio if precio is not None else "—",
                        compr if compr is not None else "—",
                        fecha
                    ]
                )

        def aplicar_filtros_insumos(*_):
            # texto
            filtro_texto["texto"] = txt_buscar_ins.get().strip().lower()

            # categoría
            sel = cmb_filtro_cat.get()
            if sel == "Todas" or not sel:
                filtro_categoria["categoria"] = None
            else:
                filtro_categoria["categoria"] = sel

            cargar_insumos()

        def limpiar_filtros_insumos():
            txt_buscar_ins.delete(0, tk.END)
            cmb_filtro_cat.set("Todas")
            filtro_texto["texto"] = ""
            filtro_categoria["categoria"] = None
            cargar_insumos()

        # Eventos de filtrado
        txt_buscar_ins.bind("<KeyRelease>", aplicar_filtros_insumos)
        cmb_filtro_cat.bind("<<ComboboxSelected>>", aplicar_filtros_insumos)

        # ========== DETALLE (doble clic) ==========
        def mostrar_detalle_insumo(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            def safe(v):
                return "—" if v in (None, "", "—") else v

            datos = [
                ("ID",                 safe(vals[0])),
                ("Categoría",          safe(vals[1])),
                ("Nombre",             safe(vals[2])),
                ("Cantidad disponible", safe(vals[3])),
                ("Cantidad dañada",    safe(vals[4])),
                ("Proveedor",          safe(vals[5])),
                ("Precio compra",      safe(vals[6])),
                ("Cantidad comprada",  safe(vals[7])),
                ("Fecha de ingreso",   safe(vals[8])),
            ]

            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle del insumo #{safe(vals[0])}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 460
            alto_ventana = 300
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")
            detalle.minsize(420, 260)

            detalle.update_idletasks()
            sw = detalle.winfo_screenwidth()
            sh = detalle.winfo_screenheight()
            ww = detalle.winfo_width()
            wh = detalle.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            detalle.geometry(f"{ww}x{wh}+{x}+{y}")

            container = tk.Frame(detalle, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            card = tk.Frame(
                container,
                bg="#FDF7EA",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(fill="both", expand=True)

            canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
            canvas_d.pack(side="left", fill="both", expand=True)

            scrollbar_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
            scrollbar_d.pack(side="right", fill="y")

            canvas_d.configure(yscrollcommand=scrollbar_d.set)

            content = tk.Frame(canvas_d, bg="#FDF7EA")
            canvas_d.create_window((0, 0), window=content, anchor="nw")

            def on_configure(event):
                canvas_d.configure(scrollregion=canvas_d.bbox("all"))

            content.bind("<Configure>", on_configure)

            tk.Label(
                content,
                text=f"Insumo: {safe(vals[2])}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(content, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            for i, (label_txt, valor) in enumerate(datos, start=2):
                tk.Label(
                    content,
                    text=label_txt + ":", 
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 10, "bold"),
                ).grid(row=i, column=0, sticky="w", padx=10, pady=3)

                tk.Label(
                    content,
                    text=str(valor),
                    bg="#FDF7EA",
                    fg="#222222",
                    font=("Segoe UI", 10),
                ).grid(row=i, column=1, sticky="w", padx=5, pady=3)

            last_row = len(datos) + 2

            ttk.Separator(content, orient="horizontal").grid(
                row=last_row, column=0, columnspan=2, sticky="ew", padx=5, pady=(8, 5)
            )

            # ----- botón EDITAR (rellena formulario) -----
            def preparar_edicion():
                cat, nombre, disp, dan, prov, precio, cant, _fecha = (
                    safe(vals[1]), safe(vals[2]), safe(vals[3]), safe(vals[4]),
                    safe(vals[5]), safe(vals[6]), safe(vals[7]), safe(vals[8])
                )

                combo_categoria.set("" if cat == "—" else cat)
                cargar_nombres_insumo()
                cmb_nombre_insumo.set("" if nombre == "—" else nombre)

                entries["Cantidad Disponible"].delete(0, tk.END)
                entries["Cantidad Disponible"].insert(0, "" if disp == "—" else disp)

                entries["Cantidad Dañada"].delete(0, tk.END)
                entries["Cantidad Dañada"].insert(0, "" if dan == "—" else dan)

                self.combo_proveedores_insumos.set("" if prov == "—" else prov)

                entries["Precio Compra"].delete(0, tk.END)
                entries["Precio Compra"].insert(0, "" if precio == "—" else precio)

                entries["Cantidad Comprada"].delete(0, tk.END)
                entries["Cantidad Comprada"].insert(0, "" if cant == "—" else cant)

                detalle.destroy()

            btn_editar_detalle = ttk.Button(
                content, text="Editar este insumo", command=preparar_edicion
            )
            btn_editar_detalle.grid(
                row=last_row + 1, column=0, padx=10, pady=(5, 10), sticky="w"
            )

            btn_cerrar = ttk.Button(content, text="Cerrar", command=detalle.destroy)
            btn_cerrar.grid(
                row=last_row + 1, column=1, padx=10, pady=(5, 10), sticky="e"
            )

            detalle.transient(self)
            detalle.grab_set()

        tree.bind("<Double-1>", mostrar_detalle_insumo)

        # ------------------------------------------------------------------
        # GESTOR DE CATEGORÍAS (botón "Categorías...")
        # ------------------------------------------------------------------
        
        def abrir_gestor_categorias_insumos():
            win = tk.Toplevel(self)
            win.title("Gestor de Categorías de Insumos")
            win.configure(bg="#F5F1E8")
            win.geometry("540x380")

            win.update_idletasks()
            sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
            ww, wh = win.winfo_width(), win.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            win.geometry(f"{ww}x{wh}+{x}+{y}")

            cont = tk.Frame(win, bg="#FDF7EA", bd=1, relief="solid")
            cont.pack(fill="both", expand=True, padx=10, pady=10)

            tk.Label(
                cont,
                text="Categorías de Insumos",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", padx=10, pady=(5, 5))

            ttk.Separator(cont, orient="horizontal").pack(
                fill="x", padx=10, pady=(0, 8)
            )

            # ---------- Treeview ----------
            tabla_frame = tk.Frame(cont, bg="#FDF7EA")
            tabla_frame.pack(fill="both", expand=True, padx=10, pady=(5, 5))

            cols = ("ID", "Nombre")
            tree_cat = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=7)
            tree_cat.pack(side="left", fill="both", expand=True)

            for c in cols:
                tree_cat.heading(c, text=c)
            tree_cat.column("ID", width=70, anchor="center")
            tree_cat.column("Nombre", width=280, anchor="w")

            scroll_cat = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree_cat.yview)
            scroll_cat.pack(side="right", fill="y")
            tree_cat.configure(yscrollcommand=scroll_cat.set)

            # ---------- Formulario ----------
            form = tk.Frame(cont, bg="#FDF7EA")
            form.pack(fill="x", padx=10, pady=(5, 5))

            tk.Label(
                form,
                text="Nombre categoría:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 9),
            ).grid(row=0, column=0, sticky="e", padx=5, pady=3)

            ent_nombre_cat = tk.Entry(form)
            ent_nombre_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
            form.columnconfigure(1, weight=1)

            id_cat_seleccionado = {"id": None}

            # ---------- Helpers ----------
            def limpiar_form():
                id_cat_seleccionado["id"] = None
                ent_nombre_cat.delete(0, tk.END)

            def cargar_tabla():
                tree_cat.delete(*tree_cat.get_children())

                cursor = self.conexion.cursor()
                cursor.execute("SELECT IDCategoriaInsumos, NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria")
                for (idc, nom) in cursor.fetchall():
                    tree_cat.insert("", "end", values=(idc, nom))

                limpiar_form()

            def sincronizar_toolboxes():
                """Actualizar TODOS los combobox de categorías del CRUD de insumos."""
                cursor = self.conexion.cursor()
                cursor.execute("SELECT NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria")

                categorias = [c[0] for c in cursor.fetchall()]

                # IMPORTANTE → estos son los combobox que existen en tu CRUD de Insumos
                # Asegúrate que los nombres coincidan con entries[...] de insumos.
                try:
                    self.entries_insumos["Categoría"]["values"] = categorias
                except:
                    pass

                try:
                    self.entries_insumos_buscar["Categoría"]["values"] = categorias
                except:
                    pass

                try:
                    self.entries_insumos_editar["Categoría"]["values"] = categorias
                except:
                    pass

            def on_select(event=None):
                sel = tree_cat.selection()
                if not sel:
                    return
                vals = tree_cat.item(sel)["values"]
                if not vals:
                    return
                id_cat_seleccionado["id"] = vals[0]
                ent_nombre_cat.delete(0, tk.END)
                ent_nombre_cat.insert(0, vals[1])

            tree_cat.bind("<<TreeviewSelect>>", on_select)

            # ---------- Agregar ----------
            def agregar_categoria():
                nombre = ent_nombre_cat.get().strip()
                if not nombre:
                    return msg.showwarning("Atención", "Ingrese un nombre.")

                try:
                    cursor = self.conexion.cursor()
                    cursor.execute(
                        "INSERT INTO CategoriaInsumos (NombreCategoria) VALUES (?)",
                        (nombre,)
                    )
                    self.conexion.commit()
                    cargar_tabla()
                    sincronizar_toolboxes()
                    msg.showinfo("Éxito", "Categoría agregada.")
                except Exception as e:
                    msg.showerror("Error", f"No se pudo agregar:\n{e}")

            # ---------- Guardar cambios ----------
            def guardar_categoria():
                idc = id_cat_seleccionado["id"]
                if idc is None:
                    msg.showwarning("Atención", "Seleccione una categoría.")
                    return

                nombre = ent_nombre_cat.get().strip()
                if not nombre:
                    return msg.showwarning("Atención", "Ingrese un nombre.")

                try:
                    cursor = self.conexion.cursor()
                    cursor.execute("""
                        UPDATE CategoriaInsumos
                        SET NombreCategoria = ?
                        WHERE IDCategoriaInsumos = ?
                    """, (nombre, idc))
                    self.conexion.commit()
                    cargar_tabla()
                    sincronizar_toolboxes()
                    msg.showinfo("Éxito", "Cambios guardados.")
                except Exception as e:
                    msg.showerror("Error", f"No se pudo actualizar:\n{e}")

            # ---------- Eliminar ----------
            def eliminar_categoria():
                idc = id_cat_seleccionado["id"]
                if idc is None:
                    return msg.showwarning("Atención", "Seleccione una categoría.")

                if not msg.askyesno("Confirmar", "¿Eliminar esta categoría?"):
                    return

                try:
                    cursor = self.conexion.cursor()
                    cursor.execute("DELETE FROM CategoriaInsumos WHERE IDCategoriaInsumos = ?", (idc,))
                    self.conexion.commit()
                    cargar_tabla()
                    sincronizar_toolboxes()
                    msg.showinfo("Éxito", "Categoría eliminada.")
                except Exception as e:
                    msg.showerror("Error", f"No se pudo eliminar:\n{e}")

            # ---------- Botones ----------
            botones = tk.Frame(cont, bg="#FDF7EA")
            botones.pack(fill="x", padx=10, pady=(5, 5))

            tk.Button(
                botones, text="Agregar", bg="#E5D8B4", fg="#333333",
                relief="flat", font=("Segoe UI", 9, "bold"),
                command=agregar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones, text="Guardar cambios", bg="#E5D8B4", fg="#333333",
                relief="flat", font=("Segoe UI", 9, "bold"),
                command=guardar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones, text="Eliminar", bg="#E5D8B4", fg="#333333",
                relief="flat", font=("Segoe UI", 9, "bold"),
                command=eliminar_categoria
            ).pack(side="left", padx=5)

            cargar_tabla()
            win.transient(self)
            win.grab_set()

        # ============================================================
        # FUNCIONES CRUD
        # ============================================================
        def agregar_insumo():
            from datetime import date
            try:
                categoria = combo_categoria.get().strip()
                nombre = cmb_nombre_insumo.get().strip()
                disp_txt = entries["Cantidad Disponible"].get().strip()
                danio_txt = entries["Cantidad Dañada"].get().strip()
                proveedor = self.combo_proveedores_insumos.get().strip()
                precio_txt = entries["Precio Compra"].get().strip()
                comprada_txt = entries["Cantidad Comprada"].get().strip()

                if not categoria or not nombre:
                    return msg.showwarning("Atención", "Seleccione categoría y nombre del insumo.")
                if not proveedor:
                    return msg.showwarning("Atención", "Seleccione un proveedor.")
                if not comprada_txt:
                    return msg.showwarning("Atención", "Ingrese la cantidad comprada.")

                # Valores por defecto 0 si quedan vacíos
                disp_txt = disp_txt or "0"
                danio_txt = danio_txt or "0"
                precio_txt = precio_txt or "0"
                comprada_txt = comprada_txt or "0"

                try:
                    # DISPONIBLE se valida pero NO se usa para sumar
                    disp = int(disp_txt)
                    danio = int(danio_txt)
                    precio = float(precio_txt)
                    comprada = int(comprada_txt)
                except ValueError:
                    return msg.showwarning(
                        "Atención",
                        "Cantidad disponible, dañada, comprada y precio deben ser numéricos."
                    )

                if categoria not in id_cat_por_nombre:
                    return msg.showerror("Error", "Categoría de insumo no encontrada.")
                id_cat = id_cat_por_nombre[categoria]

                # ¿Ya existe el insumo con esa categoría y nombre?
                cursor.execute(
                    """
                    SELECT IDInsumos, CantidadDisponible, CantidadDañada
                    FROM Insumos
                    WHERE IDCategoriaInsumos = ? AND NombreInsumo = ?;
                    """,
                    (id_cat, nombre)
                )
                row = cursor.fetchone()

                if row:
                    # --- EXISTE: sumamos SOLO la cantidad comprada al stock ---
                    id_ins = row[0]
                    cant_actual = row[1] or 0
                    danio_actual = row[2] or 0

                    nueva_disp = cant_actual + comprada      # 👈 se suma Comprada
                    nueva_danio = danio_actual + danio       # dañada también se acumula

                    cursor.execute(
                        """
                        UPDATE Insumos
                        SET CantidadDisponible = ?, CantidadDañada = ?
                        WHERE IDInsumos = ?;
                        """,
                        (nueva_disp, nueva_danio, id_ins)
                    )
                else:
                    # --- NO EXISTE: se crea con cantidad disponible = cantidad comprada ---
                    nueva_disp = comprada                    # 👈 aquí también usamos Comprada
                    nueva_danio = danio

                    cursor.execute(
                        """
                        INSERT INTO Insumos
                            (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada)
                        VALUES (?, ?, ?, ?);
                        """,
                        (id_cat, nombre, nueva_disp, nueva_danio)
                    )
                    conexion.commit()
                    cursor.execute("SELECT MAX(IDInsumos) FROM Insumos;")
                    id_ins = cursor.fetchone()[0]

                # ID del proveedor
                cursor.execute(
                    "SELECT IDProveedor FROM Proveedores WHERE NombreProveedor = ?;",
                    (proveedor,)
                )
                row_prov = cursor.fetchone()
                if not row_prov:
                    return msg.showerror("Error", "Proveedor no encontrado.")
                id_prov = row_prov[0]

                # Fecha automática (hoy)
                hoy = date.today()
                dia, mes, ano = hoy.day, hoy.month, hoy.year

                # Registrar la compra del proveedor
                cursor.execute(
                    """
                    INSERT INTO ProveedoresInsumos
                        (IDInsumos, IDProveedor, PrecioCompra, CantidadComprada, Dia, Mes, Ano)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (id_ins, id_prov, precio, comprada, dia, mes, ano)
                )

                conexion.commit()
                msg.showinfo("Éxito", "Insumo registrado correctamente.")
                cargar_insumos()
                cargar_nombres_insumo()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar el insumo:\n{e}")
        
        #---------------------------------------eliminar ------------------
        def eliminar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un insumo.")

                id_ins = tree.item(sel)["values"][0]

                confirmar = msg.askyesno(
                    "Confirmar eliminación",
                    "¿Está seguro de que desea eliminar este insumo?\n"
                    
                )
                if not confirmar:
                    return  

                cursor.execute("DELETE FROM ProveedoresInsumos WHERE IDInsumos = ?;", (id_ins,))
                cursor.execute("DELETE FROM Insumos WHERE IDInsumos = ?;", (id_ins,))
                conexion.commit()

                msg.showinfo("Éxito", "Insumo eliminado.")
                cargar_insumos()
                cargar_nombres_insumo()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")

        #------------------------editar------------------------
        def editar_insumo():
            from datetime import date
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un insumo.")

                id_ins = tree.item(sel)["values"][0]

                categoria = combo_categoria.get().strip()
                nombre = cmb_nombre_insumo.get().strip()
                disp_txt = entries["Cantidad Disponible"].get().strip()
                danio_txt = entries["Cantidad Dañada"].get().strip()
                proveedor = self.combo_proveedores_insumos.get().strip()
                precio_txt = entries["Precio Compra"].get().strip()
                comprada_txt = entries["Cantidad Comprada"].get().strip()

                if not categoria or not nombre:
                    return msg.showwarning("Atención", "Complete categoría y nombre.")
                if not proveedor:
                    return msg.showwarning("Atención", "Seleccione un proveedor.")

                disp_txt = disp_txt or "0"
                danio_txt = danio_txt or "0"
                precio_txt = precio_txt or "0"
                comprada_txt = comprada_txt or "0"

                try:
                    disp = int(disp_txt)
                    danio = int(danio_txt)
                    precio = float(precio_txt)
                    comprada = int(comprada_txt)
                except ValueError:
                    return msg.showwarning("Atención",
                                        "Cantidad, dañada, compra y precio deben ser numéricos.")

                if categoria not in id_cat_por_nombre:
                    return msg.showerror("Error", "Categoría de insumo no encontrada.")
                id_cat = id_cat_por_nombre[categoria]

                # Actualizar tabla Insumos
                cursor.execute(
                    """
                    UPDATE Insumos
                    SET IDCategoriaInsumos = ?, NombreInsumo = ?,
                        CantidadDisponible = ?, CantidadDañada = ?
                    WHERE IDInsumos = ?;
                    """,
                    (id_cat, nombre, disp, danio, id_ins)
                )

                # ID proveedor
                cursor.execute(
                    "SELECT IDProveedor FROM Proveedores WHERE NombreProveedor = ?;",
                    (proveedor,)
                )
                row_prov = cursor.fetchone()
                if not row_prov:
                    return msg.showerror("Error", "Proveedor no encontrado.")
                id_prov = row_prov[0]

                # Buscar el último registro en ProveedoresInsumos de ese insumo
                cursor.execute(
                    """
                    SELECT TOP 1 IDProveedoresInsumos
                    FROM ProveedoresInsumos
                    WHERE IDInsumos = ?
                    ORDER BY IDProveedoresInsumos DESC;
                    """,
                    (id_ins,)
                )
                row_pi = cursor.fetchone()

                hoy = date.today()
                dia, mes, ano = hoy.day, hoy.month, hoy.year

                if row_pi:
                    id_pi = row_pi[0]
                    cursor.execute(
                        """
                        UPDATE ProveedoresInsumos
                        SET IDProveedor = ?, PrecioCompra = ?, CantidadComprada = ?,
                            Dia = ?, Mes = ?, Ano = ?
                        WHERE IDProveedoresInsumos = ?;
                        """,
                        (id_prov, precio, comprada, dia, mes, ano, id_pi)
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ProveedoresInsumos
                            (IDInsumos, IDProveedor, PrecioCompra, CantidadComprada, Dia, Mes, Ano)
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                        """,
                        (id_ins, id_prov, precio, comprada, dia, mes, ano)
                    )

                conexion.commit()
                msg.showinfo("Éxito", "Insumo actualizado.")
                cargar_insumos()
                cargar_nombres_insumo()
                limpiar_campos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar:\n{e}")

        # ============================================================
        # LIMPIAR CAMPOS
        # ============================================================
        def limpiar_campos():
            for k, w in entries.items():
                if isinstance(w, ttk.Entry):
                    w.delete(0, tk.END)
                elif isinstance(w, ttk.Combobox):
                    w.set("")
            combo_categoria.set("")
            cmb_nombre_insumo["values"] = ()

        # ================================
        # VENTANA: VER STOCK COMPLETO (INSUMOS)
        # ================================
        def abrir_ventana_stock_insumos():
            win = tk.Toplevel(self)
            win.title("Stock completo de Insumos")
            win.configure(bg="#F5F1E8")

            win.geometry("720x420")
            win.update_idletasks()
            sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
            ww, wh = win.winfo_width(), win.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            win.geometry(f"{ww}x{wh}+{x}+{y}")

            marco = tk.Frame(win, bg="#FDF7EA", bd=1, relief="solid")
            marco.pack(fill="both", expand=True, padx=10, pady=10)

            # ---------------- BARRA SUPERIOR ----------------
            filtro_frame = tk.Frame(marco, bg="#FDF7EA")
            filtro_frame.pack(fill="x", padx=5, pady=5)

            # Buscador
            tk.Label(filtro_frame, text="Buscar:", bg="#FDF7EA").pack(side="left")
            txt_buscar = tk.Entry(filtro_frame, width=20)
            txt_buscar.pack(side="left", padx=(4, 10))

            # Filtro categoría
            tk.Label(filtro_frame, text="Categoría:", bg="#FDF7EA").pack(side="left")

            # Obtener categorías
            conexion_stock = conectar()
            cursor_stock = conexion_stock.cursor()
            cursor_stock.execute("SELECT NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria;")
            categorias_stock = ["Todas"] + [c[0] for c in cursor_stock.fetchall()]

            cmb_cat = ttk.Combobox(filtro_frame, state="readonly", values=categorias_stock, width=15)
            cmb_cat.current(0)
            cmb_cat.pack(side="left", padx=5)

            # ---------------- TREEVIEW ----------------
            cols = ("ID", "Categoría", "Nombre")
            frame_tree = tk.Frame(marco, bg="#FDF7EA")
            frame_tree.pack(fill="both", expand=True)

            tree_stock = ttk.Treeview(frame_tree, columns=cols, show="headings", height=15)
            tree_stock.pack(side="left", fill="both", expand=True)

            for c in cols:
                tree_stock.heading(c, text=c)

            tree_stock.column("ID", width=60, anchor="center")
            tree_stock.column("Categoría", width=180, anchor="w")
            tree_stock.column("Nombre", width=240, anchor="w")

            scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree_stock.yview)
            scroll.pack(side="right", fill="y")
            tree_stock.configure(yscrollcommand=scroll.set)

            # ---------------- FUNCIÓN PARA CARGAR ----------------
            def cargar_insumos_stock():
                tree_stock.delete(*tree_stock.get_children())

                txt = txt_buscar.get().strip().lower()
                fil_cat = cmb_cat.get()

                cursor_stock.execute("""
                    SELECT 
                        I.IDInsumos,
                        C.NombreCategoria,
                        I.NombreInsumo
                    FROM Insumos I
                    INNER JOIN CategoriaInsumos C
                        ON C.IDCategoriaInsumos = I.IDCategoriaInsumos
                    ORDER BY C.NombreCategoria, I.NombreInsumo;
                """)

                for (id_in, cat, nombre) in cursor_stock.fetchall():
                    # Filtro categoría
                    if fil_cat != "Todas" and fil_cat != cat:
                        continue

                    # Filtro texto
                    if txt and txt not in nombre.lower():
                        continue

                    tree_stock.insert("", "end", values=(id_in, cat, nombre))

            # ---------------- EVENTOS ----------------
            txt_buscar.bind("<KeyRelease>", lambda e: cargar_insumos_stock())
            cmb_cat.bind("<<ComboboxSelected>>", lambda e: cargar_insumos_stock())

            cargar_insumos_stock()

            # ----------- Doble clic: detalle con scroll + edición ------------
            def abrir_detalle_insumo(event=None):
                sel = tree_stock.selection()
                if not sel:
                    return

                vals = tree_stock.item(sel)["values"]
                if not vals:
                    return

                id_ins, cat_actual, nombre_actual = vals

                detalle = tk.Toplevel(win)
                detalle.title(f"Insumo: {nombre_actual}")
                detalle.configure(bg="#F5F1E8")
                detalle.geometry("420x320")

                detalle.update_idletasks()
                sw, sh = detalle.winfo_screenwidth(), detalle.winfo_screenheight()
                ww, wh = detalle.winfo_width(), detalle.winfo_height()
                x = (sw // 2) - (ww // 2)
                y = (sh // 2) - (wh // 2)
                detalle.geometry(f"{ww}x{wh}+{x}+{y}")

                # ----- Scroll -----
                card = tk.Frame(detalle, bg="#FDF7EA", bd=1, relief="solid")
                card.pack(fill="both", expand=True, padx=10, pady=10)

                canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
                canvas_d.pack(side="left", fill="both", expand=True)

                scroll_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
                scroll_d.pack(side="right", fill="y")

                canvas_d.configure(yscrollcommand=scroll_d.set)

                content = tk.Frame(canvas_d, bg="#FDF7EA")
                canvas_d.create_window((0, 0), window=content, anchor="nw")

                def on_configure(_):
                    canvas_d.configure(scrollregion=canvas_d.bbox("all"))

                content.bind("<Configure>", on_configure)

                # ---------- Título ----------
                tk.Label(
                    content,
                    text=f"Insumo: {nombre_actual}",
                    bg="#FDF7EA",
                    fg="#333333",
                    font=("Segoe UI", 12, "bold"),
                ).pack(pady=(5, 5))

                ttk.Separator(content).pack(fill="x", pady=(0, 10))

                # ---------- Campos ----------
                tk.Label(
                    content, text="Categoría:", bg="#FDF7EA",
                    fg="#333333", font=("Segoe UI", 10)
                ).pack(anchor="w")

                # Cargar categorías
                conexion_detalle = conectar()
                cursor_detalle = conexion_detalle.cursor()
                cursor_detalle.execute("SELECT IDCategoriaInsumos, NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria;")
                categorias_all = cursor_detalle.fetchall()

                nombres_categorias = [c[1] for c in categorias_all]
                id_por_nombre = {c[1]: c[0] for c in categorias_all}

                cmb_cat_editar = ttk.Combobox(content, state="readonly", values=nombres_categorias)
                cmb_cat_editar.pack(fill="x", padx=10, pady=2)
                cmb_cat_editar.set(cat_actual)

                tk.Label(
                    content, text="Nombre:", bg="#FDF7EA",
                    fg="#333333", font=("Segoe UI", 10)
                ).pack(anchor="w", pady=(10,0))

                entry_nombre = tk.Entry(content)
                entry_nombre.pack(fill="x", padx=10, pady=2)
                entry_nombre.insert(0, nombre_actual)

                # ---------- ACCIONES ----------
                def guardar_cambios():
                    nueva_cat = cmb_cat_editar.get().strip()
                    nuevo_nombre = entry_nombre.get().strip()

                    if not nuevo_nombre:
                        msg.showwarning("Atención", "Ingrese un nombre.")
                        return

                    id_cat = id_por_nombre.get(nueva_cat)
                    if not id_cat:
                        msg.showerror("Error", "Categoría no válida.")
                        return

                    try:
                        cursor_detalle.execute("""
                            UPDATE Insumos
                            SET IDCategoriaInsumos = ?, NombreInsumo = ?
                            WHERE IDInsumos = ?;
                        """, (id_cat, nuevo_nombre, id_ins))

                        conexion_detalle.commit()
                        msg.showinfo("Éxito", "Insumo actualizado correctamente.")

                        cargar_insumos_stock()    # refrescar catálogo
                        cargar_insumos()          # refrescar panel principal
                        detalle.destroy()

                    except Exception as e:
                        msg.showerror("Error", f"No se pudo actualizar:\n{e}")

                def eliminar_insumo_catalogo():
                    if not msg.askyesno("Confirmar", "¿Desea eliminar este insumo del catálogo completamente?"):
                        return

                    try:
                        cursor_detalle.execute("DELETE FROM ProveedoresInsumos WHERE IDInsumos = ?", (id_ins,))
                        cursor_detalle.execute("DELETE FROM Insumos WHERE IDInsumos = ?", (id_ins,))
                        conexion_detalle.commit()

                        msg.showinfo("Éxito", "Insumo eliminado del catálogo.")

                        cargar_insumos_stock()
                        cargar_insumos()
                        detalle.destroy()

                    except Exception as e:
                        msg.showerror("Error", f"No se pudo eliminar:\n{e}")

                # ---------- BOTONES ----------
                btns = tk.Frame(content, bg="#FDF7EA")
                btns.pack(pady=10)

                tk.Button(
                    btns, text="Guardar cambios",
                    bg="#CFE5C8", fg="#333333",
                    relief="flat", command=guardar_cambios
                ).pack(side="left", padx=5)

                tk.Button(
                    btns, text="Eliminar",
                    bg="#F2B6B6", fg="#333333",
                    relief="flat", command=eliminar_insumo_catalogo
                ).pack(side="left", padx=5)

                tk.Button(
                    btns, text="Cerrar",
                    bg="#E5D8B4", fg="#333333",
                    relief="flat", command=detalle.destroy
                ).pack(side="left", padx=5)

                detalle.transient(win)
                detalle.grab_set()

            # ---- ENLACE DOBLE CLIC ----
            tree_stock.bind("<Double-1>", abrir_detalle_insumo)

            win.transient(self)
            win.grab_set()

        # ============================================================
        # VENTANA "AGREGAR NUEVO INSUMO"
        # ============================================================
        def abrir_ventana_nuevo_insumo():
            ventana = tk.Toplevel(self)
            ventana.title("Agregar nuevo insumo")
            ventana.configure(bg="#F5F1E8")

            ancho_ventana = 420
            alto_ventana = 220
            ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

            ventana.update_idletasks()
            sw = ventana.winfo_screenwidth()
            sh = ventana.winfo_screenheight()
            ww = ventana.winfo_width()
            wh = ventana.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            ventana.geometry(f"{ww}x{wh}+{x}+{y}")

            main = tk.Frame(ventana, bg="#FDF7EA", bd=1, relief="solid")
            main.pack(fill="both", expand=True, padx=10, pady=10)

            row = 0
            tk.Label(
                main,
                text="Nuevo insumo",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=row, column=0, columnspan=2,
                sticky="w", padx=10, pady=(8, 5))
            row += 1

            ttk.Separator(main, orient="horizontal").grid(
                row=row, column=0, columnspan=2,
                sticky="ew", padx=10, pady=(0, 8)
            )
            row += 1

            # Categoría
            tk.Label(
                main,
                text="Categoría:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 10),
            ).grid(row=row, column=0, sticky="e", padx=10, pady=3)

            cmb_cat_nuevo = ttk.Combobox(
                main,
                state="readonly",
                values=nombres_categorias_ins,
            )
            cmb_cat_nuevo.grid(row=row, column=1, sticky="ew", padx=10, pady=3)
            row += 1

            # Nombre
            tk.Label(
                main,
                text="Nombre del insumo:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 10),
            ).grid(row=row, column=0, sticky="e", padx=10, pady=3)

            txt_nombre_nuevo = tk.Entry(main)
            txt_nombre_nuevo.grid(row=row, column=1, sticky="ew", padx=10, pady=3)
            row += 1

            # Botones
            btn_cancelar = ttk.Button(main, text="Cancelar", command=ventana.destroy)
            btn_guardar = ttk.Button(main, text="Guardar")

            btn_cancelar.grid(row=row, column=0, sticky="e", padx=10, pady=(8, 10))
            btn_guardar.grid(row=row, column=1, sticky="w", padx=10, pady=(8, 10))

            def guardar_nuevo_insumo():
                try:
                    cat_n = cmb_cat_nuevo.get().strip()
                    nombre_n = txt_nombre_nuevo.get().strip()

                    if not cat_n or not nombre_n:
                        return msg.showwarning(
                            "Atención",
                            "Seleccione una categoría e ingrese el nombre del insumo."
                        )

                    if cat_n not in id_cat_por_nombre:
                        return msg.showerror("Error", "Categoría de insumo no encontrada.")

                    id_cat = id_cat_por_nombre[cat_n]

                    # Crear insumo base con cantidades en 0
                    cursor.execute(
                        """
                        INSERT INTO Insumos
                            (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada)
                        VALUES (?, ?, 0, 0);
                        """,
                        (id_cat, nombre_n)
                    )
                    conexion.commit()

                    msg.showinfo("Éxito", "Nuevo insumo registrado correctamente.")

                    # Recargar nombres en el combo principal
                    cargar_nombres_insumo()

                    ventana.destroy()

                except Exception as e:
                    msg.showerror("Error", f"No se pudo guardar el nuevo insumo:\n{e}")

            btn_guardar.config(command=guardar_nuevo_insumo)

            ventana.transient(self)
            ventana.grab_set()

        # -------- Botón "Agregar nuevo" debajo de los otros --------
        parent_botones = btn_agregar.master
        btn_agregar_nuevo = tk.Button(
            parent_botones,
            text="Agregar nuevo",
            bg="#E5D8B4",
            fg="#333333",
            activebackground="#D9C79A",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            command=abrir_ventana_nuevo_insumo,
        )
        btn_agregar_nuevo.pack(fill="x", pady=(5, 0))

        btn_ver_stock_ins = tk.Button(
            parent_botones,
            text="Ver stock completo",
            bg="#E5D8B4",
            fg="#333333",
            activebackground="#D9C79A",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            command=abrir_ventana_stock_insumos
        )
        btn_ver_stock_ins.pack(fill="x", pady=(4, 0))

        btn_categorias_insumos = tk.Button(
            parent_botones,
            text="Categorías...",
            bg="#E5D8B4",
            fg="#333333",
            font=("Segoe UI", 9, "bold"),
            activebackground="#D9C79A",
            relief="flat",
            command=abrir_gestor_categorias_insumos
        )
        btn_categorias_insumos.pack(fill="x", pady=(5,0))

        # Asignar CRUD
        btn_agregar.config(command=agregar_insumo)
        btn_eliminar.config(command=eliminar_insumo)
        btn_editar.config(text="Guardar cambios", command=editar_insumo)
        btn_limpiar.config(command=limpiar_campos)

        # Cargar datos iniciales
        cargar_insumos()


   
        # -------------------------------------------------- TAB PRODUCCIÓN ----------------
    def _create_tab_produccion(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Producción")

        # Panel base reutilizable
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = self._create_tab_content(
            frame,
            "Registro de Producción",
            ["Tipo de Producción", "Categoría", "Nombre", "Cantidad"],
            ["IDProduccion", "Tipo", "Categoría", "Nombre", "Cantidad", "Costo Unitario"]
        )

        conexion = conectar()
        cursor = conexion.cursor()


                # ---------------- Filtros para el TreeView (Producción) ----------------
        #   - filtro_tipo_tree: None = todos, "Plato" o "Bebida"
        #   - filtro_texto_tree: texto de búsqueda por nombre
        filtro_tipo_tree = {"tipo": None}
        filtro_texto_tree = {"texto": ""}

        # Frame donde está el tree (lo devuelve _create_tab_content)
        cont_tabla = tree.master

        barra_filtros = tk.Frame(cont_tabla, bg="#FDF7EA")
        # Lo colocamos por encima del tree
        barra_filtros.pack(fill="x", padx=2, pady=(0, 3), before=tree)

        tk.Label(
            barra_filtros,
            text="Filtro:",
            bg="#FDF7EA",
            fg="#333333",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(2, 4))

        cmb_filtro_tree = ttk.Combobox(
            barra_filtros,
            state="readonly",
            values=["Todos", "Plato", "Bebida"],
            width=9,
        )
        cmb_filtro_tree.current(0)
        cmb_filtro_tree.pack(side="left", padx=(0, 8))

        tk.Label(
            barra_filtros,
            text="Buscar nombre:",
            bg="#FDF7EA",
            fg="#333333",
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(0, 4))

        entry_buscar_tree = tk.Entry(barra_filtros, width=18)
        entry_buscar_tree.pack(side="left", padx=(0, 4))
#---------------------------busqueda----------------------
        def aplicar_filtros_tree(*_):
            # Tipo
            sel_tipo = cmb_filtro_tree.get()
            if sel_tipo == "Plato":
                filtro_tipo_tree["tipo"] = "Plato"
            elif sel_tipo == "Bebida":
                filtro_tipo_tree["tipo"] = "Bebida"
            else:
                filtro_tipo_tree["tipo"] = None

            # Texto de búsqueda
            filtro_texto_tree["texto"] = entry_buscar_tree.get().strip().lower()
            cargar_produccion()

        # Cambiar el combo o presionar ENTER en la búsqueda recarga el tree
        cmb_filtro_tree.bind("<<ComboboxSelected>>", aplicar_filtros_tree)
        entry_buscar_tree.bind("<Return>", aplicar_filtros_tree)

        def limpiar_busqueda_tree():
            entry_buscar_tree.delete(0, tk.END)   # borra el texto
            filtro_texto_tree["texto"] = ""       # reinicia el filtro
            cargar_produccion()                   # recarga el Treeview

        # Usa el mismo contenedor donde están cmb_filtro_tree y entry_buscar_tree.
        # En tu código probablemente se llama algo como 'filtros_tree' o parecido.
            btn_limpiar_busqueda = tk.Button(
                aplicar_filtros_tree,          # <-- pon aquí el frame correcto
                text="Limpiar",
                bg="#E5D8B4",
                fg="#333333",
                activebackground="#D9C79A",
                relief="flat",
                font=("Segoe UI", 8, "bold"),
                command=limpiar_busqueda_tree,
            )
            btn_limpiar_busqueda.pack(side="left", padx=5)

        # ---------------- Helpers básicos ----------------
        def limpiar_valor(v):
            if v is None:
                return ""
            v = str(v)
            return v.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()

                # ---------------- Cargar categorías desde BD  ----------------
        cat_platos_nombres = []
        id_cat_plato_por_nombre = {}
        cat_bebidas_nombres = []
        id_cat_bebida_por_nombre = {}

        def recargar_categorias():
            nonlocal cat_platos_nombres, id_cat_plato_por_nombre
            nonlocal cat_bebidas_nombres, id_cat_bebida_por_nombre

            # Platos
            cursor.execute("""
                SELECT IDCategoriaPlatos, NombreCategoria
                FROM CategoriaPlatos
                ORDER BY NombreCategoria;
            """)
            filas_platos = cursor.fetchall()
            cat_platos_nombres = [c[1] for c in filas_platos]
            id_cat_plato_por_nombre = {c[1]: c[0] for c in filas_platos}

            # Bebidas
            cursor.execute("""
                SELECT IDCategoriaBebidas, NombreCategoria
                FROM CategoriaBebidas
                ORDER BY NombreCategoria;
            """)
            filas_bebidas = cursor.fetchall()
            cat_bebidas_nombres = [c[1] for c in filas_bebidas]
            id_cat_bebida_por_nombre = {c[1]: c[0] for c in filas_bebidas}

        # Cargar categorías al iniciar
        recargar_categorias()


        # ---------------- Reemplazar entries por combobox ----------------
                # ------------------------------------------------------------------
        # Reemplazar un Entry del formulario por un Combobox
        # (manteniendo su posición en el layout)
        # ------------------------------------------------------------------
        def _reemplazar_por_combobox(clave, values=()):
            old = entries[clave]
            parent = old.master
            manager = old.winfo_manager()

            if manager == "grid":
                info = old.grid_info()
                cmb = ttk.Combobox(parent, state="readonly", values=values)

                # destruir el viejo *después* de grid del nuevo, para evitar parpadeos
                old.destroy()

                cmb.grid(
                    row=info.get("row", 0),
                    column=info.get("column", 1),
                    columnspan=info.get("columnspan", 1),
                    sticky=info.get("sticky", "ew"),
                    padx=info.get("padx", 5),
                    pady=info.get("pady", 2),
                )
            else:  # pack (lo que usas en el panel de la izquierda)
                info = old.pack_info()
                cmb = ttk.Combobox(parent, state="readonly", values=values)

                # lo colocamos exactamente donde estaba el Entry
                pack_kwargs = {
                    "side": info.get("side", "top"),
                    "fill": info.get("fill", "x"),
                    "expand": info.get("expand", False),
                    "padx": info.get("padx", 5),
                    "pady": info.get("pady", 2),
                }
                cmb.pack(before=old, **pack_kwargs)

                old.destroy()

            entries[clave] = cmb
            return cmb
        


                # ------------------------------------------------------------------
        # Campos del formulario que deben ser Combobox
        # ------------------------------------------------------------------
        cmb_tipo = _reemplazar_por_combobox(
            "Tipo de Producción",
            ["Plato", "Bebida"]
        )

        cmb_categoria = _reemplazar_por_combobox(
            "Categoría",
            []  # se llenará según el tipo
        )

        cmb_nombre = _reemplazar_por_combobox(
            "Nombre",
            []  # se llenará según tipo + categoría o según tu lógica
        )

        # ---------------- Funciones de combos ----------------
                # ---------------- Funciones de combos ----------------
        def cargar_nombres(*_):
            """Rellena el combo de nombres según el tipo y la categoría."""
            tipo = cmb_tipo.get().strip()
            categoria = cmb_categoria.get().strip()

            # Si es PLATO
            if tipo == "Plato":
                if categoria:
                    # Filtrar por categoría (MenuDePlatos)
                    id_cat = id_cat_plato_por_nombre.get(categoria)
                    if id_cat is None:
                        cmb_nombre["values"] = ()
                        cmb_nombre.set("")
                        return
                    cursor.execute("""
                        SELECT DISTINCT P.NombrePlato
                        FROM Produccion P
                        INNER JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
                        WHERE P.NombrePlato IS NOT NULL
                          AND MP.IDCategoriaPlatos = ?
                        ORDER BY P.NombrePlato;
                    """, (id_cat,))
                else:
                    # Sin categoría seleccionada → todos los platos
                    cursor.execute("""
                        SELECT DISTINCT NombrePlato
                        FROM Produccion
                        WHERE NombrePlato IS NOT NULL
                        ORDER BY NombrePlato;
                    """)

            # Si es BEBIDA
            elif tipo == "Bebida":
                if categoria:
                    id_cat = id_cat_bebida_por_nombre.get(categoria)
                    if id_cat is None:
                        cmb_nombre["values"] = ()
                        cmb_nombre.set("")
                        return
                    cursor.execute("""
                        SELECT DISTINCT P.NombreBebida
                        FROM Produccion P
                        INNER JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
                        WHERE P.NombreBebida IS NOT NULL
                          AND MB.IDCategoriaBebidas = ?
                        ORDER BY P.NombreBebida;
                    """, (id_cat,))
                else:
                    cursor.execute("""
                        SELECT DISTINCT NombreBebida
                        FROM Produccion
                        WHERE NombreBebida IS NOT NULL
                        ORDER BY NombreBebida;
                    """)
            else:
                cmb_nombre["values"] = ()
                cmb_nombre.set("")
                return

            nombres = [r[0] for r in cursor.fetchall()]
            cmb_nombre["values"] = nombres
            if nombres:
                cmb_nombre.set(nombres[0])
            else:
                cmb_nombre.set("")

        def actualizar_categorias(*_):
            """Rellena el combo de categorías según el tipo, y limpia nombres."""
            tipo = cmb_tipo.get().strip()
            if tipo == "Plato":
                cmb_categoria["values"] = cat_platos_nombres
            elif tipo == "Bebida":
                cmb_categoria["values"] = cat_bebidas_nombres
            else:
                cmb_categoria["values"] = ()

            cmb_categoria.set("")
            cmb_nombre["values"] = ()
            cmb_nombre.set("")

                # Cuando cambie el tipo, actualizamos categorías (y luego nombres)
        cmb_tipo.bind("<<ComboboxSelected>>", actualizar_categorias)

        # Cuando cambie la categoría, filtramos los nombres
        cmb_categoria.bind("<<ComboboxSelected>>", cargar_nombres)

        # Valor inicial
        cmb_tipo.set("Plato")
        actualizar_categorias()

        # ---------------- Cargar producción en el TreeView ----------------
                # ---------------- Cargar producción en el TreeView ----------------
        def cargar_produccion():
            # Limpiar tree
            for fila in tree.get_children():
                tree.delete(fila)

            # Valores de filtro actuales
            tipo_filtro = filtro_tipo_tree["tipo"]          # None, "Plato", "Bebida"
            texto_busqueda = filtro_texto_tree["texto"]     # string en minúsculas

            cursor.execute("""
                SELECT 
                    P.IDProduccion,
                    CASE 
                        WHEN P.NombrePlato IS NOT NULL THEN 'Plato'
                        ELSE 'Bebida'
                    END AS Tipo,
                    COALESCE(CP.NombreCategoria, CB.NombreCategoria, '—') AS Categoria,
                    COALESCE(P.NombrePlato, P.NombreBebida, '—') AS Nombre,
                    CASE 
                        WHEN P.NombrePlato IS NOT NULL THEN ISNULL(P.CantidadDePlatos,0)
                        ELSE ISNULL(P.CantidadDeBebidas,0)
                    END AS Cantidad,
                    CASE
                        WHEN P.NombrePlato IS NOT NULL THEN ISNULL(P.CostoPorPlato,0)
                        ELSE ISNULL(P.CostoPorBebida,0)
                    END AS CostoUnitario,
                    RIGHT('0' + CAST(ISNULL(P.Dia, DAY(GETDATE())) AS VARCHAR(2)), 2) + '/' +
                    RIGHT('0' + CAST(ISNULL(P.Mes, MONTH(GETDATE())) AS VARCHAR(2)), 2) + '/' +
                    CAST(ISNULL(P.Ano, YEAR(GETDATE())) AS VARCHAR(4)) AS Fecha
                FROM Produccion P
                LEFT JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
                LEFT JOIN CategoriaPlatos CP ON CP.IDCategoriaPlatos = MP.IDCategoriaPlatos
                LEFT JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
                LEFT JOIN CategoriaBebidas CB ON CB.IDCategoriaBebidas = MB.IDCategoriaBebidas
                WHERE 
                    ISNULL(P.CantidadDePlatos,0) > 0
                    OR ISNULL(P.CantidadDeBebidas,0) > 0
                ORDER BY P.IDProduccion;
            """)

            for row in cursor.fetchall():
                limpio = [limpiar_valor(x) for x in row]
                tipo = limpio[1]
                nombre = str(limpio[3]).lower()

                # Filtro por tipo (Plato/Bebida)
                if tipo_filtro and tipo != tipo_filtro:
                    continue

                # Filtro por texto de búsqueda (en el nombre)
                if texto_busqueda and texto_busqueda not in nombre:
                    continue

                tree.insert("", "end", values=limpio)

            # Mantener actualizado el combo de nombres
            cargar_nombres()


# ----------------PRODUCCION
        def abrir_gestor_categorias():
            win = tk.Toplevel(self)
            win.title("Gestor de categorías")
            win.configure(bg="#F5F1E8")
            win.geometry("520x360")

            win.update_idletasks()
            sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
            ww, wh = win.winfo_width(), win.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            win.geometry(f"{ww}x{wh}+{x}+{y}")

            cont = tk.Frame(win, bg="#FDF7EA", bd=1, relief="solid")
            cont.pack(fill="both", expand=True, padx=10, pady=10)

            # ========== VARIABLES LOCALES PARA ESTA VENTANA ==========
            cat_platos_nombres_local = []
            id_cat_plato_por_nombre_local = {}
            cat_bebidas_nombres_local = []
            id_cat_bebida_por_nombre_local = {}

            # ========== FUNCIÓN PARA RECARGAR CATEGORÍAS DESDE BD ==========
            def recargar_categorias_local():
                nonlocal cat_platos_nombres_local, id_cat_plato_por_nombre_local
                nonlocal cat_bebidas_nombres_local, id_cat_bebida_por_nombre_local
                
                # Platos
                cursor.execute("""
                    SELECT IDCategoriaPlatos, NombreCategoria
                    FROM CategoriaPlatos
                    ORDER BY NombreCategoria;
                """)
                filas_platos = cursor.fetchall()
                cat_platos_nombres_local = [c[1] for c in filas_platos]
                id_cat_plato_por_nombre_local = {c[1]: c[0] for c in filas_platos}

                # Bebidas
                cursor.execute("""
                    SELECT IDCategoriaBebidas, NombreCategoria
                    FROM CategoriaBebidas
                    ORDER BY NombreCategoria;
                """)
                filas_bebidas = cursor.fetchall()
                cat_bebidas_nombres_local = [c[1] for c in filas_bebidas]
                id_cat_bebida_por_nombre_local = {c[1]: c[0] for c in filas_bebidas}
                
                # También actualizar las variables globales del contexto principal
                if hasattr(self, 'cat_platos_nombres'):
                    self.cat_platos_nombres = cat_platos_nombres_local
                if hasattr(self, 'id_cat_plato_por_nombre'):
                    self.id_cat_plato_por_nombre = id_cat_plato_por_nombre_local
                if hasattr(self, 'cat_bebidas_nombres'):
                    self.cat_bebidas_nombres = cat_bebidas_nombres_local
                if hasattr(self, 'id_cat_bebida_por_nombre'):
                    self.id_cat_bebida_por_nombre = id_cat_bebida_por_nombre_local

            # ========== INICIALIZAR CATEGORÍAS ==========
            recargar_categorias_local()

            # ---------------- Encabezado ----------------
            tk.Label(
                cont,
                text="Catálogo de categorías",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", padx=10, pady=(8, 5))

            ttk.Separator(cont, orient="horizontal").pack(
                fill="x", padx=10, pady=(0, 8)
            )

            # ---------------- Filtro: Tipo (Plato / Bebida) ----------------
            top_filtro = tk.Frame(cont, bg="#FDF7EA")
            top_filtro.pack(fill="x", padx=10, pady=(0, 5))

            tk.Label(
                top_filtro,
                text="Mostrar:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 9, "bold"),
            ).pack(side="left")

            tipo_var = tk.StringVar(value="Plato")
            rb_plato = ttk.Radiobutton(
                top_filtro, text="Platos", variable=tipo_var, value="Plato"
            )
            rb_bebida = ttk.Radiobutton(
                top_filtro, text="Bebidas", variable=tipo_var, value="Bebida"
            )
            rb_plato.pack(side="left", padx=5)
            rb_bebida.pack(side="left", padx=5)

            # ---------------- Treeview de categorías ----------------
            tabla_frame = tk.Frame(cont, bg="#FDF7EA")
            tabla_frame.pack(fill="both", expand=True, padx=10, pady=(5, 5))

            cols = ("ID", "Nombre")
            tree_cat = ttk.Treeview(
                tabla_frame, columns=cols, show="headings", height=7
            )
            tree_cat.pack(side="left", fill="both", expand=True)

            for c in cols:
                tree_cat.heading(c, text=c)
            tree_cat.column("ID", width=60, anchor="center")
            tree_cat.column("Nombre", width=260, anchor="w")

            scroll_cat = ttk.Scrollbar(
                tabla_frame, orient="vertical", command=tree_cat.yview
            )
            scroll_cat.pack(side="right", fill="y")
            tree_cat.configure(yscrollcommand=scroll_cat.set)

            # ---------------- Formulario edición ----------------
            form = tk.Frame(cont, bg="#FDF7EA")
            form.pack(fill="x", padx=10, pady=(5, 5))

            tk.Label(
                form,
                text="Nombre categoría:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 9),
            ).grid(row=0, column=0, sticky="e", padx=5, pady=3)

            ent_nombre_cat = tk.Entry(form)
            ent_nombre_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
            form.columnconfigure(1, weight=1)

            id_cat_seleccionado = {"id": None}

            # ---------------- Helpers internos ----------------
            def limpiar_form():
                id_cat_seleccionado["id"] = None
                ent_nombre_cat.delete(0, tk.END)

            def cargar_tabla_local():
                tree_cat.delete(*tree_cat.get_children())

                tipo = tipo_var.get()
                if tipo == "Plato":
                    cursor.execute("""
                        SELECT IDCategoriaPlatos, NombreCategoria
                        FROM CategoriaPlatos
                        ORDER BY NombreCategoria;
                    """)
                else:
                    cursor.execute("""
                        SELECT IDCategoriaBebidas, NombreCategoria
                        FROM CategoriaBebidas
                        ORDER BY NombreCategoria;
                    """)

                for (idc, nom) in cursor.fetchall():
                    tree_cat.insert("", "end", values=(idc, nom))

                limpiar_form()

            def on_select(event=None):
                sel = tree_cat.selection()
                if not sel:
                    return
                vals = tree_cat.item(sel)["values"]
                if not vals:
                    return
                id_cat_seleccionado["id"] = vals[0]
                ent_nombre_cat.delete(0, tk.END)
                ent_nombre_cat.insert(0, vals[1])

            tree_cat.bind("<<TreeviewSelect>>", on_select)

            # ---------------- Agregar categoría ----------------
            def agregar_categoria():
                nombre = ent_nombre_cat.get().strip()
                if not nombre:
                    return msg.showwarning("Atención", "Ingrese un nombre.")

                tipo = tipo_var.get()
                try:
                    if tipo == "Plato":
                        cursor.execute(
                            "INSERT INTO CategoriaPlatos (NombreCategoria) VALUES (?);",
                            (nombre,)
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO CategoriaBebidas (NombreCategoria) VALUES (?);",
                            (nombre,)
                        )
                    conexion.commit()
                    
                    # 🔄 ACTUALIZAR TODAS LAS VISTAS
                    recargar_categorias_local()  # Recargar categorías locales
                    cargar_tabla_local()         # Recargar tabla local
                    if hasattr(self, 'cargar_nombres'):
                        self.cargar_nombres()    # Actualizar combos en producción
                    
                    msg.showinfo("Éxito", "Categoría agregada.")
                except Exception as e:
                    msg.showerror("Error", f"No se pudo agregar:\n{e}")

            # ---------------- Guardar cambios (EDITAR) ----------------
            def guardar_categoria():
                idc = id_cat_seleccionado["id"]
                if idc is None:
                    return msg.showwarning("Atención", "Seleccione una categoría.")

                nombre = ent_nombre_cat.get().strip()
                if not nombre:
                    return msg.showwarning("Atención", "Ingrese un nombre.")

                tipo = tipo_var.get()
                try:
                    if tipo == "Plato":
                        cursor.execute("""
                            UPDATE CategoriaPlatos
                            SET NombreCategoria = ?
                            WHERE IDCategoriaPlatos = ?;
                        """, (nombre, idc))
                    else:
                        cursor.execute("""
                            UPDATE CategoriaBebidas
                            SET NombreCategoria = ?
                            WHERE IDCategoriaBebidas = ?;
                        """, (nombre, idc))

                    conexion.commit()
                    
                    # 🔄 ACTUALIZAR TODAS LAS VISTAS
                    recargar_categorias_local()  # Recargar categorías locales
                    cargar_tabla_local()         # Recargar tabla local
                    
                    # Actualizar vistas en producción
                    if hasattr(self, 'cargar_nombres'):
                        self.cargar_nombres()    # Actualizar combos de nombres
                    if hasattr(self, 'cargar_produccion'):
                        self.cargar_produccion() # Actualizar treeview
                    
                    # 🔄 ACTUALIZAR LOS MENÚS
                    self._actualizar_vistas_menu()
                    
                    msg.showinfo("Éxito", "Cambios guardados.")
                except Exception as e:
                    msg.showerror("Error", f"No se pudo actualizar:\n{e}")

            # ---------------- Eliminar categoría ----------------
            def eliminar_categoria():
                idc = id_cat_seleccionado["id"]
                if idc is None:
                    return msg.showwarning("Atención", "Seleccione una categoría.")
                
                tipo = tipo_var.get()
                
                try:
                    # Verificar productos asociados
                    if tipo == "Plato":
                        cursor.execute("""
                            SELECT COUNT(*) FROM MenuDePlatos 
                            WHERE IDCategoriaPlatos = ?;
                        """, (idc,))
                    else:  # Bebida
                        cursor.execute("""
                            SELECT COUNT(*) FROM MenuDeBebidas 
                            WHERE IDCategoriaBebidas = ?;
                        """, (idc,))
                    
                    en_uso = cursor.fetchone()[0]
                    
                    if en_uso > 0:
                        respuesta = msg.askyesno(
                            "Categoría en uso", 
                            f"Esta categoría tiene {en_uso} producto(s) asociado(s).\n"
                            f"¿Desea eliminar TODOS los productos de esta categoría también?"
                        )
                        
                        if respuesta:
                            # PRIMERO eliminar productos asociados
                            if tipo == "Plato":
                                # 1. Obtener IDs de producción
                                cursor.execute("""
                                    SELECT MP.IDProduccion 
                                    FROM MenuDePlatos MP
                                    WHERE MP.IDCategoriaPlatos = ?;
                                """, (idc,))
                                id_producciones = cursor.fetchall()
                                
                                # 2. Eliminar de MenuDePlatos
                                cursor.execute("""
                                    DELETE FROM MenuDePlatos 
                                    WHERE IDCategoriaPlatos = ?;
                                """, (idc,))
                                
                                # 3. Eliminar de Produccion
                                for (id_prod,) in id_producciones:
                                    cursor.execute("""
                                        DELETE FROM Produccion 
                                        WHERE IDProduccion = ?;
                                    """, (id_prod,))
                                    
                            else:  # Bebida
                                # 1. Obtener IDs de producción
                                cursor.execute("""
                                    SELECT MB.IDProduccion 
                                    FROM MenuDeBebidas MB
                                    WHERE MB.IDCategoriaBebidas = ?;
                                """, (idc,))
                                id_producciones = cursor.fetchall()
                                
                                # 2. Eliminar de MenuDeBebidas
                                cursor.execute("""
                                    DELETE FROM MenuDeBebidas 
                                    WHERE IDCategoriaBebidas = ?;
                                """, (idc,))
                                
                                # 3. Eliminar de Produccion
                                for (id_prod,) in id_producciones:
                                    cursor.execute("""
                                        DELETE FROM Produccion 
                                        WHERE IDProduccion = ?;
                                    """, (id_prod,))
                            
                            # AHORA eliminar la categoría
                            if tipo == "Plato":
                                cursor.execute(
                                    "DELETE FROM CategoriaPlatos WHERE IDCategoriaPlatos = ?;",
                                    (idc,)
                                )
                            else:
                                cursor.execute(
                                    "DELETE FROM CategoriaBebidas WHERE IDCategoriaBebidas = ?;",
                                    (idc,)
                                )
                            
                            conexion.commit()
                            msg.showinfo("Éxito", f"Categoría y {en_uso} producto(s) eliminados.")
                            
                            # 🔄 ACTUALIZAR TODAS LAS VISTAS
                            # ... (tu código de actualización)
                            
                            limpiar_form()
                            return
                        else:
                            msg.showinfo("Operación cancelada", "La categoría no fue eliminada.")
                            return
                    
                    # Si no hay productos, eliminar normalmente
                    if tipo == "Plato":
                        cursor.execute(
                            "DELETE FROM CategoriaPlatos WHERE IDCategoriaPlatos = ?;",
                            (idc,)
                        )
                    else:
                        cursor.execute(
                            "DELETE FROM CategoriaBebidas WHERE IDCategoriaBebidas = ?;",
                            (idc,)
                        )
                    
                    conexion.commit()
                    msg.showinfo("Éxito", "Categoría eliminada.")
                    
                    # 🔄 ACTUALIZAR TODAS LAS VISTAS
                    # ... (tu código de actualización)
                    
                    limpiar_form()
                    
                except Exception as e:
                    msg.showerror("Error", f"No se pudo eliminar:\n{e}")

            # ---------------- Botones finales ----------------
            botones = tk.Frame(cont, bg="#FDF7EA")
            botones.pack(fill="x", padx=10, pady=(5, 5))

            tk.Button(
                botones,
                text="Agregar",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=agregar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones,
                text="Guardar cambios",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=guardar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones,
                text="Eliminar",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=eliminar_categoria
            ).pack(side="left", padx=5)

            # Cambio de tipo actualiza tabla
            def on_cambiar_tipo(*_):
                cargar_tabla_local()

            tipo_var.trace_add("write", lambda *args: on_cambiar_tipo())

            cargar_tabla_local()
            win.transient(self)
            win.grab_set()

            # ---------------- Botones finales ----------------
            botones = tk.Frame(cont, bg="#FDF7EA")
            botones.pack(fill="x", padx=10, pady=(5, 5))

            tk.Button(
                botones,
                text="Agregar",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=agregar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones,
                text="Guardar cambios",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=guardar_categoria
            ).pack(side="left", padx=5)

            tk.Button(
                botones,
                text="Eliminar",
                bg="#E5D8B4",
                fg="#333333",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=eliminar_categoria
            ).pack(side="left", padx=5)

            tipo_var.trace_add("write", lambda *_: cargar_tabla())

            cargar_tabla()
            win.transient(self)
            win.grab_set()

        # ---------------- AGREGAR: registrar stock ----------------
                # ---------------- AGREGAR: registrar stock ----------------
        def agregar_produccion():
            try:
                tipo = cmb_tipo.get().strip()
                categoria = cmb_categoria.get().strip()
                nombre = cmb_nombre.get().strip()
                cant_txt = entries["Cantidad"].get().strip()

                if tipo not in ("Plato", "Bebida"):
                    return msg.showwarning("Atención", "Seleccione el tipo de producción.")
                if not categoria:
                    return msg.showwarning("Atención", "Seleccione la categoría.")
                if not nombre:
                    return msg.showwarning("Atención", "Seleccione el nombre.")
              

                try:
                    cantidad = int(cant_txt)
                except ValueError:
                    return msg.showwarning("Atención", "Cantidad y costo deben ser numéricos.")

                if cantidad <= 0:
                    return msg.showwarning("Atención", "La cantidad debe ser mayor que cero.")
              

                # Buscar producción base (creada con "Agregar nuevo")
                if tipo == "Plato":
                    cursor.execute(
                        "SELECT IDProduccion FROM Produccion WHERE NombrePlato = ?;",
                        (nombre,))
                else:
                    cursor.execute(
                        "SELECT IDProduccion FROM Produccion WHERE NombreBebida = ?;",
                        (nombre,))
                row = cursor.fetchone()
                if not row:
                    return msg.showerror(
                        "Error",
                        "No existe una producción base con ese nombre.\n"
                        "Primero use el botón 'Agregar nuevo'."
                    )

                id_prod = row[0]

                if tipo == "Plato":
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos = ISNULL(CantidadDePlatos,0) + ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, id_prod))
                else:
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas = ISNULL(CantidadDeBebidas,0) + ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, id_prod))

                conexion.commit()
                msg.showinfo("Éxito", "Producción registrada correctamente.")
                cargar_produccion()
                limpiar()

            except Exception as e:
                msg.showerror("Error", f"No se pudo registrar la producción:\n{e}")


        # ---------------- EDITAR: guardar cambios ----------------
        def editar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un registro para editar.")

                fila = tree.item(sel)["values"]
                if not fila:
                    return

                id_prod = int(limpiar_valor(fila[0]))
                tipo = fila[1]

                
                cant_txt = entries["Cantidad"].get().strip()
                cantidad = int(cant_txt)

                if cantidad < 0:
                    return msg.showwarning("Atención", "La cantidad no puede ser negativa.")
                

                if tipo == "Plato":
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos = ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad,  id_prod))
                else:
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas = ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, id_prod))

                conexion.commit()
                msg.showinfo("Éxito", "Producción actualizada correctamente.")
                cargar_produccion()
                limpiar()

            except Exception as e:
                msg.showerror("Error", f"No se pudo actualizar:\n{e}")


        # ---------------- ELIMINAR: vaciar stock ----------------
        def eliminar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un registro para eliminar.")

                fila = tree.item(sel)["values"]
                if not fila:
                    return

                id_prod = int(limpiar_valor(fila[0]))
                tipo = fila[1]

                if not msg.askyesno("Confirmar", "¿Desea eliminar el stock de esta producción?"
                                                ):
                    return

                if tipo == "Plato":
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos = 0,
                            CostoPorPlato = 0
                        WHERE IDProduccion = ?;
                    """, (id_prod,))
                else:
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas = 0,
                            CostoPorBebida = 0
                        WHERE IDProduccion = ?;
                    """, (id_prod,))

                conexion.commit()
                msg.showinfo("Éxito", "Stock eliminado correctamente.")
                cargar_produccion()
                limpiar()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")

        # ---------------- LIMPIAR CAMPOS ----------------
        def limpiar():
            for clave, w in entries.items():
                if isinstance(w, ttk.Combobox):
                    w.set("")
                else:
                    w.delete(0, tk.END)

        # ---------------- DETALLE (doble clic) con foto ----------------
        def mostrar_detalle_produccion(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            id_prod, tipo, categoria, nombre, cantidad, costo, fecha = vals

            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle de producción #{id_prod}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 540
            alto_ventana = 360
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")

            detalle.update_idletasks()
            sw = detalle.winfo_screenwidth()
            sh = detalle.winfo_screenheight()
            ww = detalle.winfo_width()
            wh = detalle.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            detalle.geometry(f"{ww}x{wh}+{x}+{y}")

            container = tk.Frame(detalle, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            card = tk.Frame(
                container,
                bg="#FDF7EA",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(fill="both", expand=True)

            # Layout: izquierda datos, derecha imagen
            datos_frame = tk.Frame(card, bg="#FDF7EA")
            datos_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

            img_frame = tk.Frame(card, bg="#FDF7EA")
            img_frame.pack(side="right", fill="both", expand=False)

            # Título
            tk.Label(
                datos_frame,
                text=f"{tipo}: {nombre}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(datos_frame, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            campos = [
                ("ID Producción", id_prod),
                ("Tipo", tipo),
                ("Categoría", categoria),
                ("Nombre", nombre),
                ("Cantidad", cantidad),
                ("Costo unitario", costo),
                ("Fecha último registro", fecha),
            ]

            for i, (lbl, valor) in enumerate(campos, start=2):
                tk.Label(
                    datos_frame,
                    text=lbl + ":",
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 10, "bold"),
                ).grid(row=i, column=0, sticky="w", padx=5, pady=3)

                tk.Label(
                    datos_frame,
                    text=str(valor),
                    bg="#FDF7EA",
                    fg="#222222",
                    font=("Segoe UI", 10),
                ).grid(row=i, column=1, sticky="w", padx=5, pady=3)

            # ----- Imagen -----
            tk.Label(
                img_frame,
                text="Imagen:",
                bg="#FDF7EA",
                fg="#6A4E23",
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w", pady=(0, 5))

            try:
                cursor.execute(
                    "SELECT Imagen FROM Produccion WHERE IDProduccion = ?;",
                    (id_prod,),
                )
                row = cursor.fetchone()
                img_bytes = row[0] if row and row[0] is not None else None
            except Exception:
                img_bytes = None

            if img_bytes:
                from io import BytesIO
                from PIL import Image, ImageTk

                imagen = Image.open(BytesIO(img_bytes))
                imagen.thumbnail((220, 220))
                photo = ImageTk.PhotoImage(imagen)

                lbl_img = tk.Label(img_frame, image=photo, bg="#FDF7EA")
                lbl_img.image = photo  # evitar GC
                lbl_img.pack(pady=5)
            else:
                tk.Label(
                    img_frame,
                    text="(Sin imagen asociada)",
                    bg="#FDF7EA",
                    fg="#777777",
                    font=("Segoe UI", 9, "italic"),
                ).pack(pady=5)

            # --------- FUNCIÓN EDITAR: RELLENA EL CRUD PRINCIPAL ----------
            def preparar_edicion():
                # Estos try/except son por si alguno de los widgets no existe
                try:
                    cmb_tipo.set(tipo)
                except Exception:
                    pass

                try:
                    cmb_categoria.set(categoria)
                except Exception:
                    pass

                try:
                    # si el nombre está en el combo, lo selecciona
                    if nombre in cmb_nombre["values"]:
                        cmb_nombre.set(nombre)
                    else:
                        cmb_nombre.set(nombre)
                except Exception:
                    pass

                # Entradas de cantidad y costo
                try:
                    if "Cantidad" in entries:
                        entries["Cantidad"].delete(0, tk.END)
                        entries["Cantidad"].insert(0, str(cantidad))
                except Exception:
                    pass

                try:
                    if "Costo Unitario" in entries:
                        entries["Costo Unitario"].delete(0, tk.END)
                        entries["Costo Unitario"].insert(0, str(costo))
                except Exception:
                    pass

                detalle.destroy()

            # --------- BOTONES (EDITAR / CERRAR) ----------
            botones = tk.Frame(detalle, bg="#F5F1E8")
            botones.pack(pady=(8, 5))

            btn_editar = ttk.Button(botones, text="Editar", command=preparar_edicion)
            btn_editar.pack(side="left", padx=5)

            btn_cerrar = ttk.Button(botones, text="Cerrar", command=detalle.destroy)
            btn_cerrar.pack(side="left", padx=5)

            detalle.transient(self)
            detalle.grab_set()

        tree.bind("<Double-1>", mostrar_detalle_produccion)

       
        # CATÁLOGO: ver  el stock (platos y bebidas) y editar base
        # ------------------------------------------------------------------
        def abrir_ventana_stock_completo():
            win = tk.Toplevel(self)
            win.title("Stock completo de producción")
            win.configure(bg="#F5F1E8")

            # Tamaño y centrado
            ancho, alto = 820, 420
            win.geometry(f"{ancho}x{alto}")
            win.update_idletasks()
            sw = win.winfo_screenwidth()
            sh = win.winfo_screenheight()
            x = (sw // 2) - (ancho // 2)
            y = (sh // 2) - (alto // 2)
            win.geometry(f"{ancho}x{alto}+{x}+{y}")

            # ---------- Marco principal ----------
            marco = tk.Frame(win, bg="#FDF7EA", bd=1, relief="solid")
            marco.pack(fill="both", expand=True, padx=10, pady=10)

            # ---------- Cabecera + filtro ----------
            top_bar = tk.Frame(marco, bg="#FDF7EA")
            top_bar.pack(fill="x", pady=(5, 5))

            tk.Label(
                top_bar,
                text="Stock completo de producción",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 11, "bold"),
            ).pack(side="left", padx=(5, 15))

            tk.Label(
                top_bar,
                text="Mostrar:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 9),
            ).pack(side="left")

            filtro_tipo = {"tipo": None}  # None = todos

            cmb_filtro = ttk.Combobox(
                top_bar,
                state="readonly",
                values=["Todos", "Plato", "Bebida"],
                width=12,
            )
            cmb_filtro.current(0)
            cmb_filtro.pack(side="left", padx=(5, 0))

            # ---------- Treeview (solo columnas base) ----------
            columns_stock = ("ID", "Tipo", "Categoría", "Nombre")

            cont_tree = tk.Frame(marco, bg="#FDF7EA")
            cont_tree.pack(fill="both", expand=True, padx=5, pady=(5, 5))

            tree_stock = ttk.Treeview(
                cont_tree,
                columns=columns_stock,
                show="headings",
                height=15,
            )

            # Encabezados
            tree_stock.heading("ID", text="ID")
            tree_stock.heading("Tipo", text="Tipo")
            tree_stock.heading("Categoría", text="Categoría")
            tree_stock.heading("Nombre", text="Nombre")

            tree_stock.column("ID", width=50, anchor="center")
            tree_stock.column("Tipo", width=80, anchor="center")
            tree_stock.column("Categoría", width=150, anchor="w")
            tree_stock.column("Nombre", width=220, anchor="w")

            vsb = ttk.Scrollbar(
                cont_tree, orient="vertical", command=tree_stock.yview
            )
            tree_stock.configure(yscrollcommand=vsb.set)

            tree_stock.pack(side="left", fill="both", expand=True)
            vsb.pack(side="right", fill="y")

            # ---------- Cargar datos en el catálogo ----------
            def cargar_stock():
                tree_stock.delete(*tree_stock.get_children())

                cursor.execute("""
                    SELECT 
                        P.IDProduccion,
                        CASE 
                            WHEN P.NombrePlato IS NOT NULL THEN 'Plato'
                            ELSE 'Bebida'
                        END AS Tipo,
                        COALESCE(CP.NombreCategoria, CB.NombreCategoria, '—') AS Categoria,
                        COALESCE(P.NombrePlato, P.NombreBebida, '—') AS Nombre
                    FROM Produccion P
                    LEFT JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
                    LEFT JOIN CategoriaPlatos CP ON CP.IDCategoriaPlatos = MP.IDCategoriaPlatos
                    LEFT JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
                    LEFT JOIN CategoriaBebidas CB ON CB.IDCategoriaBebidas = MB.IDCategoriaBebidas
                    ORDER BY P.IDProduccion;
                """)

                for row in cursor.fetchall():
                    idp, tipo, cat, nom = [limpiar_valor(x) for x in row]

                    # aplicar filtro Plato/Bebida
                    if filtro_tipo["tipo"] and tipo != filtro_tipo["tipo"]:
                        continue

                    tree_stock.insert(
                        "", "end", values=(idp, tipo, cat, nom)
                    )

            def aplicar_filtro(_=None):
                selec = cmb_filtro.get()
                if selec == "Plato":
                    filtro_tipo["tipo"] = "Plato"
                elif selec == "Bebida":
                    filtro_tipo["tipo"] = "Bebida"
                else:
                    filtro_tipo["tipo"] = None
                cargar_stock()

            cmb_filtro.bind("<<ComboboxSelected>>", aplicar_filtro)

            # Primera carga
            cargar_stock()

            # ---------- Detalle / edición desde el catálogo ----------
            def abrir_detalle_desde_stock(event=None):
                sel = tree_stock.selection()
                if not sel:
                    return

                vals = tree_stock.item(sel)["values"]
                if not vals:
                    return

                id_prod, tipo, categoria, nombre = vals

                detalle = tk.Toplevel(win)
                detalle.title(f"Producción: {tipo} - {nombre}")
                detalle.configure(bg="#F5F1E8")

                ancho_d, alto_d = 520, 420
                detalle.geometry(f"{ancho_d}x{alto_d}")
                detalle.update_idletasks()
                sw = detalle.winfo_screenwidth()
                sh = detalle.winfo_screenheight()
                x = (sw // 2) - (ancho_d // 2)
                y = (sh // 2) - (alto_d // 2)
                detalle.geometry(f"{ancho_d}x{alto_d}+{x}+{y}")

                               # ---- Contenedor con scroll ----
                card = tk.Frame(detalle, bg="#FDF7EA", bd=1, relief="solid")
                card.pack(fill="both", expand=True, padx=10, pady=10)

                canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
                canvas_d.pack(side="left", fill="both", expand=True)

                scrollbar_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
                scrollbar_d.pack(side="right", fill="y")

                canvas_d.configure(yscrollcommand=scrollbar_d.set)

                # Frame real donde van todos los widgets (título, imagen, datos, botones…)
                marco_d = tk.Frame(canvas_d, bg="#FDF7EA")
                canvas_d.create_window((0, 0), window=marco_d, anchor="nw")

                def on_configure(event):
                    canvas_d.configure(scrollregion=canvas_d.bbox("all"))

                marco_d.bind("<Configure>", on_configure)

                # ---- Título ----
                tk.Label(
                    marco_d,
                    text=f"{tipo}: {nombre}",
                    bg="#FDF7EA",
                    fg="#333333",
                    font=("Segoe UI", 12, "bold"),
                ).pack(fill="x", padx=10, pady=(5, 3))

                ttk.Separator(marco_d, orient="horizontal").pack(
                    fill="x", padx=10, pady=(0, 8)
                )

                # ---- Imagen ----
                frame_img = tk.Frame(marco_d, bg="#FDF7EA")
                frame_img.pack(pady=(0, 5))

                tk.Label(
                    frame_img,
                    text="Imagen actual.",
                    bg="#FDF7EA",
                    fg="#777777",
                    font=("Segoe UI", 9, "italic"),
                ).pack()

                lbl_img = tk.Label(frame_img, bg="#FDF7EA")
                lbl_img.pack(pady=(3, 5))

                # Cargar imagen desde BD
                imagen_actual = {"bytes": None}

                try:
                    cursor.execute(
                        "SELECT Imagen FROM Produccion WHERE IDProduccion = ?;",
                        (id_prod,),
                    )
                    row = cursor.fetchone()
                    img_bytes = row[0] if row and row[0] is not None else None
                except Exception:
                    img_bytes = None

                if img_bytes:
                    from io import BytesIO
                    from PIL import Image, ImageTk

                    imagen = Image.open(BytesIO(img_bytes))
                    imagen.thumbnail((220, 220))
                    photo = ImageTk.PhotoImage(imagen)
                    lbl_img.configure(image=photo)
                    lbl_img.image = photo
                    imagen_actual["bytes"] = img_bytes
                else:
                    lbl_img.configure(
                        text="(Sin imagen asociada)",
                        fg="#777777",
                        font=("Segoe UI", 9, "italic"),
                    )

                # ---- Datos básicos (categoría + nombre) ----
                datos_frame = tk.LabelFrame(
                    marco_d,
                    text="Datos básicos",
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 9, "bold"),
                    labelanchor="nw",
                )
                datos_frame.pack(fill="x", padx=10, pady=(5, 10))

                # Categoría
                tk.Label(
                    datos_frame,
                    text="Categoría:",
                    bg="#FDF7EA",
                    fg="#333333",
                    font=("Segoe UI", 9),
                ).grid(row=0, column=0, sticky="e", padx=5, pady=3)

                cmb_cat = ttk.Combobox(datos_frame, state="readonly")
                if tipo == "Plato":
                    cmb_cat["values"] = cat_platos_nombres
                else:
                    cmb_cat["values"] = cat_bebidas_nombres
                cmb_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
                cmb_cat.columnconfigure(1, weight=1)
                cmb_cat.set(categoria if categoria != "—" else "")

                # Nombre
                tk.Label(
                    datos_frame,
                    text="Nombre:",
                    bg="#FDF7EA",
                    fg="#333333",
                    font=("Segoe UI", 9),
                ).grid(row=1, column=0, sticky="e", padx=5, pady=3)

                entry_nombre = tk.Entry(datos_frame)
                entry_nombre.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
                entry_nombre.insert(0, nombre)

                datos_frame.columnconfigure(1, weight=1)

                #precio 
                # --- Precio venta ---
                tk.Label(datos_frame, text="Precio venta:", bg="#FDF7EA").grid(row=2, column=0, sticky="e", padx=5, pady=3)
                entry_precio = tk.Entry(datos_frame)
                entry_precio.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

                # insertar precio desde BD
                cursor.execute("""
                SELECT 
                    COALESCE(CostoPorPlato, CostoPorBebida, CostoProduccionTotal, 0)
                FROM Produccion
                WHERE IDProduccion = ?
            """, (id_prod,))

                row = cursor.fetchone()
                if row:
                    entry_precio.insert(0, str(row[0]))



                # ---- Botones inferiores ----
                frame_botones = tk.Frame(marco_d, bg="#FDF7EA")
                frame_botones.pack(pady=(5, 0))

                def cambiar_imagen():
                    from tkinter import filedialog
                    import os

                    ruta = filedialog.askopenfilename(
                        title="Seleccionar imagen",
                        filetypes=[
                            ("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                            ("Todos los archivos", "*.*"),
                        ],
                    )
                    if not ruta:
                        return
                    try:
                        with open(ruta, "rb") as f:
                            new_bytes = f.read()
                        imagen_actual["bytes"] = new_bytes

                        from PIL import Image, ImageTk
                        from io import BytesIO

                        imagen = Image.open(BytesIO(new_bytes))
                        imagen.thumbnail((220, 220))
                        photo = ImageTk.PhotoImage(imagen)
                        lbl_img.configure(image=photo, text="")
                        lbl_img.image = photo
                    except Exception as e:
                        msg.showerror("Error", f"No se pudo leer la imagen:\n{e}")

                def eliminar_produccion_definitiva():
                    if not msg.askyesno(
                        "Eliminar producción",
                        "¿Seguro que deseas eliminar este plato/bebida del catálogo?\n"
                        "Esta acción elimina la producción base y su registro en el menú,\n"
                        "pero no borra los registros históricos de producción ya realizados.",
                    ):
                        return
                    try:
                        if tipo == "Plato":
                            cursor.execute(
                                "DELETE FROM MenuDePlatos WHERE IDProduccion = ?;",
                                (id_prod,),
                            )
                        else:
                            cursor.execute(
                                "DELETE FROM MenuDeBebidas WHERE IDProduccion = ?;",
                                (id_prod,),
                            )

                        cursor.execute(
                            "DELETE FROM Produccion WHERE IDProduccion = ?;",
                            (id_prod,),
                        )

                        conexion.commit()
                        msg.showinfo(
                            "Éxito",
                            "Producción eliminada del catálogo correctamente.",
                        )

                        # refrescar todo lo que usa esta producción
                        cargar_nombres()
                        cargar_produccion()
                        cargar_stock()

                        detalle.destroy()
                    except Exception as e:
                        msg.showerror(
                            "Error",
                            f"No se pudo eliminar la producción:\n{e}",
                        )

                def guardar_datos_base():
                    nueva_cat = cmb_cat.get().strip()
                    nuevo_nombre = entry_nombre.get().strip()
                    nuevo_precio = entry_precio.get().strip()

                   
                    # --- Guardar precio según tipo ---
                    if tipo == "Plato":
                        cursor.execute("""
                            UPDATE Produccion 
                            SET CostoPorPlato = ?
                            WHERE IDProduccion = ?
                        """, (nuevo_precio, id_prod))

                        cursor.execute("""
                            UPDATE MenuDePlatos
                            SET Precio = ?
                            WHERE IDProduccion = ?
                        """, (nuevo_precio, id_prod))

                    else:  # Bebida
                        cursor.execute("""
                            UPDATE Produccion 
                            SET CostoPorBebida = ?
                            WHERE IDProduccion = ?
                        """, (nuevo_precio, id_prod))

                        cursor.execute("""
                            UPDATE MenuDeBebidas
                            SET Precio = ?
                            WHERE IDProduccion = ?
                        """, (nuevo_precio, id_prod))

                    if not nuevo_nombre:
                        return msg.showwarning(
                            "Atención", "Ingrese un nombre para la producción."
                        )

                    try:
                        if tipo == "Plato":
                            if nueva_cat not in id_cat_plato_por_nombre:
                                return msg.showerror(
                                    "Error", "Categoría de plato no encontrada."
                                )
                            id_cat = id_cat_plato_por_nombre[nueva_cat]

                            cursor.execute("""
                                UPDATE Produccion
                                SET NombrePlato = ?, Imagen = ?
                                WHERE IDProduccion = ?;
                            """, (nuevo_nombre, imagen_actual["bytes"], id_prod))

                            cursor.execute("""
                                UPDATE MenuDePlatos
                                SET NombrePlato = ?, IDCategoriaPlatos = ?
                                WHERE IDProduccion = ?;
                            """, (nuevo_nombre, id_cat, id_prod))

                        else:  # Bebida
                            if nueva_cat not in id_cat_bebida_por_nombre:
                                return msg.showerror(
                                    "Error", "Categoría de bebida no encontrada."
                                )
                            id_cat = id_cat_bebida_por_nombre[nueva_cat]

                            cursor.execute("""
                                UPDATE Produccion
                                SET NombreBebida = ?, Imagen = ?
                                WHERE IDProduccion = ?;
                            """, (nuevo_nombre, imagen_actual["bytes"], id_prod))

                            cursor.execute("""
                                UPDATE MenuDeBebidas
                                SET NombreBebida = ?, IDCategoriaBebidas = ?
                                WHERE IDProduccion = ?;
                            """, (nuevo_nombre, id_cat, id_prod))

                        conexion.commit()
                        msg.showinfo("Éxito", "Datos base actualizados correctamente.")

                        # refrescar vistas/combos
                        cargar_nombres()
                        cargar_produccion()
                        cargar_stock()

                        detalle.destroy()
                    except Exception as e:
                        msg.showerror(
                            "Error",
                            f"No se pudieron guardar los cambios:\n{e}",
                        )

                btn_cambiar_img = tk.Button(
                    frame_botones,
                    text="Cambiar imagen",
                    bg="#E5D8B4",
                    fg="#333333",
                    activebackground="#D9C79A",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    command=cambiar_imagen,
                )
                btn_cambiar_img.grid(row=0, column=0, padx=5, pady=5)

                # 👉 AHORA este botón ELIMINA la producción
                btn_eliminar = tk.Button(
                    frame_botones,
                    text="Eliminar producción",
                    bg="#F2B6B6",
                    fg="#333333",
                    activebackground="#E59A9A",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    command=eliminar_produccion_definitiva,
                )
                btn_eliminar.grid(row=0, column=1, padx=5, pady=5)

                btn_guardar = tk.Button(
                    frame_botones,
                    text="Guardar datos",
                    bg="#CFE5C8",
                    fg="#333333",
                    activebackground="#B5D7AA",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    command=guardar_datos_base,
                )
                btn_guardar.grid(row=0, column=2, padx=5, pady=5)

                btn_cerrar = tk.Button(
                    frame_botones,
                    text="Cerrar",
                    bg="#E5D8B4",
                    fg="#333333",
                    activebackground="#D9C79A",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    command=detalle.destroy,
                )
                btn_cerrar.grid(row=0, column=3, padx=5, pady=5)

                detalle.transient(win)
                detalle.grab_set()

            tree_stock.bind("<Double-1>", abrir_detalle_desde_stock)

            win.transient(self)
            win.grab_set()



        # ----------------------------------------------------------------------------- VENTANA "AGREGAR NUEVO" ----------------
        def abrir_ventana_nueva_produccion():
            ventana = tk.Toplevel(self)
            ventana.title("Agregar nueva producción")
            ventana.configure(bg="#F5F1E8")

            ancho_ventana = 520
            alto_ventana = 320
            ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

            ventana.update_idletasks()
            sw = ventana.winfo_screenwidth()
            sh = ventana.winfo_screenheight()
            ww = ventana.winfo_width()
            wh = ventana.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            ventana.geometry(f"{ww}x{wh}+{x}+{y}")

                        # =============================
            # CONTENEDOR SCROLLABLE
            # =============================
            container = tk.Frame(ventana, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            canvas = tk.Canvas(container, bg="#FDF7EA", highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scrollbar.set)

            # Frame real donde van los widgets
            main = tk.Frame(canvas, bg="#FDF7EA")
            canvas.create_window((0, 0), window=main, anchor="nw")

            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            main.bind("<Configure>", on_configure)


            row = 0
            tk.Label(main, text="Nueva producción", bg="#FDF7EA",
                     fg="#333333", font=("Segoe UI", 12, "bold")
                     ).grid(row=row, column=0, columnspan=3,
                            sticky="w", padx=10, pady=(8, 5))
            row += 1
            ttk.Separator(main, orient="horizontal").grid(
                row=row, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 8)
            )
            row += 1

            # Tipo
            tk.Label(main, text="Tipo de Producción:", bg="#FDF7EA",
                     fg="#333333", font=("Segoe UI", 10)
                     ).grid(row=row, column=0, sticky="e", padx=10, pady=3)
            cmb_tipo_nuevo = ttk.Combobox(main, state="readonly",
                                          values=["Plato", "Bebida"])
            cmb_tipo_nuevo.grid(row=row, column=1, columnspan=2,
                                sticky="ew", padx=10, pady=3)
            row += 1

            # Categoría
            tk.Label(main, text="Categoría:", bg="#FDF7EA",
                     fg="#333333", font=("Segoe UI", 10)
                     ).grid(row=row, column=0, sticky="e", padx=10, pady=3)
            cmb_categoria_nuevo = ttk.Combobox(main, state="readonly")
            cmb_categoria_nuevo.grid(row=row, column=1, columnspan=2,
                                     sticky="ew", padx=10, pady=3)
            row += 1

            # Nombre
            tk.Label(main, text="Nombre:", bg="#FDF7EA",
                     fg="#333333", font=("Segoe UI", 10)
                     ).grid(row=row, column=0, sticky="e", padx=10, pady=3)
            txt_nombre_nuevo = tk.Entry(main)
            txt_nombre_nuevo.grid(row=row, column=1, columnspan=2,
                                  sticky="ew", padx=10, pady=3)
            row += 1

            # --- Precio (tomado del Costo Unitario) ---
            tk.Label(main, text="Precio venta:", bg="#FDF7EA",
                        fg="#333333", font=("Segoe UI", 10)
                        ).grid(row=row, column=0, sticky="e", padx=10, pady=3)

            entry_precio = tk.Entry(main)
            entry_precio.grid(row=row, column=1, columnspan=2,
                            sticky="ew", padx=10, pady=3)

            row += 1



            # Imagen
             # =============================
# IMAGEN (con vista previa)
# =============================
            tk.Label(
                main,
                text="Imagen:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 10)
            ).grid(row=row, column=0, sticky="e", padx=10, pady=3)

            frame_imagen = tk.Frame(main, bg="#FDF7EA")
            frame_imagen.grid(row=row, column=1, columnspan=2, sticky="w", padx=10)

            # Aquí se guardará la imagen en bytes
            imagen_bytes = {"data": None}

            # Texto debajo
            lbl_imagen_estado = tk.Label(
                frame_imagen,
                text="(Sin imagen seleccionada)",
                bg="#FDF7EA",
                fg="#777777",
                font=("Segoe UI", 9, "italic")
            )
            lbl_imagen_estado.pack(anchor="w", pady=(0, 5))

            # Vista previa (vacía al inicio)
            lbl_preview = tk.Label(frame_imagen, bg="#FDF7EA")
            lbl_preview.pack(anchor="w", pady=(0, 5))

            # ------ FUNCIONES ------
            from PIL import Image, ImageTk
            from io import BytesIO

            def mostrar_preview(img_bytes):
                """Muestra la imagen en lbl_preview."""
                if not img_bytes:
                    lbl_preview.config(image="", text="(Sin vista previa)")
                    lbl_preview.image = None
                    return

                img = Image.open(BytesIO(img_bytes))
                img.thumbnail((180, 180))
                photo = ImageTk.PhotoImage(img)

                lbl_preview.config(image=photo, text="")
                lbl_preview.image = photo  # evitar garbage collector

            def seleccionar_imagen():
                from tkinter import filedialog

                ruta = filedialog.askopenfilename(
                    title="Seleccionar imagen",
                    filetypes=[
                        ("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                        ("Todos los archivos", "*.*"),
                    ],
                )
                if not ruta:
                    return

                try:
                    with open(ruta, "rb") as f:
                        datos = f.read()
                    imagen_bytes["data"] = datos

                    lbl_imagen_estado.config(
                        text=ruta.split("/")[-1], fg="#333333", font=("Segoe UI", 9)
                    )

                    mostrar_preview(datos)

                except Exception as e:
                    msg.showerror("Error", f"No se pudo leer la imagen:\n{e}")

            # ------ BOTONES: Seleccionar / Cambiar imagen ------
            btn_sel_img = tk.Button(
                frame_imagen,
                text="Seleccionar imagen...",
                bg="#E5D8B4",
                fg="#333333",
                activebackground="#D9C79A",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=seleccionar_imagen
            )
            btn_sel_img.pack(side="left", padx=(0, 10))

            btn_cambiar_img = tk.Button(
                frame_imagen,
                text="Cambiar imagen",
                bg="#E5D8B4",
                fg="#333333",
                activebackground="#D9C79A",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=seleccionar_imagen
            )
            btn_cambiar_img.pack(side="left")

            row += 2

            def actualizar_categorias_nuevo(*_):
                tipo_n = cmb_tipo_nuevo.get()
                if tipo_n == "Plato":
                    cmb_categoria_nuevo["values"] = cat_platos_nombres
                elif tipo_n == "Bebida":
                    cmb_categoria_nuevo["values"] = cat_bebidas_nombres
                else:
                    cmb_categoria_nuevo["values"] = ()
                cmb_categoria_nuevo.set("")

            cmb_tipo_nuevo.bind("<<ComboboxSelected>>", actualizar_categorias_nuevo)
            cmb_tipo_nuevo.set("Plato")
            actualizar_categorias_nuevo()

            # Botones guardar / cancelar
            btn_cancelar = ttk.Button(main, text="Cancelar", command=ventana.destroy)
            btn_guardar = ttk.Button(main, text="Guardar")
           
            # fila de botones: [Ver stock] [Cancelar] [Guardar]
           
            btn_cancelar.grid(row=row, column=1, sticky="e", padx=10, pady=(8, 10))
            btn_guardar.grid(row=row, column=2, sticky="w", padx=10, pady=(8, 10))


            def guardar_nueva_produccion():
                try:
                    tipo_n = cmb_tipo_nuevo.get().strip()
                    categoria_n = cmb_categoria_nuevo.get().strip()
                    nombre_n = txt_nombre_nuevo.get().strip()
                    precio = entry_precio.get()
                    img_data = imagen_bytes["data"]
         

                    if tipo_n not in ("Plato", "Bebida"):
                        return msg.showwarning("Atención", "Seleccione el tipo de producción.")
                    if not categoria_n:
                        return msg.showwarning("Atención", "Seleccione la categoría.")
                    if not nombre_n:
                        return msg.showwarning("Atención", "Ingrese el nombre de la producción.")

                    if img_data is None:
                        if not msg.askyesno(
                            "Sin imagen",
                            "No ha seleccionado ninguna imagen.\n"
                            "¿Desea guardar la producción sin imagen?"
                        ):
                            return

                    if tipo_n == "Plato":
                        if categoria_n not in id_cat_plato_por_nombre:
                            return msg.showerror("Error", "Categoría de plato no encontrada.")
                        id_cat = id_cat_plato_por_nombre[categoria_n]

                        cursor.execute("""
                            INSERT INTO Produccion
                                (NombrePlato, CantidadDePlatos, CostoPorPlato,
                                 CantidadDeBebidas, CostoPorBebida, CostoProduccionTotal, Imagen)
                            OUTPUT INSERTED.IDProduccion
                            VALUES (?, 0, 0, 0, NULL, 0, ?);
                        """, (nombre_n, img_data))
                        id_prod_nuevo = cursor.fetchone()[0]

                        cursor.execute("""
                            INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio)
                            VALUES (?, ?, ?, 0);
                        """, (id_prod_nuevo, id_cat, nombre_n))

                    else:  # Bebida
                        if categoria_n not in id_cat_bebida_por_nombre:
                            return msg.showerror("Error", "Categoría de bebida no encontrada.")
                        id_cat = id_cat_bebida_por_nombre[categoria_n]

                        cursor.execute("""
                            INSERT INTO Produccion
                                (NombreBebida, CantidadDeBebidas, CostoPorBebida,
                                 CantidadDePlatos, CostoPorPlato, CostoProduccionTotal, Imagen)
                            OUTPUT INSERTED.IDProduccion
                            VALUES (?, 0, 0, 0, NULL, 0, ?);
                        """, (nombre_n, img_data))
                        id_prod_nuevo = cursor.fetchone()[0]

                        cursor.execute("""
                            INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio)
                            VALUES (?, ?, ?, 0);
                        """, (id_prod_nuevo, id_cat, nombre_n))

                    conexion.commit()
                    msg.showinfo("Éxito", "Nueva producción registrada correctamente.")

                    # Solo actualizamos el combo de nombres;
                    # NO recargamos el TreeView para que no aparezca sin stock.
                    cargar_nombres()
                    ventana.destroy()

                except Exception as e:
                    msg.showerror("Error", f"No se pudo guardar la nueva producción:\n{e}")

            btn_guardar.config(command=guardar_nueva_produccion)

            ventana.transient(self)
            ventana.grab_set() 

           
        
        # ---------------- Botón "Agregar nuevo" debajo de los otros ----------------
        parent_botones = btn_agregar.master
        btn_agregar_nuevo = tk.Button(
            parent_botones,
            text="Agregar nuevo",
            bg="#E5D8B4",
            fg="#333333",
            activebackground="#D9C79A",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            command=abrir_ventana_nueva_produccion,
        )
        btn_agregar_nuevo.pack(fill="x", pady=(5, 0))


        btn_ver_stock = tk.Button(
            parent_botones,
            text="Ver stock completo",
            bg="#E5D8B4",
            fg="#333333",
            activebackground="#D9C79A",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            command=abrir_ventana_stock_completo,   # usa la función que ya tienes
        )
        btn_ver_stock.pack(fill="x", pady=(3, 0))

         # 🔹 Nuevo botón: gestor de categorías
        btn_categorias = tk.Button(
            parent_botones,
            text="Categorías...",
            bg="#E5D8B4",
            fg="#333333",
            activebackground="#D9C79A",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            command=abrir_gestor_categorias  # ✔ ESTE ES EL CORRECTO

        )
        btn_categorias.pack(fill="x", pady=(5, 0))

        # ---------------- Asignar comandos CRUD ----------------
        btn_agregar.config(command=agregar_produccion)
        btn_editar.config(text="Guardar cambios", command=editar_produccion)     
        btn_eliminar.config(command=eliminar_produccion)
        btn_limpiar.config(command=limpiar)

        # Cargar datos iniciales
        cargar_produccion()


    #----------------------------------------------------------------------------------TAB MENU DE PLATOS

    def _create_tab_menu_platos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Menú de Platos")

        # Sección vacía hasta proximamente salga inspo
        tk.Label(
            frame,
            text="Sección Menú de Platos (vacía por ahora)",
            font=("Segoe UI", 12, "bold"),
            bg="#F5F1E8"
        ).pack(pady=20)

# ----------------------------------------------------------------------TAB MENU DE BEBIDAS
    def _create_tab_menu_bebidas(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Menú de Bebidas")

        # Sección vacía hasta proximamente salga inspo
        tk.Label(
            frame,
            text="Sección Menú de Bebidas (vacía por ahora)",
            font=("Segoe UI", 12, "bold"),
            bg="#F5F1E8"
        ).pack(pady=20)


        # -------------------------------------  TAB CLIENTES ----------------
    def _create_tab_clientes(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Clientes")

        # --- Crear contenido del tab (entradas, tabla y botones)
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = (
            self._create_tab_content(
                frame,
                "Gestión de Clientes",
                [
                    "Número de Mesa",
                    "Nombre1",
                    "Nombre2",
                    "Apellido1",
                    "Apellido2",
                    "Teléfono",
                ],
                [
                    "IDCliente",
                    "Número de Mesa",
                    "Nombre1",
                    "Nombre2",
                    "Apellido1",
                    "Apellido2",
                    "Teléfono",
                ],
            )
        )

        # ---------- Conexión a la base de datos ----------
        conexion = conectar()
        cursor = conexion.cursor()

        # -------------------------------------------------
        # CARGAR CLIENTES EN EL TREEVIEW
        # -------------------------------------------------
        def cargar_clientes():
            """Carga los clientes desde SQL Server en la tabla."""
            for fila in tree.get_children():
                tree.delete(fila)

            cursor.execute(
                """
                SELECT c.IDClientes, c.NumeroDeMesa, c.Nombre1, c.Nombre2, 
                       c.Apellido1, c.Apellido2, t.Telefono
                FROM Clientes c
                INNER JOIN TelefonoCliente t ON c.IDTelefonoClientes = t.IDTelefonoClientes
                ORDER BY c.IDClientes
            """
            )
            for row in cursor.fetchall():
                valores = [("—" if x is None else str(x).strip()) for x in row]
                tree.insert("", "end", values=valores)

        # -------------------------------------------------
        # AGREGAR CLIENTE
        # -------------------------------------------------
        def agregar_cliente():
            """Agrega un nuevo cliente con su teléfono."""
            try:
                mesa = entries["Número de Mesa"].get().strip()
                nombre1 = entries["Nombre1"].get().strip()
                nombre2 = entries["Nombre2"].get().strip() or None
                apellido1 = entries["Apellido1"].get().strip()
                apellido2 = entries["Apellido2"].get().strip() or None
                telefono = entries["Teléfono"].get().strip()

                # --- Validaciones básicas ---
                if not mesa.isdigit():
                    msg.showwarning(
                        "Atención", "El número de mesa debe ser un número entero."
                    )
                    return
                if not nombre1 or not apellido1:
                    msg.showwarning(
                        "Atención",
                        "Debe ingresar al menos el primer nombre y primer apellido.",
                    )
                    return
                if not telefono:
                    msg.showwarning("Atención", "Debe ingresar un número de teléfono.")
                    return

                # --- Insertar teléfono y obtener su ID ---
                cursor.execute(
                    """
                    INSERT INTO TelefonoCliente (Telefono)
                    OUTPUT INSERTED.IDTelefonoClientes
                    VALUES (?);
                """,
                    (telefono,),
                )
                id_tel_row = cursor.fetchone()
                conexion.commit()

                if not id_tel_row or id_tel_row[0] is None:
                    msg.showerror(
                        "Error", "No se pudo obtener el ID del teléfono insertado."
                    )
                    return

                id_tel = int(id_tel_row[0])

                # --- Insertar cliente ---
                cursor.execute(
                    """
                    INSERT INTO Clientes (NumeroDeMesa, IDTelefonoClientes, Nombre1, Nombre2, Apellido1, Apellido2)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (int(mesa), id_tel, nombre1, nombre2, apellido1, apellido2),
                )
                conexion.commit()

                msg.showinfo("Éxito", "Cliente agregado correctamente.")
                cargar_clientes()
                limpiar_campos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar el cliente:\n{e}")

        # -------------------------------------------------
        # ELIMINAR CLIENTE
        # -------------------------------------------------
        def eliminar_cliente():
            """Elimina el cliente seleccionado en la tabla (y su teléfono asociado)."""
            try:
                seleccionado = tree.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Selecciona un cliente para eliminar.")
                    return

                vals = tree.item(seleccionado)["values"]
                if not vals:
                    return

                id_cliente = int(vals[0])

                # Obtener IDTelefonoClientes para borrar también el teléfono
                cursor.execute(
                    "SELECT IDTelefonoClientes FROM Clientes WHERE IDClientes = ?",
                    (id_cliente,),
                )
                row_tel = cursor.fetchone()
                id_tel = row_tel[0] if row_tel else None

                cursor.execute("DELETE FROM Clientes WHERE IDClientes = ?", (id_cliente,))
                if id_tel is not None:
                    cursor.execute(
                        "DELETE FROM TelefonoCliente WHERE IDTelefonoClientes = ?",
                        (id_tel,),
                    )
                conexion.commit()

                msg.showinfo("Éxito", "Cliente eliminado correctamente.")
                cargar_clientes()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar el cliente:\n{e}")

        # -------------------------------------------------
        # EDITAR CLIENTE (GUARDAR CAMBIOS)
        # -------------------------------------------------
        def editar_cliente():
            """Guarda cambios del cliente seleccionado, usando el formulario."""
            try:
                seleccionado = tree.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Selecciona un cliente para editar.")
                    return

                vals = tree.item(seleccionado)["values"]
                if not vals:
                    return

                id_cliente = int(vals[0])

                mesa = entries["Número de Mesa"].get().strip()
                nombre1 = entries["Nombre1"].get().strip()
                nombre2 = entries["Nombre2"].get().strip() or None
                apellido1 = entries["Apellido1"].get().strip()
                apellido2 = entries["Apellido2"].get().strip() or None
                telefono = entries["Teléfono"].get().strip()

                if not mesa.isdigit():
                    msg.showwarning(
                        "Atención", "El número de mesa debe ser un número entero."
                    )
                    return
                if not nombre1 or not apellido1:
                    msg.showwarning(
                        "Atención",
                        "Debe ingresar al menos el primer nombre y primer apellido.",
                    )
                    return
                if not telefono:
                    msg.showwarning("Atención", "Debe ingresar un número de teléfono.")
                    return

                # Actualizar teléfono vinculado
                cursor.execute(
                    """
                    UPDATE t
                    SET t.Telefono = ?
                    FROM TelefonoCliente t
                    INNER JOIN Clientes c ON c.IDTelefonoClientes = t.IDTelefonoClientes
                    WHERE c.IDClientes = ?
                """,
                    (telefono, id_cliente),
                )

                # Actualizar datos del cliente
                cursor.execute(
                    """
                    UPDATE Clientes
                    SET NumeroDeMesa = ?, Nombre1 = ?, Nombre2 = ?, Apellido1 = ?, Apellido2 = ?
                    WHERE IDClientes = ?
                """,
                    (int(mesa), nombre1, nombre2, apellido1, apellido2, id_cliente),
                )
                conexion.commit()

                msg.showinfo("Éxito", "Cliente actualizado correctamente.")
                cargar_clientes()
                limpiar_campos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar el cliente:\n{e}")

        # -------------------------------------------------
        # LIMPIAR CAMPOS
        # -------------------------------------------------
        def limpiar_campos():
            """Limpia todos los campos de entrada."""
            for e in entries.values():
                e.delete(0, tk.END)

        # -------------------------------------------------
        # DETALLE AL HACER DOBLE CLIC
        # -------------------------------------------------
        def mostrar_detalle_cliente(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            id_cliente, mesa, n1, n2, a1, a2, tel = vals

            def safe(v):
                return "—" if v in (None, "", "—") else v

            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle del cliente #{safe(id_cliente)}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 480
            alto_ventana = 320
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")
            detalle.minsize(440, 280)

            detalle.update_idletasks()
            sw = detalle.winfo_screenwidth()
            sh = detalle.winfo_screenheight()
            ww = detalle.winfo_width()
            wh = detalle.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            detalle.geometry(f"{ww}x{wh}+{x}+{y}")

            container = tk.Frame(detalle, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            card = tk.Frame(
                container,
                bg="#FDF7EA",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(fill="both", expand=True)

            canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
            canvas_d.pack(side="left", fill="both", expand=True)

            scrollbar_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
            scrollbar_d.pack(side="right", fill="y")

            canvas_d.configure(yscrollcommand=scrollbar_d.set)

            content = tk.Frame(canvas_d, bg="#FDF7EA")
            canvas_d.create_window((0, 0), window=content, anchor="nw")

            def on_configure(event):
                canvas_d.configure(scrollregion=canvas_d.bbox("all"))

            content.bind("<Configure>", on_configure)

            tk.Label(
                content,
                text=f"Cliente: {safe(n1)} {safe(a1)}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(content, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            datos = [
                ("ID Cliente", safe(id_cliente)),
                ("Número de Mesa", safe(mesa)),
                ("Nombre1", safe(n1)),
                ("Nombre2", safe(n2)),
                ("Apellido1", safe(a1)),
                ("Apellido2", safe(a2)),
                ("Teléfono", safe(tel)),
            ]

            for i, (label_txt, valor) in enumerate(datos, start=2):
                tk.Label(
                    content,
                    text=label_txt + ":",
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 10, "bold"),
                ).grid(row=i, column=0, sticky="w", padx=10, pady=3)

                tk.Label(
                    content,
                    text=str(valor),
                    bg="#FDF7EA",
                    fg="#222222",
                    font=("Segoe UI", 10),
                ).grid(row=i, column=1, sticky="w", padx=5, pady=3)

            last_row = len(datos) + 2

            ttk.Separator(content, orient="horizontal").grid(
                row=last_row, column=0, columnspan=2, sticky="ew", padx=5, pady=(8, 5)
            )

            # ----- botón EDITAR (rellena formulario de la izquierda) -----
            def preparar_edicion():
                entries["Número de Mesa"].delete(0, tk.END)
                entries["Número de Mesa"].insert(
                    0, "" if safe(mesa) == "—" else mesa
                )

                entries["Nombre1"].delete(0, tk.END)
                entries["Nombre1"].insert(0, "" if safe(n1) == "—" else n1)

                entries["Nombre2"].delete(0, tk.END)
                entries["Nombre2"].insert(0, "" if safe(n2) == "—" else n2)

                entries["Apellido1"].delete(0, tk.END)
                entries["Apellido1"].insert(0, "" if safe(a1) == "—" else a1)

                entries["Apellido2"].delete(0, tk.END)
                entries["Apellido2"].insert(0, "" if safe(a2) == "—" else a2)

                entries["Teléfono"].delete(0, tk.END)
                entries["Teléfono"].insert(0, "" if safe(tel) == "—" else tel)

                detalle.destroy()

            btn_editar_detalle = ttk.Button(
                content, text="Editar este cliente", command=preparar_edicion
            )
            btn_editar_detalle.grid(
                row=last_row + 1, column=0, padx=10, pady=(5, 10), sticky="w"
            )

            btn_cerrar = ttk.Button(content, text="Cerrar", command=detalle.destroy)
            btn_cerrar.grid(
                row=last_row + 1, column=1, padx=10, pady=(5, 10), sticky="e"
            )

            detalle.transient(self)
            detalle.grab_set()

        # doble clic → abrir detalle
        tree.bind("<Double-1>", mostrar_detalle_cliente)

        # ---------- ASIGNAR BOTONES ----------
        btn_agregar.config(command=agregar_cliente)
        btn_eliminar.config(command=eliminar_cliente)
        btn_limpiar.config(command=limpiar_campos)
        btn_editar.config(text="Guardar cambios", command=editar_cliente)

        # ---------- Cargar datos al inicio ----------
        cargar_clientes()


    # ---------------- ---------------------------TAB VENTAS ----------------
        # ---------------- ---------------------------TAB VENTAS ----------------
    def _create_tab_ventas(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ventas")

        # --- Crear contenido del tab ---
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = (
            self._create_tab_content(
                frame,
                "Gestión de Ventas",
                ["Número de Mesa", "Nombre Cliente (opcional)"],
                ["IDVenta", "Fecha", "Mesa", "Cliente", "Productos", "Cantidad Total", "Total Venta", "Estado"],
            )
        )

        # ---------- Conexión a la base de datos ----------
        conexion = conectar()
        cursor = conexion.cursor()

        # -------------------------------------------------
        # CARGAR VENTAS EN EL TREEVIEW
        # -------------------------------------------------
        def cargar_ventas():
            """Carga las ventas desde la base de datos en la tabla."""
            for fila in tree.get_children():
                tree.delete(fila)

            cursor.execute("""
                SELECT 
                    V.IDVentas,
                    CONCAT(RIGHT('0' + CAST(V.Dia AS VARCHAR(2)), 2), '/',
                        RIGHT('0' + CAST(V.Mes AS VARCHAR(2)), 2), '/',
                        CAST(V.Ano AS VARCHAR(4))) AS Fecha,
                    CASE 
                        WHEN VCM.IDClientes IS NOT NULL THEN 
                            (SELECT TOP 1 NumeroDeMesa FROM Clientes WHERE IDClientes = VCM.IDClientes)
                        ELSE 0
                    END AS Mesa,
                    CASE 
                        WHEN VCM.IDClientes IS NOT NULL THEN 
                            (SELECT TOP 1 CONCAT(Nombre1, ' ', Apellido1) 
                            FROM Clientes WHERE IDClientes = VCM.IDClientes)
                        ELSE 'Cliente ocasional'
                    END AS Cliente,
                    STUFF((
                        SELECT ', ' + COALESCE(VCM2.NombrePlato, VCM2.NombreBebida, '')
                        FROM VentasClientesMenuBebidasMenuPlatos VCM2
                        WHERE VCM2.IDVentas = V.IDVentas
                        FOR XML PATH('')
                    ), 1, 2, '') AS Productos,
                    (
                        SELECT SUM(Cantidad)
                        FROM VentasClientesMenuBebidasMenuPlatos VCM3
                        WHERE VCM3.IDVentas = V.IDVentas
                    ) AS CantidadTotal,
                    V.MontoTotal,
                    CASE 
                        WHEN V.MontoTotal > 0 THEN 'Completada'
                        ELSE 'Pendiente'
                    END AS Estado
                FROM Venta V
                LEFT JOIN VentasClientesMenuBebidasMenuPlatos VCM ON V.IDVentas = VCM.IDVentas
                GROUP BY V.IDVentas, V.Dia, V.Mes, V.Ano, V.MontoTotal, VCM.IDClientes
                ORDER BY V.Ano DESC, V.Mes DESC, V.Dia DESC, V.IDVentas DESC
            """)
            
            for row in cursor.fetchall():
                # Formatear valores correctamente
                valores = []
                for i, x in enumerate(row):
                    if x is None:
                        valores.append("—")
                    elif i == 5:  # CantidadTotal
                        try:
                            valores.append(str(int(x)))
                        except:
                            valores.append("0")
                    elif i == 6:  # MontoTotal (Total Venta)
                        try:
                            valores.append(f"C$ {float(x):.2f}")
                        except:
                            valores.append("C$ 0.00")
                    else:
                        valores.append(str(x).strip())
                
                tree.insert("", "end", values=valores)

        # -------------------------------------------------
        # ELIMINAR VENTA
        # -------------------------------------------------
        def eliminar_venta():
            """Elimina la venta seleccionada en la tabla."""
            try:
                seleccionado = tree.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Selecciona una venta para eliminar.")
                    return

                vals = tree.item(seleccionado)["values"]
                if not vals:
                    return

                id_venta = int(vals[0])
                
                # Confirmar eliminación
                confirmar = msg.askyesno(
                    "Confirmar eliminación",
                    f"¿Está seguro de eliminar la venta #{id_venta}?\n"
                    "Esta acción eliminará todos los registros relacionados."
                )
                
                if not confirmar:
                    return

                # Eliminar en el orden correcto para evitar violaciones de FK
                cursor.execute("DELETE FROM VentasClientesMenuBebidasMenuPlatos WHERE IDVentas = ?", (id_venta,))
                cursor.execute("DELETE FROM Venta WHERE IDVentas = ?", (id_venta,))
                conexion.commit()

                msg.showinfo("Éxito", "Venta eliminada correctamente.")
                cargar_ventas()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar la venta:\n{e}")

        # -------------------------------------------------
        # LIMPIAR CAMPOS
        # -------------------------------------------------
        def limpiar_campos():
            """Limpia todos los campos de entrada."""
            for e in entries.values():
                e.delete(0, tk.END)

        # -------------------------------------------------
        # DETALLE AL HACER DOBLE CLIC CON BOTÓN EDITAR
        # -------------------------------------------------
        def mostrar_detalle_venta(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            id_venta, fecha, mesa, cliente, productos, cantidad_total, total_venta, estado = vals

            # Limpiar formato de moneda si existe
            if "C$" in str(total_venta):
                total_venta_limpio = str(total_venta).replace("C$", "").strip()
            else:
                total_venta_limpio = total_venta

            def safe(v):
                return "—" if v in (None, "", "—") else v

            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle de la venta #{safe(id_venta)}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 600
            alto_ventana = 400
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")
            detalle.minsize(500, 350)

            detalle.update_idletasks()
            sw = detalle.winfo_screenwidth()
            sh = detalle.winfo_screenheight()
            ww = detalle.winfo_width()
            wh = detalle.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            detalle.geometry(f"{ww}x{wh}+{x}+{y}")

            container = tk.Frame(detalle, bg="#F5F1E8")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            card = tk.Frame(
                container,
                bg="#FDF7EA",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(fill="both", expand=True)

            canvas_d = tk.Canvas(card, bg="#FDF7EA", highlightthickness=0)
            canvas_d.pack(side="left", fill="both", expand=True)

            scrollbar_d = ttk.Scrollbar(card, orient="vertical", command=canvas_d.yview)
            scrollbar_d.pack(side="right", fill="y")

            canvas_d.configure(yscrollcommand=scrollbar_d.set)

            content = tk.Frame(canvas_d, bg="#FDF7EA")
            canvas_d.create_window((0, 0), window=content, anchor="nw")

            def on_configure(event):
                canvas_d.configure(scrollregion=canvas_d.bbox("all"))

            content.bind("<Configure>", on_configure)

            # Título
            tk.Label(
                content,
                text=f"Venta #{safe(id_venta)}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 14, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(content, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            # Datos de la venta
            datos = [
                ("ID Venta", safe(id_venta)),
                ("Fecha", safe(fecha)),
                ("Mesa", safe(mesa)),
                ("Cliente", safe(cliente)),
                ("Estado", safe(estado)),
                ("Productos", safe(productos)),
                ("Cantidad Total", safe(cantidad_total)),
                ("Total Venta", safe(total_venta)),
            ]

            for i, (label_txt, valor) in enumerate(datos, start=2):
                tk.Label(
                    content,
                    text=label_txt + ":",
                    bg="#FDF7EA",
                    fg="#6A4E23",
                    font=("Segoe UI", 10, "bold"),
                ).grid(row=i, column=0, sticky="w", padx=10, pady=3)

                tk.Label(
                    content,
                    text=str(valor),
                    bg="#FDF7EA",
                    fg="#222222",
                    font=("Segoe UI", 10),
                    wraplength=350 if label_txt == "Productos" else 250,
                    justify="left",
                ).grid(row=i, column=1, sticky="w", padx=5, pady=3)

            last_row = len(datos) + 2

            ttk.Separator(content, orient="horizontal").grid(
                row=last_row, column=0, columnspan=2, sticky="ew", padx=5, pady=(8, 5)
            )

            # ----- BOTONES (Editar y Cerrar) -----
            botones_frame = tk.Frame(content, bg="#FDF7EA")
            botones_frame.grid(row=last_row + 1, column=0, columnspan=2, pady=(10, 5))

            # Botón EDITAR
            def editar_venta_detalle():
                """Prepara la edición de la venta (rellena formulario principal)"""
                # Extraer solo el número de mesa
                mesa_num = ""
                if safe(mesa) != "—":
                    try:
                        # Intentar extraer números de la cadena de mesa
                        import re
                        numeros = re.findall(r'\d+', str(mesa))
                        if numeros:
                            mesa_num = numeros[0]
                    except:
                        mesa_num = str(mesa)
                
                entries["Número de Mesa"].delete(0, tk.END)
                entries["Número de Mesa"].insert(0, mesa_num)
                
                # Si el cliente no es ocasional, poner nombre
                if safe(cliente) != "—" and "ocasional" not in str(cliente).lower():
                    entries["Nombre Cliente (opcional)"].delete(0, tk.END)
                    entries["Nombre Cliente (opcional)"].insert(0, safe(cliente))
                
                detalle.destroy()
                # Aquí podrías abrir también la ventana de edición completa
                msg.showinfo("Editar Venta", 
                           "Los datos se han cargado en el formulario.\n"
                           "Para una edición completa, use el botón 'Editar' principal.")

            btn_editar_detalle = tk.Button(
                botones_frame,
                text="✏️ Editar esta venta",
                bg="#E5D8B4",
                fg="#333333",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=15,
                pady=5,
                command=editar_venta_detalle
            )
            btn_editar_detalle.pack(side="left", padx=5)

            # Botón CERRAR
            btn_cerrar = tk.Button(
                botones_frame,
                text="Cerrar",
                bg="#F2B6B6",
                fg="#333333",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=15,
                pady=5,
                command=detalle.destroy
            )
            btn_cerrar.pack(side="left", padx=5)

            detalle.transient(self)
            detalle.grab_set()

        # -------------------------------------------------
        # AGREGAR NUEVA VENTA (Ventana completa)
        # -------------------------------------------------
        def agregar_venta():
            """Abre una ventana completa para crear una nueva venta."""
            ventana = tk.Toplevel(self)
            ventana.title("Nueva Venta")
            ventana.configure(bg="#F5F1E8")
            ventana.geometry("1000x750")
            
            # Centrar ventana
            ventana.update_idletasks()
            sw = ventana.winfo_screenwidth()
            sh = ventana.winfo_screenheight()
            ww = ventana.winfo_width()
            wh = ventana.winfo_height()
            x = (sw // 2) - (ww // 2)
            y = (sh // 2) - (wh // 2)
            ventana.geometry(f"{ww}x{wh}+{x}+{y}")

            # --- Variables de la ventana ---
            productos_venta = []  # Lista de productos en esta venta
            total_venta = 0.0
            id_cliente_venta = None
            
            # --- Frame principal con scroll ---
            main_container = tk.Frame(ventana, bg="#F5F1E8")
            main_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Canvas para scroll
            canvas = tk.Canvas(main_container, bg="#F5F1E8", highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#F5F1E8")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Cargar información de productos desde la base de datos
            productos_disponibles = {"Plato": {}, "Bebida": {}}
            
            try:
                # Cargar platos
                cursor.execute("""
                    SELECT 
                        P.IDProduccion,
                        P.NombrePlato,
                        ISNULL(P.CostoPorPlato, 0) as Precio,
                        ISNULL(P.CantidadDePlatos, 0) as Stock
                    FROM Produccion P
                    WHERE P.NombrePlato IS NOT NULL 
                    AND ISNULL(P.CantidadDePlatos, 0) > 0
                    ORDER BY P.NombrePlato
                """)
                
                for row in cursor.fetchall():
                    id_prod, nombre, precio, stock = row
                    productos_disponibles["Plato"][nombre] = {
                        "id": id_prod,
                        "precio": float(precio),
                        "stock": int(stock)
                    }
                
                # Cargar bebidas
                cursor.execute("""
                    SELECT 
                        P.IDProduccion,
                        P.NombreBebida,
                        ISNULL(P.CostoPorBebida, 0) as Precio,
                        ISNULL(P.CantidadDeBebidas, 0) as Stock
                    FROM Produccion P
                    WHERE P.NombreBebida IS NOT NULL 
                    AND ISNULL(P.CantidadDeBebidas, 0) > 0
                    ORDER BY P.NombreBebida
                """)
                
                for row in cursor.fetchall():
                    id_prod, nombre, precio, stock = row
                    productos_disponibles["Bebida"][nombre] = {
                        "id": id_prod,
                        "precio": float(precio),
                        "stock": int(stock)
                    }
                    
            except Exception as e:
                msg.showerror("Error", f"No se pudieron cargar los productos:\n{e}")
                ventana.destroy()
                return

            # --- Sección 1: Información de la mesa y cliente ---
            info_frame = tk.Frame(scrollable_frame, bg="#FDF7EA", bd=2, relief="solid")
            info_frame.pack(fill="x", padx=5, pady=(0, 15))
            
            tk.Label(
                info_frame,
                text="📋 Información de la Venta",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            # Número de mesa
            mesa_frame = tk.Frame(info_frame, bg="#FDF7EA")
            mesa_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            tk.Label(mesa_frame, text="Número de Mesa*:", bg="#FDF7EA", 
                    font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5)
            
            entry_mesa = tk.Entry(mesa_frame, font=("Segoe UI", 10), width=15)
            entry_mesa.grid(row=0, column=1, sticky="w", padx=5)
            entry_mesa.insert(0, "1")
            
            # Opción de cliente
            cliente_frame = tk.Frame(info_frame, bg="#FDF7EA")
            cliente_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            tk.Label(cliente_frame, text="Cliente:", bg="#FDF7EA",
                    font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5)
            
            # Frame para opciones de cliente
            cliente_opciones_frame = tk.Frame(cliente_frame, bg="#FDF7EA")
            cliente_opciones_frame.grid(row=0, column=1, sticky="w", padx=5)
            
            # Variable para opción de cliente
            opcion_cliente = tk.StringVar(value="ocasional")
            
            # Radio buttons
            rb_ocasional = tk.Radiobutton(
                cliente_opciones_frame,
                text="Cliente ocasional",
                variable=opcion_cliente,
                value="ocasional",
                bg="#FDF7EA",
                font=("Segoe UI", 9),
                command=lambda: toggle_cliente_fields("ocasional")
            )
            rb_ocasional.pack(side="left", padx=(0, 15))
            
            rb_registrar = tk.Radiobutton(
                cliente_opciones_frame,
                text="Registrar nuevo cliente",
                variable=opcion_cliente,
                value="registrar",
                bg="#FDF7EA",
                font=("Segoe UI", 9),
                command=lambda: toggle_cliente_fields("registrar")
            )
            rb_registrar.pack(side="left")
            
            # Frame para campos de cliente (inicialmente oculto)
            campos_cliente_frame = tk.Frame(info_frame, bg="#FDF7EA")
            
            def toggle_cliente_fields(opcion):
                if opcion == "registrar":
                    campos_cliente_frame.pack(fill="x", padx=15, pady=(5, 10))
                else:
                    campos_cliente_frame.pack_forget()
            
            # Campos para nuevo cliente
            tk.Label(campos_cliente_frame, text="Nombre*:", bg="#FDF7EA").grid(row=0, column=0, sticky="e", padx=5, pady=2)
            entry_nombre_cliente = tk.Entry(campos_cliente_frame, width=25)
            entry_nombre_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            tk.Label(campos_cliente_frame, text="Apellido*:", bg="#FDF7EA").grid(row=0, column=2, sticky="e", padx=5, pady=2)
            entry_apellido_cliente = tk.Entry(campos_cliente_frame, width=25)
            entry_apellido_cliente.grid(row=0, column=3, sticky="w", padx=5, pady=2)
            
            tk.Label(campos_cliente_frame, text="Teléfono:", bg="#FDF7EA").grid(row=1, column=0, sticky="e", padx=5, pady=2)
            entry_telefono_cliente = tk.Entry(campos_cliente_frame, width=25)
            entry_telefono_cliente.grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
            campos_cliente_frame.columnconfigure(1, weight=1)
            campos_cliente_frame.columnconfigure(3, weight=1)
            
            # --- Sección 2: Agregar productos ---
            productos_frame = tk.Frame(scrollable_frame, bg="#FDF7EA", bd=2, relief="solid")
            productos_frame.pack(fill="x", padx=5, pady=(0, 15))
            
            tk.Label(
                productos_frame,
                text="🛒 Agregar Productos",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            # Controles para agregar producto
            control_frame = tk.Frame(productos_frame, bg="#FDF7EA")
            control_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            # Tipo de producto
            tk.Label(control_frame, text="Tipo:", bg="#FDF7EA", 
                    font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5)
            
            cmb_tipo = ttk.Combobox(control_frame, values=["Plato", "Bebida"], 
                                state="readonly", width=12, font=("Segoe UI", 9))
            cmb_tipo.grid(row=0, column=1, sticky="w", padx=5)
            cmb_tipo.set("Plato")
            
            # Producto
            tk.Label(control_frame, text="Producto:", bg="#FDF7EA",
                    font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5)
            
            cmb_producto = ttk.Combobox(control_frame, state="readonly", 
                                    width=35, font=("Segoe UI", 9))
            cmb_producto.grid(row=0, column=3, sticky="ew", padx=5)
            
            # Cantidad
            tk.Label(control_frame, text="Cantidad:", bg="#FDF7EA",
                    font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="e", padx=5)
            
            spin_cantidad = tk.Spinbox(control_frame, from_=1, to=100, width=8, 
                                    font=("Segoe UI", 9))
            spin_cantidad.grid(row=0, column=5, sticky="w", padx=5)
            
            control_frame.columnconfigure(3, weight=1)
            
            # Función para actualizar productos según tipo
            def actualizar_productos(*args):
                tipo = cmb_tipo.get()
                if tipo in productos_disponibles:
                    productos = list(productos_disponibles[tipo].keys())
                    cmb_producto["values"] = productos
                    if productos:
                        cmb_producto.set(productos[0])
                else:
                    cmb_producto["values"] = []
                    cmb_producto.set("")
            
            cmb_tipo.bind("<<ComboboxSelected>>", actualizar_productos)
            actualizar_productos()  # Inicializar
            
            # Botón para agregar producto
            btn_agregar_producto = tk.Button(
                control_frame,
                text="➕ Agregar a la venta",
                bg="#CFE5C8",
                fg="#333333",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=10,
                pady=4,
                command=lambda: agregar_producto_venta()
            )
            btn_agregar_producto.grid(row=0, column=6, sticky="w", padx=10)
            
            # Treeview para productos de la venta
            tree_productos_frame = tk.Frame(productos_frame, bg="#FDF7EA")
            tree_productos_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
            
            # Crear treeview para productos
            tree_productos = ttk.Treeview(
                tree_productos_frame,
                columns=("Producto", "Cantidad", "Precio Unitario", "Subtotal"),
                show="headings",
                height=6
            )
            
            # Configurar columnas
            tree_productos.heading("Producto", text="Producto")
            tree_productos.heading("Cantidad", text="Cantidad")
            tree_productos.heading("Precio Unitario", text="Precio Unitario")
            tree_productos.heading("Subtotal", text="Subtotal")
            
            tree_productos.column("Producto", width=250, anchor="w")
            tree_productos.column("Cantidad", width=80, anchor="center")
            tree_productos.column("Precio Unitario", width=120, anchor="e")
            tree_productos.column("Subtotal", width=120, anchor="e")
            
            # Scrollbar
            scroll_productos = ttk.Scrollbar(tree_productos_frame, orient="vertical", command=tree_productos.yview)
            tree_productos.configure(yscrollcommand=scroll_productos.set)
            
            tree_productos.pack(side="left", fill="both", expand=True)
            scroll_productos.pack(side="right", fill="y")
            
            # Función para agregar producto a la venta
            def agregar_producto_venta():
                tipo = cmb_tipo.get()
                producto = cmb_producto.get()
                cantidad_str = spin_cantidad.get()
                
                if not tipo or not producto:
                    msg.showwarning("Atención", "Seleccione tipo y producto.")
                    return
                
                if not cantidad_str.isdigit():
                    msg.showwarning("Atención", "Ingrese una cantidad válida.")
                    return
                
                cantidad = int(cantidad_str)
                
                if cantidad <= 0:
                    msg.showwarning("Atención", "La cantidad debe ser mayor a 0.")
                    return
                
                # Verificar stock
                if producto in productos_disponibles[tipo]:
                    info = productos_disponibles[tipo][producto]
                    if cantidad > info["stock"]:
                        msg.showwarning("Stock insuficiente", 
                                      f"Solo hay {info['stock']} unidades disponibles.")
                        return
                    
                    # Calcular subtotal
                    subtotal = info["precio"] * cantidad
                    
                    # Agregar a la lista de productos
                    productos_venta.append({
                        "tipo": tipo,
                        "nombre": producto,
                        "id_produccion": info["id"],
                        "cantidad": cantidad,
                        "precio_unitario": info["precio"],
                        "subtotal": subtotal
                    })
                    
                    # Actualizar treeview
                    tree_productos.insert("", "end", values=(
                        producto,
                        cantidad,
                        f"C$ {info['precio']:.2f}",
                        f"C$ {subtotal:.2f}"
                    ))
                    
                    # Actualizar total
                    nonlocal total_venta
                    total_venta += subtotal
                    lbl_total.config(text=f"C$ {total_venta:.2f}")
                    
                    # Actualizar stock disponible en memoria
                    productos_disponibles[tipo][producto]["stock"] -= cantidad
                    
                    # Limpiar cantidad
                    spin_cantidad.delete(0, tk.END)
                    spin_cantidad.insert(0, "1")
                    
                else:
                    msg.showerror("Error", "Producto no encontrado.")
            
            # Botón para eliminar producto seleccionado
            btn_eliminar_producto = tk.Button(
                productos_frame,
                text="🗑️ Eliminar producto seleccionado",
                bg="#F2B6B6",
                fg="#333333",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=10,
                pady=4,
                command=lambda: eliminar_producto_seleccionado()
            )
            btn_eliminar_producto.pack(anchor="e", padx=15, pady=(0, 10))
            
            def eliminar_producto_seleccionado():
                seleccionado = tree_productos.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Seleccione un producto para eliminar.")
                    return
                
                # Obtener información del producto
                item = tree_productos.item(seleccionado[0])
                valores = item["values"]
                nombre_producto = valores[0]
                cantidad = int(valores[1])
                
                # Buscar en qué tipo está el producto
                for tipo in ["Plato", "Bebida"]:
                    if nombre_producto in productos_disponibles[tipo]:
                        # Devolver stock
                        productos_disponibles[tipo][nombre_producto]["stock"] += cantidad
                        
                        # Restar del total
                        nonlocal total_venta
                        subtotal = float(valores[3].replace("C$", "").strip())
                        total_venta -= subtotal
                        lbl_total.config(text=f"C$ {total_venta:.2f}")
                        
                        # Eliminar de la lista de productos
                        for i, prod in enumerate(productos_venta):
                            if prod["nombre"] == nombre_producto and prod["cantidad"] == cantidad:
                                productos_venta.pop(i)
                                break
                        
                        break
                
                # Eliminar del treeview
                tree_productos.delete(seleccionado[0])
            
            # --- Sección 3: Resumen y total ---
            resumen_frame = tk.Frame(scrollable_frame, bg="#FDF7EA", bd=2, relief="solid")
            resumen_frame.pack(fill="x", padx=5, pady=(0, 15))
            
            tk.Label(
                resumen_frame,
                text="💰 Resumen de la Venta",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            # Frame para total
            total_frame = tk.Frame(resumen_frame, bg="#FDF7EA")
            total_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            tk.Label(
                total_frame,
                text="TOTAL:",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 14, "bold")
            ).pack(side="left", padx=(0, 10))
            
            lbl_total = tk.Label(
                total_frame,
                text="C$ 0.00",
                bg="#FDF7EA",
                fg="#157347",
                font=("Segoe UI", 16, "bold")
            )
            lbl_total.pack(side="left")
            
            # --- Sección 4: Botones finales ---
            botones_frame = tk.Frame(scrollable_frame, bg="#F5F1E8")
            botones_frame.pack(fill="x", padx=5, pady=(0, 10))
            
            # Función para finalizar venta
        # Función para finalizar venta
           # Función para finalizar venta - VERSIÓN ALTERNATIVA
            def finalizar_venta():
                # Validaciones
                mesa = entry_mesa.get().strip()
                if not mesa or not mesa.isdigit():
                    msg.showwarning("Atención", "Ingrese un número de mesa válido.")
                    return
                
                if not productos_venta:
                    msg.showwarning("Atención", "Agregue al menos un producto a la venta.")
                    return
                
                try:
                    # Procesar cliente si es necesario
                    id_cliente = None
                    if opcion_cliente.get() == "registrar":
                        nombre = entry_nombre_cliente.get().strip()
                        apellido = entry_apellido_cliente.get().strip()
                        telefono = entry_telefono_cliente.get().strip()
                        
                        if not nombre or not apellido:
                            msg.showwarning("Atención", "Ingrese nombre y apellido del cliente.")
                            return
                        
                        # Insertar teléfono si se proporcionó
                        if telefono:
                            cursor.execute(
                                "INSERT INTO TelefonoCliente (Telefono) VALUES (?)",
                                (telefono,)
                            )
                            # Obtener el ID del teléfono recién insertado
                            cursor.execute("SELECT MAX(IDTelefonoClientes) FROM TelefonoCliente")
                            id_telefono = cursor.fetchone()[0]
                        else:
                            # Insertar registro de teléfono vacío
                            cursor.execute("INSERT INTO TelefonoCliente (Telefono) VALUES ('')")
                            cursor.execute("SELECT MAX(IDTelefonoClientes) FROM TelefonoCliente")
                            id_telefono = cursor.fetchone()[0]
                        
                        # Insertar cliente
                        cursor.execute(
                            """INSERT INTO Clientes 
                            (NumeroDeMesa, IDTelefonoClientes, Nombre1, Apellido1) 
                            VALUES (?, ?, ?, ?)""",
                            (int(mesa), id_telefono, nombre, apellido)
                        )
                        cursor.execute("SELECT MAX(IDClientes) FROM Clientes")
                        id_cliente = cursor.fetchone()[0]
                    
                    # Insertar venta principal
                    fecha_actual = datetime.now()
                    cursor.execute(
                        """INSERT INTO Venta 
                        (Dia, Mes, Ano, MontoTotal, Hora) 
                        VALUES (?, ?, ?, ?, ?)""",
                        (fecha_actual.day, fecha_actual.month, fecha_actual.year, total_venta, 
                        fecha_actual.strftime('%H:%M:%S'))
                    )
                    cursor.execute("SELECT MAX(IDVentas) FROM Venta")
                    id_venta = cursor.fetchone()[0]
                    
                    # Insertar productos de la venta
                    for prod in productos_venta:
                        if prod["tipo"] == "Plato":
                            cursor.execute(
                                """INSERT INTO VentasClientesMenuBebidasMenuPlatos 
                                (IDVentas, Cantidad, NombrePlato, Precio) 
                                VALUES (?, ?, ?, ?)""",
                                (id_venta, prod["cantidad"], prod["nombre"], prod["precio_unitario"])
                            )
                            
                            # Actualizar stock en producción
                            cursor.execute(
                                """UPDATE Produccion 
                                SET CantidadDePlatos = CantidadDePlatos - ? 
                                WHERE IDProduccion = ?""",
                                (prod["cantidad"], prod["id_produccion"])
                            )
                        else:  # Bebida
                            cursor.execute(
                                """INSERT INTO VentasClientesMenuBebidasMenuPlatos 
                                (IDVentas, Cantidad, NombreBebida, Precio) 
                                VALUES (?, ?, ?, ?)""",
                                (id_venta, prod["cantidad"], prod["nombre"], prod["precio_unitario"])
                            )
                            
                            # Actualizar stock en producción
                            cursor.execute(
                                """UPDATE Produccion 
                                SET CantidadDeBebidas = CantidadDeBebidas - ? 
                                WHERE IDProduccion = ?""",
                                (prod["cantidad"], prod["id_produccion"])
                            )
                    
                    # Si hay cliente, asociarlo
                    if id_cliente:
                        cursor.execute(
                            """UPDATE VentasClientesMenuBebidasMenuPlatos 
                            SET IDClientes = ? 
                            WHERE IDVentas = ? AND IDClientes IS NULL""",
                            (id_cliente, id_venta)
                        )
                    
                    conexion.commit()
                    
                    msg.showinfo("Éxito", f"Venta #{id_venta} registrada correctamente.\nTotal: C$ {total_venta:.2f}")
                    
                    # Actualizar vistas
                    cargar_ventas()
                    if hasattr(self, 'cargar_produccion'):
                        self.cargar_produccion()
                    
                    ventana.destroy()
                    
                except Exception as e:
                    conexion.rollback()
                    msg.showerror("Error", f"No se pudo registrar la venta:\n{str(e)}")
                                    
            # Función para cancelar
            def cancelar_venta():
                if productos_venta:
                    respuesta = msg.askyesno("Cancelar", 
                                           "¿Está seguro de cancelar la venta?\nSe perderán todos los productos agregados.")
                    if respuesta:
                        ventana.destroy()
                else:
                    ventana.destroy()
            
            # Botones finales
            btn_cancelar = tk.Button(
                botones_frame,
                text="❌ Cancelar",
                bg="#F2B6B6",
                fg="#333333",
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                command=cancelar_venta
            )
            btn_cancelar.pack(side="left", padx=5)
            
            btn_finalizar = tk.Button(
                botones_frame,
                text="✅ Finalizar Venta",
                bg="#CFE5C8",
                fg="#333333",
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                command=finalizar_venta
            )
            btn_finalizar.pack(side="right", padx=5)
            
            ventana.transient(self)
            ventana.grab_set()

        # -------------------------------------------------
        # EDITAR VENTA (GUARDAR CAMBIOS)
        # -------------------------------------------------
        def editar_venta():
            """Abre ventana para editar venta existente (similar a agregar pero con datos cargados)."""
            seleccionado = tree.selection()
            if not seleccionado:
                msg.showwarning("Atención", "Seleccione una venta para editar.")
                return
            
            # Por ahora, solo mostramos mensaje de funcionalidad próxima
            msg.showinfo("Próximamente", 
                       "La funcionalidad de edición completa de ventas estará disponible en la próxima actualización.\n"
                       "Por ahora, puede eliminar la venta y crear una nueva o usar el botón 'Editar' en el detalle.")
            
            # Nota: Aquí se podría implementar una función similar a agregar_venta()
            # pero cargando los datos existentes de la venta seleccionada.

        # -------------------------------------------------
        # ASIGNAR BOTONES
        # -------------------------------------------------
        btn_agregar.config(command=agregar_venta)
        btn_eliminar.config(command=eliminar_venta)
        btn_limpiar.config(command=limpiar_campos)
        btn_editar.config(text="Editar venta", command=editar_venta)
        
        # Configurar doble clic para ver detalle
        tree.bind("<Double-1>", mostrar_detalle_venta)

        # ---------- Cargar datos al inicio ----------
        cargar_ventas()
        return frame
    
     
# ----------------------- MAIN ---------------------------------------------------
if __name__ == "__main__":
    app = RestauranteUI()
    app.mainloop()
