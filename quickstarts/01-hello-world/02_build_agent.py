from dapr_agents import tool, Agent, OpenAIChatClient
from dotenv import load_dotenv

# 環境変数用
import os

load_dotenv()
@tool
def my_weather_func() -> str:
    """Get current weather."""
    return "It's 72°F and sunny"

# Azure AI ServiceのLLM設定
azure_llm = OpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
)

weather_agent = Agent(
    llm=azure_llm,
    name="WeatherAgent",
    role="Weather Assistant",
    instructions=["Help users with weather information"],
    tools=[my_weather_func]
)

response = weather_agent.run("What's the weather?")
print(response)