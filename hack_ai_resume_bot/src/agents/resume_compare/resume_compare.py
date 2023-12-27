from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
import requests
from messages import UAgentResponse, UAgentResponseType
import os

agent = Agent(
  name="resume_compare",
  seed=os.environ.get("RESUME_COMPARE_SEED", "resume compare")
)

fund_agent_if_low(agent.wallet.address())

