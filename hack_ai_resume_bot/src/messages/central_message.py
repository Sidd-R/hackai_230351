from datetime import datetime

from uagents import Model


class CentralMessageFromClient(Model):
  type: str #"RESUME_UPLOAD" | "TITLE_SELECTED" | "POSTING_SELECTED" | "SCHEDULE_REMINDER" 
  resume: str | None
  titleOption: int | None
  postingOption: int | None
  scheduleTime: datetime | None
  postingLink: str | None

class CentralMessageFromServer(Model):
  type: str#"JOB_LISTINGS"
  jobListings: list | None
  
class ClientResponse(Model):
  type: str#"JOB_LISTINGS"
  # jobListings: list | None
  job_urls: list | None
  job_titles: list | None
  compatibility: list | None
  