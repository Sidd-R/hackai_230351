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
        # print(file_path)
        # print(encoded_string)
        return encoded_string

@job_helper_client.on_event("startup")
async def send_message(ctx: Context):
  file_path = ""
  while file_path == "":
    tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
  print(file_path,"ll")
  file = encode_to_base64(file_path)
  await ctx.send("agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj", CentralMessageFromClient(type=1, resume=file))
    # send message to server to initiate currency exchange alert
    # file = encode_to_base64("test.txt")
    # await ctx.send("agent1q2cjl4yd4e9acf7y5xddvpv8c97uuf84fusvynyda20xramjnu4zwwk99lj", CentralMessageFromClient(type=1, file=file))



@job_helper_client.on_message(model=ClientResponse)
async def message_handler(ctx: Context, sender: str, msg: ClientResponse):
    # if msg.type == UAgentResponseType.ALERT:
    #     # log alert message if target currency value exceeds specified limit
    #     ctx.logger.info(f"Alert: {msg.message}")
    # elif msg.type == UAgentResponseType.ERROR:
    #     # log error message if any error occurs
    #     ctx.logger.info(f"Error: {msg.message}")
    print("____________________________________________________________________")
    for x in range(5):
        print(msg.job_titles[x])
        print(msg.job_urls[x])
        print(msg.compatibility[x])
        print("____________________________________________________________________")
        
    # print(msg.job_descriptions, msg.compatibility)
    print("____________________________________________________________________")
    job_ids = [i+1 for i in range(5)]

    # Create Tkinter window
      # Extract job titles, similarity percentages, and job IDs
    # job_titles = [job["job_title"] for job in job_recommendations]
    # similarities = [job["similarity"] for job in job_recommendations]
    # job_ids = [job["job_id"] for job in job_recommendations]

    # Create Tkinter window
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

    x = ""
    while x != "n" and x != "y" and x != "N" and x != "Y":
      x = input("Do you want to set reminder for this job? (y/n)\n")
      if x != "n" and x != "y" and x != "N" and x != "Y":
        print("Please enter a valid input")
      
    if x == "y" or x == "Y":
      job_index = 6
      while (job_index >5 or job_index < 0):
        job_index = int(input("Enter the job number you want to set reminder for\n"))
      
      no_of_days = 0  
      while (no_of_days < 1):
        no_of_days = int(input("\nEnter the number of days you want to set reminder for\n"))
        if no_of_days < 1:
          print("Please enter a number greater than 0")
          # give date of current date + no_of_days
      
      await ctx.send("agent1qwge5z5m6ghkm35sum22zeuv7q37nv7yj5cw7n2l8k2zd44e8n5njmez40r",ScheduleReminder(job_title=msg.job_titles[job_index],job_url=msg.job_urls[job_index],job_deadline=no_of_days))
      
      print("Reminder set")  
  
    # Sample job recommendations data (job ID, job title, similarity %)
    job_recommendations = [
        {"job_id": 1, "job_title": "Software Engineer", "similarity": 80},
        {"job_id": 2, "job_title": "Data Analyst", "similarity": 70},
        {"job_id": 3, "job_title": "Project Manager", "similarity": 60},
        {"job_id": 4, "job_title": "Marketing Specialist", "similarity": 50},
        {"job_id": 5, "job_title": "Financial Analyst", "similarity": 40},
    ]

    # Extract job titles, similarity percentages, and job IDs
    # job_titles = [job["job_title"] for job in job_recommendations]
    # similarities = [job["similarity?"] for job in job_recommendations]
    

    # Create a button to trigger the graph plot
    # plot_button = tk.Button(root, text="Plot Job Recommendations", command=plot_graph)
    # plot_button.pack()

    root.mainloop()    

if __name__ == "__main__":
    # currency_exchange_client.run()
    job_helper_client.run()
