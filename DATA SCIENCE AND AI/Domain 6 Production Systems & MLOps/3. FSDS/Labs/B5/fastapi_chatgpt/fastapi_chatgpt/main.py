from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger

from utils import chat_with_llm, init_conversation

app = FastAPI()
security = HTTPBasic()

# Initialize conversation with LLM
qa = init_conversation("data/products.csv")


@app.get("/metadata")
def get_metadata():
    return {"my_metadata": "this is my metadata"}


@app.post("/chat")
def chat(text: str):
    logger.info(f"User: {text}")
    response = chat_with_llm(qa, text)
    return {"response": response}


# Please read more about this here
# https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
@app.post("/chat-auth")
def chat(text: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username != "quandv" or credentials.password != "bQeUYlfCyITO":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    logger.info(f"User: {text}")
    response = chat_with_llm(qa, text)
    return {"response": response}
