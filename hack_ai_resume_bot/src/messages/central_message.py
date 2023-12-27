from datetime import datetime

from uagents import Model


class CentralMessageFromClient(Model):
  type: "RESUME_UPLOAD" | "TITLE_SELECTED" | "POSTING_SELECTED" | "SCHEDULE_REMINDER" 
  file: str | None
  titleOption: int | None
  postingOption: int | None
  scheduleTime: datetime | None
  postingLink: str | None

class CentralMessageFromServer(Model):
  type: "JOB_LISTINGS"
  jobListings: list | None