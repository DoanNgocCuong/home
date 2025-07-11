from langchain.chat_models import init_chat_model
from src.settings import SETTINGS

# Initialize the LLM with the specified model and settings
# This code initializes a chat model using the OpenAI API with specific parameters.
# The model used is "gpt-4o-mini", with a temperature setting of 0.7 for response variability.
llm = init_chat_model(
    "gpt-4o-mini",
    api_key=SETTINGS.OPENAI_API_KEY,
    temperature=0.5,
    model_provider="openai",
)
