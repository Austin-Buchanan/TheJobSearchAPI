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

class SafetyNetApp(JobApp):
    shiftType: str 