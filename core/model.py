from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gpt_model_4o(model_name="gpt-4o-mini", temperature=0):
    return ChatOpenAI(model=model_name, temperature=temperature)

def get_gemini_model_2_5_flash(model_name="gemini-2.5-flash", temperature=0):
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)