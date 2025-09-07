# Super intelligent chatbot

This project aims at providing an API endpoint for answering questions from a CSV file.
Assumes that you are the owner of a small shop, and you want to have a chatbot available 
to answer questions from your data source, this is for you.

## How-to Guide

### 1. Create an OpenAI API token

If you haven't created any OpenAI account yet, please register one at https://platform.openai.com. After that, navigate to https://platform.openai.com/account/api-keys (or https://platform.openai.com/settings/profile?tab=api-keys), press `Start verification` to verify your phone number and click on `Create new secret key`.

![API key](chatgpt.png)

When you have already created your key, update your `.env.example` file to replace my key.

### 2. Run the API locally

```shell
set -a && source .env.example && set +a
uvicorn main:app --host 0.0.0.0 --port 8081
```

Open your browser and access this address `localhost:8081/docs` to access API doc (Swagger UI).

### 3. Enjoy your API

There are two routes in the Swagger UI:

- `/chat`: Press `Try it out`, then enter `Show me the image url of Saint Laurent YSL Men's Black/Brown Leather Zip Around Wallet` in the `text` and press `Execute`
![API key](chat.png)

- `/chat-auth`: Press `Try it out`, then enter `username`: `quandv` and `password`: `bQeUYlfCyITO` to authenticate.
After that, enter the text as the `/chat` route.