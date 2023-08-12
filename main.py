import db
from models import Producto
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import sqlite3

class Productos:
    db = 'database/productos.db'
    def __init__(self, root):
        # Le hacemos los ajustes a nuestra ventana como le pondremos titulo, le agregaremos un oicono entre mas cosas
        self.ventana = root
        self.ventana.title('App Gestor de Productos')
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")

        # Creamos el controlador Frame que va a hacer el frame principal
        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto', font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=1, columnspan=2, pady=20)

        # Creamos el Label del nombre del producto
        self.etiqueta_nombre = Label(frame, text='Nombre: ', font=('Calibri',13))
        self.etiqueta_nombre.grid(row=1, column=0)

        # Vamos a hacer el Entry del nombre
        self.nombre_producto = Entry(frame,font=('Calibri',13))
        self.nombre_producto.focus()
        self.nombre_producto.grid(row=1, column=1)

        # Vamos a hacer el Label del precio
        self.etiqueta_precio = Label(frame, text='Precio: ',font=('Calibri',13))
        self.etiqueta_precio.grid(row=2, column=0)

        # Vamos a crear el Entry del precio
        self.precio_producto = Entry(frame,font=('Calibri',13))
        self.precio_producto.grid(row=2, column=1)


        # Vamos a crear el label de numero de productos que se recibieron y esto nos servira para poder saber que tanto stok tenemos en el invetario
        # ya despues esto nos servira para poder hacer otro programa de ventas que cada que se venda un producto se vaya quitando al stok, por mientras
        # Solo nos servira para poder saber cuanto stok tenemos
        self.etiqueta_num_productos = Label(frame, text='Stock: ',font=('Calibri',13))
        self.etiqueta_num_productos.grid(row=3, column=0)

        # Hacemos el Entry de los productos
        self.entry_num_productos = Entry(frame,font=('Calibri',13))
        self.entry_num_productos.grid(row=3, column=1)

        # Ahora usaremos una funcion de ttk que es el combobox, primero le daremos su Label
        self.etiqueta_categoria_producto = Label(frame, text='Categoria: ', font=('Calibri', 13))
        self.etiqueta_categoria_producto.grid(row=4, column=0)

        # Ahora si usaremos el combobox
        self.categoria_producto = ttk.Combobox(frame, font=('Calibri', 13), width=18, state='readonly')
        self.categoria_producto['values'] = ('Tecnologia', 'Moda', 'Mascotas', 'Hogar', 'Carnes')
        self.categoria_producto.grid(row=4, column=1)

        # Creamos el boton añadir productos
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Añadir producto", style='my.TButton', command=self.add_producto)
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Creamos los estilos de la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Creamos la estructura de la tabla
        columns = ("Nombre","Precio","Stock","Categoria")
        self.tabla = ttk.Treeview(height=20, columns=columns, style='mystyle.Treeview', show='headings')
        self.tabla.grid(row=6, column=0, columnspan=4)
        self.tabla.heading("Nombre", text="Nombre", anchor=CENTER)
        self.tabla.heading("Precio", text="Precio", anchor=CENTER)
        self.tabla.heading("Stock", text="Stock", anchor=CENTER)
        self.tabla.heading("Categoria", text="Categoria", anchor=CENTER)

        # Vamos a crear los botones de eliminar y editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text="ELIMINAR", style='my.TButton', command=self.del_producto)
        boton_eliminar.grid(row=7, column=0, columnspan=2,sticky=W + E)
        boton_editar = ttk.Button(text="EDITAR", style='my.TButton',command=self.edit_producto)
        boton_editar.grid(row=7,column=2,columnspan=2,sticky=W + E)

        self.get_producto()


    # Aqui preferi hacerlo de la manera tradicional con sqlite ya que al momento de recibir los parametros, me daba un objeto de models que por mas que intente
    # no podia convertirlos
    def db_consulta(self, consulta, parametros = ()):
       with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
       return resultado

    def get_producto(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM productos ORDER BY categoria DESC'
        registros = self.db_consulta(query)
        for i in registros:
            self.tabla.insert("", 0, text= i[1], values=(i[1],i[2],i[3],i[4]))


    def validacion_nombre(self):
        nombre_introducido = self.nombre_producto.get()
        return len(nombre_introducido) != 0

    def validacion_precio(self):
        precio_introducido = self.precio_producto.get()
        return len(precio_introducido) != 0

    def validacion_num_productos(self):
        num_introducido = self.entry_num_productos.get()
        return len(num_introducido) != 0

    def vaidacion_categoria(self):
        categoria_introducida = self.categoria_producto.get()
        return len(categoria_introducida) != 0

    def add_producto(self):
        if(self.validacion_nombre() and self.validacion_precio() and self.validacion_num_productos() and self.vaidacion_categoria()):
            query = "INSERT INTO productos VALUES(NULL, ?, ?, ?, ?)"
            parametros = (self.nombre_producto.get(), self.precio_producto.get(), self.entry_num_productos.get(), self.categoria_producto.get())
            self.db_consulta(query, parametros)
            messagebox.showinfo("Exito!", "Datos Guardados")

        elif(self.validacion_nombre() == False and self.validacion_precio() and self.validacion_num_productos() and self.vaidacion_categoria()):
            messagebox.showerror("Error","El campo nombre es obligatorio")

        elif(self.validacion_nombre() and self.validacion_precio() == False and self.validacion_num_productos() and self.vaidacion_categoria()):
            messagebox.showerror("Error","El campo precio es obligatorio")

        elif(self.validacion_nombre() and self.validacion_precio() and self.validacion_num_productos()==False and self.vaidacion_categoria()):
            messagebox.showerror("Error","El campo numero de productos es obligatorio")

        elif(self.validacion_nombre() and self.validacion_precio() and self.validacion_num_productos() and self.vaidacion_categoria()==False):
            messagebox.showerror("Error","El campo categoria es obligatorio")

        else:
            messagebox.showerror("Error","Todos los campos son requeridos")

        self.get_producto()

    def del_producto(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError:
            messagebox.showerror("Error","Porfavor seleccione un producto")
            return

        nombre = self.tabla.item(self.tabla.selection())['text']
        query = "DELETE FROM productos WHERE nombre = ?"
        self.db_consulta(query,(nombre,))
        messagebox.showinfo("Exito", "Producto Borrado con Exito")

        self.get_producto()

    def edit_producto(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError:
            messagebox.showerror("Error","Porfavor seleccione un producto")
            return

        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][1] # Este es el precio que esta en una lista y es el valor uno
        old_productos = self.tabla.item(self.tabla.selection())['values'][2] # Este es el numero de productos por si se desea editar
        old_categoria = self.tabla.item(self.tabla.selection())['values'][3] # Este seria la categoria para poder editarla

        self.ventana_editar = Toplevel() # Creamos una ventana por delante de la principal
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')

        # Creacion de todo lo que contendra nuestra nueva ventana

        # Creamos el nuevo frame para la ventana editar
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente producto",font=('Calibri',16,'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ",font=('Calibri',13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Entry nombre antiguo (Texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),state="readonly", font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)


        # Label Nombre Nuevo
        self.nombre_nuevo = Label(frame_ep, text="Nombre Nuevo: ", font=('Calibri', 13))
        self.nombre_nuevo.grid(row=3, column=0)
        # EntrY Nombre nuevo (Texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este entry al inicio



        # Label Precio antiguo
        self.precio_antiguo = Label(frame_ep, text="Precio Antiguo: ", font=('Calibri', 13))
        self.precio_antiguo.grid(row=4, column=0)
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)
        # Label Precio Nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry precio nuevo (Texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)



        # Label Numero de productos
        self.etiqueta_num_productos_antiguo = Label(frame_ep,text="Stock antiguo: ",font=('Calibri', 13))
        self.etiqueta_num_productos_antiguo.grid(row=6,column=0)
        # Entry productos antiguos
        self.num_productos_antiguos = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=old_productos),state='readonly', font=('Calibri', 13))
        self.num_productos_antiguos.grid(row=6,column=1)

        # Label Numero de Productos Nuevo
        self.producto_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.producto_nuevo.grid(row=7, column=0)
        # Entry precio nuevo (Texto que si se podra modificar)
        self.input_producto_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_producto_nuevo.grid(row=7, column=1)

        # Label categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13))
        self.etiqueta_categoria_antigua.grid(row=8, column=0)
        # Entry productos antiguos
        self.categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),state='readonly', font=('Calibri', 13))
        self.categoria_antigua.grid(row=8, column=1)

        # Label categoria nueva
        self.categoria_nueva = Label(frame_ep, text="Nueva categoria: ", font=('Calibri', 13))
        self.categoria_nueva.grid(row=9, column=0)
        # Entry precio nuevo (Texto que si se podra modificar)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, font=('Calibri', 13), width=18,state='readonly' )
        self.input_categoria_nueva['values'] = ('Tecnologia', 'Moda', 'Mascotas', 'Hogar', 'Carnes')
        self.input_categoria_nueva.grid(row=9, column=1)

        # Boton actualizar producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep,text="Actualizar Producto",style='my.TButton',
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_antiguo.get(),
                                                                     self.input_nombre_nuevo.get(),
                                                                     self.input_precio_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.num_productos_antiguos.get(),
                                                                     self.input_producto_nuevo.get(),
                                                                     self.categoria_antigua.get(),
                                                                     self.input_categoria_nueva.get()))
        self.boton_actualizar.grid(row=10,columnspan=2,sticky=W + E)

    def actualizar_productos(self,antiguo_nombre,nuevo_nombre,antiguo_precio,nuevo_precio,antiguo_num_producto,nuevo_num_producto,antigua_categoria, nueva_categoria):
        producto_modificado = False
        query = "UPDATE productos SET nombre = ?, precio = ?, num_producto = ?, categoria = ? WHERE nombre = ? AND precio = ? AND num_producto = ? AND categoria = ?"
        if(nuevo_nombre != "" and nuevo_precio != "" and nuevo_num_producto != "" and nueva_categoria != ""):
            parametros = (nuevo_nombre, nuevo_precio, nuevo_num_producto, nueva_categoria, antiguo_nombre, antiguo_precio,antiguo_num_producto, antigua_categoria)
            producto_modificado = True
        elif(nuevo_nombre == "" and nuevo_precio != "" and nuevo_num_producto != "" and nueva_categoria != ""):
            parametros = (antiguo_nombre,nuevo_precio,nuevo_num_producto,nueva_categoria, antiguo_nombre, antiguo_precio,antiguo_num_producto, antigua_categoria)
            producto_modificado = True

        elif(nuevo_nombre != "" and nuevo_precio == "" and nuevo_num_producto != "" and nueva_categoria != ""):
            parametros = (nuevo_nombre,antiguo_precio,antiguo_num_producto,antigua_categoria,antiguo_nombre, antiguo_precio,antiguo_num_producto, antigua_categoria)
            producto_modificado = True

        elif(nuevo_nombre != "" and nuevo_precio != "" and nuevo_num_producto == "" and nueva_categoria != ""):
            parametros = (nuevo_nombre,nuevo_precio,antiguo_num_producto,nueva_categoria,antiguo_nombre, antiguo_precio,antiguo_num_producto, antigua_categoria)
            producto_modificado = True

        elif(nuevo_nombre != "" and nuevo_precio != "" and nuevo_num_producto != "" and nueva_categoria == ""):
            parametros = (nuevo_nombre, nuevo_precio, nuevo_num_producto, antigua_categoria,antiguo_nombre, antiguo_precio,antiguo_num_producto, antigua_categoria)
            producto_modificado = True

        if(producto_modificado):
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            messagebox.showinfo("Exito","El Producto {} se Hactualizo Correctamente".format(antiguo_nombre))
            self.get_producto()

        else:
            self.ventana_editar.destroy()
            messagebox.showerror("Error","El producto {} no ha sido actualizado ".format(antiguo_nombre))

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    root = Tk()
    app = Productos(root)
    root.mainloop()