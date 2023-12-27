from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
from messages import CentralMessageFromClient, JobTitleRequest
import os
from typing import TextIO
import base64

agent = Agent(
  name="central_agent",
  seed=os.environ.get("CENTRAL_AGENT_SEED", "central agent")
)

fund_agent_if_low(agent.wallet.address())

def decode_from_base64(encoded_string):
  decoded_data = base64.b64decode(encoded_string)
  output_file_path = "./decoded_file.txt"
  with open(output_file_path, "wb") as file:
      print("The file does not exist.",encoded_string)
      file.write(decoded_data)
  return output_file_path

@agent.on_event("startup")
async def startup_event(context: Context):
  print("Central agent started")

@agent.on_message(model=CentralMessageFromClient)
async def message_event(context: Context, sender: str, msg: CentralMessageFromClient):
  print("Central agent received a message from",sender)
  await context.send("agent1q0e6p9geqsk772mw6uz46y3868c5ymtpdmxlvfnv9zmswl7vwwdeul6tpfm",JobTitleRequest(resume=msg.resume,client_address=sender))
