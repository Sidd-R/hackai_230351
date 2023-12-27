from messages import UAgentResponse, ScheduleReminder
from uagents import Agent, Context, Protocol
import requests
from uagents.setup import fund_agent_if_low
import os
from datetime import datetime, timedelta

SCHEDULE_REMINDER_SEED = os.getenv("JOB_TITLE_SEED", "schedule_reminder really secret phrase")

# create schedule reminder agent
agent = Agent(
    name="schedule_reminder_recommendation",
    seed=SCHEDULE_REMINDER_SEED,
)

fund_agent_if_low(agent.wallet.address())

# get no of days to schedule reminder 
@agent.on_message(model=ScheduleReminder)
async def receive_schedule_remainder(ctx: Context, sender: str, msg: ScheduleReminder):
    jobs = ctx.storage.get("jobs") or {}
    job_deadline = datetime.now() + timedelta(days=msg.job_deadline)
    ctx.logger.info(f"Received schedule reminder from {sender}")
    if msg.job_deadline in jobs:
        jobs[msg.job_deadline].append((msg.job_title, msg.job_url))
    else:
        jobs[msg.job_deadline] = [(msg.job_title, msg.job_url)]
    ctx.storage.set("jobs", jobs)

@agent.on_interval(period=60)
async def send_schedule_reminder(ctx: Context):
    jobs = ctx.storage.get("jobs") or {}
    tomorrow = datetime.now() + timedelta(days=1)
    for deadline, job_details_list in jobs.items():
        if deadline == tomorrow:
            for job_title, job_url in job_details_list:
                reminder_msg = f"Reminder: Tomorrow is the deadline for job '{job_title}'. Don't forget to complete it! {job_url}"
                await ctx.send(sender=msg.client_address, text=reminder_msg)


# agent.include(schedule_remainder_protocol)