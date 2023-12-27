from messages import UAgentResponse, JobTitleResponse, ClientResponse
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
import os
import google.generativeai as palm
import PyPDF2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
import base64
import requests
import json


RESUME_COMPARE_SEED = os.getenv("RESUME_COMPARE_SEED", "resume_compare really secret phrase")

palm.configure(api_key="AIzaSyAmJZX92dPwWWwyWRyPzWukcmbawQiAzGg")

defaults = {
    "model": "models/text-bison-001",
    "temperature": 0.7,
    "candidate_count": 1,
    "top_k": 40,
    "top_p": 0.95,
    "max_output_tokens": 1024,
    "stop_sequences": [],
    "safety_settings": [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2},
    ],
}

agent = Agent(
    name="resume_compare_recommendation",
    seed=RESUME_COMPARE_SEED
)

def pdf_to_text(pdf_file):
    text = ""
    with open(pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def decode_from_base64(encoded_string):
    decoded_data = base64.b64decode(encoded_string)
    output_file_path = os.path.join("./decoded_file.pdf")
    with open(output_file_path, "wb") as file:
        file.write(decoded_data)
    return output_file_path

fund_agent_if_low(agent.wallet.address())

# resume_compare_protocol = Protocol(ResumeCompare)

async def get_job_postings(job_title:str):
    import requests
    import json

    url = "https://api.coresignal.com/cdapi/v1/linkedin/job/search/filter"

    payload = json.dumps({
    "title": job_title,
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjE4MmE3MDM1LWRmN2EtYzdkOS04MGQwLTljOThjZjFlYTA5OCJ9.eyJhdWQiOiJzcGl0IiwiZXhwIjoxNzM1MjM0MjgxLCJpYXQiOjE3MDM2NzczMjksImlzcyI6Imh0dHBzOi8vb3BzLmNvcmVzaWduYWwuY29tOjgzMDAvdjEvaWRlbnRpdHkvb2lkYyIsIm5hbWVzcGFjZSI6InJvb3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzcGl0Iiwic3ViIjoiZmEwYzRjOWMtYzIxYy1mZmRmLWMwYjktNDhhZWQ1YWY5YzE2IiwidXNlcmluZm8iOnsic2NvcGVzIjoiY2RhcGkifX0.N13pF6Lh4EZSK9dYknUIl6aZTjHEiynhvuTWIKa_xhNSU9SN0_kYqHH4lXRjDlpCKkUrVZ09JFbPswG3Y_I5BA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    job_ids = json.loads(response.text)
    
    job_descriptions = []
    job_urls = []
    job_titles = []
    
    for i in range(5):
        url = f"https://api.coresignal.com/cdapi/v1/linkedin/job/collect/{job_ids[i]}"

        payload = {}
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjE4MmE3MDM1LWRmN2EtYzdkOS04MGQwLTljOThjZjFlYTA5OCJ9.eyJhdWQiOiJzcGl0IiwiZXhwIjoxNzM1MjM0MjgxLCJpYXQiOjE3MDM2NzczMjksImlzcyI6Imh0dHBzOi8vb3BzLmNvcmVzaWduYWwuY29tOjgzMDAvdjEvaWRlbnRpdHkvb2lkYyIsIm5hbWVzcGFjZSI6InJvb3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzcGl0Iiwic3ViIjoiZmEwYzRjOWMtYzIxYy1mZmRmLWMwYjktNDhhZWQ1YWY5YzE2IiwidXNlcmluZm8iOnsic2NvcGVzIjoiY2RhcGkifX0.N13pF6Lh4EZSK9dYknUIl6aZTjHEiynhvuTWIKa_xhNSU9SN0_kYqHH4lXRjDlpCKkUrVZ09JFbPswG3Y_I5BA'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        job = json.loads(response.text)
        job_descriptions.append(job.get("description"))
        job_urls.append(job.get("url"))
        job_titles.append(job.get("title"))
        
    return job_descriptions, job_urls, job_titles
    

@agent.on_message(model=JobTitleResponse)
async def receive_schedule_remainder(ctx: Context, sender: str, msg: JobTitleResponse):
    ctx.logger.info(f"Received resume compare from {sender}")
    ctx.storage.set("resume", msg.resume)
    job_descriptions, job_urls, job_titles = await get_job_postings(msg.job_title)

    pdf_content_resume = decode_from_base64(msg.resume)

    text_resume = pdf_to_text(pdf_content_resume)
    text_resume = text_resume.replace("\n", " ")
    prompt_resume = f"Resume Of Candidate : {text_resume}. Extract this candidate's educational qualifications, work experience, and skills following these guidelines: 0) Do not add headings. 1) If there is no work experience found, add None. 2) Do not use symbols, just represent in text. 3) For educational qualifications, simply extract the Bachelor's degree of the candidate."

    response_resume = palm.generate_text(**defaults, prompt=prompt_resume)
    generated_resume = response_resume.result
    
    compatibility = []
    
    for job_description in job_descriptions:
        prompt2 = f"Job Description : {job_description}. Extract this job's required educational qualifications and skills. Do not add headings"
        response_jd = palm.generate_text(**defaults, prompt=prompt2)
        generated_jd = response_jd.result

        model_name = "bert-base-uncased"
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertModel.from_pretrained(model_name)

        tokens_resume = tokenizer.encode(
            generated_resume, max_length=512, add_special_tokens=True, truncation=True
        )
        tokens_jd = tokenizer.encode(
            generated_jd, max_length=512, add_special_tokens=True, truncation=True
        )

        tokens_tensor_resume = torch.tensor([tokens_resume])
        tokens_tensor_jd = torch.tensor([tokens_jd])

        model.eval()

        with torch.no_grad():
            outputs_resume = model(tokens_tensor_resume)
            word_embeddings_resume = outputs_resume.last_hidden_state
            outputs_jd = model(tokens_tensor_jd)
            word_embeddings_jd = outputs_jd.last_hidden_state

        vector_data_resume = word_embeddings_resume.mean(dim=1).squeeze().numpy()
        vector_data_jd = word_embeddings_jd.mean(dim=1).squeeze().numpy()
        similarity = cosine_similarity(np.array([vector_data_resume]), np.array([vector_data_jd]))

        response_message = similarity[0][0] * 100
        compatibility.append(response_message)
        # print("similarity", response_message)
        # print("job description", job_descriptions)
    
    for x in range(5):
        for y in range(5):
            if compatibility[x] > compatibility[y]:
                temp = compatibility[x]
                compatibility[x] = compatibility[y]
                compatibility[y] = temp
                
                temp = job_descriptions[x]
                job_descriptions[x] = job_descriptions[y]
                job_descriptions[y] = temp
                
                temp = job_urls[x]
                job_urls[x] = job_urls[y]
                job_urls[y] = temp
                
                temp = job_titles[x]
                job_titles[x] = job_titles[y]
                job_titles[y] = temp    
    
    await ctx.send(msg.client_address, ClientResponse(type="JOB_LISTINGS",compatibility=compatibility,job_descriptions=job_descriptions,job_urls=job_urls,job_titles=job_titles))

# agent.include(resume_compare_protocol)
