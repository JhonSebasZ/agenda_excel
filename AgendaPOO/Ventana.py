from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

from Agenda import Agenda
from Contacto import Contacto


class Ventana(tk.Tk):

    def __init__(self):

        super().__init__()
        self.agenda = Agenda()  # Creacion de un objeto de tipo ajenda

        self.title('Agenda')  # Titulo de la ventana
        self.geometry('670x500')  # Tamaño de la ventana (ancho - alto)
        colorFondo = '#006'  # Color en hexademimal
        colorLetra = '#FFF'  # Color en hexademimal
        # Asignacion del color para la ventana
        self.config(background=colorFondo)
        # Para que el tamaño de la ventana no pueda ser modificado
        self.resizable(0, 0)

        # varibles para almacenar las entradas del usuario
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.telefono = StringVar()
        self.correo = StringVar()
        self.buscarContacto = StringVar()

        # Creacion de caracteristicas de la ventana
        self.crearEtiquetas(colorFondo, colorLetra)
        self.crearEntradas()
        self.crearBotones()
        self.tabla = self.crearTabla()

        self.mostrarContactos()  # Muestra en la tabla los contactos registrados

        self.contactoSeleccionado = []  # Almacena los datos del contacto seleccionado
        self.banModificar = False  # Bandera para saber si el boton modificar esta activo o no

    def crearEtiquetas(self, colorFondo, colorLetra):

        lbTitulo = Label(self, text='Mi Agenda', bg=colorFondo,
                         fg=colorLetra)  # Creacion del Label
        lbTitulo.place(x=270, y=10)  # Ubicacion del Label

        lbNombre = Label(self, text='Nombre', bg=colorFondo, fg=colorLetra)
        lbNombre.place(x=50, y=50)

        lbApellido = Label(self, text='Apellido', bg=colorFondo, fg=colorLetra)
        lbApellido.place(x=50, y=80)

        lbCorreo = Label(self, text='Correo', bg=colorFondo, fg=colorLetra)
        lbCorreo.place(x=50, y=140)

        lbTelefono = Label(self, text='Telefono', bg=colorFondo, fg=colorLetra)
        lbTelefono.place(x=50, y=170)

        lbBuscar = Label(self, text='Buscar', bg=colorFondo, fg=colorLetra)
        lbBuscar.place(x=430, y=50)

    def crearEntradas(self):

        # Creacion de una entrada "Entry"
        self.etNombre = Entry(self, textvariable=self.nombre, width=25)
        self.etNombre.place(x=130, y=50)  # Ubicacion de la entrada
        self.etNombre.focus_set()  # Autofocus

        etApellido = Entry(self, textvariable=self.apellido, width=25)
        etApellido.place(x=130, y=80)

        etCorreo = Entry(self, textvariable=self.correo, width=25)
        etCorreo.place(x=130, y=140)

        etTelefono = Entry(self, textvariable=self.telefono, width=25)
        etTelefono.place(x=130, y=170)

        self.buscarContacto.trace("w", self.buscarCon)
        etBuscar = Entry(self, width=25, textvariable=self.buscarContacto)
        etBuscar.place(x=480, y=50)

    def crearBotones(self):

        # Creacion de un boton
        btnGuardar = Button(self, text='Guardar',
                            command=lambda: self.crearContacto())
        btnGuardar.place(x=330, y=170)  # Ubicacion del boton

        btnModificar = Button(self, text='Modificar',
                              command=lambda: self.mostrarContactoSeleccionado())
        btnModificar.place(x=410, y=170)

        btnEliminar = Button(self, text='Eliminar',
                             command=self.eliminarContacto)
        btnEliminar.place(x=500, y=170)

        btnLimpiar = Button(self, text="Limpiar", command=self.limpiarVentana)
        btnLimpiar.place(x=580, y=170)

    def crearTabla(self):

        frame = Frame(self, width=120)  # Creacion de un frame
        frame.place(x=20, y=230)  # Ubicacion del frame

        # Definicion de las columnas para la tabla
        columnas = ('Id', 'Nombre', 'Apellido', 'Correo', 'Telefono')

        tabla = ttk.Treeview(frame, columns=columnas,
                             show='headings', height=11)

        # Encabezado de la tabla
        tabla.grid(row=0, column=0, sticky='nsew')
        tabla.heading('Id', text='Id')
        tabla.column('Id', width=20)
        tabla.heading('Nombre', text='Nombre')
        tabla.column('Nombre', width=150)
        tabla.heading('Apellido', text='Apellido')
        tabla.column('Apellido', width=150)
        tabla.heading('Correo', text='Correo')
        tabla.heading('Telefono', text='Telefono')
        tabla.column('Telefono', width=100)

        # agregar scroll
        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # evento al seleccionar un contacto en la tabla
        tabla.bind('<<TreeviewSelect>>', self.seleccionarContacto)
        return tabla

    def seleccionarContacto(self, event):
        item = self.tabla.item(self.tabla.selection())
        self.contactoSeleccionado = item['values']

    def crearContacto(self):

        # Si todos las entradas tienen algun valor
        if self.nombre.get().strip() and self.apellido.get().strip() and self.correo.get().strip() and self.telefono.get().strip():
            if self.banModificar:  # Si la bandera del boton modificar esta activa
                try:
                    self.modificarContacto()  # Modifica el contacto
                    messagebox.showinfo("Modificar", "Contacto Modificado")
                except:
                    messagebox.showerror("Modificar", "Error al Modificar")

                self.limpiarVentana()
                # Limpia los datos de la variable contactoSeleccionado
                self.contactoSeleccionado = []
                self.banModificar = False  # Apaga la bandera de el boton modificar
            else:  # Si la bandera del boton modificar esta apagada
                nombre, apellido, telefono, correo = self.formatearEntradas(self.nombre.get(), self.apellido.get(),
                                                                            self.telefono.get(), self.correo.get())
                contacto = Contacto(nombre, apellido, telefono, correo)
                try:
                    self.agenda.guardar(contacto)  # guarda el contacto
                    messagebox.showinfo("Guardar", "Se guardo correctamente")
                except:
                    messagebox.showerror("Guardar", "Error al guardar")

                self.mostrarContactos()  # Actualiza los datos de la tabla
                self.limpiarVentana()
                # Limpia los datos de la variable contactoSeleccionado
                self.contactoSeleccionado = []
        else:
            messagebox.showinfo("Vacio", "Algunas entradas estan vacias")

    def mostrarContactoSeleccionado(self):
        if len(self.contactoSeleccionado) > 0:  # Si se selecciona un contacto
            # Establecer en las entradas los datos del contacto seleccionado
            self.nombre.set(self.contactoSeleccionado[1])
            self.apellido.set(self.contactoSeleccionado[2])
            self.correo.set(self.contactoSeleccionado[3])
            self.telefono.set(self.contactoSeleccionado[4])
            self.banModificar = True  # Enciende la bandera de el boton modificar
        else:
            messagebox.showerror("Modificar", "Ningun contacto seleccionado")

    def eliminarContacto(self):

        if len(self.contactoSeleccionado) > 0:  # Si se selecciona un contacto
            try:
                index = int(self.contactoSeleccionado[0])
                self.agenda.eliminar(index)  # Elimina el contacto
                messagebox.showinfo(
                    "Eliminar", "Contacto " + str(self.contactoSeleccionado[1]) + " eliminado")
            except:
                messagebox.showerror("Eliminar", "Contacto no eliminado")
        else:
            messagebox.showerror("Eliminar", "Ningun contacto seleccionado")

        # Limpia los datos de la variable contactoSeleccionado
        self.contactoSeleccionado = []

        self.mostrarContactos()  # Actualiza los datos de la tabla

    def modificarContacto(self):
        # Si todas las entradas tienen un valor
        if self.nombre.get().split() and self.apellido.get().split() and self.correo.get().split() and self.telefono.get().split():
            contactoModificado = []  # Garda los datos modificados del contacto seleccionado

            nombre, apellido, telefono, correo = self.formatearEntradas(self.nombre.get(), self.apellido.get(),
                                                                        self.telefono.get(), self.correo.get())
            contactoModificado.append(nombre)
            contactoModificado.append(apellido)
            contactoModificado.append(telefono)
            contactoModificado.append(correo)

            # Modifica el contacto
            self.agenda.modificar(
                int(self.contactoSeleccionado[0]), contactoModificado)
            self.mostrarContactos()  # Actualiza los datos de la tabla
        else:
            messagebox.showinfo("vacio", "algunas entradas estan vacias")

    def buscarCon(self, *args):
        contactosEncontrados = self.agenda.buscar(self.buscarContacto.get())
        if self.buscarContacto.get():  # Si se esta buscando un contacto
            # Elimina todos los datos de la tabla, menos los encabezados
            self.tabla.delete(*self.tabla.get_children())
            for contacto in contactosEncontrados:
                # Inserta los contactos en la tabla
                self.tabla.insert('', END, values=contacto)
        else:
            self.mostrarContactos()

    def mostrarContactos(self):
        contactos = self.agenda.cargar()
        # Elimina todos los datos de la tabla, menos los encabezados
        self.tabla.delete(*self.tabla.get_children())

        for contacto in contactos:
            # Inserta los contactos en la tabla
            self.tabla.insert('', END, values=contacto)

    def limpiarVentana(self):

        self.nombre.set("")
        self.apellido.set("")
        self.telefono.set("")
        self.correo.set("")
        self.etNombre.focus_set()

    def formatearEntradas(self, nombre, apellido, telefono, correo):
        nombre = nombre.strip()  # Elimina espacios en blanco al inicio y al final
        apellido = apellido.strip()
        telefono = telefono.strip()
        correo = correo.strip()

        nombre = nombre.capitalize()  # Convierte la primer letra en mayuscula
        apellido = apellido.capitalize()

        return nombre, apellido, telefono, correo
