import discord
from discord.ext import commands
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Setup
client = OpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store conversation history
thread_context = {}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.Thread):
        thread_id = message.channel.id

        # Initialize or update thread context
        if thread_id not in thread_context:
            thread_context[thread_id] = []
        thread_context[thread_id].append(f"{message.author.name}: {message.content}")
        thread_context[thread_id] = thread_context[thread_id][-20:]  # Keep last 20 messages

        try:
            # Get response from OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Your reply will be displayed in discord; use it's formatting for code etc"},
                    {"role": "user", "content": "\n".join(thread_context[thread_id])}
                ],
                max_tokens=1000
            )
            answer = response.choices[0].message.content.strip()

            # Split the response into paragraphs
            paragraphs = answer.split('\n\n')
            current_chunk = ""

            # Process each paragraph
            for paragraph in paragraphs:
                # If adding this paragraph would exceed Discord's limit
                if len(current_chunk) + len(paragraph) + 2 > 1900:
                    # Send current chunk if it's not empty
                    if current_chunk:
                        await message.channel.send(current_chunk + "\n")
                        current_chunk = ""

                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

            # Send any remaining content
            if current_chunk:
                await message.channel.send(current_chunk)

            # Append the bot's response to the thread context
            thread_context[thread_id].append(f"Bot: {answer}")

        except Exception as e:
            await message.channel.send("Sorry, I couldn't process that. Please try again!")
            print(f"Error: {e}")

    await bot.process_commands(message)

@bot.command()
async def clear(ctx):
    """Clear conversation history for current thread"""
    if isinstance(ctx.channel, discord.Thread):
        thread_context.pop(ctx.channel.id, None)
        await ctx.send("Conversation history cleared.")
    else:
        await ctx.send("This command only works in threads.")

# Start bot
print("Starting bot...")
bot.run(DISCORD_BOT_TOKEN)
