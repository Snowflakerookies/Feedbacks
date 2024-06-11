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
        cursor.execute("SELECT * FROM FACTS_FEEDBACK ORDER BY FECHA DESC")
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
        query = """INSERT INTO FACTS_FEEDBACK (FECHA, PUNT_SKILLS, DESC_SKILLS, PUNT_TEAMWORK, DESC_TEAMWORK, 
                PUNT_EMPATHY, DESC_EMPATHY, PUNT_MOTIVATION, DESC_MOTIVATION, EMAIL_EVALUADOR, EMAIL_EVALUADO)
                   VALUES (CURRENT_DATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            feedback.PUNT_SKILLS, feedback.DESC_SKILLS, feedback.PUNT_TEAMWORK,
            feedback.DESC_TEAMWORK, feedback.PUNT_EMPATHY, feedback.DESC_EMPATHY,
            feedback.PUNT_MOTIVATION, feedback.DESC_MOTIVATION,  feedback.EMAIL_EVALUADOR, feedback.EMAIL_EVALUADO
        ))
        query2 = """
        INSERT INTO DIM_FECHA (FECHA) VALUES (CURRENT_DATE())
        """
        cursor.execute(query2,)
        db.commit()
        return {"message": "Feedback insertado con éxito"}
    except Exception as e:
        print(f"Error al insertar el nuevo feedback en Snowflake: {e}")
        raise HTTPException(status_code=500, detail="Error al crear el feedback")
    finally:
        cursor.close() 
        
# Obtener  feedback por EMAIL_EVALUADOR
@router.get("/feedback/evaluador/{EMAIL_EVALUADOR}")
def get_feedback_by_evaluator_email(EMAIL_EVALUADOR: str, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail_evaluador = EMAIL_EVALUADOR.lower().strip()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE LOWER(EMAIL_EVALUADOR) = LOWER(%s) ORDER BY FECHA DESC", (mail_evaluador,))
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

# Obtener feedback por EMAIL_EVALUADO
@router.get("/feedback/evaluado/{EMAIL_EVALUADO}")
def get_feedback_by_evaluated_email(EMAIL_EVALUADO: str, db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail_evaluado = EMAIL_EVALUADO.lower().strip()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE LOWER(EMAIL_EVALUADO) = LOWER(%s) ORDER BY FECHA DESC", (mail_evaluado,))
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
        
#Obtener feedbacks de evualuador a evaluado
@router.get("/feedback/evaluado/{EMAIL_EVALUADOR}/{EMAIL_EVALUADO}")
def get_feedback_by_evaluator_and_evaluated_email(EMAIL_EVALUADOR: str,EMAIL_EVALUADO: str ,db: snowflake.connector.SnowflakeConnection = Depends(get_snowflake_connection)):
    try:
        mail_evaluador = EMAIL_EVALUADOR.lower().strip()
        mail_evaluado = EMAIL_EVALUADO.lower().strip()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM FACTS_FEEDBACK WHERE LOWER(EMAIL_EVALUADOR) = LOWER(%s) AND LOWER(EMAIL_EVALUADO) = LOWER(%s) ORDER BY FECHA DESC", (mail_evaluador, mail_evaluado))
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
        