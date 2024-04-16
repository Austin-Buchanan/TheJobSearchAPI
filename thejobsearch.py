import psycopg2
from config import load_config
from fastapi import FastAPI
from pydantic import BaseModel

class JobApp(BaseModel):
    employerName: str
    jobName: str
    location: str
    appDate: str | None = None
    status: str | None = None
    updateLink: str | None = None
    notes: str | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/jobapps/")
async def add_job_application(jobApp: JobApp):
    appDate = ''
    if jobApp.appDate is None or jobApp.appDate == '':
        appDate = 'CURRENT_DATE'
    else:
        appDate = "'" + jobApp.appDate + "'"
    sqlInsert = """
                INSERT INTO main_applications (
                    "employer_name", 
                    "job_name", 
                    "location", 
                    "application_date", 
                    "status", 
                    "link_for_updates", 
                    "notes"
                ) 
                VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', '{6}') 
                RETURNING application_id;
                """.format(
                    remove_apostrophes(jobApp.employerName), 
                    remove_apostrophes(jobApp.jobName),
                    remove_apostrophes(jobApp.location), 
                    appDate, 
                    remove_apostrophes(jobApp.status),
                    jobApp.updateLink, 
                    remove_apostrophes(jobApp.notes)
                )
    
    success, result = execute_SQL(sqlInsert)
    if not success:
        return {"error": result[0]}
    else:
        return {"application_id": result[0]}

def execute_SQL(sql: str):
    config = load_config()
    rows = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if sql.startswith('SELECT'):
                    rows = cur.fetchall()
                elif 'RETURNING' in sql:
                    rows = cur.fetchone()
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        rows.append(str(error))
        return False, rows
    return True, rows

def remove_apostrophes(inString):
    return inString.replace("'", "")