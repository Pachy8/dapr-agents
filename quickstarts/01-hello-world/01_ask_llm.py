from dapr_agents import OpenAIChatClient
from dotenv import load_dotenv

# 環境変数用
import os

load_dotenv()

# Azure AI ServiceのLLM設定
llm = OpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
)

response = llm.generate("ダジャレを言ってください。")
if len(response.get_content())>0:
    print("Got response:", response.get_content())
