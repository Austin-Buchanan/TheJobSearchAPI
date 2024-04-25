import psycopg2
from config import load_config
from models import JobAppUpdate, SafetyNetUpdate

def dict_from_JobAppUpdate(appUpdate: JobAppUpdate):
    updateDict = {}
    if appUpdate.employer_name is not None:
        updateDict["employer_name"] = appUpdate.employer_name
    if appUpdate.job_name is not None:
        updateDict["job_name"] = appUpdate.job_name
    if appUpdate.location is not None:
        updateDict["location"] = appUpdate.location
    if appUpdate.app_date is not None:
        updateDict["app_date"] = appUpdate.app_date
    if appUpdate.status is not None:
        updateDict["status"] = appUpdate.status
    if appUpdate.update_link is not None:
        updateDict["update_link"] = appUpdate.update_link
    if appUpdate.notes is not None:
        updateDict["notes"] = appUpdate.notes
    return updateDict

def dict_from_SafetyNetUpdate(sNetUpdate: SafetyNetUpdate):
    updateDict = {}
    if sNetUpdate.employer_name is not None:
        updateDict["employer_name"] = sNetUpdate.employer_name
    if sNetUpdate.job_name is not None:
        updateDict["job_name"] = sNetUpdate.job_name
    if sNetUpdate.shift_type is not None:
        updateDict["shift_type"] = sNetUpdate.shift_type
    if sNetUpdate.location is not None:
        updateDict["location"] = sNetUpdate.location
    if sNetUpdate.app_date is not None:
        updateDict["app_date"] = sNetUpdate.app_date
    if sNetUpdate.status is not None:
        updateDict["status"] = sNetUpdate.status
    if sNetUpdate.update_link is not None:
        updateDict["update_link"] = sNetUpdate.update_link
    if sNetUpdate.notes is not None:
        updateDict["notes"] = sNetUpdate.notes
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
        "app_id": record[0],
        "employer_name": record[1],
        "job_name": record[2],
        "location": record[3],
        "app_date": record[4],
        "status": record[5],
        "update_link": record[6],
        "notes": record[7]
    }

def safetyNetFromRecord(record):
    return {
        "app_id": record[0],
        "employer_name": record[1],
        "job_name": record[2],
        "shift_type": record[3],
        "location": record[4],
        "app_date": record[5],
        "status": record[6],
        "update_link": record[7],
        "notes": record[8]
    }

def getUpdateFromDict(updateDict: dict[str], tableName: str, id: int):
    updateKeys = list(updateDict.keys())
    sql = f"""UPDATE {tableName} """
    for i in range(len(updateKeys)):
        if i == 0:
            sql += """SET"""
        sql += f""" {updateKeys[i]} = '{updateDict[updateKeys[i]]}'"""
        if i < len(updateKeys) - 1:
            sql += ""","""
    sql += f""" WHERE app_id = {id}"""
    return sql
