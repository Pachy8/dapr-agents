from dapr_agents import tool, ReActAgent, OpenAIChatClient
from dotenv import load_dotenv

# 環境変数用
import os


load_dotenv()

@tool
def search_weather(city: str) -> str:
    """Get weather information for a city."""
    weather_data = {"london": "rainy", "paris": "sunny"}
    return weather_data.get(city.lower(), "Unknown")

@tool
def get_activities(weather: str) -> str:
    """Get activity recommendations."""
    activities = {"rainy": "Visit museums", "sunny": "Go hiking"}
    return activities.get(weather.lower(), "Stay comfortable")

# Azure AI ServiceのLLM設定
azure_llm = OpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
)


react_agent = ReActAgent(
    llm=azure_llm,
    name="TravelAgent",
    role="Travel Assistant",
    instructions=["Check weather, then suggest activities"],
    tools=[search_weather, get_activities]
)

result = react_agent.run("What should I do in London today?")

if len(result) > 0:
    print ("Result:", result)