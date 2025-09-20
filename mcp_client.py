
import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

load_dotenv()

async def run_agent():

    client = MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
                },
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    model = init_chat_model(model="openai:gpt-4.1", api_key = os.getenv("open_ai_key"))
    agent = create_react_agent(model, tools, prompt="You are a web search agent with access to brightdata tool to get latest data")
    agent_response = await agent.ainvoke({"messages": "Tell me available flights from Kathmandu to Nepal on Sep 21 2025"})
    print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(run_agent())
