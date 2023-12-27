from messages import UAgentResponse, UAgentResponseType, ScheduleReminder
from uagents import Agent, Context, Protocol
import requests
from uagents.setup import fund_agent_if_low
import os
from datetime import datetime, timedelta

SCHEDULE_REMINDER_SEED = os.getenv("JOB_TITLE_SEED", "schedule_reminder really secret phrase")

agent = Agent(
    name="schedule_reminder_recommendation",
    seed=SCHEDULE_REMINDER_SEED
)

fund_agent_if_low(agent.wallet.address())

schedule_remainder_protocol = Protocol(ScheduleReminder)

@schedule_remainder_protocol.on_message(model=ScheduleReminder, replies=UAgentResponse)
async def receive_schedule_remainder(ctx: Context, sender: str, msg: ScheduleReminder):
    jobs = ctx.storage.get("jobs") or {}
    ctx.logger.info(f"Received schedule reminder from {sender}")
    if msg.job_deadline in jobs:
        jobs[msg.job_deadline].append((msg.job_title, msg.job_url))
    else:
        jobs[msg.job_deadline] = [(msg.job_title, msg.job_url)]
    ctx.storage.set("jobs", jobs)

@schedule_remainder_protocol.on_interval(period=60)
async def send_schedule_reminder(ctx: Context, sender: str, msg: ScheduleReminder):
    jobs = ctx.storage.get("jobs") or {}
    tomorrow = datetime.now() + timedelta(days=1)
    for deadline, job_details_list in jobs.items():
        if deadline.date() == tomorrow.date():
            for job_title, job_url in job_details_list:
                reminder_msg = f"Reminder: Tomorrow is the deadline for job '{job_title}'. Don't forget to complete it! {job_url}"
                await ctx.send_message(sender=sender, text=reminder_msg)


agent.include(schedule_remainder_protocol)
