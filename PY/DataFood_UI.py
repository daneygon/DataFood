from conexion_db import conectar  # type: ignore
import tkinter.messagebox as msg


import tkinter as tk
from tkinter import ttk


class RestauranteUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---------- Ventana principal ---------------
        self.title("Sistema de Gestión de Restaurante - DataFood")
        self.geometry("1200x700")
        self.configure(bg="#F5F1E8")

        # --------------- Estilo ------------------
        self._apply_style()

        # --------------- Encabezado ------------------
        header = tk.Frame(self, bg="#C8B88A", height=50)
        header.pack(side="top", fill="x")
        tk.Label(
            header,
            text="  DataFood  |  Sistema de Gestión de Restaurante",
            bg="#C8B88A",
            fg="#ffffff",
            font=("Segoe UI", 15, "bold"),
        ).pack(pady=5)

        # -------- Notebook (Tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self._create_tab_proveedores(notebook)
        self._create_tab_insumos(notebook)
        self._create_tab_produccion(notebook)
        self._create_tab_menu_platos(notebook)
        self._create_tab_menu_bebidas(notebook)
        self._create_tab_clientes(notebook)
        self._create_tab_ventas(notebook)
   

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
    
    # ---------------- ------------------------------------------------------------------------TAB PROVEEDORES ----------------
    def _create_tab_proveedores(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Proveedores")

        # Crear seccion con los widgets
        entries, tree, btn_agregar, btn_editar, btn_eliminar, btn_limpiar = self._create_tab_content(
            frame,
            "Gestión de Proveedores",
            ["Nombre Proveedor", "Teléfono"],
            ["IDProveedor", "Nombre Proveedor", "Teléfono"]
        )

        conexion = conectar()
        cursor = conexion.cursor()

        # --------------- FUNCIONES INTERNAS -------------------

        def limpiar_valor(v):
            """Limpia '(1,' 'lol',' etc."""
            if v is None:
                return ""
            v = str(v)
            return v.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()

        # ------------------ Cargar Proveedores ------------------
        def cargar_proveedores():
            for fila in tree.get_children():
                tree.delete(fila)

            cursor.execute("""
                SELECT P.IDProveedor,
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

        # ------------------ Agregar Proveedor ------------------
        def agregar_proveedor():
            try:
                nombre = entries["Nombre Proveedor"].get().strip()
                telefono = entries["Teléfono"].get().strip()

                if not nombre:
                    msg.showwarning("Atención", "Debe ingresar el nombre del proveedor.")
                    return
                if not telefono:
                    msg.showwarning("Atención", "Debe ingresar un número de teléfono.")
                    return

                # Insertar teléfono y obtener ID
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

        # ------------------ Eliminar Proveedor ------------------
        def eliminar_proveedor():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Seleccione un proveedor para eliminar.")
                    return

                vals = tree.item(sel)["values"]
                id_prov = int(limpiar_valor(vals[0]))

                cursor.execute("SELECT IDTelefonoProveedores FROM Proveedores WHERE IDProveedor = ?", id_prov)
                id_tel = cursor.fetchone()[0]

                cursor.execute("DELETE FROM Proveedores WHERE IDProveedor = ?", id_prov)
                cursor.execute("DELETE FROM TelefonoProveedores WHERE IDTelefonoProveedores = ?", id_tel)

                conexion.commit()
                msg.showinfo("Éxito", "Proveedor eliminado correctamente.")
                cargar_proveedores()

            except Exception as e:
                msg.showerror("Error", f"No se pudo eliminar:\n{e}")

        # ------------------ Editar Proveedor ------------------
        def editar_proveedor():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Seleccione un proveedor para editar.")
                    return

                vals = tree.item(sel)["values"]
                id_prov = int(limpiar_valor(vals[0]))

                nombre = entries["Nombre Proveedor"].get().strip()
                telefono = entries["Teléfono"].get().strip()

                cursor.execute("SELECT IDTelefonoProveedores FROM Proveedores WHERE IDProveedor = ?", id_prov)
                id_tel = cursor.fetchone()[0]

                cursor.execute("""
                    UPDATE Proveedores
                    SET NombreProveedor = ?
                    WHERE IDProveedor = ?
                """, (nombre, id_prov))

                cursor.execute("""
                    UPDATE TelefonoProveedores
                    SET Telefono = ?
                    WHERE IDTelefonoProveedores = ?
                """, (telefono, id_tel))

                conexion.commit()
                msg.showinfo("Éxito", "Proveedor actualizado correctamente.")
                cargar_proveedores()

            except Exception as e:
                msg.showerror("Error", f"No se pudo editar:\n{e}")

        # ------------------ Limpiar campos ------------------
        def limpiar():
            for e in entries.values():
                e.delete(0, tk.END)

        # ------------------ Asignar botones ------------------
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

        # Panel izquierdo
        left = tk.Frame(main_frame, bg="#E9E2D0", padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="📦 Insumos", bg="#E9E2D0",
                font=("Segoe UI", 12, "bold"), fg="#6A4E23").pack(pady=(0, 10))

        # Campos
        entries = {}

        # ---- CATEGORÍA (Combobox normal)
        tk.Label(left, text="Categoría:", bg="#E9E2D0", font=("Segoe UI", 10)).pack(anchor="w")
        combo_categoria = ttk.Combobox(left, state="readonly")
        combo_categoria.pack(fill="x", pady=2)
        entries["Categoría"] = combo_categoria

        cursor.execute("SELECT NombreCategoria FROM CategoriaInsumos ORDER BY NombreCategoria")
        categorias = [row[0] for row in cursor.fetchall()]
        combo_categoria["values"] = categorias

        # ---- Nombre
        tk.Label(left, text="Nombre:", bg="#E9E2D0", font=("Segoe UI", 10)).pack(anchor="w")
        entry = ttk.Entry(left)
        entry.pack(fill="x", pady=2)
        entries["Nombre"] = entry

        # ---- Cantidad Disponible
        tk.Label(left, text="Cantidad Disponible:", bg="#E9E2D0", font=("Segoe UI", 10)).pack(anchor="w")
        entry = ttk.Entry(left)
        entry.pack(fill="x", pady=2)
        entries["Cantidad Disponible"] = entry

        # ---- Cantidad Dañada
        tk.Label(left, text="Cantidad Dañada (opcional):", bg="#E9E2D0", font=("Segoe UI", 10)).pack(anchor="w")
        entry = ttk.Entry(left)
        entry.pack(fill="x", pady=2)
        entries["Cantidad Dañada"] = entry

        # ---- BOTONES
        btn_frame = tk.Frame(left, bg="#E9E2D0")
        btn_frame.pack(pady=10, fill="x")

        btn_agregar = ttk.Button(btn_frame, text="Agregar")
        btn_agregar.pack(fill="x", pady=2)
        btn_editar = ttk.Button(btn_frame, text="Editar")
        btn_editar.pack(fill="x", pady=2)
        btn_eliminar = ttk.Button(btn_frame, text="Eliminar")
        btn_eliminar.pack(fill="x", pady=2)
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar",
                                command=lambda: [e.delete(0, tk.END) for e in entries.values() if isinstance(e, ttk.Entry)])
        btn_limpiar.pack(fill="x", pady=2)

        # ---- Tabla derecha
        right = ttk.Frame(main_frame)
        right.pack(side="right", fill="both", expand=True)

        columns = ["IDInsumos", "Categoría", "Nombre", "Cantidad Disponible", "Cantidad Dañada"]
        tree = self._create_treeview(right, columns)

        # ===================== FUNCIONES =====================

        def cargar_insumos():
            for i in tree.get_children():
                tree.delete(i)

            cursor.execute("""
                SELECT 
                    I.IDInsumos,
                    C.NombreCategoria,
                    I.NombreInsumo,
                    I.CantidadDisponible,
                    I.CantidadDañada
                FROM Insumos I
                JOIN CategoriaInsumos C
                    ON C.IDCategoriaInsumos = I.IDCategoriaInsumos
                ORDER BY I.IDInsumos ASC
            """)

            for row in cursor.fetchall():
                tree.insert("", "end", values=list(row))

        def agregar_insumo():
            try:
                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                cant = entries["Cantidad Disponible"].get().strip()
                danio = entries["Cantidad Dañada"].get().strip()

                if not categoria or not nombre or not cant.isdigit():
                    msg.showwarning("Atención", "Completa categoría, nombre y cantidad disponible.")
                    return

                danio = int(danio) if danio.isdigit() else 0

                cursor.execute("SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?", categoria)
                id_cat = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO Insumos (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada)
                    VALUES (?, ?, ?, ?)
                """, (id_cat, nombre, int(cant), danio))

                conexion.commit()
                msg.showinfo("Éxito", "Insumo agregado.")
                cargar_insumos()

            except Exception as e:
                msg.showerror("Error", f"No se pudo agregar:\n{e}")

        def eliminar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Selecciona un insumo.")
                    return

                id_ins = tree.item(sel)["values"][0]

                try:
                    cursor.execute("DELETE FROM Insumos WHERE IDInsumos=?", (id_ins,))
                    conexion.commit()
                    cargar_insumos()
                    msg.showinfo("Éxito", "Insumo eliminado correctamente.")
                except Exception as e:
                    # Error por clave foránea → insumo usado en ProveedoresInsumos
                    if "FK_Proveedor" in str(e) or "REFERENCE" in str(e):
                        msg.showerror(
                            "No permitido",
                            "Este insumo no puede eliminarse porque está relacionado con proveedores."
                        )
                    else:
                        msg.showerror("Error", str(e))

            except Exception as e:
                msg.showerror("Error general", str(e))


        def editar_insumo():
            try:
                sel = tree.selection()
                if not sel:
                    msg.showwarning("Atención", "Selecciona un insumo.")
                    return

                id_ins = int(tree.item(sel)["values"][0])

                categoria = entries["Categoría"].get()
                nombre = entries["Nombre"].get().strip()
                cant = entries["Cantidad Disponible"].get().strip()
                danio = entries["Cantidad Dañada"].get().strip()

                if not categoria or not nombre or not cant.isdigit():
                    msg.showwarning("Atención", "Completa categoría, nombre y cantidad disponible.")
                    return

                danio = int(danio) if danio.isdigit() else 0

                cursor.execute(
                    "SELECT IDCategoriaInsumos FROM CategoriaInsumos WHERE NombreCategoria=?",
                    categoria
                )
                id_cat = cursor.fetchone()[0]

                cursor.execute("""
                    UPDATE Insumos
                    SET IDCategoriaInsumos=?, NombreInsumo=?, CantidadDisponible=?, CantidadDañada=?
                    WHERE IDInsumos=?
                """, (id_cat, nombre, int(cant), danio, id_ins))

                conexion.commit()
                msg.showinfo("Éxito", "Insumo actualizado.")
                cargar_insumos()

            except Exception as e:
             msg.showerror("Error", f"No se pudo editar:\n{e}")

        # Asignar botones
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
