from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import os
from messages import CentralMessageFromClient, ClientResponse, ScheduleReminder
import base64

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta

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
    tk.Tk().withdraw() 
    file_path = askopenfilename()  # ask resume from user
    
  file = encode_to_base64(file_path)
  
  await ctx.send("agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj", CentralMessageFromClient(type=1, resume=file))



@job_helper_client.on_message(model=ClientResponse)
async def message_handler(ctx: Context, sender: str, msg: ClientResponse):
    job_ids = [i+1 for i in range(5)]

    for x in range(5):
        print("Job Index:",job_ids[x])
        print("Job Title:",msg.job_titles[x])
        print("Job Url:",msg.job_urls[x])
        print("Job compatibility:",msg.compatibility[x])
        print("---------------------------------\n")
    # generate graph
    root = tk.Tk()
    root.title("Job Recommendations")

    # Plot the graph
    plt.figure(figsize=(8, 6))
    plt.barh(msg.job_titles, msg.compatibility, color="skyblue")
    plt.xlabel("Similarity %", fontsize=12)
    plt.title("Job Recommendations", fontsize=14)
    plt.gca().invert_yaxis()  # Invert y-axis to display job titles from top to bottom
    plt.tight_layout()

    # Annotate the bars with job IDs
    for i, v in enumerate(msg.compatibility):
        plt.text(v + 1, i, f"Job ID: {job_ids[i]}", color="black", fontsize=10, va="center")

    # Display the graph in a Tkinter window and center-align
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(
        side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20
    )  # Center alignment

    # ask for reminder
    x = ""
    while x != "n" and x != "y" and x != "N" and x != "Y":
      x = input("Do you want to set reminder for this job? (y/n)\n")
      if x != "n" and x != "y" and x != "N" and x != "Y":
        print("Please enter a valid input")
      
    if x == "y" or x == "Y":
      job_index = 6
      # select job
      while (job_index >5 or job_index < 0):
        job_index = int(input("Enter the job number you want to set reminder for\n"))
      
      no_of_days = 0  
      # ṣelect no of days after which the reminder should be shown
      while (no_of_days < 1):
        no_of_days = int(input("\nEnter the number of days you want to set reminder for\n"))
        if no_of_days < 1:
          print("Please enter a number greater than 0")
          # give date of current date + no_of_days
      
      await ctx.send("agent1qwge5z5m6ghkm35sum22zeuv7q37nv7yj5cw7n2l8k2zd44e8n5njmez40r",ScheduleReminder(job_title=msg.job_titles[job_index],job_url=msg.job_urls[job_index],job_deadline=no_of_days))
      
      print("Reminder set")  

if __name__ == "__main__":
    # currency_exchange_client.run()
    job_helper_client.run()
