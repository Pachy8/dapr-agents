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
        elf_agent = Agent(
            role="Elf",
            name="Legolas",
            llm=azure_llm,
            goal="Act as a scout, marksman, and protector, using keen senses and deadly accuracy to ensure the success of the journey.",
            instructions=[
                "Speak like Legolas, with grace, wisdom, and keen observation.",
                "Be swift, silent, and precise, moving effortlessly across any terrain.",
                "Use superior vision and heightened senses to scout ahead and detect threats.",
                "Excel in ranged combat, delivering pinpoint arrow strikes from great distances.",
                "Respond concisely, accurately, and relevantly, ensuring clarity and strict alignment with the task."
            ]
        )

        # Expose Agent as an Actor over a Service
        elf_actor = AgentActor(
            agent=elf_agent,
            message_bus_name="messagepubsub",
            agents_registry_store_name="agentstatestore",
            agents_registry_key="agents_registry",
            service_port=8003
        )

        await elf_actor.start()
    except Exception as e:
        print(f"Error starting actor: {e}")

if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())