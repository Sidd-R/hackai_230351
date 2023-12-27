from messages import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Protocol
import requests
from uagents.setup import fund_agent_if_low
import os

JOB_TITLE_SEED = os.getenv("JOB_TITLE_SEED", "job_title really secret phrase")

agent = Agent(
    name="job_title_recommendation",
    seed=JOB_TITLE_SEED
)

fund_agent_if_low(agent.wallet.address())
