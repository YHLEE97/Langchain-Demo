from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from .slm_model import get_slm_hyperclovax_1_5B

# LLM Model
def get_gpt_model_4o(model_name="gpt-4o-mini", temperature=0):
    return ChatOpenAI(model=model_name, temperature=temperature)

def get_gemini_model_2_5_flash(model_name="gemini-2.5-flash", temperature=0):
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

# Embedding Model
def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

# SLM Model
def get_hyperclovax_1_5B(model_name="HyperCLOVAX-SEED-Text-Instruct-1.5B", temperature=0):
    return get_slm_hyperclovax_1_5B(model_name=model_name, temperature=temperature)