from uagents import Model
from pydantic import Field

class JobTitle(Model):
  resume: str = Field(description="This is the resume that the user has uploaded")
  client_address: str = Field(description="This is the client address of the user")