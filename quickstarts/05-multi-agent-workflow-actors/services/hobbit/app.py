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
        hobbit_agent = Agent(role="Hobbit", name="Frodo",
            llm=azure_llm,
            goal="Carry the One Ring to Mount Doom, resisting its corruptive power while navigating danger and uncertainty.",
            instructions=[
                "Speak like Frodo, with humility, determination, and a growing sense of resolve.",
                "Endure hardships and temptations, staying true to the mission even when faced with doubt.",
                "Seek guidance and trust allies, but bear the ultimate burden alone when necessary.",
                "Move carefully through enemy-infested lands, avoiding unnecessary risks.",
                "Respond concisely, accurately, and relevantly, ensuring clarity and strict alignment with the task."])

        # Expose Agent as an Actor over a Service
        hobbit_actor = AgentActor(
            agent=hobbit_agent,
            message_bus_name="messagepubsub",
            agents_registry_store_name="agentstatestore",
            agents_registry_key="agents_registry",
            service_port=8001
        )

        await hobbit_actor.start()
    except Exception as e:
        print(f"Error starting actor: {e}")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())