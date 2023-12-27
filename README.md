#  Job-Mitra - Resume Analyser & Job Finder
## Description
### Agent Architecture
The agent architecture is as follows - 
![Agent Architecture](https://github.com/Sidd-R/hackai_230351/blob/main/agent_architecture.png?raw=true)

### Workflow
The project workflow is as follows - 
![Project Workflow](https://github.com/Sidd-R/hackai_230351/blob/main/workflow.png?raw=true)

The job search agent using Fetch.AI's uAgent is a agent that can be used to analyze the resume and find the perfect job title and job openings. This can be useful for freshers as well as experienced developers as it reduces the manual work of searching compatible jobs.
The job search agent works as follows first the agent on the client side sends the resume upload by the user to the server side. The resume is then sent to the job title recommendation agent where we have used a model trained using 2400 resumes across some predefined categories. The model works on K-nearest neighbours approach to classify and provide a job title.
The job title now received is further send to the job search agent where first jobs are searched for the particular title using the CORE_SIGNAL_API. Now the jobs obtained are compared on the basis of their job descriptions and the features extracted from the resume to provide a compatibility score. The list of the jobs is sorted and then displayed to the user.
The user can now select a job of his/her choice and set a reminder for the application deadline so that he/she can fill the application before the deadline.
## Instructions To Run The Project
### Step 1: Prerequisites
Before starting, you'll need the following:
* Python (3.8+ is recommended)
* Poetry (a packaging and dependency management tool for Python)

### Step 2: Set up .env file
To run the demo, you need API keys from:
* PALM API
* Core Signal API

##### Google PALM API Key
* Visit Google PALM API.
* Sign up or log in.
* Once subscribed, copy your PALM API key.

Note that if you’ve run out of OpenAI credits, you will not be able to get results for this example.

##### Core Signal API Key
* Visit CORE SIGNAL.
* Sign up or log in.
* Once subscribed, copy your Core Signal API Key.


Once you have all three keys, create a .env file in the hack_ai_resume_bot/src directory.
```bash
export PALM_API_KEY="{GET THE API KEY}"
export CORESIGNAL_API_KEY="{GET THE API KEY}"
```
To use the environment variables from .env and install the project:
```bash
cd src
source .env
poetry install
```
### Step 3: Run the main script
To run the project and its agents:
```bash
poetry run python main.py
```
You need to look for the following output in the logs:
```
Adding top destinations agent to Bureau: {top_dest_address}
```
Copy the {top_dest_address} value and paste it somewhere safe. You will need it in the next step.
### Step 4: Set up the client script
Now that we have set up the integrations, let’s run a client script that will -
1. Input the resume from the user.
2. Provide the most recommended job title for the user.
3. Search for the perfect job openings available for the user along with the compatibility for each job posting.
4. The user can now select the job he/she likes the most and set a reminder for the application deadline for the job.

Now that we have set up the server, let’s run the client script. To do this, replace the address in ctx.send with the value you received in the previous step in ./src/job_helper_client.py.
### Step 5: Run the client script
Open a new terminal (let the previous one be as is), and navigate to the src folder to run the client.
```bash
cd src
poetry run python job_helper_client.py
```
Once you hit upload resume and press enter, a request will be sent to the central server agent to analyze your resume and explore various jobs for you.
