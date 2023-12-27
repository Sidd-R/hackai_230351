from uagents import Model
from pydantic import Field

class JobTitleRequest(Model):
  resume: str 
  client_address: str
  
class JobTitleResponse(Model):
  job_title: str
  client_address: str
  resume: str 