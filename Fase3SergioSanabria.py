"""
=======================================================================
Universidad Nacional Abierta y a Distancia - UNAD
Escuela de Ciencias Básicas Tecnología e Ingeniería - ECBTI
Curso: Estructura de Datos (301305)
Fase 3 - Componente Práctico - Prácticas Simuladas

Estudiante: Sergio Sanabria
Grupo: 158

Aplicación: Sistema de Control de Afiliados "Compensándote"
Estructuras implementadas: Pila (list), Cola (collections.deque), Lista (list)
=======================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from collections import deque
from tkcalendar import DateEntry



# CLASE PRINCIPAL - Almacena los datos del afiliado
class EstructuraDatosAfiliado:
    """Clase que representa a un afiliado de la Caja de Compensación."""

    def __init__(self, tipo_identificacion, numero_identificacion, nombre_completo,
                 ingresos_actuales, servicio_deseado, modalidad_empleo,
                 tarifa_afiliacion, fecha_afiliacion):
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.nombre_completo = nombre_completo
        self.ingresos_actuales = ingresos_actuales
        self.servicio_deseado = servicio_deseado
        self.modalidad_empleo = modalidad_empleo
        self.tarifa_afiliacion = tarifa_afiliacion
        self.fecha_afiliacion = fecha_afiliacion

    def to_tuple(self):
        """Convierte el afiliado a tupla para mostrarlo en el Treeview."""
        return (
            self.tipo_identificacion,
            self.numero_identificacion,
            self.nombre_completo,
            f"{self.ingresos_actuales:,.0f}",
            self.servicio_deseado,
            self.modalidad_empleo,
            f"{self.tarifa_afiliacion:,.0f}",
            self.fecha_afiliacion
        )


# VENTANA DE LOGIN
class VentanaLogin:
    """Formulario de inicio de sesión."""

    CLAVE_CORRECTA = "Caja"
    NOMBRE_ESTUDIANTE = "Sergio Sanabria"
    GRUPO = "158"  
    NOMBRE_CURSO = "Estructura de Datos - 301305"

    def __init__(self, root):
        self.root = root
        self.root.title("Login - Compensándote")
        self.root.geometry("380x230")
        self.root.resizable(False, False)

        # Menú superior "Acerca de"
        menubar = tk.Menu(self.root)
        menubar.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.root.config(menu=menubar)

        # Frame principal
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Título del formulario
        tk.Label(frame, text="FORMULARIO DE INICIO DE SESIÓN",
                 font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Etiqueta Clave
        tk.Label(frame, text="* Clave:", font=("Arial", 10)).grid(
            row=1, column=0, columnspan=2)

        # Entrada de clave (enmascarada con *)
        self.entry_clave = tk.Entry(frame, show="*", width=28, font=("Arial", 10))
        self.entry_clave.grid(row=2, column=0, columnspan=2, pady=10)
        self.entry_clave.bind("<Return>", lambda e: self.validar_login())

        # Botones Ingresar y Salir
        tk.Button(frame, text="Ingresar", width=10,
                  command=self.validar_login).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(frame, text="Salir", width=10,
                  command=self.salir).grid(row=3, column=1, padx=5, pady=5)

        self.entry_clave.focus()

    def mostrar_acerca_de(self):
        """Muestra la información del estudiante."""
        mensaje = (f"Caja Compensándote\n"
                   f"Desarrollo de Aplicación - Python Tkinter\n"
                   f"Estudiante: {self.NOMBRE_ESTUDIANTE}\n"
                   f"Grupo: {self.GRUPO}")
        messagebox.showinfo("Información", mensaje)

    def validar_login(self):
        """Valida la clave. Si es correcta abre la ventana principal."""
        clave = self.entry_clave.get()
        if clave == self.CLAVE_CORRECTA:
            self.root.destroy()
            root_principal = tk.Tk()
            VentanaPrincipal(root_principal)
            root_principal.mainloop()
        else:
            messagebox.showerror("Error de autenticación",
                                 "Clave incorrecta. Por favor intente de nuevo.")
            self.entry_clave.delete(0, tk.END)
            self.entry_clave.focus()

    def salir(self):
        """Finaliza la aplicación."""
        self.root.destroy()


# VENTANA PRINCIPAL - Formulario de ingreso de datos
class VentanaPrincipal:
    """Formulario principal para el registro de afiliados."""

    def __init__(self, root):
        self.root = root
        self.root.title("Caja Compensándote - Control de Afiliados")
        self.root.geometry("1150x720")
        self.root.resizable(True, True)

        # --- Estructuras de datos 
        self.pila = []           # Pila (LIFO) implementada con list
        self.cola = deque()      # Cola (FIFO) implementada con collections.deque
        self.lista = []          # Lista implementada con list

        self.construir_interfaz()

    # Construcción de la interfaz gráfica
    def construir_interfaz(self):
        # --- Frame de registro 
        frame_registro = tk.LabelFrame(
            self.root, text=" REGISTRO DE AFILIADOS ",
            font=("Arial", 10, "bold"), padx=10, pady=5)
        frame_registro.pack(fill="x", padx=10, pady=5)

        # Tipo de estructura
        tk.Label(frame_registro, text="* Tipo de estructura:").grid(
            row=0, column=0, sticky="w", padx=5, pady=3)
        self.combo_estructura = ttk.Combobox(
            frame_registro, values=["Pila", "Cola", "Lista"],
            state="readonly", width=28)
        self.combo_estructura.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        # Tipo de identificación
        tk.Label(frame_registro, text="* Tipo de identificación:").grid(
            row=1, column=0, sticky="w", padx=5, pady=3)
        self.combo_tipo_id = ttk.Combobox(
            frame_registro, values=["CC", "CE", "NUIP", "PAS"],
            state="readonly", width=28)
        self.combo_tipo_id.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        # Número de identificación 
        tk.Label(frame_registro, text="* Nro. de identificación:").grid(
            row=2, column=0, sticky="w", padx=5, pady=3)
        vcmd_num = (self.root.register(self.validar_solo_numeros), "%P")
        self.entry_num_id = tk.Entry(
            frame_registro, width=30, validate="key", validatecommand=vcmd_num)
        self.entry_num_id.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        # Nombre completo 
        tk.Label(frame_registro, text="* Nombre completo:").grid(
            row=3, column=0, sticky="w", padx=5, pady=3)
        vcmd_letras = (self.root.register(self.validar_solo_letras), "%P")
        self.entry_nombre = tk.Entry(
            frame_registro, width=30, validate="key", validatecommand=vcmd_letras)
        self.entry_nombre.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        # Ingresos actuales 
        tk.Label(frame_registro, text="* Ingresos actuales:").grid(
            row=4, column=0, sticky="w", padx=5, pady=3)
        self.entry_ingresos = tk.Entry(
            frame_registro, width=30, validate="key", validatecommand=vcmd_num)
        self.entry_ingresos.grid(row=4, column=1, padx=5, pady=3, sticky="w")
        self.entry_ingresos.bind("<KeyRelease>", lambda e: self.calcular_tarifa())

        # Servicio deseado
        tk.Label(frame_registro, text="* Servicio deseado:").grid(
            row=5, column=0, sticky="w", padx=5, pady=3)
        servicios = ["Subsidio de desempleo", "Ingreso a parque",
                     "Curso de formación", "Paquete de viaje", "Medicina preventiva"]
        self.combo_servicio = ttk.Combobox(
            frame_registro, values=servicios, state="readonly", width=28)
        self.combo_servicio.grid(row=5, column=1, padx=5, pady=3, sticky="w")
        self.combo_servicio.bind("<<ComboboxSelected>>", lambda e: self.calcular_tarifa())

        # Modalidad de empleo 
        tk.Label(frame_registro, text="* Modalidad de empleo:").grid(
            row=6, column=0, sticky="w", padx=5, pady=3)
        self.var_modalidad = tk.StringVar()
        frame_radio = tk.Frame(frame_registro)
        frame_radio.grid(row=6, column=1, sticky="w")
        tk.Radiobutton(frame_radio, text="Empleado", variable=self.var_modalidad,
                       value="Empleado", command=self.calcular_tarifa).pack(side="left")
        tk.Radiobutton(frame_radio, text="Independiente", variable=self.var_modalidad,
                       value="Independiente", command=self.calcular_tarifa).pack(side="left")

        # Tarifa de afiliación 
        tk.Label(frame_registro, text="Tarifa de afiliación ($):").grid(
            row=7, column=0, sticky="w", padx=5, pady=3)
        self.entry_tarifa = tk.Entry(frame_registro, width=30, state="readonly")
        self.entry_tarifa.grid(row=7, column=1, padx=5, pady=3, sticky="w")

        # Fecha de afiliación
        tk.Label(frame_registro, text="* Fecha de afiliación:").grid(
            row=8, column=0, sticky="w", padx=5, pady=3)
        self.date_entry = DateEntry(
            frame_registro, width=27, date_pattern="dd/mm/yyyy",
            background="darkblue", foreground="white", borderwidth=2)
        self.date_entry.grid(row=8, column=1, padx=5, pady=3, sticky="w")

        # Botones Registrar y Limpiar
        frame_botones = tk.Frame(frame_registro)
        frame_botones.grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(frame_botones, text="Registrar", width=12,
                  command=self.registrar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Limpiar", width=12,
                  command=self.limpiar).pack(side="left", padx=5)

        # ---- Frame de datos de afiliados 
        frame_datos = tk.LabelFrame(
            self.root, text=" DATOS DE AFILIADOS ",
            font=("Arial", 10, "bold"), padx=10, pady=5)
        frame_datos.pack(fill="both", expand=True, padx=10, pady=5)

        # Selector de estructura y botones superiores
        frame_sup = tk.Frame(frame_datos)
        frame_sup.pack(fill="x", pady=5)

        tk.Label(frame_sup, text="* Ver estructura:").pack(side="left", padx=5)
        self.combo_ver = ttk.Combobox(
            frame_sup, values=["Pila", "Cola", "Lista"], state="readonly", width=15)
        self.combo_ver.pack(side="left", padx=5)
        self.combo_ver.bind("<<ComboboxSelected>>", lambda e: self.actualizar_treeview())
        self.combo_ver.set("Pila")

        # Botones de la derecha
        tk.Button(frame_sup, text="Salir", width=10,
                  command=self.salir).pack(side="right", padx=5)
        tk.Button(frame_sup, text="Eliminar", width=10,
                  command=self.eliminar).pack(side="right", padx=5)
        tk.Button(frame_sup, text="Reporte", width=10,
                  command=self.mostrar_reporte).pack(side="right", padx=5)

        # Treeview para mostrar los registros
        columnas = ("tipo_id", "num_id", "nombre", "ingresos",
                    "servicio", "modalidad", "tarifa", "fecha")
        self.tree = ttk.Treeview(frame_datos, columns=columnas, show="headings", height=12)

        encabezados = ["Tipo de id.", "Número de id.", "Nombre", "Ingresos",
                       "Servicio", "Modalidad", "Tarifa de afiliación", "Fecha de afiliación"]
        anchos = [80, 110, 180, 100, 150, 110, 140, 130]

        for col, enc, ancho in zip(columnas, encabezados, anchos):
            self.tree.heading(col, text=enc)
            self.tree.column(col, width=ancho, anchor="center")

        scrollbar = ttk.Scrollbar(frame_datos, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Validaciones
    def validar_solo_numeros(self, valor):
        """Permite solo dígitos numéricos."""
        if valor == "":
            return True
        return valor.isdigit()

    def validar_solo_letras(self, valor):
        """Permite solo letras y espacios."""
        if valor == "":
            return True
        return all(c.isalpha() or c.isspace() for c in valor)

    # Cálculo de tarifa
    def calcular_tarifa(self):
        """Calcula la tarifa según modalidad, ingresos y servicio."""
        try:
            ingresos_str = self.entry_ingresos.get()
            modalidad = self.var_modalidad.get()
            servicio = self.combo_servicio.get()

            if not ingresos_str or not modalidad or not servicio:
                return

            ingresos = float(ingresos_str)

            # Tarifa base según modalidad 
            if modalidad == "Empleado":
                if 1000000 <= ingresos <= 2000000:
                    tarifa = 45000
                elif 2000000 < ingresos <= 3000000:
                    tarifa = 60000
                elif 3000000 < ingresos <= 4000000:
                    tarifa = 75000
                elif 4000000 < ingresos <= 5000000:
                    tarifa = 90000
                elif ingresos > 5000000:
                    tarifa = 150000
                else:
                    tarifa = 0
            else:  # Independiente
                if 1000000 <= ingresos <= 2000000:
                    tarifa = 10000
                elif 2000000 < ingresos <= 3000000:
                    tarifa = 20000
                elif 3000000 < ingresos <= 4000000:
                    tarifa = 30000
                elif 4000000 < ingresos <= 5000000:
                    tarifa = 40000
                elif ingresos > 5000000:
                    tarifa = 80000
                else:
                    tarifa = 0

            # Ajuste según servicio deseado
            if servicio == "Subsidio de desempleo":
                pass  
            elif servicio == "Ingreso a parque":
                tarifa += 2500
            elif servicio == "Curso de formación":
                tarifa += 7500
            elif servicio == "Paquete de viaje":
                tarifa += 10000
            elif servicio == "Medicina preventiva":
                tarifa += ingresos * 0.10

            # Mostrar en el campo 
            self.entry_tarifa.config(state="normal")
            self.entry_tarifa.delete(0, tk.END)
            self.entry_tarifa.insert(0, f"{tarifa:,.0f}")
            self.entry_tarifa.config(state="readonly")
        except ValueError:
            pass

    # Registrar afiliado
    def registrar(self):
        """Registra un afiliado en la estructura seleccionada."""
        estructura = self.combo_estructura.get()
        tipo_id = self.combo_tipo_id.get()
        num_id = self.entry_num_id.get()
        nombre = self.entry_nombre.get().strip()
        ingresos = self.entry_ingresos.get()
        servicio = self.combo_servicio.get()
        modalidad = self.var_modalidad.get()
        tarifa_str = self.entry_tarifa.get()
        fecha = self.date_entry.get()

        # Validar que todos los campos estén diligenciados
        if not all([estructura, tipo_id, num_id, nombre, ingresos,
                    servicio, modalidad, tarifa_str, fecha]):
            messagebox.showwarning(
                "Datos incompletos",
                "Por favor diligencie todos los campos del formulario.")
            return

        # Crear el objeto afiliado
        tarifa = float(tarifa_str.replace(",", ""))
        afiliado = EstructuraDatosAfiliado(
            tipo_id, num_id, nombre, float(ingresos),
            servicio, modalidad, tarifa, fecha)

        # Agregar según la estructura seleccionada
        if estructura == "Pila":
            self.pila.append(afiliado)  # Apilar
            messagebox.showinfo("Registro exitoso",
                                "Afiliado APILADO correctamente en la Pila.")
        elif estructura == "Cola":
            self.cola.append(afiliado)  # Encolar
            messagebox.showinfo("Registro exitoso",
                                "Afiliado ENCOLADO correctamente en la Cola.")
        elif estructura == "Lista":
            self.lista.append(afiliado)  # Agregar al final
            messagebox.showinfo("Registro exitoso",
                                "Afiliado AGREGADO correctamente a la Lista.")
        self.combo_ver.set(estructura)
        self.actualizar_treeview()
        self.limpiar()

    # Limpiar campos
    def limpiar(self):
        """Limpia los campos del formulario sin afectar los registros."""
        self.combo_estructura.set("")
        self.combo_tipo_id.set("")
        self.entry_num_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_ingresos.delete(0, tk.END)
        self.combo_servicio.set("")
        self.var_modalidad.set("")
        self.entry_tarifa.config(state="normal")
        self.entry_tarifa.delete(0, tk.END)
        self.entry_tarifa.config(state="readonly")

    # Actualizar Treeview
    def actualizar_treeview(self):
        """Actualiza el Treeview según la estructura seleccionada."""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        estructura = self.combo_ver.get()

        if estructura == "Pila":
            for afiliado in reversed(self.pila):
                self.tree.insert("", "end", values=afiliado.to_tuple())
        elif estructura == "Cola":
            for afiliado in self.cola:
                self.tree.insert("", "end", values=afiliado.to_tuple())
        elif estructura == "Lista":
            for afiliado in self.lista:
                self.tree.insert("", "end", values=afiliado.to_tuple())

    # Reporte
    def mostrar_reporte(self):
        """Muestra el reporte según la estructura seleccionada."""
        estructura = self.combo_ver.get()

        if estructura == "Pila":
            if not self.pila:
                messagebox.showinfo("Reporte Pila", "La pila está vacía.")
                return
            suma = sum(a.tarifa_afiliacion for a in self.pila)
            messagebox.showinfo(
                "Reporte Pila",
                f"Suma total de tarifas de afiliación en la Pila:\n"
                f"${suma:,.0f}\n\n"
                f"Total de registros: {len(self.pila)}")

        elif estructura == "Cola":
            cantidad = len(self.cola)
            messagebox.showinfo(
                "Reporte Cola",
                f"Cantidad de registros actuales en la Cola: {cantidad}")

        elif estructura == "Lista":
            if not self.lista:
                messagebox.showinfo("Reporte Lista", "La lista está vacía.")
                return
            promedio = sum(a.ingresos_actuales for a in self.lista) / len(self.lista)
            messagebox.showinfo(
                "Reporte Lista",
                f"Promedio de ingresos actuales en la Lista:\n"
                f"${promedio:,.2f}\n\n"
                f"Total de registros: {len(self.lista)}")

    # Eliminar
    def eliminar(self):
        """Elimina registros según el comportamiento de cada estructura."""
        estructura = self.combo_ver.get()

        if estructura == "Pila":
            if not self.pila:
                messagebox.showwarning(
                    "Pila vacía", "No hay elementos para desapilar.")
                return
            ultimo = self.pila[-1]
            if messagebox.askyesno(
                    "Confirmación",
                    f"¿Está seguro de DESAPILAR el último registro?\n\n"
                    f"Afiliado: {ultimo.nombre_completo}\n"
                    f"Identificación: {ultimo.numero_identificacion}"):
                self.pila.pop()  
                self.actualizar_treeview()
                messagebox.showinfo("Eliminación exitosa",
                                    "Elemento DESAPILADO correctamente.")

        elif estructura == "Cola":
            if not self.cola:
                messagebox.showwarning(
                    "Cola vacía", "No hay elementos para desencolar.")
                return
            primero = self.cola[0]
            if messagebox.askyesno(
                    "Confirmación",
                    f"¿Está seguro de DESENCOLAR el primer registro?\n\n"
                    f"Afiliado: {primero.nombre_completo}\n"
                    f"Identificación: {primero.numero_identificacion}"):
                self.cola.popleft() 
                self.actualizar_treeview()
                messagebox.showinfo("Eliminación exitosa",
                                    "Elemento DESENCOLADO correctamente.")

        elif estructura == "Lista":
            if not self.lista:
                messagebox.showwarning(
                    "Lista vacía", "No hay elementos en la lista.")
                return
            num_id = simpledialog.askstring(
                "Eliminar de la Lista",
                "Digite el número de identificación del afiliado a eliminar:")
            if not num_id:
                return
            encontrado = None
            for afiliado in self.lista:
                if afiliado.numero_identificacion == num_id:
                    encontrado = afiliado
                    break
            if encontrado:
                if messagebox.askyesno(
                        "Confirmación",
                        f"¿Seguro que desea eliminar al siguiente afiliado?\n\n"
                        f"Nombre: {encontrado.nombre_completo}\n"
                        f"Identificación: {encontrado.numero_identificacion}"):
                    self.lista.remove(encontrado)
                    self.actualizar_treeview()
                    messagebox.showinfo("Eliminación exitosa",
                                        "Afiliado eliminado de la Lista.")
            else:
                messagebox.showerror(
                    "No encontrado",
                    f"No se encontró un afiliado con identificación: {num_id}")
                
    # Salir
    def salir(self):
        """Finaliza la aplicación."""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir de la aplicación?"):
            self.root.destroy()


# FUNCIÓN PRINCIPAL
if __name__ == "__main__":
    root = tk.Tk()
    VentanaLogin(root)
    root.mainloop()