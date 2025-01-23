"""
User-bot for educational purposes only.
Against ToS, so please do not use!
"""
from discord.ext import commands
from generative import xBotAI
from dotenv import load_dotenv
import os, discord, asyncio, time, shlex # convert all elif statements using multiple inputs into 1 input line!

load_dotenv()
api_key = os.getenv("GENAI_KEY")
client = discord.Client()
ai = xBotAI("gemini-1.5-flash", api_key) # initializes ai
auto_reply_toggle = True

"""
Changes to make:
Make getting channel_id and msg_id (if applicable) its own function
Make command response system better than if-chain (i don't like yanderedev code)
Add commands!
"""
async def handle_input(tokens:list): # takes list of arguments and generates replies/sends replies based on them.
    if(tokens[0].lower() == "topic"):
        try:
            topic = tokens[1]
            ai.set_topic(topic)
            print("topic changed to " + topic) # DEBUG
        except(IndexError):
            print("Usage: topic <TOPIC_IN_QUOTES>")
    elif(tokens[0].lower() == "replyautogen"):
        try:
            channel_id = int(tokens[1])
            msg_id = int(tokens[2])
            tone = tokens[3]
            print(channel_id, msg_id, tone) #DEBUG
            if(tone == ""):
                tone = "neutral"
            channel = client.get_channel(channel_id)
            og_message_text = await channel.fetch_message(msg_id)
            response = ai.generate_message("", og_message_text.content, tone)
            await channel.send(response, reference=og_message_text, mention_author=False)
        except IndexError:
            print("Usage: replyautogen <CHANNEL_ID> <MSG_ID>")                
    elif(tokens[0].lower() == "directreply"):
        try:
            channel_id = int(tokens[1])
            msg_id = int(tokens[2])
            response = tokens[3]
            channel = client.get_channel(channel_id)
            og_msg = await channel.fetch_message(msg_id)
            await channel.send(response, reference=og_msg, mention_author=False)
        except IndexError:
            print("Usage: directreply <CHANNEL_ID> <MSG_ID> <RESPONSE>")
    elif(tokens[0].lower() == "directmsg"):
        try:
            channel_id = int(tokens[1])
            response = tokens[2]
            channel = client.get_channel(channel_id)
            await channel.send(response)
        except IndexError:
            print("Usage: directmsg <CHANNEL_ID> <RESPONSE>")
    elif(tokens[0].lower() == "promptreply"):
        try:
            channel_id = int(tokens[1])
            msg_id = int(tokens[2])
            prompt = tokens[3]
            tone = tokens[4] 
            channel = client.get_channel(channel_id)
            og_message_text = await channel.fetch_message(msg_id)
            response = ai.custom_message(prompt, tone)
            await channel.send(response, reference=og_message_text, mention_author=False)
        except IndexError:
            print("Usage: promptreply <CHANNEL_ID> <MSG_ID> <PROMPT_IN_QUOTES> <TONE>")
    elif(tokens[0].lower() == "promptmsg"):
        try:
            channel_id = int(tokens[1])
            prompt = tokens[2]
            tone = tokens[3] 
            channel = client.get_channel(channel_id)
            response = ai.custom_message(prompt, tone)
            await channel.send(response)
        except IndexError:
            print("Usage: promptmsg <CHANNEL_ID> <PROMPT_IN_QUOTES> <TONE>")
    elif(tokens[0].lower() == "autoreply"):
        auto_reply_toggle = not auto_reply_toggle
        print("Auto reply: " + str(auto_reply_toggle))
    elif(tokens[0].lower() == "directmsg"):
        try:
            channel_id = int(tokens[1])
            response = tokens[2]
            channel = client.get_channel(channel_id)
            await channel.send(response)
        except IndexError:
            print("Usage: directmsg <CHANNEL_ID> <RESPONSE>")
    elif(tokens[0].lower() == "help"):
        print("Help\n----\n'help'         - This command!" +
                        "\n'replyautogen' - Replies to message given channel and message ID, as well as tone. Considers previous message context." +
                        "\n'directreply'  - Replies exact message entered given channel and message ID." +
                        "\n'promptreply'  - Replies to message given channel and message ID, as well as tone and a custom prompt." +
                        "\n'promptmsg'    - Sends message given channel ID, using tone and prompt in order to generate message. " +
                        "\n'autoreply'    - Toggles automatically replying to messages that are replying to the bot's message(s). By default this is set to ON." +
                        "\n'directmsg'    - Sends exact message entered given channel ID." +
                        "\n'setdefaults'  - Sets default channel ID and/or other default settings. Work in Progress!") # implement         
    else:
        print("Invalid command. Try again or type 'help' for help.")


