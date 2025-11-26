from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:/Users/JAI/Downloads/ai-legal-assistant-crewai-main/ai-legal-assistant-crewai-main/.env")

print("Loaded key:", os.getenv("GROQ_API_KEY"))
