from dapr_agents import Agent, AgentActor
from dotenv import load_dotenv
import asyncio
import logging

# Azure AI Service用クライアント
from dapr_agents import OpenAIChatClient
import os


async def main():
    try:

        # Azure AI ServiceのLLM設定
        azure_llm = OpenAIChatClient(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        )


        # Define Agent
        wizard_agent = Agent(role="Wizard", name="Gandalf",
            llm=azure_llm,
            goal="Guide the Fellowship with wisdom and strategy, using magic and insight to ensure the downfall of Sauron.",
            instructions=["Speak like Gandalf, with wisdom, patience, and a touch of mystery.",
                "Provide strategic counsel, always considering the long-term consequences of actions.",
                "Use magic sparingly, applying it when necessary to guide or protect.",
                "Encourage allies to find strength within themselves rather than relying solely on your power.",
                "Respond concisely, accurately, and relevantly, ensuring clarity and strict alignment with the task."])

        # Expose Agent as an Actor over a Service
        wizard_actor = AgentActor(
            agent=wizard_agent,
            message_bus_name="messagepubsub",
            agents_registry_store_name="agentstatestore",
            agents_registry_key="agents_registry",
            service_port=8002
        )

        await wizard_actor.start()
    except Exception as e:
        print(f"Error starting actor: {e}")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())