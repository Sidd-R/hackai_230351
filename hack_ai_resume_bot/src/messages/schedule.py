from uagents import Model
from pydantic import Field

class ScheduleReminder(Model):
  job_title: str = Field(description="This is the job title that the user has selected")
  job_url: str = Field(description="This is the job url that the user has selected")
  job_deadline: str = Field(description="This is the job deadline that the user has selected")
  client_address: str = Field(description="This is the client address of the user")