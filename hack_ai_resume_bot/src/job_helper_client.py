from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import os
from typing import TextIO
from messages import CentralMessage

# class CentralMessage(Model):
#     type: int
#     # file: TextIO | None
#     titleOption: int | None
#     compareOption: int | None

# get seed from .env
JOB_HELPER_CLIENT_SEED = os.environ.get("JOB_HELPER_CLIENT_SEED", "job helper client")

# create currency exchange agent for client
# currency_exchange_client = Agent(
#     name="currency_exchange_client",
#     port=8008,
#     seed=JOB_HELPER_CLIENT_SEED,
#     endpoint=["http://127.0.0.1:8008/submit"],
# )

job_helper_client = Agent(
  name="job_helper_client",
  port=8008,
  seed=JOB_HELPER_CLIENT_SEED,
  endpoint=["http://127.0.0.1:8008/submit"],
)


fund_agent_if_low(job_helper_client.wallet.address())

job_helper_request = CentralMessage(type=1)
                                            # file=None, 

# @currency_exchange_client.on_event("startup")
# async def send_message(ctx: Context):
#     # send message to server to initiate currency exchange alert
#     await ctx.send("{exchange_currency_address}", currency_exchange_request)


# @currency_exchange_client.on_message(model=UAgentResponse)
# async def message_handler(ctx: Context, _: str, msg: UAgentResponse):
#     if msg.type == UAgentResponseType.ALERT:
#         # log alert message if target currency value exceeds specified limit
#         ctx.logger.info(f"Alert: {msg.message}")
#     elif msg.type == UAgentResponseType.ERROR:
#         # log error message if any error occurs
#         ctx.logger.info(f"Error: {msg.message}")

@job_helper_client.on_interval(period=2.0)
async def temp(ctx: Context):
  ctx.logger.info(f'hello, my name is {ctx.name}')
  await ctx.send('agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj',job_helper_request)


if __name__ == "__main__":
    # currency_exchange_client.run()
    job_helper_client.run()
