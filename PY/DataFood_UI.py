import tkinter as tk
from tkinter import ttk
from datetime import datetime
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
    LEFT_PANEL_WIDTH = 260

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
            text="  DataFood  |  Sistema de Gestión de Restaurante",
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

        ttk.Button(self.sidebar, text="Pedidos (próximamente)").pack(
            fill="x", padx=15, pady=5
        )
        ttk.Button(self.sidebar, text="Reportes (próximamente)").pack(
            fill="x", padx=15, pady=5
        )

        # ------------------ ZONA CENTRAL DINÁMICA ----------------
        self.center_frame = tk.Frame(main_content, bg="#FFFFFF")
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # ------------------ COLUMNA DERECHA (SOLO PARA INICIO) ----------------
        self.right_panel = tk.Frame(main_content, bg="#F5F1E8", width=260)
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
        ).pack(padx=10, pady=5)

        # estado de paneles
        self.sidebar_visible = True
        self.right_panel_visible = True  # <- importante

        # al iniciar, mostramos el “Menú de Platos y Bebidas”
        self._mostrar_dashboard_inicial()

    # ------------------------------------------------------------------
    # PÁGINA DE INICIO (MENÚ DE PLATOS Y BEBIDAS)
    # ------------------------------------------------------------------
    def _mostrar_dashboard_inicial(self):
        """Contenido central por defecto: Menú de Platos y Bebidas."""
        # Asegurar que el panel derecho esté visible en el INICIO
        if not getattr(self, "right_panel_visible", False):
            self.right_panel.pack(side="left", fill="y")
            self.right_panel.pack_propagate(False)
            self.right_panel_visible = True

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
            text="aqui vas a poner los cruds de los menus\n"
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
            text="(Aquí el menu plato )",
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
            text="(Aquí poner  una cuadrícula de bebidas con foto, nombre y precio.)",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=10, pady=5)

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

        # Canvas + scrollbar para poder desplazar campos y botones
                # Canvas + scrollbar para poder desplazar campos y botones
        canvas = tk.Canvas(left_container, bg="#E9E2D0", highlightthickness=0)

        # ⬇️ Scrollbar VISIBLE, igual que la del Treeview
        scrollbar_left = tk.Scrollbar(
            left_container,
            orient="vertical",
            command=canvas.yview
        )

        # primero el scrollbar a la derecha, luego el canvas
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

        # ---------------- TAB INSUMOS ----------------
    def _create_tab_insumos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Insumos")

        conexion = conectar()
        cursor = conexion.cursor()

        # --------- Definimos los campos del formulario ---------
        labels = [
            "Categoría",
            "Nombre del Insumo",
            "Cantidad Disponible",
            "Cantidad Dañada",
            "Proveedor",
            "Precio Compra",
            "Cantidad Comprada",
            "Fecha de Ingreso (DD/MM/AAAA)",
        ]

        columns = [
            "ID", "Categoría", "Nombre", "Disponible",
            "Dañada", "Proveedor", "Precio Compra",
            "Cantidad Comprada", "Fecha"
        ]

        # Fábrica para crear Combobox
        def make_combo(parent):
            return ttk.Combobox(parent, state="readonly")

        special = {
            "Categoría": make_combo,
            "Proveedor": make_combo,
        }

        # Usamos la función genérica de molde
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
        self.combo_proveedores_insumos = entries["Proveedor"]

        # Ocultar columnas a partir de "Dañada" en el Treeview (si quieres que se vean menos)
        for col in ("Dañada", "Proveedor", "Precio Compra", "Cantidad Comprada", "Fecha"):
            tree.column(col, width=0, stretch=False)

        # ========== CARGAR COMBOS DESDE BD ==========
        cursor.execute("SELECT NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria")
        combo_categoria["values"] = [row[0] for row in cursor.fetchall()]

        # Cargar proveedores globalmente y llenar el combo
        self.cargar_proveedores_global()
        self.combo_proveedores_insumos["values"] = [p[1] for p in self.lista_proveedores]

        # ============================================================
        # VENTANA DE DETALLE AL HACER DOBLE CLIC
        # ============================================================
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

            # ----- botón EDITAR (rellena formulario de la izquierda) -----
            def preparar_edicion():
                cat, nombre, disp, dan, prov, precio, cant, fecha = (
                    safe(vals[1]), safe(vals[2]), safe(vals[3]), safe(vals[4]),
                    safe(vals[5]), safe(vals[6]), safe(vals[7]), safe(vals[8])
                )

                combo_categoria.set("" if cat == "—" else cat)
                entries["Nombre del Insumo"].delete(0, tk.END)
                entries["Nombre del Insumo"].insert(0, "" if nombre == "—" else nombre)

                entries["Cantidad Disponible"].delete(0, tk.END)
                entries["Cantidad Disponible"].insert(0, "" if disp == "—" else disp)

                entries["Cantidad Dañada"].delete(0, tk.END)
                entries["Cantidad Dañada"].insert(0, "" if dan == "—" else dan)

                self.combo_proveedores_insumos.set("" if prov == "—" else prov)

                entries["Precio Compra"].delete(0, tk.END)
                entries["Precio Compra"].insert(0, "" if precio == "—" else precio)

                entries["Cantidad Comprada"].delete(0, tk.END)
                entries["Cantidad Comprada"].insert(0, "" if cant == "—" else cant)

                entries["Fecha de Ingreso (DD/MM/AAAA)"].delete(0, tk.END)
                entries["Fecha de Ingreso (DD/MM/AAAA)"].insert(0, "" if fecha == "—" else fecha)

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

        # ============================================================
        # FUNCIONES CRUD
        # ============================================================
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

        def agregar_insumo():
            try:
                categoria = entries["Categoría"].get()
                nombre = entries["Nombre del Insumo"].get().strip()
                disp = entries["Cantidad Disponible"].get().strip()
                danio = entries["Cantidad Dañada"].get().strip()
                proveedor = entries["Proveedor"].get()
                precio = entries["Precio Compra"].get().strip()
                comprada = entries["Cantidad Comprada"].get().strip()
                fecha = entries["Fecha de Ingreso (DD/MM/AAAA)"].get().strip()

                if not categoria or not nombre or not disp.isdigit() or not comprada.isdigit() or not precio.replace(".", "", 1).isdigit():
                    msg.showwarning("Atención", "Complete todos los campos obligatorios.")
                    return

                disp = int(disp)
                danio = int(danio) if danio.isdigit() else 0
                comprada = int(comprada)
                precio = float(precio)

                cursor.execute("SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?", (categoria,))
                id_cat = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO Insumos (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada)
                    VALUES (?, ?, ?, ?)
                """, (id_cat, nombre, disp, danio))
                conexion.commit()

                cursor.execute("SELECT MAX(IDInsumos) FROM Insumos")
                id_insumo = cursor.fetchone()[0]

                cursor.execute("SELECT IDProveedor FROM Proveedores WHERE NombreProveedor=?", (proveedor,))
                id_prov = cursor.fetchone()[0]

                try:
                    dia, mes, ano = map(int, fecha.split("/"))
                except:
                    dia = mes = ano = None

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

        def editar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    return msg.showwarning("Atención", "Seleccione un insumo.")

                id_ins = tree.item(sel)["values"][0]

                categoria = entries["Categoría"].get()
                nombre = entries["Nombre del Insumo"].get().strip()
                disp = entries["Cantidad Disponible"].get().strip()
                danio = entries["Cantidad Dañada"].get().strip()
                proveedor = entries["Proveedor"].get()
                precio = entries["Precio Compra"].get().strip()
                comprada = entries["Cantidad Comprada"].get().strip()
                fecha = entries["Fecha de Ingreso (DD/MM/AAAA)"].get().strip()

                if not categoria or not nombre or not disp.isdigit():
                    return msg.showwarning("Atención", "Complete todos los campos.")

                disp = int(disp)
                danio = int(danio) if danio.isdigit() else 0
                precio = float(precio)
                comprada = int(comprada)

                cursor.execute("SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?", (categoria,))
                id_cat = cursor.fetchone()[0]

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
        btn_editar.config(text="Guardar cambios", command=editar_insumo)

        def limpiar_campos():
            for k, w in entries.items():
                if isinstance(w, ttk.Entry):
                    w.delete(0, tk.END)
                elif isinstance(w, ttk.Combobox):
                    w.set("")

        btn_limpiar.config(command=limpiar_campos)

        cargar_insumos()


 # -----------------------------PRODUCCION 
    # --------------------------------------------------------- TAB PRODUCCIÓN ----------------
    def _create_tab_produccion(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Producción")

        conexion = conectar()
        cursor = conexion.cursor()

        # --------- Campos del formulario ---------
        labels = [
            "Tipo de Producción",
            "Categoría",
            "Nombre",
            "Cantidad",
            "Costo Unitario",
        ]

        columns = [
            "IDProduccion",
            "Tipo",
            "Categoría",
            "Nombre",
            "Cantidad",
            "Costo Unitario",
            "Costo Producción Total",
        ]

        # Combobox para Tipo y Categoría
        def make_combo(parent):
            return ttk.Combobox(parent, state="readonly")

        special = {
            "Tipo de Producción": make_combo,
            "Categoría": make_combo,
        }

        # ---------- Usamos el helper genérico ----------
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = (
            self._create_tab_content(
                frame,
                "Registro de Producción",
                labels,
                columns,
                special_widgets=special,
            )
        )

        combo_tipo = entries["Tipo de Producción"]
        combo_categoria = entries["Categoría"]

        combo_tipo["values"] = ["Plato", "Bebida"]

        # ================= CARGAR CATEGORÍAS SEGÚN TIPO =================
        def cargar_categorias(event=None):
            tipo = combo_tipo.get()
            if tipo == "Plato":
                cursor.execute(
                    "SELECT NombreCategoria FROM CategoriaPlatos ORDER BY NombreCategoria"
                )
            elif tipo == "Bebida":
                cursor.execute(
                    "SELECT NombreCategoria FROM CategoriaBebidas ORDER BY NombreCategoria"
                )
            else:
                combo_categoria["values"] = []
                combo_categoria.set("")
                return

            categorias = [row[0] for row in cursor.fetchall()]
            combo_categoria["values"] = categorias
            if categorias:
                combo_categoria.set(categorias[0])

        combo_tipo.bind("<<ComboboxSelected>>", cargar_categorias)

        # ================= VENTANA DE DETALLE (DOBLE CLIC) =================
        def mostrar_detalle_produccion(event=None):
            sel = tree.selection()
            if not sel:
                return

            vals = tree.item(sel)["values"]
            if not vals:
                return

            idp, tipo, categoria, nombre, cantidad, costo_unit, costo_total = vals

            def safe(v):
                return "—" if v in (None, "", "—") else v

            detalle = tk.Toplevel(self)
            detalle.title(f"Detalle de producción #{safe(idp)}")
            detalle.configure(bg="#F5F1E8")

            ancho_ventana = 480
            alto_ventana = 280
            detalle.geometry(f"{ancho_ventana}x{alto_ventana}")
            detalle.minsize(440, 260)

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
                text=f"Producción: {safe(nombre)}",
                bg="#FDF7EA",
                fg="#333333",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, columnspan=2, pady=(5, 5), padx=5, sticky="w")

            ttk.Separator(content, orient="horizontal").grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 8)
            )

            datos = [
                ("ID Producción", safe(idp)),
                ("Tipo", safe(tipo)),
                ("Categoría", safe(categoria)),
                ("Nombre", safe(nombre)),
                ("Cantidad", safe(cantidad)),
                ("Costo unitario", safe(costo_unit)),
                ("Costo total producción", safe(costo_total)),
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
                combo_tipo.set("" if safe(tipo) == "—" else tipo)
                # recargar categorías para ese tipo
                cargar_categorias()
                combo_categoria.set("" if safe(categoria) == "—" else categoria)

                entries["Nombre"].delete(0, tk.END)
                entries["Nombre"].insert(0, "" if safe(nombre) == "—" else nombre)

                entries["Cantidad"].delete(0, tk.END)
                entries["Cantidad"].insert(0, "" if safe(cantidad) == "—" else cantidad)

                entries["Costo Unitario"].delete(0, tk.END)
                entries["Costo Unitario"].insert(
                    0, "" if safe(costo_unit) == "—" else costo_unit
                )

                detalle.destroy()

            btn_editar_detalle = ttk.Button(
                content, text="Editar este registro", command=preparar_edicion
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

        tree.bind("<Double-1>", mostrar_detalle_produccion)

        # ================= CARGAR PRODUCCIÓN =================
        def cargar_produccion():
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

        # ================= FUNCIONES CRUD =================

        def agregar_produccion():
            try:
                tipo = combo_tipo.get()
                categoria = combo_categoria.get()
                nombre = entries["Nombre"].get().strip()
                cantidad_str = entries["Cantidad"].get().strip()
                costo_str = entries["Costo Unitario"].get().strip()

                if (
                    not tipo
                    or not categoria
                    or not nombre
                    or not cantidad_str
                    or not costo_str
                ):
                    msg.showwarning("Atención", "Completa todos los campos.")
                    return

                if not cantidad_str.isdigit() or not costo_str.replace(".", "", 1).isdigit():
                    msg.showwarning(
                        "Atención", "Cantidad y costo unitario deben ser numéricos."
                    )
                    return

                cantidad = int(cantidad_str)
                costo_unit = float(costo_str)
                costo_total = cantidad * costo_unit

                # Insert base en Produccion
                cursor.execute(
                    """
                    INSERT INTO Produccion (
                        CantidadDeBebidas, CantidadDePlatos,
                        NombreBebida, NombrePlato,
                        CostoPorPlato, CostoPorBebida,
                        CostoProduccionTotal
                    )
                    VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                """
                )
                conexion.commit()

                cursor.execute("SELECT MAX(IDProduccion) FROM Produccion")
                id_prod = cursor.fetchone()[0]

                if tipo == "Plato":
                    cursor.execute(
                        "SELECT IDCategoriaPlatos FROM CategoriaPlatos WHERE NombreCategoria=?",
                        (categoria,),
                    )
                    id_cat = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio)
                        VALUES (?, ?, ?, ?)
                    """,
                        (id_prod, id_cat, nombre, costo_unit),
                    )

                    cursor.execute(
                        """
                        UPDATE Produccion
                        SET CantidadDePlatos=?, NombrePlato=?, CostoPorPlato=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """,
                        (cantidad, nombre, costo_unit, costo_total, id_prod),
                    )

                elif tipo == "Bebida":
                    cursor.execute(
                        "SELECT IDCategoriaBebidas FROM CategoriaBebidas WHERE NombreCategoria=?",
                        (categoria,),
                    )
                    id_cat = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio)
                        VALUES (?, ?, ?, ?)
                    """,
                        (id_prod, id_cat, nombre, costo_unit),
                    )

                    cursor.execute(
                        """
                        UPDATE Produccion
                        SET CantidadDeBebidas=?, NombreBebida=?, CostoPorBebida=?, CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """,
                        (cantidad, nombre, costo_unit, costo_total, id_prod),
                    )

                conexion.commit()
                msg.showinfo("Éxito", "Registro de producción agregado correctamente.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar el registro:\n{e}")

        def eliminar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning(
                        "Atención", "Selecciona un registro de producción para eliminar."
                    )
                    return

                id_prod = int(tree.item(sel)["values"][0])

                cursor.execute("DELETE FROM MenuDePlatos WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM MenuDeBebidas WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM Produccion WHERE IDProduccion=?", (id_prod,))
                conexion.commit()

                msg.showinfo("Éxito", "Registro eliminado.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar el registro:\n{e}")

        def editar_produccion():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning(
                        "Atención", "Selecciona un registro de producción para editar."
                    )
                    return

                id_prod = int(tree.item(sel)["values"][0])

                tipo = combo_tipo.get()
                categoria = combo_categoria.get()
                nombre = entries["Nombre"].get().strip()
                cantidad_str = entries["Cantidad"].get().strip()
                costo_str = entries["Costo Unitario"].get().strip()

                if (
                    not tipo
                    or not categoria
                    or not nombre
                    or not cantidad_str
                    or not costo_str
                ):
                    msg.showwarning("Atención", "Completa todos los campos.")
                    return

                if not cantidad_str.isdigit() or not costo_str.replace(".", "", 1).isdigit():
                    msg.showwarning(
                        "Atención", "Cantidad y costo unitario deben ser numéricos."
                    )
                    return

                cantidad = int(cantidad_str)
                costo_unit = float(costo_str)
                costo_total = cantidad * costo_unit

                # Limpiar vínculos en menús
                cursor.execute("DELETE FROM MenuDePlatos WHERE IDProduccion=?", (id_prod,))
                cursor.execute("DELETE FROM MenuDeBebidas WHERE IDProduccion=?", (id_prod,))

                if tipo == "Plato":
                    cursor.execute(
                        "SELECT IDCategoriaPlatos FROM CategoriaPlatos WHERE NombreCategoria=?",
                        (categoria,),
                    )
                    id_cat = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        UPDATE Produccion
                        SET CantidadDePlatos=?, NombrePlato=?, CostoPorPlato=?, 
                            CantidadDeBebidas=NULL, NombreBebida=NULL, CostoPorBebida=NULL,
                            CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """,
                        (cantidad, nombre, costo_unit, costo_total, id_prod),
                    )

                    cursor.execute(
                        """
                        INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio)
                        VALUES (?, ?, ?, ?)
                    """,
                        (id_prod, id_cat, nombre, costo_unit),
                    )

                elif tipo == "Bebida":
                    cursor.execute(
                        "SELECT IDCategoriaBebidas FROM CategoriaBebidas WHERE NombreCategoria=?",
                        (categoria,),
                    )
                    id_cat = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        UPDATE Produccion
                        SET CantidadDeBebidas=?, NombreBebida=?, CostoPorBebida=?, 
                            CantidadDePlatos=NULL, NombrePlato=NULL, CostoPorPlato=NULL,
                            CostoProduccionTotal=?
                        WHERE IDProduccion=?
                    """,
                        (cantidad, nombre, costo_unit, costo_total, id_prod),
                    )

                    cursor.execute(
                        """
                        INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio)
                        VALUES (?, ?, ?, ?)
                    """,
                        (id_prod, id_cat, nombre, costo_unit),
                    )

                conexion.commit()
                msg.showinfo("Éxito", "Registro actualizado.")
                cargar_produccion()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar el registro:\n{e}")

        def limpiar_campos():
            for k, w in entries.items():
                if isinstance(w, ttk.Entry):
                    w.delete(0, tk.END)
                elif isinstance(w, ttk.Combobox):
                    w.set("")

        # ---------- Asignar botones ----------
        btn_agregar.config(command=agregar_produccion)
        btn_eliminar.config(command=eliminar_produccion)
        btn_editar.config(text="Guardar cambios", command=editar_produccion)
        btn_limpiar.config(command=limpiar_campos)

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
