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
  request_id: Optional[str]