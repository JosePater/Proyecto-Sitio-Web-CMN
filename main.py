from flask import Flask, render_template, request, redirect

# Importando el controlador cliente
# from nombreCarpeta.nombreModulo import nombreClase <estructora>
from Controlador.Cliente_cmn import Cliente

from flask import flash
import os

app = Flask(__name__)

app.secret_key = os.urandom(24) 

@app.route("/")
def inicio(): #Ir a la página principal
    return render_template ("Carrusel.html")

@app.route("/Quiénes somos")
def quienes_somos(): #Ir a la quiénes somos
    return render_template ("Quiénes somos.html")

@app.route("/Preguntas frecuentes")
def preguntas_frecuentes():
    return render_template("Preguntas frecuentes.html")

@app.route("/Revision")
def revision_tecnomecanica():
    return render_template("Revision_CMN.html")

@app.route("/soat")
def soat():
    return render_template("SOAT.html")

@app.route("/admin")
def admin():
    c = Cliente()
    clientesConsultados = c.consultar_cliente() # Captura los datos de la consulta en la variable clientes
    return render_template("ConsultaClientes_Admin.html", clientesObtenidos = clientesConsultados)

@app.route("/agregar_cliente")
def agregar_cliente():
    return render_template("ConsultaClientes_Admin.html")


@app.route("/buscar_cliente_por_cedula", methods=["POST"])
def buscar_cliente_por_cedula():
    print("\n----------- Entrando al método buscar_cliente_por_cedula---------")
    if request.method == 'POST': 
        id_buscar = request.form['buscar']
        print("El número cédula a buscar es: "+id_buscar)
        c = Cliente()
        clientesConsultados =  c.consultar_cliente_por_cedula(id_buscar) #cambiar por conslultar_cliente_por_cedula
        # Si el cliente NO está registrado
        if clientesConsultados == None:
            flash("Cliente "+id_buscar+" no registrado",'Advertencia')
        # Si el cliente sí está registrado
        else:
            nombreApellido = c.obtenerNombreApellido(id_buscar)
            nombre = nombreApellido[0]
            apellido = nombreApellido[1]
            flash("La cédula "+id_buscar+" corresponde a: "+nombre+" "+apellido)
    return redirect("/admin")

@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    cedula = request.form["cedula"]
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    print("-----"+cedula+" "+nombre+" "+apellido+" "+telefono+" "+direccion+" "+correo)
    c = Cliente()
    mensaje = c.insertar_cliente(cedula,nombre,apellido,telefono,direccion,correo)
    #aqui debo validad si todo fue OK
    if mensaje!="OK":
        flash(mensaje,'Advertencia')
        direccion_url=redirect("/Revision")
    else:
        flash("¡Registro insertado con exito!") #Pendiente personalizar (Nombre y apellido)
        direccion_url = redirect("/admin")
    # De cualquier modo, y si todo fue bien, redireccionar
    # return redirect(direccion_url) #En_prueba
    return (direccion_url)


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    numCC=request.form['id']
    c = Cliente()
    c.eliminar_cliente(request.form['id'])
    flash("¡Registro CC: "+numCC+" eliminado con exito!")
    return redirect("/admin") # Vuelve a mostrar los clientes actualizados

# la ruta /editar_cliente, la cual tiene asociada la funcion editar_cliente() recibe un dato que es pasado con la URL
# es decir es pasado como un método GET, este dato es id del registro que se quiere editar. Esta ruta es llamada desde la
# plantilla ConsultaClientes_admin.html cuando se hace clic en el boton Editar. Ya con el id, se realiza una consulta a la base de datos
# para ello se invoca el método consultar_cliente_por_id del objeto controlador tipo Cliente, pasandole como argumento el id.
# Este método devuelve el registro a editar, el cual es almacenado
# en una variable cliente, la cual es pasada a la plantilla
# editar_cliente.html cuando se hace el renderizado.
# La plantilla editar_cliente.html es basicamente un formulario html
# que recibe los datos para que el usuario pueda modificarlos y despues
# ejecutar la orden de guardar
@app.route("/editar_cliente/<int:id>")
def editar_cliente(id):
    mensaje = 'Está intentando actualizar datos'
    print("--------- Ingreso a plantilla de edición de registro cliente --------")
    c = Cliente()
    # Obtener el cliente por ID
    registro_cc_cliente = c.consultar_cliente_por_cedula(id)
    flash(mensaje,'Advertencia')
    # cc_primera para almacenar la cédula que tenía el registro en caso que sea la cédula que se vaya a cambiar...
    # ... Ya que no se tendría la referencia WHERE cedula que tenía {Pater}
    return render_template("editar_cliente.html", cliente=registro_cc_cliente, cc_primera=id)


@app.route("/actualizar_cliente", methods=["POST"])
def actualizar_cliente():
    cedula = request.form["cedula"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    email = request.form["correo"]
    cc_primera = request.form["cc_primera"]

    c = Cliente()
    mensaje = c.actualizar_cliente(cedula,nombres,apellidos,telefono,direccion,email,cc_primera)
    # Se valida si el mensaje fue OK
    if mensaje!="OK":
        flash(mensaje, 'Advertencia')
    else:
        # Para personalizar la actualización
        nombreApellido = c.obtenerNombreApellido(cedula)
        nombre = nombreApellido[0]
        apellido = nombreApellido[1]
        flash("¡¡¡Registro de: "+nombre+" "+apellido+" ACTUALIZADO con ÉXITO!!!") #Para enviar mensaje
    return redirect("/admin")

@app.route("/Ordenar_cliente", methods=["POST"]) #En_prueba
def ordenar_cliente():
    filtro=request.form['filtro']
    print("-------El filtro es: "+filtro)
    c = Cliente()
    ordenarClientes = c.ordenar_cliente_por(filtro) # Captura los datos de la consulta en la variable clientes
    return render_template("ConsultaClientes_Admin.html", clientesObtenidos = ordenarClientes)

if __name__ == '__main__':
    app.run(debug=True)
