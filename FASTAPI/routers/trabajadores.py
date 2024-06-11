from fastapi import APIRouter, HTTPException, Depends
from models.trabajador import Trabajador
from db.connection import get_snowflake_connection
import snowflake.connector
from typing import Optional

router = APIRouter()

#Obtener todos los trabajadores
@router.get("/trabajadores/")
def get_all_workers(db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM LANDING_TRABAJADOR")
        trabajadores = cursor.fetchall()
        return trabajadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

#Obtener todos los nombres de los trabajadores
@router.get("/trabajadores/name")
def get_all_names(db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT NOMBRE, APELLIDO1, APELLIDO2 FROM LANDING_TRABAJADOR")
        trabajadores = cursor.fetchall()
        return trabajadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

#Obtener todos los emails de los trabajadores        
@router.get("/trabajadores/email")
def get_all_emails(db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT EMAIL FROM LANDING_TRABAJADOR")
        trabajadores = cursor.fetchall()
        return trabajadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

#Obtener el trabajador por el email
@router.get("/trabajadores/{EMAIL}")
def get_worker_by_id(EMAIL : str, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail = EMAIL.lower().strip()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM LANDING_TRABAJADOR WHERE LOWER(EMAIL) = LOWER(%s)", (mail,))
        trabajador = cursor.fetchone()
        if not trabajador:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        return trabajador
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

#Obtener el nombre del trabajador por el email
@router.get("/trabajadores/name/{EMAIL}")
def get_worker_name_by_email(EMAIL: str, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail = EMAIL.lower().strip()
        cursor = db.cursor()
        cursor.execute("SELECT NOMBRE, APELLIDO1, APELLIDO2 FROM LANDING_TRABAJADOR WHERE LOWER(EMAIL) = LOWER(%s)", (mail,))
        trabajador = cursor.fetchone()
        if not trabajador:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        return trabajador
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

#Obtener email por nombre completo
@router.get("/trabajadores/{TRABAJADOR_NOMBRE}/{TRABAJADOR_APELLIDO1}")
def get_worker_email_by_name(
    TRABAJADOR_NOMBRE: str,
    TRABAJADOR_APELLIDO1: str,
    TRABAJADOR_APELLIDO2: Optional[str] = None,
    db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)
):
    cursor = None
    try:
        nombre = TRABAJADOR_NOMBRE.lower().strip()
        apellido1 = TRABAJADOR_APELLIDO1.lower().strip()

        cursor = db.cursor()

        if TRABAJADOR_APELLIDO2:
            apellido2 = TRABAJADOR_APELLIDO2.lower().strip()
            query = """
                SELECT EMAIL FROM LANDING_TRABAJADOR 
                WHERE LOWER(NOMBRE) = %s 
                AND LOWER(APELLIDO1) = %s 
                AND LOWER(APELLIDO2) = %s
            """
            cursor.execute(query, (nombre, apellido1, apellido2))
        else:
            query = """
                SELECT EMAIL FROM LANDING_TRABAJADOR 
                WHERE LOWER(NOMBRE) = %s 
                AND LOWER(APELLIDO1) = %s
            """
            cursor.execute(query, (nombre, apellido1))

        trabajador = cursor.fetchall()
        if not trabajador:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        if len(trabajador) > 1:
            raise HTTPException(status_code=400, detail="Hay más de un trabajador con ese nombre y primer apellido, por favor introduzca el segundo apellido")
        return {"email": trabajador[0]}
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as e:

                raise HTTPException(status_code=500, detail=f"Error closing cursor: {e}")
        try:
            db.close()
        except Exception as e:

            raise HTTPException(status_code=500, detail=f"Error closing database connection: {e}")      

#Crear nuevo trabajador
@router.post("/trabajadores/")
def create_worker(trabajador: Trabajador, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        
        # Comprobar si el EMAIL ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM LANDING_TRABAJADOR 
            WHERE EMAIL = %s
        """, (trabajador.EMAIL,))
        result = cursor.fetchone()
        
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="Ya existe un trabajador con ese email")

        cursor.execute("""
            INSERT INTO LANDING_TRABAJADOR (NOMBRE, APELLIDO1, APELLIDO2, EMAIL, VERTICAL, COHORTE, PUESTO)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.EMAIL, trabajador.VERTICAL, trabajador.COHORTE ,trabajador.PUESTO))
        db.commit()
        return {"message": "Trabajador creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el trabajador en Snowflake: {e}")
    finally:
        cursor.close()

#Actualizar trabajador por id
@router.put("/trabajadores/{EMAIL}")
def update_worker_by_id(EMAIL: str, trabajador: Trabajador, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail = EMAIL.lower().strip()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE LANDING_TRABAJADOR SET NOMBRE = %s, APELLIDO1 = %s, APELLIDO2 = %s,  EMAIL = %s, VERTICAL = %s, COHORTE = %s ,PUESTO = %s
            WHERE LOWER(EMAIL) = LOWER(%s)
        """, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.EMAIL, trabajador.VERTICAL, trabajador.COHORTE, trabajador.PUESTO, mail))
        db.commit()
        return {"message": "Trabajador actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Trabajador en Snowflake: {e}")
    finally:
        cursor.close()

#Actualizar trabajador por nombre completo
@router.put("/trabajadores/{TRABAJADOR_NOMBRE}/{TRABAJADOR_APELLIDO1}}")
def update_worker_by_name(TRABAJADOR_NOMBRE: str, TRABAJADOR_APELLIDO1: str,  trabajador: Trabajador, TRABAJADOR_APELLIDO2: Optional[str] = None, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        nombre = TRABAJADOR_NOMBRE.lower().strip()
        apellido1 = TRABAJADOR_APELLIDO1.lower().strip()
        cursor = db.cursor()
        
        if TRABAJADOR_APELLIDO2:
            apellido2 = TRABAJADOR_APELLIDO2.lower().strip()
            query = ("""
            UPDATE LANDING_TRABAJADOR SET NOMBRE = %s, APELLIDO1 = %s, APELLIDO2 = %s, EMAIL = %s, VERTICAL = %s, COHORTE = %s ,PUESTO = %s
            WHERE LOWER(NOMBRE) = LOWER(%s) AND LOWER(APELLIDO1) = LOWER(%s) AND LOWER(APELLIDO2) = LOWER(%s)
            """)
            cursor.execute(query, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.EMAIL,
                                   trabajador.VERTICAL, trabajador.COHORTE, trabajador.PUESTO, nombre, apellido1, apellido2))
        else:
            query = ("""
            UPDATE LANDING_TRABAJADOR SET NOMBRE = %s, APELLIDO1 = %s, APELLIDO2 = %s, EMAIL = %s, VERTICAL = %s, COHORTE = %s ,PUESTO = %s
            WHERE LOWER(NOMBRE) = LOWER(%s) AND LOWER(APELLIDO1) = LOWER(%s)  
            """)
            cursor.execute(query, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.EMAIL,
                                   trabajador.VERTICAL, trabajador.COHORTE, trabajador.PUESTO, nombre, apellido1))
        db.commit()
        return {"message": "Trabajador actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Trabajador en Snowflake: {e}")
    finally:
        cursor.close()

#Borrar trabajador por id
@router.delete("/trabajadores/{EMAIL}")
def delete_worker_by_id(EMAIL: str, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail = EMAIL.lower().strip()
        cursor = db.cursor()
        cursor.execute("DELETE FROM LANDING_TRABAJADOR WHERE LOWER(EMAIL) = LOWER(%s)", (mail,))
        db.commit()
        return {"message": "Trabajador eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el trabajador en Snowflake: {e}")
    finally:
        cursor.close()

#Borrar trabajador por nombre completo
@router.delete("/trabajadores/{TRABAJADOR_NOMBRE}/{TRABAJADOR_APELLIDO1}/{TRABAJADOR_APELLIDO2}")
def delete_worker_by_name(TRABAJADOR_NOMBRE: str, TRABAJADOR_APELLIDO1: str, TRABAJADOR_APELLIDO2: str, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        nombre = TRABAJADOR_NOMBRE.lower().strip()
        apellido1 = TRABAJADOR_APELLIDO1.lower().strip()
        apellido2 = TRABAJADOR_APELLIDO2.lower().strip()
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM LANDING_TRABAJADOR 
            WHERE LOWER(NOMBRE) = LOWER(%s) AND LOWER(APELLIDO1) = LOWER(%s) AND LOWER(APELLIDO2) = LOWER(%s)
        """, (nombre, apellido1, apellido2))
        db.commit()
        return {"message": "Trabajador eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el trabajador en Snowflake: {e}")
    finally:
        cursor.close()
