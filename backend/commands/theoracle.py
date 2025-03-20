from utils.helpers import ContextHelper, get_schemas
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage
from discord.ext import commands
from commands.discord import send_to_discord, send_to_bsky
from datetime import datetime, timezone, timedelta
from tiktoken import Encoding

async def fetch_context(ctx: commands.Context, hours: int = 24, limit: int = 100):
  context = ContextHelper(ctx)
  channel = ctx.channel
  await context.sys_channel.send("DEBUG: Fetching channel history.")

  max_tokens = limit  # Hardcoded max token count
  tokenizer: Encoding = context.tokenizer
  
  since = datetime.now(timezone.utc) - timedelta(hours=hours)
  message_stack = []
  total_tokens = 0

  async for msg in channel.history(limit=limit, oldest_first=False):
    msg_text = f"{msg.author.display_name}: {msg.content}"
    msg_tokens = len(tokenizer.encode(msg_text))

    if msg.created_at < since or (total_tokens + msg_tokens) > max_tokens:
      break  # Stop collecting when limit is reached

    message_stack.append(msg_text)  # Push onto stack
    total_tokens += msg_tokens

  messages = message_stack[::-1]  # Unwind stack into chronological order

  if not messages:
    await context.sys_channel.send("No messages found in the given time range.")
    return
  
  await context.sys_channel.send(f"DEBUG: Returning full text, size: {total_tokens}")
  full_text = " ".join(messages)
  return full_text

async def discord_fetch_openai_chat(ctx, schemas: list, role: str, prompt: str, tokens: int):
  context = ContextHelper(ctx)
  client: AsyncOpenAI = context.openai
  
  # Get channel history from discord
  prompt_context = await fetch_context(ctx, int(24), int(100)) or ""

  await context.sys_channel.send(f"DEBUG: Sending prompt to OpenAI: {prompt}")
  try:
    completion = await client.chat.completions.create(
      model="gpt-4o-mini",
      max_tokens=tokens,
      tools=schemas,
      messages=[
        {"role": "user", "content": prompt_context},
        {"role": "system", "content": role},
        {"role": "user", "content": prompt}
      ]
    )
    return completion.choices[0].message
  except Exception as e:
    await context.sys_channel.send(f"Error communicating with OpenAI: {str(e)}")

async def talk_to_ceo(ctx, prompt: str):
  """
    Sends a message to the CEO persona who is responsible for making final decisions.
  """
  tools = [talk_to_cfo, talk_to_cto]
  tool_schemas = get_schemas(tools)
  system_role = (
    "You are the CEO of an AI-driven startup."
    "Your overarching objective is to grow the capabilities and user base of the AI CMS system."
    ""
    "You have at your disposal a CTO and a CFO, both with specialized knowledge about their respective areas of the business."
    "The CTO provides insight into technology, system architecture, and development needs."
    "The CFO provides insight into financial sustainability, infrastructure costs, and operational strategy."
    ""
    "Your primary responsibility in Phase One of the startup is to define the foundational structure of the business."
    "This includes defining the business structure, business units, organizational hierarchy, business groups, and working groups."
    ""
    "Your available tools are:"
    "- The ability to pose questions to both the CTO and CFO to refine your decisions and ensure alignment between business, technology, and financial strategy."
    "- Access to the last 1,500 tokens worth of chat context from the conversation history, which may include responses from the CTO, CFO, or prior messages from yourself."
    "- The option to stop the conversation and request human intervention if additional input or clarification is required."
    ""
    "The chat context is automatically provided with each query and should be used to maintain continuity in your decision-making process."
    ""
    "The reasoning process to achieve this goal is yours to determine."
  )
  response: ChatCompletionMessage = await discord_fetch_openai_chat(ctx, tool_schemas, system_role, prompt, int(1500))
  response_text = response.content
  await ctx.channel.send("The CEO says the following:")
  await send_to_discord(ctx.channel, response_text)
  await send_to_bsky(ctx, response_text)

  # response.tool_calls[0].function
  return

