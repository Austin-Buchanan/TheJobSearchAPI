from fastapi import FastAPI, Query, Path, Body
from typing import Annotated
from models import JobApp, JobAppUpdate, SafetyNetApp, SafetyNetUpdate
import utilities as u

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/jobapps/")
async def get_all_applications(
    employer_name: Annotated[str | None, Query(max_length=256)] = None,
    job_name: Annotated[str | None, Query(max_length=256)] = None,
    location: Annotated[str | None, Query(max_length=256)] = None,
    status: Annotated[str | None, Query(max_length=256)] = None 
):
    sql = "SELECT * FROM main_applications"
    if employer_name or job_name or location or status:
        sql += " WHERE "
    paramCounter = 0
    if employer_name:
        sql += "employer_name = '" + employer_name.replace('_', '') + "'"
        paramCounter += 1
    if job_name:
        if paramCounter != 0:
            sql += " and "
        sql += "job_name = '" + job_name.replace('_', '') + "'"
        paramCounter += 1
    if location:
        if paramCounter != 0:
            sql += " and "
        sql += "location = '" + location.replace('_', '') + "'"
        paramCounter += 1
    if status:
        if paramCounter != 0:
            sql += " and "
        sql += "status = '" + status.replace('_', '') + "'"
    sql += ';'

    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        applications = []
        for result in results:
            applications.append(u.appFromRecord(result))
        return {"applications": applications}

@app.post("/jobapps/")
async def add_job_application(
    jobApp: Annotated[
        JobApp,
        Body(
            examples=[
                {
                    "employer_name": "AustinCodesOnline Inc.",
                    "job_name": "Software Engineer",
                    "location": "Remote",
                    "app_date": "2024-05-01",
                    "status": "Scheduling second interview",
                    "update_link": "http://austincodes.online/careers/this_does_not_exist/",
                    "notes": "Requires 2 cups of coffee per day"                    
                }
            ]
        )
    ]
):
    appDate = ''
    if jobApp.app_date is None or jobApp.app_date == '':
        appDate = 'CURRENT_DATE'
    else:
        appDate = "'" + jobApp.app_date + "'"
    sqlInsert = """
                INSERT INTO main_applications (
                    "employer_name", 
                    "job_name", 
                    "location", 
                    "app_date", 
                    "status", 
                    "update_link", 
                    "notes"
                ) 
                VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', '{6}') 
                RETURNING app_id;
                """.format(
                    u.remove_apostrophes(jobApp.employer_name), 
                    u.remove_apostrophes(jobApp.job_name),
                    u.remove_apostrophes(jobApp.location), 
                    appDate, 
                    u.remove_apostrophes(jobApp.status),
                    jobApp.update_link, 
                    u.remove_apostrophes(jobApp.notes)
                )
    
    success, result = u.execute_SQL(sqlInsert)
    if not success:
        return {"error": result[0]}
    else:
        return {"app_id": result[0]}
    
@app.get("/jobapps/{id}/")
async def get_app_by_id(id: Annotated[int, Path(gt=0)]):
    sql = """SELECT * FROM main_applications WHERE app_id = {0}""".format(id)
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"application": u.appFromRecord(result[0])}
    
@app.delete("/jobapps/{id}/")
async def delete_app_by_id(id: Annotated[int, Path(gt=0)]):
    sql = """DELETE FROM main_applications WHERE app_id = {0}""".format(id)
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} deleted."}
    
@app.put("/jobapps/{id}/")
async def update_app_by_id(
    id: Annotated[int, Path(gt=0)], 
    appUpdate: JobAppUpdate
):
    updateDict = u.dict_from_JobAppUpdate(appUpdate)
    sql = u.getUpdateFromDict(updateDict, "main_applications", id)
    success, result = u.execute_SQL(sql)
    if not success: 
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} updated."}
    
@app.get("/employers/")
async def get_employer_names():
    sql = "SELECT DISTINCT employer_name FROM main_applications;"
    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        return {"employer_names": results}

@app.get("/jobnames/")
async def get_job_names():
    sql = "SELECT DISTINCT job_name FROM main_applications;"
    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        return {"job_names": results}

@app.get("/locations/")
async def get_locations():
    sql = "SELECT DISTINCT location FROM main_applications;"
    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        return {"locations": results}

@app.get("/statuses/")
async def get_statuses():
    sql = "SELECT DISTINCT status FROM main_applications;"
    success, results = u.execute_SQL(sql)
    if not success:
        return {"error": results[0]}
    else:
        return {"statuses": results}

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
    if safetyNetApp.app_date is None or safetyNetApp.app_date == '':
        appDate = 'CURRENT_DATE'
    else:
        appDate = "'" + safetyNetApp.app_date + "'"
    sql = """
            INSERT INTO safety_nets (
                "employer_name",
                "job_name",
                "shift_type",
                "location",
                "app_date",
                "status",
                "update_link",
                "notes"
            ) VALUES ('{0}', '{1}', '{2}', '{3}', {4}, '{5}', '{6}', '{7}')
            RETURNING app_id;
          """.format(
              u.remove_apostrophes(safetyNetApp.employer_name),
              u.remove_apostrophes(safetyNetApp.job_name),
              u.remove_apostrophes(safetyNetApp.shift_type),
              u.remove_apostrophes(safetyNetApp.location),
              appDate,
              u.remove_apostrophes(safetyNetApp.status),
              safetyNetApp.update_link,
              u.remove_apostrophes(safetyNetApp.notes)
          )
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"application_id": result[0]}    

@app.put("/safetynets/{id}/")
async def update_safety_net_by_id(
    id: Annotated[int, Path(gt=0)], 
    sNetUpdate: SafetyNetUpdate
):
    updateDict = u.dict_from_SafetyNetUpdate(sNetUpdate)
    sql = u.getUpdateFromDict(updateDict, "safety_nets", id)
    success, result = u.execute_SQL(sql)
    if not success:
        return {"error": result[0]}
    else:
        return {"message": f"Application {id} updated."}       