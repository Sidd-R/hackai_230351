from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
import requests
from messages import UAgentResponse, UAgentResponseType
import os

agent = Agent(
  name="schedule_reminder",
  seed=os.environ.get("SCHEDULE_REMINDER_SEED", "schedule reminder")
)

fund_agent_if_low(agent.wallet.address())

