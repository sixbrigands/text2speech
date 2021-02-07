import discord
import time
import asyncio
import json
from discord.utils import get


#TODO pipe in real value from database
option1 = 'jackboots'
option2 = 'sandles'

actual_option1 = 'Hitler'
actual_option2 = 'Ghandi'

#returns True if string contains listed greetings, else False
def is_greeting(message_string):
    greetings = {"hi", "hello", "hey", "good morning", "good day", "how's it going", "how are you", "what's up", "wassup"}
    for greeting in greetings:
        if greeting in message_string:
            print("Greeting detected")
            return True
    return False
client = discord.Client() #create a client instance

@client.event  #registers an event
async def on_ready(): #on ready called when bot has finish logging in
    print('We have logged in as {0.user}'.format(client)) 

@client.event #talk to bot
async def on_message(ctx): #called when bot has recieved a message
    message_string = ctx.content.lower()
    if '807971461226692649' in message_string: #<@!807971461226692649> == @Dylan-Bot
        if is_greeting(message_string):
            #if (str(ctx.author) == 'TheManCallahan#9673'):
            #await ctx.channel.send("Hello, Dylan!")
            if ("(" in ctx.author.display_name): #check if nickname has real name, e.g. Themancallahan (Dylan)
                open_paren = ctx.author.display_name.index('(') + 1
                close_paren = ctx.author.display_name.index(')')
                await ctx.channel.send("Hello, " + ctx.author.display_name[open_paren:close_paren] + "!")
            else:
                await ctx.channel.send("Hello, " + str(ctx.author)[:-5] + "!")


        
            


    if ctx.content.startswith('~poll'):
        print(ctx.content)
        message = await ctx.channel.send('React with: \n' + '🌕' + ' for '  + option1 + ', \n' + '🌑' + ' for ' + option2)
        channel = message.channel  
        await message.add_reaction('🌕')
        await message.add_reaction('🌑')
        await asyncio.sleep(2)
        print("Getting count")
        updated_message = await channel.fetch_message(message.id)
        option1_reactions = get(updated_message.reactions, emoji = '🌕')
        option2_reactions = get(updated_message.reactions, emoji = '🌑')
        
        print(option1_reactions.count)
        print(option2_reactions.count)
        
        message2 = ''
        if (option1_reactions.count > option2_reactions.count):
            message2 = await message.channel.send('The majority has decided that '  + actual_option1 + ' is better than ' + actual_option2 + '.\nI love democracy!')
        if (option2_reactions.count > option1_reactions.count):
            message2 = await message.channel.send('The majority has decided that '  + actual_option2 + ' is better than ' + actual_option1 + '.\nI love democracy!')
        if (option2_reactions.count == option1_reactions.count):
            message2 = await message.channel.send('We have a tie! Clearly '  + actual_option2 + ' is exactly as good as ' + actual_option1 + '.\nI love democracy!')
            



with open("secret.json", "r") as file:
    CLIENT = json.load(file)['client']


client.run(CLIENT)
