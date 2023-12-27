from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import os
from messages import CentralMessageFromClient
import base64
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

JOB_HELPER_CLIENT_SEED = os.environ.get("JOB_HELPER_CLIENT_SEED", "job helper client")

job_helper_client = Agent(
  name="job_helper_client",
  port=8008,
  seed=JOB_HELPER_CLIENT_SEED,
  endpoint=["http://127.0.0.1:8008/submit"],
)

fund_agent_if_low(job_helper_client.wallet.address())

job_helper_request = CentralMessageFromClient(type=1)

def encode_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string

@job_helper_client.on_event("startup")
async def send_message(ctx: Context):
  file_path = ""
  while file_path == "":
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
  file = encode_to_base64(file_path)
  await ctx.send("agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj", CentralMessageFromClient(type=1, file=file))
    # send message to server to initiate currency exchange alert
    # file = encode_to_base64("test.txt")
    # await ctx.send("agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj", CentralMessageFromClient(type=1, file=file))



# @currency_exchange_client.on_message(model=UAgentResponse)
# async def message_handler(ctx: Context, _: str, msg: UAgentResponse):
#     if msg.type == UAgentResponseType.ALERT:
#         # log alert message if target currency value exceeds specified limit
#         ctx.logger.info(f"Alert: {msg.message}")
#     elif msg.type == UAgentResponseType.ERROR:
#         # log error message if any error occurs
#         ctx.logger.info(f"Error: {msg.message}")

# @job_helper_client.on_interval(period=2.0)
# async def temp(ctx: Context):
#   ctx.logger.info(f'hello, my name is {ctx.name}')
#   await ctx.send('agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj',job_helper_request)


if __name__ == "__main__":
    # currency_exchange_client.run()
    job_helper_client.run()
