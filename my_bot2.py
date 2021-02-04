# Import Discord Package
import discord
import time
import random
from discord.ext import commands, tasks
from datetime import datetime
import os
import discord.utils

# Client (bot)
client = commands.Bot(command_prefix='shane ')



#######################################################################










#region HELP COMMAND
client.remove_command('help')
@client.command(name='help')
async def halp(context):
    
    helpEmbed = discord.Embed(title='Bubs Bot Help Page', description='bard moment')
    helpEmbed.add_field(name = 'shane version', value = 'shows the current version of Bubs Bot')
    helpEmbed.add_field(name = 'shane del <value>', value = 'deletes specified amount of messages')
    helpEmbed.add_field(name = 'shane userinfo @user', value = 'shows server information of the user')
    helpEmbed.add_field(name = 'shane ban @user', value = 'doesn\'t actually ban XD')
    helpEmbed.add_field(name = 'shane dm @user <message>', value = 'messages specified user')
    helpEmbed.add_field(name = 'shane say <message>', value = 'repeats specified messages')
    helpEmbed.add_field(name = 'shane snipe', value = 'sends the last deleted message')

    
    helpEmbed.set_footer(text='official bot of the Bubs server!')
    
    await context.message.channel.send(embed=helpEmbed)
#endregion

#region VERSION COMMAND
@client.command(name='version')
async def version(context):
    
    versionEmbed = discord.Embed(title='Current Version:', description='The bot is in version 1.0', color=0xffc0cb)
    versionEmbed.add_field(name='Version Code:', value='v1.0', inline=False)
    versionEmbed.add_field(name='Date Released:', value='1/26/21', inline=False)
    versionEmbed.set_footer(text='i-i swear im legal!')
    versionEmbed.set_author(name='Bubs Bot')

    await context.message.channel.send(embed=versionEmbed)
#endregion

#

#region DEL COMMAND
@client.command(name='del')
#@commands.has_permissions(manage_messages=True)
@commands.has_any_role('OWNER','Magenta')
async def dele(context, amount=5):
    try:
        await context.channel.purge(limit=amount+1)
        time.sleep(0.5)
        await context.message.channel.send('Deleted ' + str(amount) + ' messages.')
    except:
        await context.message.channel.send('No permissions.')
#endregion
    




#region FAKEBAN COMMAND
@client.command(name='ban')

@commands.has_any_role('BUB')
async def ban(context, member: discord.Member):
    try:
        banEmbed = discord.Embed(color = member.color, timestamp = context.message.created_at)
        banEmbed.set_author(name = f'User banned: {member} \n\nNickname: {member.display_name}')
        banEmbed.set_thumbnail(url = member.avatar_url)
        banEmbed.set_footer(text = f'Authorized by: {context.author}', icon_url = context.author.avatar_url)

        await context.message.channel.send(embed=banEmbed)
    except:
        await context.message.channel.send('You need bub role in order to ban, smh.')
#endregion

#region USERINFO COMMAND
@client.command(name='userinfo')
async def userinfo(context, member: discord.Member):
    
    userinfoEmbed = discord.Embed(color = member.color, timestamp = context.message.created_at)
    userinfoEmbed.set_author(name = f'User Info - {member}')
    userinfoEmbed.set_thumbnail(url = member.avatar_url)
    userinfoEmbed.set_footer(text = f'Requested by: {context.author}', icon_url = context.author.avatar_url)

    userinfoEmbed.add_field(name = 'ID', value = member.id)
    userinfoEmbed.add_field(name = 'Server Nickname:', value = member.display_name)
    userinfoEmbed.add_field(name = 'Creation Date:', value = member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    userinfoEmbed.add_field(name = 'Joined at:', value = member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    userinfoEmbed.add_field(name = 'Highest Role:', value = member.top_role.mention)
    userinfoEmbed.add_field(name = 'Bot?', value = member.bot)
    #userinfoEmbed.add_field(name = 'Status:', value = member.status)


    await context.message.channel.send(embed=userinfoEmbed)
#endregion

#region SAY COMMAND
@client.command(name='say')
async def say(ctx, *, arg):
    try:
        await ctx.message.delete()
        await ctx.send(arg)
    except:
        await ctx.message.channel.send('sorry :/ i don\'t have permission to read messages...')
#endregion

#region DM COMMAND
@client.command(name='dm')
#@commands.has_permissions(manage_messages=True)
async def dm(context, member : discord.Member, *, arg):
    try:
        #sends arg to specified member
        await member.send(arg)

        #shows embed of who sent what to whom
        dmEmbed = discord.Embed(color = member.color, timestamp = context.message.created_at)
        dmEmbed.add_field(name = f'User: {member}', value = f'Message sent: {arg}')
        dmEmbed.set_thumbnail(url = member.avatar_url)
        dmEmbed.set_footer(text = f'Authorized by: {context.author}', icon_url = context.author.avatar_url)

        await context.message.channel.send(embed=dmEmbed)
    except:
        await context.message.channel.send('No permissions.')


#endregion



#region SNIPE COMMAND
@client.event
async def on_message_delete(message):

    #stores deleted message in a variable
    global deletedMessage
    deletedMessage = str(message.content)

    global deletedMessageUser
    deletedMessageUser = str(message.author)

    global deletedMessageChannel
    deletedMessageChannel = str(message.channel)


    msg = str(message.author)+ ' deleted message in '+str(message.channel)+': '+str(message.content)
    print(msg)

    deletedMessageLogs = client.get_channel(799080817116577823)
    await deletedMessageLogs.send(msg)

@client.command(name = 'snipe')
async def snipe(context):
    # msg = deletedMessageUser + ' deleted message in '+ deletedMessageChannel + ': ' + deletedMessage
    # await context.message.channel.send(msg)
    try:
        snipeEmbed = discord.Embed(title = f'{deletedMessageUser} deleted message:', description = f'`{deletedMessage}`\n\n in #{deletedMessageChannel}',color=0x3E7FD3)
        snipeEmbed.set_footer(text = f'Authorized by: {context.author}', icon_url = context.author.avatar_url)
    
        await context.message.channel.send(embed=snipeEmbed)
    except:
        await context.message.channel.send("No deleted message found!")




#endregion

# client.event

#region bot start-up message
@client.event
async def on_ready(message): #when bot starts up
    startup_channel = client.get_channel(799071963485831168)
    await startup_channel.send('Bubs Bot has come online')
    
    uwubotGeneral_channel = client.get_channel(794466074305232920)
    
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = 'your commands!'))

#endregion



#region CHATFILTER
    with open('badwords.txt','r') as file:
        bad_words = file.read().strip().lower().split(', ')
    if any(bad_word in message.content.strip().lower() for bad_word in bad_words):
        if message.author != client.user:
            await message.channel.purge(limit=1)
            await message.channel.send(f'{message.author.mention}, don\'t use that word >w<')

            badword_channel = client.get_channel(797120309756952626)
            await badword_channel.send(f'{message.author.name} used unauthorized phrase \'{message.content}\' in {message.guild.name}')
#endregion

    await client.process_commands(message)


# Run the client on the server
client.run('ODAzNjE2MDQyMjEwNDI2OTAx.YBAXwg.-C5y5yxQW9ydcNhyw-mlV7AxpqI')