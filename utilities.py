import psycopg2
from config import load_config
from models import JobAppUpdate

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

def safetyNetFromRecord(record):
    return {
        "applicationId": record[0],
        "employerName": record[1],
        "jobName": record[2],
        "shiftType": record[3],
        "location": record[4],
        "appDate": record[5],
        "status": record[6],
        "updateLink": record[7],
        "notes": record[8]
    }