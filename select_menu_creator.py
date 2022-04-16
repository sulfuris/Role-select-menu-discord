import discord
from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption, Button, ButtonStyle


import info  #info file is the file were is put my token, bot status and prefix

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = info.prefix,intents = intents)
DiscordComponents(bot)

@bot.event
async def on_ready():
    print("ready !")
    activity = discord.Game(name=info.status)
    await bot.change_presence(activity=activity)

@bot.command()
async def ping(ctx,title,max,roles: commands.Greedy[discord.Role],*,emoji: str):
    emojis = emoji.split(" ")
    desc = ""
    em = 0
    for i in roles:
        desc = desc + f"{emojis[em]} | <@&{i.id}> \n"
        em = em + 1
    embed=discord.Embed(
    title=f":sparkles: | {title}",  
    description=desc,
    color=0xC70039)

    select_test = Select(placeholder=f"{title}",options=[SelectOption(label=" ",value=" ")],min_values=0,max_values=max,custom_id="__ROLE_SELECTOR")

    em = 0
    for i in roles:
        select_test.options.append(SelectOption(label=f"{i.name}",emoji=f'{emojis[em]}',value=f"{i.id}"))
        em = em + 1
    del select_test.options[0]

    await ctx.send(embed = embed,components=[select_test])

        
@bot.event
async def on_select_option(interaction):
    if interaction.component.custom_id == "__ROLE_SELECTOR":
        await interaction.respond(type=6)
        guild = interaction.guild
        member = interaction.user
        
        for i in interaction.component.options:
            await member.remove_roles(guild.get_role(int(i.value)))
        for i in interaction.values:
            await member.add_roles(guild.get_role(int(i)))
        return
    await interaction.respond(type=6)
    

bot.run(info.token)

#by sulfu 

