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

            # ============================================================
            # FUNCIONES CRUD
            # ============================================================
            def cargar_insumos():
                # Limpiar tree
                for item in tree.get_children():
                    tree.delete(item)

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
                                ORDER BY
                                    PI.Ano DESC,
                                    PI.Mes DESC,
                                    PI.Dia DESC,
                                    PI.IDProveedoresInsumos DESC
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
                        ON UC.IDInsumos = I.IDInsumos
                    AND UC.rn = 1        -- solo la última compra
                    LEFT JOIN Proveedores P
                        ON P.IDProveedor = UC.IDProveedor
                    ORDER BY I.IDInsumos ASC;
                """)

                for row in cursor.fetchall():
                    (id_in, cat, nombre, disp, danio,
                    proveedor, precio, cant_comp,
                    dia, mes, ano) = row

                    fecha = f"{dia}/{mes}/{ano}" if dia and mes and ano else "—"

                    tree.insert(
                        "", "end",
                        values=[
                            id_in,
                            cat,
                            nombre,
                            disp,
                            danio,
                            proveedor or "—",
                            precio if precio is not None else "—",
                            cant_comp if cant_comp is not None else "—",
                            fecha
                        ]
                    )


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

            # Asignar CRUD
            btn_agregar.config(command=agregar_insumo)
            btn_eliminar.config(command=eliminar_insumo)
            btn_editar.config(text="Guardar cambios", command=editar_insumo)
            btn_limpiar.config(command=limpiar_campos)

            cargar_insumos()



   
        # -------------------------------------------------- TAB PRODUCCIÓN ----------------
    def _create_tab_produccion(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Producción")

        # Panel base reutilizable
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = self._create_tab_content(
            frame,
            "Registro de Producción",
            ["Tipo de Producción", "Categoría", "Nombre", "Cantidad", "Costo Unitario"],
            ["IDProduccion", "Tipo", "Categoría", "Nombre", "Cantidad", "Costo Unitario"]
        )

        conexion = conectar()
        cursor = conexion.cursor()

        # ---------------- Helpers básicos ----------------
        def limpiar_valor(v):
            if v is None:
                return ""
            v = str(v)
            return v.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()

        # ---------------- Cargar cat. desde BD ----------------
        cursor.execute("SELECT IDCategoriaPlatos, NombreCategoria FROM CategoriaPlatos ORDER BY NombreCategoria;")
        categorias_platos = cursor.fetchall()
        cat_platos_nombres = [c[1] for c in categorias_platos]
        id_cat_plato_por_nombre = {c[1]: c[0] for c in categorias_platos}

        cursor.execute("SELECT IDCategoriaBebidas, NombreCategoria FROM CategoriaBebidas ORDER BY NombreCategoria;")
        categorias_bebidas = cursor.fetchall()
        cat_bebidas_nombres = [c[1] for c in categorias_bebidas]
        id_cat_bebida_por_nombre = {c[1]: c[0] for c in categorias_bebidas}

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
        def cargar_nombres():
            """Rellena el combo de nombres según el tipo."""
            tipo = cmb_tipo.get()
            if tipo == "Plato":
                cursor.execute("""
                    SELECT DISTINCT NombrePlato
                    FROM Produccion
                    WHERE NombrePlato IS NOT NULL
                    ORDER BY NombrePlato;
                """)
            elif tipo == "Bebida":
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
            tipo = cmb_tipo.get()
            if tipo == "Plato":
                cmb_categoria["values"] = cat_platos_nombres
            elif tipo == "Bebida":
                cmb_categoria["values"] = cat_bebidas_nombres
            else:
                cmb_categoria["values"] = ()
            cmb_categoria.set("")
            cargar_nombres()

        cmb_tipo.bind("<<ComboboxSelected>>", actualizar_categorias)

        # Valor inicial
        cmb_tipo.set("Plato")
        actualizar_categorias()

        # ---------------- Cargar producción en el TreeView ----------------
        def cargar_produccion():
            for fila in tree.get_children():
                tree.delete(fila)

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
                    -- 👇 Fecha formateada dd/mm/aaaa usando las columnas Dia, Mes, Ano
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
                tree.insert("", "end", values=limpio)

            cargar_nombres()

        # ---------------- AGREGAR: registrar stock ----------------
                # ---------------- AGREGAR: registrar stock ----------------
        def agregar_produccion():
            try:
                tipo = cmb_tipo.get().strip()
                categoria = cmb_categoria.get().strip()
                nombre = cmb_nombre.get().strip()
                cant_txt = entries["Cantidad"].get().strip()
                costo_txt = entries["Costo Unitario"].get().strip()

                if tipo not in ("Plato", "Bebida"):
                    return msg.showwarning("Atención", "Seleccione el tipo de producción.")
                if not categoria:
                    return msg.showwarning("Atención", "Seleccione la categoría.")
                if not nombre:
                    return msg.showwarning("Atención", "Seleccione el nombre.")
                if not cant_txt or not costo_txt:
                    return msg.showwarning("Atención", "Ingrese cantidad y costo unitario.")

                try:
                    cantidad = int(cant_txt)
                    costo_unit = float(costo_txt)
                except ValueError:
                    return msg.showwarning("Atención", "Cantidad y costo deben ser numéricos.")

                if cantidad <= 0:
                    return msg.showwarning("Atención", "La cantidad debe ser mayor que cero.")
                if costo_unit < 0:
                    return msg.showwarning("Atención", "El costo no puede ser negativo.")

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
                            CostoPorPlato = ?,
                            CostoProduccionTotal = ISNULL(CostoProduccionTotal,0) + (? * ?),
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, costo_unit, cantidad, costo_unit, id_prod))
                else:
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas = ISNULL(CantidadDeBebidas,0) + ?,
                            CostoPorBebida = ?,
                            CostoProduccionTotal = ISNULL(CostoProduccionTotal,0) + (? * ?),
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, costo_unit, cantidad, costo_unit, id_prod))

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
                costo_txt = entries["Costo Unitario"].get().strip()

                if not cant_txt or not costo_txt:
                    return msg.showwarning("Atención", "Ingrese cantidad y costo unitario.")

                try:
                    cantidad = int(cant_txt)
                    costo_unit = float(costo_txt)
                except ValueError:
                    return msg.showwarning("Atención", "Cantidad y costo deben ser numéricos.")

                if cantidad < 0:
                    return msg.showwarning("Atención", "La cantidad no puede ser negativa.")
                if costo_unit < 0:
                    return msg.showwarning("Atención", "El costo no puede ser negativo.")

                if tipo == "Plato":
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDePlatos = ?,
                            CostoPorPlato = ?,
                            CostoProduccionTotal = ? * ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, costo_unit, cantidad, costo_unit, id_prod))
                else:
                    cursor.execute("""
                        UPDATE Produccion
                        SET CantidadDeBebidas = ?,
                            CostoPorBebida = ?,
                            CostoProduccionTotal = ? * ?,
                            Dia = DAY(GETDATE()),
                            Mes = MONTH(GETDATE()),
                            Ano = YEAR(GETDATE())
                        WHERE IDProduccion = ?;
                    """, (cantidad, costo_unit, cantidad, costo_unit, id_prod))

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

            main = tk.Frame(ventana, bg="#FDF7EA", bd=1, relief="solid")
            main.pack(fill="both", expand=True, padx=10, pady=10)

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

            # Imagen
            tk.Label(main, text="Imagen:", bg="#FDF7EA",
                     fg="#333333", font=("Segoe UI", 10)
                     ).grid(row=row, column=0, sticky="e", padx=10, pady=3)

            lbl_imagen_info = tk.Label(
                main,
                text="(Sin imagen seleccionada)",
                bg="#FDF7EA",
                fg="#777777",
                font=("Segoe UI", 9, "italic"),
                anchor="w",
            )
            lbl_imagen_info.grid(row=row + 1, column=1, sticky="w", padx=10, pady=(0, 5))

            imagen_bytes = {"data": None}

            def seleccionar_imagen():
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
                        imagen_bytes["data"] = f.read()
                    lbl_imagen_info.config(text=os.path.basename(ruta), fg="#333333",
                                           font=("Segoe UI", 9, "normal"))
                except Exception as e:
                    msg.showerror("Error", f"No se pudo leer la imagen:\n{e}")

            btn_sel_imagen = tk.Button(
                main,
                text="Seleccionar imagen...",
                bg="#E5D8B4",
                fg="#333333",
                activebackground="#D9C79A",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                command=seleccionar_imagen,
            )
            btn_sel_imagen.grid(row=row, column=1, columnspan=2,
                                sticky="w", padx=10, pady=3)
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

            btn_cancelar.grid(row=row, column=1, sticky="e", padx=10, pady=(8, 10))
            btn_guardar.grid(row=row, column=2, sticky="w", padx=10, pady=(8, 10))

            def guardar_nueva_produccion():
                try:
                    tipo_n = cmb_tipo_nuevo.get().strip()
                    categoria_n = cmb_categoria_nuevo.get().strip()
                    nombre_n = txt_nombre_nuevo.get().strip()
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
