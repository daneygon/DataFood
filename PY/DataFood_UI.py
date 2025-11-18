import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg   # <--- NUEVO
import pyodbc                           # <--- NUEVO


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
    def __init__(self):
        super().__init__()

        # ---------- Ventana principal ---------------
        self.title("Sistema de Gestión de Restaurante - DataFood")
        self.geometry("1200x700")
        self.configure(bg="#F5F1E8")

        # --------------- Estilo ------------------
        self._apply_style()

        # Estado inicial del sidebar (visible)
        self.sidebar_visible = True

        # --------------- Encabezado ------------------
        header = tk.Frame(self, bg="#C8B88A", height=50)
        header.pack(side="top", fill="x")

        # Para poder centrar el título y tener la flecha a la izquierda
        header.grid_columnconfigure(1, weight=1)

        # 🔽 Botón flecha para ocultar/mostrar el panel principal
        self.btn_toggle_sidebar = tk.Button(
            header,
            text="⮜",  # flecha apuntando al sidebar
            bg="#C8B88A",
            fg="#ffffff",
            bd=0,
            font=("Segoe UI", 12, "bold"),
            activebackground="#C8B88A",
            activeforeground="#ffffff",
            command=self._toggle_sidebar
        )
        self.btn_toggle_sidebar.grid(row=0, column=0, padx=(8, 5), pady=5)

        # Título centrado
        tk.Label(
            header,
            text="DataFood  |  Sistema de Gestión de Restaurante",
            bg="#C8B88A",
            fg="#ffffff",
            font=("Segoe UI", 15, "bold")
        ).grid(row=0, column=1, pady=5)

        # --------------- CONTENEDOR PRINCIPAL (3 COLUMNAS) ------------------
        main_content = tk.Frame(self, bg="#F5F1E8")
        main_content.pack(expand=True, fill="both", padx=10, pady=10)

        # ------------------ COLUMNA IZQUIERDA (PANEL PRINCIPAL) -------------
        self.sidebar = tk.Frame(main_content, bg="#C8B88A", width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="Food Delivery\nDataFood",
            bg="#C8B88A",
            fg="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            justify="left"
        ).pack(padx=15, pady=(20, 10), anchor="w")

        tk.Label(
            self.sidebar,
            text="Panel principal",
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

        # 🔙 Botón INICIO (encima de Gestión)
        inicio_btn = ttk.Button(
            self.sidebar,
            text="Inicio",
            command=self._mostrar_dashboard_inicial
        )
        inicio_btn.pack(fill="x", padx=15, pady=(5, 5))

        # Botón de Gestión → ahora cambia el centro (no abre ventana nueva)
        gestion_btn = ttk.Button(
            self.sidebar,
            text="Gestión",
            command=self._abrir_ventana_gestion
        )
        gestion_btn.pack(fill="x", padx=15, pady=(5, 5))

        ttk.Button(self.sidebar, text="Pedidos (próximamente)").pack(
            fill="x", padx=15, pady=5
        )
        ttk.Button(self.sidebar, text="Reportes (próximamente)").pack(
            fill="x", padx=15, pady=5
        )

        # ------------------ ZONA CENTRAL DINÁMICA ----------------
        self.center_frame = tk.Frame(main_content, bg="#FFFFFF")
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # al iniciar, mostramos el “Menú de Platos y Bebidas”
        self._mostrar_dashboard_inicial()

        # ------------------ COLUMNA DERECHA (ESPACIO FUTURO) ----------------
        self.right_frame = tk.Frame(main_content, bg="#F5F1E8", width=260)
        self.right_frame.pack(side="left", fill="y")
        self.right_frame.pack_propagate(False)

        tk.Label(
            self.right_frame,
            text="Panel derecho\n(próximas funciones)",
            bg="#F5F1E8",
            fg="#444444",
            font=("Segoe UI", 11, "bold"),
            justify="center"
        ).pack(padx=10, pady=20)

        tk.Label(
            self.right_frame,
            text="Aquí puedes añadir más adelante:\n"
                 "- Detalle del pedido actual\n"
                 "- Resumen de venta\n"
                 "- Métodos de pago, etc.",
            bg="#F5F1E8",
            fg="#666666",
            font=("Segoe UI", 9),
            justify="left"
        ).pack(padx=10, pady=5)

    def _mostrar_dashboard_inicial(self):
        """Contenido central por defecto: Menú de Platos y Bebidas."""
        # limpiar todo lo que haya en el centro
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.center_frame,
            text="Menú de Platos y Bebidas",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tk.Label(
            self.center_frame,
            text="Aquí irán las tarjetas/fotos de los platos y bebidas.\n"
                 "Esta zona corresponde a donde ves las imágenes de comida en la referencia.",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 10),
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        cards_container = tk.Frame(self.center_frame, bg="#FFFFFF")
        cards_container.pack(fill="both", expand=True, padx=15, pady=10)

        frame_platos = tk.LabelFrame(
            cards_container,
            text="Menú de Platos",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 11, "bold")
        )
        frame_platos.pack(side="top", fill="both", expand=True, pady=(0, 10))

        tk.Label(
            frame_platos,
            text="(Aquí puedes colocar una cuadrícula de platos con foto, nombre y precio.)",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=10, pady=5)

        frame_bebidas = tk.LabelFrame(
            cards_container,
            text="Menú de Bebidas",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 11, "bold")
        )
        frame_bebidas.pack(side="top", fill="both", expand=True)

        tk.Label(
            frame_bebidas,
            text="(Aquí puedes colocar una cuadrícula de bebidas con foto, nombre y precio.)",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=10, pady=5)

    def _abrir_ventana_gestion(self):
        """Muestra el notebook de CRUDs dentro del centro (misma ventana)."""
        # limpiar contenido central
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        # contenedor para el título + notebook
        container = tk.Frame(self.center_frame, bg="#F5F1E8")
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="Gestión de Datos  |  CRUD DataFood",
            bg="#F5F1E8",
            fg="#333333",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self._create_tab_proveedores(notebook)
        self._create_tab_insumos(notebook)
        self._create_tab_produccion(notebook)
        self._create_tab_clientes(notebook)
        self._create_tab_ventas(notebook)

    def _toggle_sidebar(self):
        """Oculta o muestra el panel principal y expande/contrae el CRUD."""
        if self.sidebar_visible:
            # Ocultar panel izquierdo y derecho para que el CRUD use todo el ancho
            self.sidebar.pack_forget()
            self.right_frame.pack_forget()
            self.btn_toggle_sidebar.config(text="⮞")  # flecha hacia la derecha (expandir)
            self.sidebar_visible = False
        else:
            # Volver a mostrar ambos paneles
            self.sidebar.pack(side="left", fill="y")
            self.right_frame.pack(side="left", fill="y")
            self.btn_toggle_sidebar.config(text="⮜")  # flecha hacia el panel
            self.sidebar_visible = True

      
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
    def _create_tab_content(self, parent, title, labels, tree_columns):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        # ---------- Panel izquierdo con scroll ----------
        left_container = tk.Frame(frame, bg="#E9E2D0")
        left_container.pack(side="left", fill="y")

        canvas = tk.Canvas(left_container, bg="#E9E2D0", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_left = ttk.Scrollbar(
            left_container, orient="vertical", command=canvas.yview
        )
        scrollbar_left.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar_left.set)

        # Frame interno desplazable
        left = tk.Frame(canvas, bg="#E9E2D0", padx=15, pady=15)
        canvas.create_window((0, 0), window=left, anchor="nw")

        # Permitir el scroll cuando el contenido crezca
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        left.bind("<Configure>", on_configure)

        # ---------- Contenido de la izquierda ----------
        tk.Label(
            left,
            text=f"📦 {title}",
            bg="#E9E2D0",
            font=("Segoe UI", 12, "bold"),
            fg="#6A4E23",
        ).pack(pady=5)

        entries = {}
        for lbl in labels:
            tk.Label(left, text=lbl + ":", bg="#E9E2D0", font=("Segoe UI", 10)).pack(
                anchor="w"
            )
            entry = ttk.Entry(left)
            entry.pack(fill="x", pady=2)
            entries[lbl] = entry

        # ------------------------------------------------------------------------------ Botones
        # Botones
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

        # ---------- Tabla derecha ----------
        right = ttk.Frame(frame)
        right.pack(side="right", fill="both", expand=True)

        tree = self._create_treeview(right, tree_columns)
        return entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar

        # ---------- Tabla derecha ----------
        right = ttk.Frame(frame)
        right.pack(side="right", fill="both", expand=True)

        tree = self._create_treeview(right, tree_columns)
        return entries, tree
    

            # -------------------------------------------------------------
    # FUNCIÓN GLOBAL – ACTUALIZA LISTA DE PROVEEDORES EN INSUMOS
    # -------------------------------------------------------------
    def cargar_proveedores_global(self):
        """Carga la lista de proveedores en el combobox de Insumos."""
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT IDProveedor, NombreProveedor
                FROM Proveedores
                ORDER BY NombreProveedor
            """)

            proveedores = cursor.fetchall()

            # Guardar la lista dentro del objeto
            self.lista_proveedores = proveedores

            # Si existe combobox en insumos, actualizarlo:
            if hasattr(self, "combo_proveedores_insumos"):
                self.combo_proveedores_insumos["values"] = [p[1] for p in proveedores]

        except Exception as e:
            print("Error cargando proveedores global:", e)

    # ---------------- ------------------------------------------------------------------------TAB PROVEEDORES ----------------
    # ---------------- TAB PROVEEDORES ----------------
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

            # 🔥 ACTUALIZA COMBOBOX GLOBAL
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
        # ASIGNAR BOTONES
        # -------------------------------------------------
        btn_agregar.config(command=agregar_proveedor)
        btn_eliminar.config(command=eliminar_proveedor)
        btn_editar.config(command=editar_proveedor)
        btn_limpiar.config(command=limpiar)

        cargar_proveedores()



     # ---------------- ------------------------------------------------------------------TAB INSUMOS ----------------
     
    def _create_tab_insumos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Insumos")

        conexion = conectar()
        cursor = conexion.cursor()

        main_frame = tk.Frame(frame, bg="#F5F1E8")
        main_frame.pack(fill="both", expand=True)

        # =========== PANEL IZQUIERDO CON SCROLL ===========
        left_container = tk.Frame(main_frame, bg="#E9E2D0")
        left_container.pack(side="left", fill="y")

        canvas = tk.Canvas(left_container, bg="#E9E2D0", highlightthickness=0)
        canvas.pack(side="left", fill="y", expand=False)

        scrollbar_left = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
        scrollbar_left.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar_left.set)

        left = tk.Frame(canvas, bg="#E9E2D0", padx=15, pady=15)
        canvas.create_window((0, 0), window=left, anchor="nw")

        def update_scroll(_):
            canvas.configure(scrollregion=canvas.bbox("all"))
        left.bind("<Configure>", update_scroll)

        # =========== TITULO ===========
        tk.Label(left, text="📦 Gestión de Insumos", bg="#E9E2D0",
                font=("Segoe UI", 12, "bold"), fg="#6A4E23").pack(pady=(0,10))

        entries = {}

        # ============================================================
        # 1️⃣ CATEGORÍA
        # ============================================================
        tk.Label(left, text="Categoría:", bg="#E9E2D0").pack(anchor="w")
        combo_categoria = ttk.Combobox(left, state="readonly")
        combo_categoria.pack(fill="x", pady=3)
        entries["Categoría"] = combo_categoria

        cursor.execute("SELECT NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria")
        combo_categoria["values"] = [row[0] for row in cursor.fetchall()]

        # ============================================================
        # 2️⃣ NOMBRE INSUMO
        # ============================================================
        tk.Label(left, text="Nombre del Insumo:", bg="#E9E2D0").pack(anchor="w")
        e = ttk.Entry(left)
        e.pack(fill="x", pady=3)
        entries["Nombre"] = e

        # ============================================================
        # 3️⃣ CANTIDADES
        # ============================================================
        tk.Label(left, text="Cantidad Disponible:", bg="#E9E2D0").pack(anchor="w")
        entries["Disponible"] = ttk.Entry(left)
        entries["Disponible"].pack(fill="x", pady=3)

        tk.Label(left, text="Cantidad Dañada:", bg="#E9E2D0").pack(anchor="w")
        entries["Dañada"] = ttk.Entry(left)
        entries["Dañada"].pack(fill="x", pady=3)

        # ============================================================
        # 4️⃣ PROVEEDOR (DINÁMICO)
        # ============================================================
        tk.Label(left, text="Proveedor:", bg="#E9E2D0").pack(anchor="w")
        self.combo_proveedores_insumos = ttk.Combobox(left, state="readonly")
        self.combo_proveedores_insumos.pack(fill="x", pady=3)
        entries["Proveedor"] = self.combo_proveedores_insumos

        self.cargar_proveedores_global()
        self.combo_proveedores_insumos["values"] = [p[1] for p in self.lista_proveedores]

        # ============================================================
        # 5️⃣ PRECIO COMPRA
        # ============================================================
        tk.Label(left, text="Precio Compra:", bg="#E9E2D0").pack(anchor="w")
        entries["Precio"] = ttk.Entry(left)
        entries["Precio"].pack(fill="x", pady=3)

        # ============================================================
        # 6️⃣ CANTIDAD COMPRADA
        # ============================================================
        tk.Label(left, text="Cantidad Comprada:", bg="#E9E2D0").pack(anchor="w")
        entries["Comprada"] = ttk.Entry(left)
        entries["Comprada"].pack(fill="x", pady=3)

        # ============================================================
        # 7️⃣ FECHA
        # ============================================================
        tk.Label(left, text="Fecha de Ingreso (DD/MM/AAAA):", bg="#E9E2D0").pack(anchor="w")
        entries["Fecha"] = ttk.Entry(left)
        entries["Fecha"].pack(fill="x", pady=3)

        # ============================================================
        # BOTONES
        # ============================================================
        btn_frame = tk.Frame(left, bg="#E9E2D0")
        btn_frame.pack(pady=10, fill="x")

        btn_agregar = ttk.Button(btn_frame, text="Agregar")
        btn_agregar.pack(fill="x", pady=3)

        btn_editar = ttk.Button(btn_frame, text="Editar")
        btn_editar.pack(fill="x", pady=3)

        btn_eliminar = ttk.Button(btn_frame, text="Eliminar")
        btn_eliminar.pack(fill="x", pady=3)

        btn_limpiar = ttk.Button(btn_frame, text="Limpiar",
                                command=lambda: [
                                    e.delete(0, tk.END)
                                    for k, e in entries.items()
                                    if isinstance(e, ttk.Entry)
                                ])
        btn_limpiar.pack(fill="x", pady=3)

        # ============================================================
        # PANEL DERECHO – TREEVIEW
        # ============================================================
        right = ttk.Frame(main_frame)
        right.pack(side="right", fill="both", expand=True)

        columns = [
            "ID", "Categoría", "Nombre", "Disponible", "Dañada",
            "Proveedor", "Precio Compra", "Cantidad Comprada", "Fecha"
        ]

        tree = self._create_treeview(right, columns)

        # ============================================================
        # FUNCIONES CRUD
        # ============================================================

        # --------- CARGAR INSUMOS ---------
        def cargar_insumos():
            for item in tree.get_children():
                tree.delete(item)

            cursor.execute("""
                SELECT 
                    I.IDInsumos,
                    C.NombreCategoria,
                    I.NombreInsumo,
                    I.CantidadDisponible,
                    I.CantidadDañada,
                    P.NombreProveedor,
                    PI.PrecioCompra,
                    PI.CantidadComprada,
                    PI.Dia, PI.Mes, PI.Ano
                FROM Insumos I
                JOIN CategoriaInsumos C ON C.IDCategoriaInsumos = I.IDCategoriaInsumos
                LEFT JOIN ProveedoresInsumos PI ON PI.IDInsumos = I.IDInsumos
                LEFT JOIN Proveedores P ON P.IDProveedor = PI.IDProveedor
                ORDER BY I.IDInsumos ASC
            """)

            for row in cursor.fetchall():
                (id_in, cat, nombre, disp, danio,
                proveedor, precio, cant_comp, dia, mes, ano) = row

                fecha = f"{dia}/{mes}/{ano}" if dia and mes and ano else "—"

                tree.insert(
                    "", "end",
                    values=[
                        id_in, cat, nombre, disp, danio,
                        proveedor or "—", precio or "—",
                        cant_comp or "—", fecha
                    ]
                )

        # --------- AGREGAR INSUMO ---------
        def agregar_insumo():
            try:
                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                disp = entries["Disponible"].get().strip()
                danio = entries["Dañada"].get().strip()
                proveedor = entries["Proveedor"].get()
                precio = entries["Precio"].get().strip()
                comprada = entries["Comprada"].get().strip()
                fecha = entries["Fecha"].get().strip()

                if not categoria or not nombre or not disp.isdigit() or not comprada.isdigit() or not precio.replace(".", "", 1).isdigit():
                    msg.showwarning("Atención", "Complete todos los campos obligatorios.")
                    return

                disp = int(disp)
                danio = int(danio) if danio.isdigit() else 0
                comprada = int(comprada)
                precio = float(precio)

                cursor.execute("SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?", (categoria,))
                id_cat = cursor.fetchone()[0]

                # Insertar en Insumos
                cursor.execute("""
                    INSERT INTO Insumos (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada)
                    VALUES (?, ?, ?, ?)
                """, (id_cat, nombre, disp, danio))
                conexion.commit()

                cursor.execute("SELECT MAX(IDInsumos) FROM Insumos")
                id_insumo = cursor.fetchone()[0]

                # proveedor id
                cursor.execute("SELECT IDProveedor FROM Proveedores WHERE NombreProveedor=?", (proveedor,))
                id_prov = cursor.fetchone()[0]

                try:
                    dia, mes, ano = map(int, fecha.split("/"))
                except:
                    dia = mes = ano = None

                # Insertar en ProveedoresInsumos
                cursor.execute("""
                    INSERT INTO ProveedoresInsumos 
                    (IDInsumos, IDProveedor, PrecioCompra, CantidadComprada, Dia, Mes, Ano)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id_insumo, id_prov, precio, comprada, dia, mes, ano))

                conexion.commit()

                msg.showinfo("Éxito", "Insumo agregado correctamente.")
                cargar_insumos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar el insumo:\n{e}")

        # --------- ELIMINAR INSUMO ---------
        def eliminar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un insumo.")

                id_ins = tree.item(sel)["values"][0]

                cursor.execute("DELETE FROM ProveedoresInsumos WHERE IDInsumos=?", (id_ins,))
                cursor.execute("DELETE FROM Insumos WHERE IDInsumos=?", (id_ins,))
                conexion.commit()

                msg.showinfo("Éxito", "Insumo eliminado.")
                cargar_insumos()
            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")

        # --------- EDITAR INSUMO ---------
        def editar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un insumo.")

                id_ins = tree.item(sel)["values"][0]

                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                disp = entries["Disponible"].get().strip()
                danio = entries["Dañada"].get().strip()
                proveedor = entries["Proveedor"].get()
                precio = entries["Precio"].get().strip()
                comprada = entries["Comprada"].get().strip()
                fecha = entries["Fecha"].get().strip()

                if not categoria or not nombre or not disp.isdigit():
                    return msg.showwarning("Atención", "Complete todos los campos.")

                disp = int(disp)
                danio = int(danio) if danio.isdigit() else 0
                precio = float(precio)
                comprada = int(comprada)

                cursor.execute("SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?", (categoria,))
                id_cat = cursor.fetchone()[0]

                # actualizar Insumo
                cursor.execute("""
                    UPDATE Insumos
                    SET IDCategoriaInsumos=?, NombreInsumo=?, CantidadDisponible=?, CantidadDañada=?
                    WHERE IDInsumos=?
                """, (id_cat, nombre, disp, danio, id_ins))

                cursor.execute("SELECT IDProveedor FROM Proveedores WHERE NombreProveedor=?", (proveedor,))
                id_prov = cursor.fetchone()[0]

                try:
                    dia, mes, ano = map(int, fecha.split("/"))
                except:
                    dia = mes = ano = None

                cursor.execute("""
                    UPDATE ProveedoresInsumos
                    SET IDProveedor=?, PrecioCompra=?, CantidadComprada=?, Dia=?, Mes=?, Ano=?
                    WHERE IDInsumos=?
                """, (id_prov, precio, comprada, dia, mes, ano, id_ins))

                conexion.commit()

                msg.showinfo("Éxito", "Insumo actualizado.")
                cargar_insumos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar:\n{e}")

        # Asignar CRUD
        btn_agregar.config(command=agregar_insumo)
        btn_eliminar.config(command=eliminar_insumo)
        btn_editar.config(command=editar_insumo)

        cargar_insumos()


    # --------------------------------------------------------- +---------TAB PRODUCCIÓN ----------------
    def _create_tab_produccion(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Producción")

        conexion = conectar()
        cursor = conexion.cursor()

        # --- Frame principal ---
        main_frame = tk.Frame(frame, bg="#F5F1E8")
        main_frame.pack(fill="both", expand=True)

        # --- Panel izquierdo ---
        left = tk.Frame(main_frame, bg="#E9E2D0", padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(
            left,
            text="📦 Registro de Producción",
            bg="#E9E2D0",
            font=("Segoe UI", 12, "bold"),
            fg="#6A4E23",
        ).pack(pady=(0, 10))

        labels = [
            "Tipo de Producción",
            "Categoría",
            "Nombre",
            "Cantidad",
            "Costo Unitario",
        ]
        entries = {}

        for lbl in labels:
            tk.Label(left, text=f"{lbl}:", bg="#E9E2D0", font=("Segoe UI", 10)).pack(
                anchor="w"
            )
            if lbl in ["Tipo de Producción", "Categoría"]:
                combo = ttk.Combobox(left, state="readonly")
                combo.pack(fill="x", pady=2)
                entries[lbl] = combo
            else:
                entry = ttk.Entry(left)
                entry.pack(fill="x", pady=2)
                entries[lbl] = entry

        # --- Combobox de tipo ---
        entries["Tipo de Producción"]["values"] = ["Plato", "Bebida"]

        # --- Botones ---
        btn_frame = tk.Frame(left, bg="#E9E2D0")
        btn_frame.pack(pady=10, fill="x")


        btn_agregar = ttk.Button(btn_frame, text="Agregar")
        btn_agregar.pack(fill="x", pady=2)
        btn_editar = ttk.Button(btn_frame, text="Editar")
        btn_editar.pack(fill="x", pady=2)
        btn_eliminar = ttk.Button(btn_frame, text="Eliminar")
        btn_eliminar.pack(fill="x", pady=2)
        ttk.Button(
            btn_frame,
            text="Limpiar",
            command=lambda: [
                e.delete(0, tk.END)
                for e in entries.values()
                if isinstance(e, ttk.Entry)
            ],
        ).pack(fill="x", pady=2)

        # --- Tabla derecha ---
        right = ttk.Frame(main_frame)
        right.pack(side="right", fill="both", expand=True)

        columns = [
            "IDProduccion",
            "Tipo",
            "Categoría",
            "Nombre",
            "Cantidad",
            "Costo Unitario",
            "Costo Producción Total",
        ]
        tree = self._create_treeview(right, columns)

        # ===================== FUNCIONES =====================

        def fmt_cost(val):
            """Formatea los costos o muestra '-' si es nulo."""
            if val is None:
                return "-"
            try:
                return f"{float(val):.2f}"
            except Exception:
                return str(val)

        def cargar_categorias(event=None):
            """Carga las categorías según el tipo de producción."""
            tipo = entries["Tipo de Producción"].get()
            if tipo == "Plato":
                cursor.execute("SELECT NombreCategoria FROM CategoriaPlatos")
            elif tipo == "Bebida":
                cursor.execute("SELECT NombreCategoria FROM CategoriaBebidas")
            else:
                entries["Categoría"]["values"] = []
                return
            categorias = [row[0] for row in cursor.fetchall()]
            entries["Categoría"]["values"] = categorias
            if categorias:
                entries["Categoría"].set(categorias[0])

        entries["Tipo de Producción"].bind("<<ComboboxSelected>>", cargar_categorias)

        def cargar_produccion():
            """Carga correctamente los registros de Producción mostrando costos reales desde SQL."""
            for i in tree.get_children():
                tree.delete(i)

            query = """
            SELECT 
                P.IDProduccion,
                CASE 
                    WHEN MP.IDProduccion IS NOT NULL THEN 'Plato'
                    WHEN MB.IDProduccion IS NOT NULL THEN 'Bebida'
                    ELSE 'Sin tipo'
                END AS Tipo,
                COALESCE(CP.NombreCategoria, CB.NombreCategoria, 'Sin categoría') AS Categoria,
                COALESCE(MP.NombrePlato, MB.NombreBebida, 'Sin nombre') AS Nombre,
                COALESCE(P.CantidadDePlatos, P.CantidadDeBebidas, 0) AS Cantidad,
                CASE 
                    WHEN MP.IDProduccion IS NOT NULL THEN P.CostoPorPlato
                    WHEN MB.IDProduccion IS NOT NULL THEN P.CostoPorBebida
                    ELSE 0
                END AS CostoUnitario,
                P.CostoProduccionTotal AS CostoTotal
            FROM Produccion P
            LEFT JOIN MenuDePlatos MP ON MP.IDProduccion = P.IDProduccion
            LEFT JOIN CategoriaPlatos CP ON CP.IDCategoriaPlatos = MP.IDCategoriaPlatos
            LEFT JOIN MenuDeBebidas MB ON MB.IDProduccion = P.IDProduccion
            LEFT JOIN CategoriaBebidas CB ON CB.IDCategoriaBebidas = MB.IDCategoriaBebidas
            ORDER BY P.IDProduccion ASC;
            """

            cursor.execute(query)
            filas = cursor.fetchall()

            for row in filas:
                idp, tipo, categoria, nombre, cantidad, costo_unit, costo_total = row
                tree.insert(
                    "",
                    "end",
                    values=[
                        idp,
                        tipo,
                        categoria,
                        nombre,
                        int(cantidad),
                        f"{float(costo_unit or 0):.2f}",
                        f"{float(costo_total or 0):.2f}",
                    ],
                )

 # ---------- FUNCIONES CRUD ----------


        def agregar_produccion():
            try:
                tipo = entries["Tipo de Producción"].get()
                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                cantidad_str = entries["Cantidad"].get().strip()
                costo_str = entries["Costo Unitario"].get().strip()

                if (not tipo or not categoria or not nombre or not cantidad_str or not costo_str):
                    msg.showwarning("Atención", "Completa todos los campos.")
                    return

                if (not cantidad_str.isdigit() or not costo_str.replace(".", "", 1).isdigit()):
                    msg.showwarning("Atención", "Cantidad y costo deben ser numéricos.")
                    return

                cantidad = int(cantidad_str)
                costo_unit = float(costo_str)

                # Cálculo total
                costo_total = cantidad * costo_unit

                # Insert base
                cursor.execute("""
                    INSERT INTO Produccion (CantidadDeBebidas, CantidadDePlatos,
                                            NombreBebida, NombrePlato,
                                            CostoPorPlato, CostoPorBebida,
                                            CostoProduccionTotal)
                    VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                """)
                conexion.commit()

                cursor.execute("SELECT MAX(IDProduccion) FROM Produccion")
                id_prod = cursor.fetchone()[0]

                # Plato
                if tipo == "Plato":
                    cursor.execute("SELECT IDCategoriaPlatos FROM CategoriaPlatos WHERE NombreCategoria=?", (categoria,))
                    id_cat = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio)
                        VALUES (?, ?, ?, ?)
                    """, (id_prod, id_cat, nombre, costo_unit))

                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos=?, NombrePlato=?, CostoPorPlato=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """, (cantidad, nombre, costo_unit, costo_total, id_prod))

                # Bebida
                else:
                    cursor.execute("SELECT IDCategoriaBebidas FROM CategoriaBebidas WHERE NombreCategoria=?", (categoria,))
                    id_cat = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio)
                        VALUES (?, ?, ?, ?)
                    """, (id_prod, id_cat, nombre, costo_unit))

                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas=?, NombreBebida=?, CostoPorBebida=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """, (cantidad, nombre, costo_unit, costo_total, id_prod))

                conexion.commit()
                msg.showinfo("Éxito", "Registro agregado correctamente.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar el registro:\n{e}")


        def eliminar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Selecciona un registro para eliminar.")
                    return

                id_prod = int(tree.item(sel)["values"][0])

                cursor.execute("DELETE FROM MenuDePlatos WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM MenuDeBebidas WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM Produccion WHERE IDProduccion=?", (id_prod,))
                conexion.commit()

                msg.showinfo("Éxito", "Registro eliminado.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")


        def editar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Selecciona un registro para editar.")
                    return

                vals = tree.item(sel)["values"]
                id_prod = int(vals[0])

                tipo = entries["Tipo de Producción"].get()
                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                cantidad = int(entries["Cantidad"].get())
                costo_unit = float(entries["Costo Unitario"].get())
                costo_total = cantidad * costo_unit

                cursor.execute("DELETE FROM MenuDePlatos WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM MenuDeBebidas WHERE IDProduccion=?", (id_prod,))

                if tipo == "Plato":
                    cursor.execute("SELECT IDCategoriaPlatos FROM CategoriaPlatos WHERE NombreCategoria=?", (categoria,))
                    id_cat = cursor.fetchone()[0]

                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos=?, NombrePlato=?, CostoPorPlato=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """, (cantidad, nombre, costo_unit, costo_total, id_prod))

                    cursor.execute("""
                        INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio)
                        VALUES (?, ?, ?, ?)
                    """, (id_prod, id_cat, nombre, costo_unit))

                else:
                    cursor.execute("SELECT IDCategoriaBebidas FROM CategoriaBebidas WHERE NombreCategoria=?", (categoria,))
                    id_cat = cursor.fetchone()[0]

                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas=?, NombreBebida=?, CostoPorBebida=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """, (cantidad, nombre, costo_unit, costo_total, id_prod))

                    cursor.execute("""
                        INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio)
                        VALUES (?, ?, ?, ?)
                    """, (id_prod, id_cat, nombre, costo_unit))

                conexion.commit()
                msg.showinfo("Éxito", "Registro actualizado.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar el registro:\n{e}")


        # --- ASIGNAR BOTONES ---
        btn_agregar.config(command=agregar_produccion)
        btn_eliminar.config(command=eliminar_produccion)
        btn_editar.config(command=editar_produccion)

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
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
        conexion = self.conexion
        cursor = self.cursor

        # ---------- FUNCIONES CRUD ----------
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
                tree.insert(
                    "",
                    "end",
                    values=["—" if x is None else str(x).strip() for x in row],
                )

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
                        "Debe ingresar al menos el primer nombre y apellido.",
                    )
                    return
                if not telefono:
                    msg.showwarning("Atención", "Debe ingresar un número de teléfono.")
                    return

                # --- Insertar teléfono y obtener su ID de forma segura ---
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

        def eliminar_cliente():
            """Elimina el cliente seleccionado en la tabla."""
            try:
                seleccionado = tree.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Selecciona un cliente para eliminar.")
                    return

                id_cliente = tree.item(seleccionado)["values"][0]
                id_cliente = int(str(id_cliente).strip("(), '"))

                cursor.execute("DELETE FROM Clientes WHERE IDClientes = ?", id_cliente)
                conexion.commit()

                msg.showinfo("Éxito", "Cliente eliminado correctamente.")
                cargar_clientes()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar el cliente:\n{e}")

        def editar_cliente():
            """Edita el cliente seleccionado."""
            try:
                seleccionado = tree.selection()
                if not seleccionado:
                    msg.showwarning("Atención", "Selecciona un cliente para editar.")
                    return

                id_cliente = tree.item(seleccionado)["values"][0]
                id_cliente = int(str(id_cliente).strip("(), '"))

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
                        "Debe ingresar al menos el primer nombre y apellido.",
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

        def limpiar_campos():
            """Limpia todos los campos de entrada."""
            for e in entries.values():
                e.delete(0, tk.END)

        # ---------- ASIGNAR BOTONES ----------
        btn_agregar.config(command=agregar_cliente)
        btn_eliminar.config(command=eliminar_cliente)
        btn_limpiar.config(command=limpiar_campos)
        btn_editar.config(command=editar_cliente)

        # ---------- Cargar datos al inicio ----------
        cargar_clientes()

    # ---------------- ---------------------------TAB VENTAS ----------------
    def _create_tab_ventas(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ventas")

        self._create_tab_content(
            frame,
            "Registro de Ventas",
            [
                "Monto Total",
                "Pérdidas",
                "Ganancias",
                "Hora",
                "Día",
                "Mes",
                "Año",
                "ID Cliente",
                "ID Menú Bebidas",
                "ID Menú Platos",
                "Cantidad",
            ],
            [
                "IDVenta",
                "Monto Total",
                "Pérdidas",
                "Ganancias",
                "Hora",
                "Día",
                "Mes",
                "Año",
                "IDCliente",
                "IDMenuBebidas",
                "IDMenuPlatos",
                "Cantidad",
            ],
        )


# ----------------------- MAIN ---------------------------------------------------
if __name__ == "__main__":
    app = RestauranteUI()
    app.mainloop()
