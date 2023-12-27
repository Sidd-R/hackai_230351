from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
# from messages import UAgentResponse, UAgentResponseType
from messages import CentralMessage
import os
from typing import TextIO
# class CentralMessage(Model):
#   type: int
#   # file: TextIO | None
#   titleOption: int | None
#   compareOption: int | None


agent = Agent(
  name="central_agent",
  seed=os.environ.get("CENTRAL_AGENT_SEED", "central agent")
)

fund_agent_if_low(agent.wallet.address())

@agent.on_event("startup")
async def startup_event(context: Context):
  print("Central agent started")

@agent.on_message(model=CentralMessage)
async def message_event(context: Context, sender: str, message: CentralMessage):
  print("Central agent received a message from",sender)
  # print(context)
  print("type of message ",message.type)
  
  # if context.message.type == UAgentResponseType.ALERT:
  #   print("Central agent received an alert")
  #   print(context.message)
  #   print("Central agent sending an alert to the user")
  #   response = requests.post("http://