from pydantic import BaseModel

class JobApp(BaseModel):
    employer_name: str
    job_name: str
    location: str
    app_date: str | None = None
    status: str | None = None
    update_link: str | None = None
    notes: str | None = None

class JobAppUpdate(BaseModel):
    employer_name: str | None = None
    job_name: str | None = None
    location: str | None = None
    app_date: str | None = None
    status: str | None = None
    update_link: str | None = None
    notes: str | None = None  

class SafetyNetApp(JobApp):
    shift_type: str 