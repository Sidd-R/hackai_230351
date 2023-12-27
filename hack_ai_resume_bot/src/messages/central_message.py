from uagents import Model


class CentralMessageFromClient(Model):
  type: str 
  resume: str | None
  titleOption: int | None
  postingOption: int | None
  scheduleTime: datetime | None
  postingLink: str | None

class CentralMessageFromServer(Model):
  type: str
  jobListings: list | None
  
class ClientResponse(Model):
  type: str
  job_urls: list | None
  job_titles: list | None
  compatibility: list | None
  