# 21-07-2022

import mysql.connector

# Conexión a la base de datos
class ConectorBD:
    def obtener_conexion(self):
        return mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='db_motos_norte',
            port='3306'
        )

if __name__=="__main__":
    print("Llamado desde el mismo modulo (ConexionBD_cmn)")
else:
    print("Llamado desde otro modulo")