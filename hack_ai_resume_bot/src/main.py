from agents.central_agent.central_agent import agent as central_agent
from agents.resume_compare.resume_compare import agent as resume_compare_agent
from agents.schedule_reminder.schedule_reminder import agent as schedule_reminder_agent
from agents.job_title_recommendation.job_title_recommendation import agent as job_title_recommendation_agent
from uagents import Bureau
import warnings

warnings.filterwarnings("ignore",)

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    print(f"Adding central agent to Bureau: {central_agent.address}")
    bureau.add(central_agent)
    print(f"Adding resume compare agent to Bureau: {resume_compare_agent.address}")
    bureau.add(resume_compare_agent)
    print(f"Adding schedule reminder agent to Bureau: {schedule_reminder_agent.address}")
    bureau.add(schedule_reminder_agent)
    print(f"Adding job title recommendation agent to Bureau: {job_title_recommendation_agent.address}")
    bureau.add(job_title_recommendation_agent)

    bureau.run()
