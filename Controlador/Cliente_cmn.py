# 21-07-2022
# importando el Conector de BD
from BD.ConexionBD_cmn import ConectorBD

class Cliente:
    def __init__(self):
        self.cedula = None
        self.nombre = None
        self.apellido = None
        self.telefono = None
        self.direccion = None
        self.email = None
    
    def _insertar_cliente__(self, cedula, nombre, apellido, telefono, direccion, email):
        sql = "INSERT INTO tbl_cliente(cedula, nombre, apellido, telefono, direccion, email) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (cedula,nombre,apellido,telefono,direccion,email)
        objConector = ConectorBD #Se crea un objeto de la clase ConectorBD (Carpeta: BD)
        conexion = objConector.obtener_conexion() #Almacena el valor de retorno de obtener_conexion
        #preguntar si ya existe una cliente con esa cedula
        if not self.consultar_cliente_por_cedula(cedula):
            with conexion.cursor() as myCursor: #Conexion como alias cursor
                myCursor.execute(sql, val)
            conexion.commit() #Guarda los cambios
            conexion.close()  #Cierra la conexion
        else:
            print("ya existe un cliente con el numero de cedula ", cedula)

    # Método del instructor
    def insertar_cliente(self, cedula, nombre, apellido, telefono, direccion, email):
        print("\nEntrando al método insertar_cliente")
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion() #abre la conexion
        mensaje = "OK"
        #preguntar si ya existe una cliente con esa cedula
        if not self.consultar_cliente_por_cedula(cedula): #En prueba
            print("---- Entrando al primer caso")
            with conexion.cursor() as cursor: #asegura la escritura sobre la tabla
                # cursor.execute("INSERT INTO tbl_cliente(cedula,nombre,apellido,telefono,direccion,email) VALUES (%s, %s, %s, %s,%s,%s)",
                cursor.execute("INSERT INTO tbl_cliente VALUES (%s, %s, %s, %s,%s,%s)",(cedula, nombre, apellido, telefono, direccion, email))
            conexion.commit() #confirma la instrucción dada
            conexion.close() #cierra la conexion
        else:
            print("---- Entrando al segundo caso")
            mensaje = "¡ya existe un cliente con el numero de cedula " + cedula + "!"
            print(mensaje)
            conexion.close() #cierra la conexion
        return mensaje

    # ----- Método funcional -----
    def consultar_cliente(self, ): #Código de instructor
        print("\n---------- Consultando todos los clientes ------------------")
        objConector = ConectorBD() 
        conexion = objConector.obtener_conexion() #abre la conexión

        clientes = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_cliente")
            clientes = cursor.fetchall()
        conexion.close()
        return clientes

    # def consultar_cliente_por_cedula_OLD(self, cedula):
    #     objConector = ConectorBD()
    #     conexion = objConector.obtener_conexion()
    #     cliente = []
    #     with conexion.cursor() as myCursor:
    #         myCursor.execute("SELECT cedula,nombre,apellido,telefono,direccion,email FROM tbl_cliente WHERE cedula = %s", (cedula,))
    #         cliente = myCursor.fetchone()
    #     conexion.close()
    #     return cliente
    
    # def _consultar_cliente_por_cedula_p(self, cedula):
    #     print("\----- ENTRANDO A LA FUNCIÓN -----")
    #     resultadoCliente = []
    #     objConector = ConectorBD()
    #     myCursor = objConector.obtener_conexion()
    #     # myCursor.execute("SELECT * FROM tbl_cliente WHERE cedula = %s", (cedula,))
    #     myCursor.execute("SELECT * FROM tbl_cliente")
    #     resultadoCliente = myCursor.fetchone() #fetchone ayuda a obtener los resultados consultados
    #     myCursor.close()
        
    #     # Si la cédula está registrada la variable será de tipo tupla
    #     if(type(resultadoCliente)==tuple):
    #         print("\n----- El cliente con la cédula: "+cedula+" es: -----")
    #         for x in resultadoCliente:
    #             print(x)
    #         return resultadoCliente
    #     else:
    #         print("Cliente no encontrado")
    #     # print(type(resultadoCliente)) Era para ver el tipo de la variable según los datos almacenados
    
    # def consultar_cliente_por_id(self, id):
    #     objConector = ConectorBD()
    #     conexion = objConector.obtener_conexion()
    #     cliente = []
    #     with conexion.cursor() as cursor:
    #         cursor.execute("SELECT * FROM tbl_cliente WHERE cedula = %s", (id,))
    #         cliente = cursor.fetchone()
    #     conexion.close()
    #     return cliente

    # Método del instructor 
    def consultar_cliente_por_cedula(self, cedula):
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion()
        registro_cc_cliente = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_cliente WHERE cedula = %s", (cedula,))
            registro_cc_cliente = cursor.fetchone()
        conexion.close()
        return registro_cc_cliente

    # ----- Método funcional -----
    def eliminar_cliente(self, id):
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM tbl_cliente WHERE cedula = %s", (id,))
        conexion.commit()
        conexion.close()

    # El método actualizar_cliente recibe como parametros adicionales al self, los datos del registro cliente a actualizar.
    # Este método es llamado por el módulo principal (main) desde la ruta /actualizar_cliente, la cual es a su vez llamada
    # desde la plantilla editar_cliente.html al dar click en el <button>Guardar. Este método realiza un llamado al método
    # consultar_cliente_por_cedula para poder preguntar si ya existe una cedula igual en otro registro si ya existe, puede darse por dos cosas:
    # 1. porque es la del propio registro que se quiere actualizar, en cuyo caso no hay problema y se actualiza el registro, puesto
    # que lo que se está intentando es actualizar otros campos
    # 2. se encuentra en otro registro, en este caso no se intenta actualizar, porque ocurriría un error, en este caso lo mejor es
    # simplemente retornar un mensaje de que ya existe. Ahora si no existe la cedula, quiere decir que se puede realizar
    # igualmente la actualización, incluso la de la cédula.
    #   
    # ----- Método funcional -----#
    def actualizar_cliente(self,cedula,nombres,apellidos,telefono,direccion,email,cc_primera):
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion()
        mensaje = "OK" # OK si no hay ducaplicados de cedula
        #preguntar si ya existe una cliente con esa cedula
        registro_cc_buscada = self.consultar_cliente_por_cedula(cedula)
        print("------- id:"+cc_primera)
        if registro_cc_buscada: #Si la cédula tiene registro...

            if str(registro_cc_buscada[0]) == cc_primera: #si es el mismo registro
                print("-------- Se dejará la misma cédula ----------")
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE tbl_cliente SET cedula = %s, nombre = %s, apellido = %s, telefono = %s, direccion = %s,  email = %s WHERE cedula = %s", (cedula,nombres,apellidos,telefono,direccion,email,cc_primera))
                conexion.commit()
                conexion.close()
            else:
                nombreApellido = self.obtenerNombreApellido(cedula)
                nombre = nombreApellido[0]
                apellido = nombreApellido[1]
                mensaje="¡ya existe un cliente con la cédula " + cedula + "! Corresponde a " + nombre+" "+apellido
                print(mensaje)
        else: #Si la cédula no está registrada (None)
            print("----Mensaje else (if registro_cc_buscada:) ",mensaje)  
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE tbl_cliente SET cedula = %s, nombre = %s, apellido = %s, telefono = %s, direccion = %s,  email = %s WHERE cedula = %s", (cedula,nombres,apellidos,telefono,direccion,email,cc_primera))
            conexion.commit()
            conexion.close()
        return mensaje

    # ----- Método funcional ----- Obtener nombre y apellido
    def obtenerNombreApellido(self,cc):
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion()
        cliente = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT nombre, apellido FROM tbl_cliente WHERE cedula = %s", (cc,))
            cliente = cursor.fetchone()
        conexion.close()
        return cliente

    # Ordenar cliente por 
    def ordenar_cliente_por(self,x): #En_prueba
        print("\n---------- Consultando cliente por "+x+"------------------")
        objConector = ConectorBD()
        conexion = objConector.obtener_conexion() #abre la conexión

        clientes = []
        with conexion.cursor() as cursor:
            cursor.execute("Select * from tbl_cliente order by "+x) #(" SELECT * FROM tbl_cliente ORDER BY %s;",(x,)) # SELECT * FROM tbl_cliente ORDER BY apellido;
            clientes = cursor.fetchall()
        conexion.close()
        print(clientes)
        return clientes