from messages import UAgentResponse, ResumeCompare
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
    return decoded_data

fund_agent_if_low(agent.wallet.address())

resume_compare_protocol = Protocol(ResumeCompare)

@resume_compare_protocol.on_message(model=ResumeCompare, replies=UAgentResponse)
def receive_schedule_remainder(ctx: Context, sender: str, msg: ResumeCompare):
    ctx.logger.info(f"Received resume compare from {sender}")
    ctx.storage.set("resume", msg.resume)
    ctx.storage.set("job_description", msg.job_description)

    pdf_content_resume = decode_from_base64(msg.resume)
    pdf_content_jd = msg.job_description

    text_resume = pdf_to_text(pdf_content_resume)
    text_resume = text_resume.replace("\n", " ")
    prompt_resume = f"Resume Of Candidate : {text_resume}. Extract this candidate's educational qualifications, work experience, and skills following these guidelines: 0) Do not add headings. 1) If there is no work experience found, add None. 2) Do not use symbols, just represent in text. 3) For educational qualifications, simply extract the Bachelor's degree of the candidate."

    response_resume = palm.generate_text(**defaults, prompt=prompt_resume)
    generated_resume = response_resume.result

    response_jd = palm.generate_text(**defaults, prompt=pdf_content_jd)
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

    response_message = f"Resume similarity to job description: {similarity[0][0] * 100}%"

    ctx.send_message(sender=msg.client_address, text=response_message)

agent.include(resume_compare_protocol)