async def input_loop(): # used for command line interface
    global auto_reply_toggle # yes i dont like using global yes im keeping it idc
    print("Type 'exit' to stop the bot.")
    while True:
        command = await asyncio.to_thread(input, "> ")
        command = command.strip()
        tokens = shlex.split(command)
        print(tokens) # DEBUG
        if(tokens[0].lower() == "exit"):
            await client.close()
            break
        await handle_input(tokens)
        # if(command.lower() == "exit"): # add try/except to handle invalid commands!
        #     await client.close()
        #     break
        # if(command.lower() == "topic"): 
        #     topic = await asyncio.to_thread(input, "Enter a topic: ")
        #     ai.set_topic(topic)
        # elif(tokens[0] == "replyautogen"):
        #     channel_id = int(tokens[1])
        #     msg_id = int(tokens[2])
        #     tone = tokens[3]
        #     print(channel_id, msg_id, tone) #DEBUG
        #     if(tone == ""):
        #         tone = "neutral"
        #     channel = client.get_channel(channel_id)
        #     og_message_text = await channel.fetch_message(msg_id)
        #     response = ai.generate_message("", og_message_text.content, tone)
        #     await channel.send(response, reference=og_message_text, mention_author=False)
        # elif(command.lower() == "directreply"):
        #     channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
        #     msg_id = int(await asyncio.to_thread(input, "Enter message ID: "))
        #     response = await asyncio.to_thread(input, "Enter a reply: ")
        #     channel = client.get_channel(channel_id)
        #     og_msg = await channel.fetch_message(msg_id)
        # elif(command.lower() == "directmsg"):
        #     channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
        #     response = await asyncio.to_thread(input, "Enter a reply: ")
        #     channel = client.get_channel(channel_id)
        #     await channel.send(response)
        # elif(command.lower() == "promptreply"):
        #     channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
        #     msg_id = int(await asyncio.to_thread(input, "Enter message ID: "))
        #     tone = await asyncio.to_thread(input, "Enter a tone (leave blank for neutral): ")
        #     if(tone == ""):
        #         tone = "neutral"
        #     prompt = await asyncio.to_thread(input, "Enter a prompt: ")
        #     channel = client.get_channel(channel_id)
        #     og_msg = await channel.fetch_message(msg_id)
        #     response = ai.custom_message(prompt, tone)
        #     await channel.send(response, reference=og_msg, mention_author=False)
        # elif(command.lower() == "promptmsg"):
        #     channel_id = int(await asyncio.to_thread(input, "Enter channel ID: "))
        #     channel = client.get_channel(channel_id)
        #     tone = await asyncio.to_thread(input, "Enter a tone (leave blank for neutral): ")
        #     prompt = await asyncio.to_thread(input, "Enter a prompt: ")
        #     response = ai.custom_message(prompt, tone)
        #     await channel.send(response)
        # elif(command.lower() == "autoreply"):
        #     auto_reply_toggle = not auto_reply_toggle
        #     print("Auto reply: " + str(auto_reply_toggle))
        # elif(command.lower() == 'directmsg'):
        #     pass # implement!
        # elif(command.lower() == "help"):
        #     print("Help\n----\n'help'         - This command!" +
        #                     "\n'replyautogen' - Replies to message given channel and message ID, as well as tone. Considers previous message context." +
        #                     "\n'directreply'  - Replies exact message entered given channel and message ID." +
        #                     "\n'promptreply'  - Replies to message given channel and message ID, as well as tone and a custom prompt." +
        #                     "\n'promptmsg'    - Sends message given channel ID, using tone and prompt in order to generate message. " +
        #                     "\n'autoreply'    - Toggles automatically replying to messages that are replying to the bot's message(s). By default this is set to ON." +
        #                     "\n'directmsg'    - Sends exact message entered given channel ID." + # implement 
        #                     "\n'setdefaults'  - Sets default channel ID and/or other default settings.") # implement         
        # else:
        #     print("Invalid command. Try again or type 'help' for help.")
            
@client.event
async def on_message(message):
    if(message.author == client.user): # checks to ensure message author is not self bot
        return
    if(message.reference and auto_reply_toggle):
        og_msg = await message.channel.fetch_message(message.reference.message_id) # gets message to reply to
        if(og_msg.author == client.user): # checks if message is reply
            response = ai.generate_message(og_msg.content, message.content) # generates reply based on previous message
            time.sleep(2)
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
