from fastapi import APIRouter, HTTPException, Depends
from models.feedback import Feedback
from db.connection import get_snowflake_connection
import snowflake.connector

router = APIRouter()

#Obtener todos los feedbacks
@router.get("/feedback/")
def read_feedbacks(db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK")
        trabajadores = cursor.fetchall()
        return trabajadores
    except Exception as e:
        print(f"Error al leer los datos desde Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al leer los datos")

#Crear nuevo feedback
@router.post("/feedback/")
def insert_new_feedback(feedback: Feedback, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        query = """INSERT INTO FACTS_FEEDBACK (FECHA, PUNT_SKILLS, DESC_SKILLS, PUNT_TEAMWORK, DESC_TEAMWORK, PUNT_EMPATHY, DESC_EMPATHY, PUNT_MOTIVATION, DESC_MOTIVATION, EMAIL_EVALUADOR, EMAIL_EVALUADO)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            feedback.FECHA, feedback.PUNT_SKILLS, feedback.DESC_SKILLS, feedback.PUNT_TEAMWORK,
            feedback.DESC_TEAMWORK, feedback.PUNT_EMPATHY, feedback.DESC_EMPATHY,
            feedback.PUNT_MOTIVATION, feedback.DESC_MOTIVATION,  feedback.EMAIL_EVALUADOR, feedback.EMAIL_EVALUADO
        ))
        db.commit()
        return {"message": "Feedback insertado con éxito"}
    except Exception as e:
        print(f"Error al insertar el nuevo feedback en Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al crear el feedback")
    finally:
        cursor.close()

#Obtener un feedback por id
@router.get("/feedback/{FEEDBACK_ID}/")
def get_feedback_by_id(FEEDBACK_ID: int, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE FEEDBACK_ID = %s", (FEEDBACK_ID,))
        feedback = cursor.fetchone()
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        return feedback
    except Exception as e:
        print(f"Error al leer desde Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al leer los datos")
        
        
# Obtener un feedback por EMAIL_EVALUADOR
@router.get("/feedback/evaluador/{EMAIL_EVALUADOR}")
def get_feedback_by_evaluator_email(EMAIL_EVALUADOR: str, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail_evaluador = EMAIL_EVALUADOR.lower().strip()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE LOWER(EMAIL_EVALUADOR) = LOWER(%s)", (mail_evaluador,))
        feedback = cursor.fetchone()
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        return feedback
    except Exception as e:
        print(f"Error al leer desde Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al leer los datos")
    finally:
        cursor.close()
        db.close()

# Obtener un feedback por EMAIL_EVALUADO
@router.get("/feedback/evaluado/{EMAIL_EVALUADO}")
def get_feedback_by_evaluated_email(EMAIL_EVALUADO: str, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail_evaluado = EMAIL_EVALUADO.lower().strip()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE LOWER(EMAIL_EVALUADO) = LOWER(%s)", (mail_evaluado,))
        feedback = cursor.fetchone()
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        return feedback
    except Exception as e:
        print(f"Error al leer desde Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al leer los datos")
    finally:
        cursor.close()
        db.close()
        
#Actualizar un feedback por id
@router.put("/feedback/{FEEDBACK_ID}")
def update_feedback(FEEDBACK_ID: int, feedback: Feedback, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        query = """UPDATE FACTS_FEEDBACK SET 
                   FECHA = %s, PUNT_SKILLS = %s, DESC_SKILLS = %s, PUNT_TEAMWORK = %s,
                   DESC_TEAMWORK = %s, PUNT_EMPATHY = %s, DESC_EMPATHY = %s, PUNT_MOTIVATION = %s, DESC_MOTIVATION = %s,
                   EMAIL_EVALUADOR = %s, EMAIL_EVALUADO = %s 
                   WHERE FEEDBACK_ID = %s"""
        cursor.execute(query, (
            feedback.FECHA, feedback.PUNT_SKILLS, feedback.DESC_SKILLS, feedback.PUNT_TEAMWORK,
            feedback.DESC_TEAMWORK, feedback.PUNT_EMPATHY, feedback.DESC_EMPATHY,
            feedback.PUNT_MOTIVATION, feedback.DESC_MOTIVATION, feedback.EMAIL_EVALUADOR, feedback.EMAIL_EVALUADO,
            FEEDBACK_ID
        ))
        db.commit()
        return {"message": "Feedback actualizado con éxito"}
    except Exception as e:
        print(f"Error al actualizar el feedback en Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el feedback")
    finally:
        cursor.close()

#Borrar un feedback
@router.delete("/feedback/{FEEDBACK_ID}")
def delete_feedback_by_id(FEEDBACK_ID: int, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        cursor = db.cursor()
        query = "DELETE FROM FACTS_FEEDBACK WHERE FEEDBACK_ID = %s"
        cursor.execute(query, (FEEDBACK_ID,)) #SIN LA COMA DA 500
        db.commit()
        return {"message": "Feedback eliminado correctamente"}
    except Exception as e:
        print(f"Error al eliminar el feedback: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el feedback")
    finally:
        cursor.close()    