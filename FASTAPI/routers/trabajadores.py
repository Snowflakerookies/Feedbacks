from fastapi import APIRouter, HTTPException, Depends
from models.trabajador import Trabajador
from db.connection import get_snowflake_connection
import snowflake.connector

router = APIRouter()

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

@router.get("/trabajadores/{TRABAJADOR_NOMBRE}/{TRABAJADOR_APELLIDO1}/{TRABAJADOR_APELLIDO2}")
def get_worker_email_by_name(TRABAJADOR_NOMBRE: str, TRABAJADOR_APELLIDO1: str, TRABAJADOR_APELLIDO2: str, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        nombre = TRABAJADOR_NOMBRE.lower().strip()
        apellido1 = TRABAJADOR_APELLIDO1.lower().strip()
        apellido2 = TRABAJADOR_APELLIDO2.lower().strip()
        cursor = db.cursor()
        cursor.execute("""
            SELECT EMAIL FROM LANDING_TRABAJADOR 
            WHERE LOWER(NOMBRE) = LOWER(%s) 
            AND LOWER(APELLIDO1) = LOWER(%s) 
            AND LOWER(APELLIDO2) = LOWER(%s)
        """, (nombre, apellido1, apellido2))
        trabajador = cursor.fetchone()
        if not trabajador:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        return trabajador
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer datos desde Snowflake: {e}")
    finally:
        cursor.close()

@router.post("/trabajadores/")
def create_worker(trabajador: Trabajador, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO LANDING_TRABAJADOR (NOMBRE, APELLIDO1, APELLIDO2, PUESTO, EMAIL, VERTICAL)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.PUESTO, trabajador.EMAIL, trabajador.VERTICAL))
        db.commit()
        return {"message": "Trabajador creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el trabajador en Snowflake: {e}")
    finally:
        cursor.close()

@router.put("/trabajadores/{EMAIL}")
def update_worker_by_id(EMAIL: str, trabajador: Trabajador, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail = EMAIL.lower().strip()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE LANDING_TRABAJADOR SET NOMBRE = %s, APELLIDO1 = %s, APELLIDO2 = %s, PUESTO = %s, EMAIL = %s, VERTICAL = %s 
            WHERE LOWER(EMAIL) = LOWER(%s)
        """, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.PUESTO, trabajador.EMAIL, trabajador.VERTICAL, mail))
        db.commit()
        return {"message": "Trabajador actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Trabajador en Snowflake: {e}")
    finally:
        cursor.close()

@router.put("/trabajadores/{TRABAJADOR_NOMBRE}/{TRABAJADOR_APELLIDO1}/{TRABAJADOR_APELLIDO2}")
def update_worker_by_name(TRABAJADOR_NOMBRE: str, TRABAJADOR_APELLIDO1: str, TRABAJADOR_APELLIDO2: str, trabajador: Trabajador, db: snowflake.connector.connection.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        nombre = TRABAJADOR_NOMBRE.lower().strip()
        apellido1 = TRABAJADOR_APELLIDO1.lower().strip()
        apellido2 = TRABAJADOR_APELLIDO2.lower().strip()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE LANDING_TRABAJADOR SET NOMBRE = %s, APELLIDO1 = %s, APELLIDO2 = %s, PUESTO = %s, EMAIL = %s, VERTICAL = %s 
            WHERE LOWER(NOMBRE) = LOWER(%s) AND LOWER(APELLIDO1) = LOWER(%s) AND LOWER(APELLIDO2) = LOWER(%s)
        """, (trabajador.NOMBRE, trabajador.APELLIDO1, trabajador.APELLIDO2, trabajador.PUESTO, trabajador.EMAIL, trabajador.VERTICAL, nombre, apellido1, apellido2))
        db.commit()
        return {"message": "Trabajador actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Trabajador en Snowflake: {e}")
    finally:
        cursor.close()

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
