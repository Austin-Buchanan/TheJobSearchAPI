from fastapi import FastAPI
from models import JobApp, JobAppUpdate, SafetyNetApp
import utilities as u

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/jobapps/")
async def get_all_applications():
    sqlSelect = "SELECT * FROM main_applications"
    success, results = u.execute_SQL(sqlSelect)
    if not success:
        return {"error": results[0]}
    else:
        applications = []
        for result in results:
            applications.append(u.appFromRecord(result))
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
                    u.remove_apostrophes(jobApp.employerName), 
                    u.remove_apostrophes(jobApp.jobName),
                    u.remove_apostrophes(jobApp.location), 
                    appDate, 
                    u.remove_apostrophes(jobApp.status),
                    jobApp.updateLink, 
                    u.remove_apostrophes(jobApp.notes)
                )
    
    success, result = u.execute_SQL(sqlInsert)
    if not success:
        return {"error": result[0]}
    else:
        return {"application_id": result[0]}
    
@app.get("/jobapps/{id}/")
async def get_app_by_id(id: int):
    sql = """SELECT * FROM main_applications WHERE application_id = {0}""".format(id)
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"application": u.appFromRecord(result[0])}
    
@app.delete("/jobapps/{id}/")
async def delete_app_by_id(id: int):
    sql = """DELETE FROM main_applications WHERE application_id = {0}""".format(id)
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} deleted."}
    
@app.put("/jobapps/{id}/")
async def update_app_by_id(id: int, appUpdate: JobAppUpdate):
    updateDict = u.dict_from_JobAppUpdate(appUpdate)
    updateKeys = list(updateDict.keys())
    
    sql = """UPDATE main_applications """
    for i in range(len(updateKeys)):
        if i == 0:
            sql += """SET"""
        sql += f""" {updateKeys[i]} = '{updateDict[updateKeys[i]]}'"""
        if i < len(updateKeys) - 1:
            sql += ""","""
    sql += f""" WHERE application_id = {id}"""

    success, result = u.execute_SQL(sql)
    if not success: 
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} updated."}

@app.get("/safetynets/")
async def get_all_safety_nets():
    sql = "SELECT * from safety_nets"
    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        applications = []
        for result in results:
            applications.append(u.safetyNetFromRecord(result))
        return {"applications": applications}     

@app.post("/safetynets/")
async def add_safety_net_app(safetyNetApp: SafetyNetApp):
    appDate = ''
    if safetyNetApp.appDate is None or safetyNetApp.appDate == '':
        appDate = 'CURRENT_DATE'
    else:
        appDate = "'" + safetyNetApp.appDate + "'"
    sql = """
            INSERT INTO safety_nets (
                "employer_name",
                "job_name",
                "shift_type",
                "location",
                "application_date",
                "status",
                "link_for_updates",
                "notes"
            ) VALUES ('{0}', '{1}', '{2}', '{3}', {4}, '{5}', '{6}', '{7}')
            RETURNING application_id;
          """.format(
              u.remove_apostrophes(safetyNetApp.employerName),
              u.remove_apostrophes(safetyNetApp.jobName),
              u.remove_apostrophes(safetyNetApp.shiftType),
              u.remove_apostrophes(safetyNetApp.location),
              appDate,
              u.remove_apostrophes(safetyNetApp.status),
              safetyNetApp.updateLink,
              u.remove_apostrophes(safetyNetApp.notes)
          )
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"application_id": result[0]}           