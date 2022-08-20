from discord.ext import commands
import discord, random
import openai
import os 

openai.api_key = os.environ["OPENAI_KEY"]

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='Chatting')) #Change presence

 
@bot.event
async def on_message(message):
    send = message.channel.send
    sender = message.author
    content = message.content
    conversation = ""
    user_name = sender.name

    if sender.id == bot.user.id: #So it doesn't respond to itself
        return
    
    if "who made you" in content.lower() or "who created you" in content.lower() or "parents" in content.lower(): 
        await send("I was made by Zyrex")
        return
    
    try: 
        user_input = content
            

        prompt = user_name + ": " + user_input + "\n amy:"

        conversation += prompt

        response = openai.Completion.create(engine='text-davinci-001', prompt=conversation, max_tokens=100)
        response_str = response["choices"][0]["text"].replace("\n", " ")
        response_str = response_str.split(user_name + ": ", 1)[0].split("amy: ", 1)[0]


        conversation += response_str + "\n"
        await send(response_str)
    except discord.HTTPException:
        await send("i dont have a response to that")
    except Exception as e:
        await send(e)
             

bot.run(os.environ["DISCORD_TOKEN"])
