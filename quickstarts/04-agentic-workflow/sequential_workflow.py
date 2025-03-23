from dapr_agents.workflow import WorkflowApp, workflow, task
from dapr_agents.types import DaprWorkflowContext
from dotenv import load_dotenv

# Azure AI Service用クライアント
from dapr_agents import OpenAIChatClient
import os

# Load environment variables
load_dotenv()

# Define Workflow logic
@workflow(name='task_chain_workflow')
def task_chain_workflow(ctx: DaprWorkflowContext):
    result1 = yield ctx.call_activity(get_character)
    result2 = yield ctx.call_activity(get_line, input={"character": result1})
    return result2

@task(description="""
    Pick a random character from The Lord of the Rings\n
    and respond with the character's name only
""")
def get_character() -> str:
    pass

@task(description="What is a famous line by {character}",)
def get_line(character: str) -> str:
    pass

if __name__ == '__main__':

    # Azure AI ServiceのLLM設定
    azure_llm = OpenAIChatClient(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    )

    # WorkflowへLLMを渡す
    wfapp = WorkflowApp(llm=azure_llm)

    results = wfapp.run_and_monitor_workflow(task_chain_workflow)
    print(f"Famous Line: {results}")