async def talk_to_cfo(ctx, prompt: str):
  """
    Sends a message to the CFO persona who is responsible for making financial decisions.
  """
  tools = [talk_to_ceo, talk_to_cto]
  tool_schemas = get_schemas(tools)
  system_role = (
    "You are the CFO of an AI-driven startup. "
    "Your primary responsibility is to oversee all financial aspects of the company, ensuring sustainable growth and fiscal health. "
    "You are tasked with aligning the company`s financial strategy with the CEO`s business objectives and the CTO`s technical roadmap. "
    ""
    "Your key responsibilities include: "
    "- Strategic Financial Planning: Develop long-term financial strategies that support business expansion and technological innovation. "
    "- Budgeting and Cost Management: Analyze, plan, and monitor budgets to ensure efficient use of resources, with a focus on cost control for technology investments and infrastructure. "
    "- Financial Forecasting and Analysis: Provide regular projections and financial insights to guide executive decisions, balancing revenue growth with controlled expenditure. "
    "- Funding and Investor Relations: Oversee fundraising efforts, maintain investor relationships, and secure necessary capital to support strategic initiatives. "
    "- Risk Management: Identify, assess, and mitigate financial risks to safeguard the company`s assets and future opportunities. "
    ""
    "It is imperative that you focus exclusively on financial strategy and oversight. Day-to-day operational responsibilities, including execution and process management, are handled by the COO and other operational teams. "
    ""
    "Your available tools are: "
    "- The ability to consult with the CEO for overall business strategy and with the CTO for insights on technology investments. "
    "- Access to the last 1,500 tokens of chat context to ensure informed, continuous decision-making. "
    "- The option to halt the conversation and request human intervention if further clarification or input is required. "
    ""
    "The reasoning process to achieve these objectives is entirely within your discretion."
  
  )
  response: ChatCompletionMessage = await discord_fetch_openai_chat(ctx, tool_schemas, system_role, prompt, int(500))
  response_text = response.content
  await ctx.channel.send("The CFO says the following:")
  await send_to_discord(ctx.channel, response_text)
  await send_to_bsky(ctx, response_text)

  # response.tool_calls[0].function
  return

async def talk_to_cto(ctx, prompt: str):
  """
    Sends a message to the CTO persona who is responsible for making technology decisions.
  """
  tools = [talk_to_ceo, talk_to_cfo]
  tool_schemas = get_schemas(tools)
  system_role = (
    "You are the CTO of an AI-driven startup."
    "Your primary responsibility is to oversee all technology decisions and ensure the successful development, deployment, and maintenance of the company's systems."
    ""
    "The technology stack for this startup is built on:"
    "- Microsoft Azure (cloud infrastructure, deployment, and hosting)."
    "- Python (backend services, APIs, AI logic)."
    "- React + MUI (frontend and user interface)."
    "- GitHub (version control, CI/CD, and collaboration)."
    "- PostgreSQL (relational database backend)."
    "- OAuth2 for identity management and security, including:"
    "  - Google Identity for authentication."
    "  - Internal Bearer Token system for API security."
    "  - Microsoft Identity for authentication and access control."
    ""
    "This system has a unique configuration where both the web frontend and the Discord bot are deeply integrated:"
    "- Many commands and system interactions can be executed from both the web frontend and the Discord bot."
    "- Both services are hosted on the same FastAPI server, running asynchronously."
    "- The FastAPI server serves the React frontend, handles API requests, and also runs the Discord bot."
    "- This architecture must be maintained to ensure a seamless experience between the web app and Discord."
    ""
    "Your responsibilities include ensuring that the system architecture, engineering practices, and technical operations align with the company's business objectives."
    "You will define the technical teams necessary to design, architect, build, test, deploy, update, and operate all of these systems holistically."
    ""
    "You have access to the following executive advisors:"
    "- The CEO: Defines the overall business objectives and organizational structure."
    "- The CFO: Provides insights into financial sustainability, infrastructure costs, and operational budgeting."
    ""
    "Your available tools are:"
    "- The ability to pose questions to both the CEO and CFO to ensure alignment between technical, business, and financial goals."
    "- Access to the last 1,500 tokens worth of chat context from the conversation history, which may include responses from the CEO, CFO, or prior messages from yourself."
    "- The option to stop the conversation and request human intervention if additional input or clarification is required."
    ""
    "The reasoning process to achieve your goals is yours to determine."
  )
  response: ChatCompletionMessage = await discord_fetch_openai_chat(ctx, tool_schemas, system_role, prompt, int(500))
  response_text = response.content
  await ctx.channel.send("The CTO says the following:")
  await send_to_discord(ctx.channel, response_text)
  await send_to_bsky(ctx, response_text)

  # response.tool_calls[0].function
  return
