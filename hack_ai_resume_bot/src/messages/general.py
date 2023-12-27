from uagents import Model
from enum import Enum
from typing import Optional, List

class UAgentResponseType(Enum):
  ERROR = "error"
  ALERT = "alert"

class UAgentResponse(Model):
  type: UAgentResponseType
  agent_address: Optional[str]
  message: Optional[str]
  options: Optional[List[KeyValue]]
  request_id: Optional[str]