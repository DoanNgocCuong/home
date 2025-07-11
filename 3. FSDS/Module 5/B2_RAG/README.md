# Welcome to lab of lesson 2 - Introduction to RAG

## Mission: You need to add router a.k.a API to the demo.

`Objective of API` is receiving an user's mesage and forwarding to Langchain's graph and response an answer.

## Hint:

1. Create a file named `demo-rag/routers.py` and add API rounter to this file.
2. Refactor a file named `main.py` with instance of FastAPI and assign above router to it. You can set any port for this application. Example 8000.
3. Open your browser and access application's Swagger via localhost:8000/docs to test your API.
4. Reference: https://fastapi.tiangolo.com/tutorial/


---

## Set up env: 
```bash
# Create a virtual environment named 'venv'
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```


# Run: 
```bash
pip install uv # install uv

uv sync           # Install all dependencies from pyproject.toml and uv.lock
uv run main.py    # Run your main.py file using uv
```