from messages import UAgentResponse, JobTitleRequest, JobTitleResponse, ClientResponse
from uagents import Agent, Context, Protocol
import requests
from uagents.setup import fund_agent_if_low
import os
import re
import PyPDF2
import joblib
from io import BytesIO
import base64

JOB_TITLE_SEED = os.getenv("JOB_TITLE_SEED", "job_title really secret phrase")

clf = joblib.load("clf.joblib")

categories = [
    "Java Developer",
    "DevOps Engineer",
    "Python Developer",
    "Web Designing ",
    "Hadoop",
    "ETL Developer",
    "Blockchain",
    "Data Science",
    "Database",
    "DotNet Developer",
    "Automation Testing",
    "Network Security Engineer",
    "SAP Developer",
]

def pdf_to_text(pdf_file):
    text = ""
    with open(pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def cleanResume(resumeText):
    resumeText = re.sub("http\S+\s*", " ", resumeText)  # remove URLs
    resumeText = re.sub("RT|cc", " ", resumeText)  # remove RT and cc
    resumeText = re.sub("#\S+", "", resumeText)  # remove hashtags
    resumeText = re.sub("@\S+", "  ", resumeText)  # remove mentions
    resumeText = re.sub(
        "[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", resumeText
    )  # remove punctuations
    resumeText = re.sub(r"[^\x00-\x7f]", r" ", resumeText)
    resumeText = re.sub("\s+", " ", resumeText)  # remove extra whitespace
    return resumeText

agent = Agent(
    name="job_title_recommendation",
    seed=JOB_TITLE_SEED
)

fund_agent_if_low(agent.wallet.address())

def decode_from_base64(encoded_string):
    decoded_data = base64.b64decode(encoded_string)
    output_file_path = os.path.join("./decoded_file.pdf")
    with open(output_file_path, "wb") as file:
        file.write(decoded_data)
    return output_file_path

@agent.on_message(model=JobTitleRequest)#, replies=UAgentResponse)
async def job_title_recommendation(ctx: Context, sender: str, msg: JobTitleRequest):
    pdf_content = decode_from_base64(msg.resume)
    text = pdf_to_text(pdf_content)
    cleaned_resume = cleanResume(text)
    word_vectorizer = joblib.load("./wordvec.joblib")
    WordFeatures = word_vectorizer.transform([cleaned_resume])
    category = clf.predict(WordFeatures)
    recommended_job_title = categories[category[0]]
    print("job title recommendation", recommended_job_title)
    await ctx.send('agent1qthu0ll2z92ckynm96x5fx3qdlwp46e0ksnpnqt29mdp48tghsqaq4rppz3', JobTitleResponse(job_title=recommended_job_title, client_address=msg.client_address, resume=msg.resume))
