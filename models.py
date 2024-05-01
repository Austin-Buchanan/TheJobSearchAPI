from pydantic import BaseModel, Field, HttpUrl

class JobApp(BaseModel):
    employer_name: str = Field(max_length=256)
    job_name: str = Field(max_length=256)
    location: str = Field(max_length=256)
    app_date: str | None = Field(
        default=None,
        description="Format as yyyy-mm-dd",
        max_length=256
    )
    status: str | None = Field(
        default=None,
        max_length=256 
    )
    update_link: HttpUrl | None = None
    notes: str | None = None

class JobAppUpdate(BaseModel):
    employer_name: str = Field(default=None, max_length=256)
    job_name: str = Field(default=None, max_length=256)
    location: str = Field(default=None, max_length=256)
    app_date: str | None = Field(
        default=None,
        description="Format as yyyy-mm-dd",
        max_length=256
    )
    status: str | None = Field(
        default=None,
        max_length=256 
    )
    update_link: HttpUrl | None = None
    notes: str | None = None

class SafetyNetApp(JobApp):
    shift_type: str 

class SafetyNetUpdate(BaseModel):
    employer_name: str = Field(default=None, max_length=256)
    job_name: str = Field(default=None, max_length=256)
    shift_type: str = Field(default=None, max_length=256)
    location: str = Field(default=None, max_length=256)
    app_date: str | None = Field(
        default=None,
        description="Format as yyyy-mm-dd",
        max_length=256
    )
    status: str | None = Field(
        default=None,
        max_length=256 
    )
    update_link: HttpUrl | None = None
    notes: str | None = None