# Search Engine with LLM
import os
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
import logging

load_dotenv()
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL")
GOOGLE_PROJECT = os.getenv("GOOGLE_PROJECT")
GOOGLE_LOCATION = os.getenv("GOOGLE_LOCATION")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tools and models
tools = load_tools(["google-search"], llm=ChatAnthropicVertex(model_name=CLAUDE_MODEL, project=GOOGLE_PROJECT, location=GOOGLE_LOCATION))
template = '''Answer the following questions as best you can in the same language as the question. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)
model = ChatAnthropicVertex(model_name=CLAUDE_MODEL, project=GOOGLE_PROJECT, location=GOOGLE_LOCATION, temperature=0)
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=5, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)

# Initialize Discord bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot is ready as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    text = prepare_message_content(message.content)
    await message.add_reaction('💬')
    
    try:
        response, log_message = get_agent_response(text)
    except ValueError as e:
        response = f'Error occurred during agent execution: {str(e)}'
        log_message = ''
    
    await message.channel.send(response)
    await send_log_message(message.channel, log_message)

def prepare_message_content(content):
    current_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    return f"[{current_date}@Kyoto] {content}"

def get_agent_response(text):
    result = agent_executor.invoke({"input": text})
    log_data = result['intermediate_steps'][0][0]
    log_message = log_data.log
    response = result.get('output', 'No output received')
    return response, log_message

async def send_log_message(channel, log_message):
    if log_message:
        log_message = "**Logs:**\n" + log_message
        if len(log_message) > 1900:
            chunks = [log_message[i:i+1900] for i in range(0, len(log_message), 1900)]
            for chunk in chunks:
                await channel.send(chunk)
        else:
            await channel.send(log_message)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
