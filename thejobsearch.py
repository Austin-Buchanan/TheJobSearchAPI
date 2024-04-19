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

class JobAppUpdate(BaseModel):
    employerName: str | None = None
    jobName: str | None = None
    location: str | None = None
    appDate: str | None = None
    status: str | None = None
    updateLink: str | None = None
    notes: str | None = None   

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/jobapps/")
async def get_all_applications():
    sqlSelect = "SELECT * FROM main_applications"
    success, results = execute_SQL(sqlSelect)
    if not success:
        return {"error": results[0]}
    else:
        applications = []
        for result in results:
            applications.append(appFromRecord(result))
        return {"applications": applications}

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
    
@app.get("/jobapps/{id}/")
async def get_app_by_id(id: int):
    sql = """SELECT * FROM main_applications WHERE application_id = {0}""".format(id)
    success, result = execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"application": appFromRecord(result[0])}
    
@app.delete("/jobapps/{id}/")
async def delete_app_by_id(id: int):
    sql = """DELETE FROM main_applications WHERE application_id = {0}""".format(id)
    success, result = execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} deleted."}
    
@app.put("/jobapps/{id}/")
async def update_app_by_id(id: int, appUpdate: JobAppUpdate):
    updateDict = dict_from_JobAppUpdate(appUpdate)
    updateKeys = list(updateDict.keys())
    
    sql = """UPDATE main_applications """
    for i in range(len(updateKeys)):
        if i == 0:
            sql += """SET"""
        sql += f""" {updateKeys[i]} = '{updateDict[updateKeys[i]]}'"""
        if i < len(updateKeys) - 1:
            sql += ""","""
    sql += f""" WHERE application_id = {id}"""

    success, result = execute_SQL(sql)
    if not success: 
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} updated."}

def dict_from_JobAppUpdate(appUpdate: JobAppUpdate):
    updateDict = {}
    if appUpdate.employerName is not None:
        updateDict["employer_name"] = appUpdate.employerName
    if appUpdate.jobName is not None:
        updateDict["job_name"] = appUpdate.jobName
    if appUpdate.location is not None:
        updateDict["location"] = appUpdate.location
    if appUpdate.appDate is not None:
        updateDict["application_date"] = appUpdate.appDate
    if appUpdate.status is not None:
        updateDict["status"] = appUpdate.status
    if appUpdate.updateLink is not None:
        updateDict["link_for_updates"] = appUpdate.updateLink
    if appUpdate.notes is not None:
        updateDict["notes"] = appUpdate.notes
    return updateDict

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

def appFromRecord(record):
    print(record)
    return {
        "applicationId": record[0],
        "employerName": record[1],
        "jobName": record[2],
        "location": record[3],
        "appDate": record[4],
        "status": record[5],
        "updateLink": record[6],
        "notes": record[7]
    }    