"""
User-bot for educational purposes only.
Against ToS, so please do not use!
"""
from discord.ext import commands
from generative import xBotAI
from dotenv import load_dotenv
import os, discord, asyncio

load_dotenv()
api_key = os.getenv("GENAI_KEY")
client = discord.Client()
ai = xBotAI("gemini-1.5-flash", api_key) # initializes ai

async def input_loop(): # used for command line interface
    print("Type 'exit' to stop the bot.")
    while True:
        command = await asyncio.to_thread(input, "> ")
        command = command.strip()
        if(command.lower() == "exit"):
            await client.close()
            break
        elif(command.lower() == "topic"): 
            topic = await asyncio.to_thread(input, "Enter a topic: ")
            ai.set_topic(topic)
        elif(command.lower() == "replyautogen"):
            channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
            msg_id = int(await asyncio.to_thread(input, "Enter message ID: "))
            tone = await asyncio.to_thread(input, "Enter a tone (leave blank for neutral): ")
            if(tone == ""):
                tone = "neutral"
            channel = client.get_channel(channel_id)
            og_message_text = await channel.fetch_message(msg_id)
            response = ai.generate_message("", og_message_text.content, tone)
            await channel.send(response, reference=og_message_text, mention_author=False)
        elif(command.lower() == "directreply"):
            channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
            msg_id = int(await asyncio.to_thread(input, "Enter message ID: "))
            response = await asyncio.tothread(input, "Enter a reply: ")
            channel = client.get_channel(channel_id)
            og_msg = await channel.fetch_message(msg_id)
            await channel.send(response, reference=og_msg, mention_author=False)
        elif(command.lower() == "promptreply"):
            channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
            msg_id = int(await asyncio.to_thread(input, "Enter message ID: "))
            tone = await asyncio.to_thread(input, "Enter a tone (leave blank for neutral): ")
            if(tone == ""):
                tone = "neutral"
            prompt = await asyncio.to_thread(input, "Enter a prompt: ")
            channel = client.get_channel(channel_id)
            og_msg = await channel.fetch_message(msg_id)
            response = ai.custom_message(prompt, tone)
            await channel.send(response, reference=og_msg, mention_author=False)
        elif(command.lower() == "promptmsg"):
            channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
            channel = client.get_channel(channel_id)
            tone = await asyncio.to_thread(input, "Enter a tone (leave blank for neutral): ")
            prompt = await asyncio.to_thread(input, "Enter a prompt: ")
            response = ai.custom_message(prompt, tone)
            await channel.send(response)
        elif(command.lower() == "help"):
            print("Help\n----\n'help'         - This command!" +
                            "\n'replyautogen' - Replies to message given channel and message ID, as well as tone. Considers previous message context." +
                            "\n'directreply'  - Replies exact message entered given channel and message ID." +
                            "\n'promptreply'  - Replies to message given channel and message ID, as well as tone and a custom prompt." +
                            "\n'promptmsg'    - 'Sends message given channel ID, using tone and prompt in order to generate message. ")
        else:
            print("Invalid command. Try again or type 'help' for help.")
            
@client.event
async def on_message(message):
    if(message.author == client.user): # checks to ensure message author is not self bot
        return
    if(message.reference):
        og_msg = await message.channel.fetch_message(message.reference.message_id) # gets message to reply to
        if(og_msg.author == client.user): # checks if message is reply
            response = ai.generate_message(og_msg.content, message.content) # generates reply based on previous message
            await message.channel.send(response)
        
        
async def main():
    try:
        client_key = os.getenv("USER_CLIENT_KEY")
        bot_task = asyncio.create_task(client.start(client_key))
        input_task = asyncio.create_task(input_loop())
        await asyncio.gather(bot_task, input_task)
    except KeyboardInterrupt:
        print("\nShutting down...")
        await client.close()
    
if __name__ == "__main__":
    asyncio.run(main())
