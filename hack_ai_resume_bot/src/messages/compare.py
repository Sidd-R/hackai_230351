from uagents import Model
from pydantic import Field

class ResumeCompareResponse(Model):
    job_description: str = Field(description="This is the job description that the user has uploaded")
    job_compatibility: int = Field(description="This is the job compatibility that the user has uploaded")