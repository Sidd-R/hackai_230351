from uagents import Model
from pydantic import Field

class ResumeCompareResponse(Model):
    # resume: str = Field(description="This is the resume that the user has uploaded")
    job_description: str = Field(description="This is the job description that the user has uploaded")
    # client_address: str = Field(description="This is the client address of the user")
    job_compatibility: int = Field(description="This is the job compatibility that the user has uploaded")