import asyncio, base64, codecs, colorama, ctypes, datetime, discord, json, os, random, requests, time, sys
from colorama import Fore
from discord.ext import commands
from urllib.parse import urlencode

colorama.init()
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=130))
ctypes.windll.kernel32.SetConsoleTitleW(f'GeezerBot | made by piombacciaio')



#Bot settings
with open("main.json", "r+") as f:

    BOT = json.load(f)

BOT_GUILD = int(BOT["server"]["id"])
MANAGER = int(BOT["server"]["manager"])
OWNER = int(BOT["server"]["owner"])
TOKEN =  BOT["bot"]["token"]
PREFIX = BOT["bot"]["prefix"]

#Server settings (IDs)
MOD_ROLE = int(BOT["server"]["roles"]["mod_role"])
MUTE_ROLE = int(BOT["server"]["roles"]["mute_role"])
MEMBER_ROLE = int(BOT["server"]["roles"]["member_role"])
ROLE_CHANNEL = int(BOT["server"]["channels"]["role_channel"])
LEVEL_CHANNEL = int(BOT["server"]["channels"]["level_channel"])
MODMAIL_CHANNEL = int(BOT["server"]["channels"]["modmail_channel"])
MODLOG_CHANNEL = int(BOT["server"]["channels"]["modlog_channel"])
WELCOME_CHANNEL = int(BOT["server"]["channels"]["welcome_channel"])

#Embed settings
COLOR = discord.Colour(int(BOT["bot"]["embed"]["color"].replace("#", "0x"), base=16))
ERROR_COLOR = discord.Colour(int(BOT["bot"]["embed"]["error_color"].replace("#", "0x"), base=16))
TITLE = BOT["bot"]["embed"]["title"]
ICON = BOT["bot"]["embed"]["icon"]
FOOTER = chr(173)



#Functions
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
def convert(time):
    """extract seconds from days, hours and minutes"""
    try:

        return int(time[:-1]) * time_convert[time[-1]]

    except:

        return time

def actual_time():
    """Get actual time format: DD/MM/YYYY H:M:S"""

    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return now

async def update_users(users, user):
    
    if not users["levels"][str(user.id)]:

        users["levels"][str(user.id)] = {}
        users["levels"][str(user.id)]["experience"] = 0
        users["levels"][str(user.id)]["level"] = 0
    
    else:

        pass

async def add_experience(users, user, exp):

    users["levels"][str(user.id)]["experience"] += exp

async def lvl_up(users, user):

    experience = users["levels"][str(user.id)]["experience"]
    level_now = users["levels"][str(user.id)]["level"]
    level_limit = int(experience ** (1/4))
    if level_now < level_limit:
        users["levels"][str(user.id)]["level"] += 1
        msg = f"Yay! {user.mention} just levelled up! You are now level {level_now + 1}"
        await bot.get_guild(BOT_GUILD).get_channel(LEVEL_CHANNEL).send(msg)

#Add function to check if main.json exists



#Bot setup
print("" + actual_time() + " | " + Fore.GREEN + "[Event]  " + Fore.RESET + f' | Connecting to discord')

intents = discord.Intents.all()
intents.members = True
intents.reactions = True
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, owner_ids=(MANAGER, OWNER),intents=intents)
bot.remove_command("help")
version = 0.0



#Commands
@bot.command()
async def level(ctx, member: discord.Member = None):

    if not member:

        id = ctx.message.author.id

        with open('main.json', 'r') as f:

            users = json.load(f)

        lvl = users["levels"][str(id)]['level']
        await ctx.send(f'You are at level {lvl}')

    else:

        try:

            id = member.id

            with open('main.json', 'r') as f:

                users = json.load(f)

            lvl = users["levels"][str(id)]['level']
            await ctx.send(f'{member} is at level {lvl}')

        except:

            await update_users(users, member)

emoji_list = [
    "1️⃣",
    "2️⃣",
    "3️⃣", 
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣"]

@bot.command()
@commands.has_permissions(manage_roles=True)
async def setuprolecolor(ctx, channel=None):
    if not channel:
        channel = ctx.message.channel.id

    message_channel = bot.get_channel(int(channel))
    await message_channel.purge(limit=25)
    embed = discord.Embed(title="Color Roles", color=COLOR)
    embed.add_field(name="Role", value="1️⃣ - Gold", inline=True)
    embed.add_field(name="Role", value="2️⃣ - Scarlet", inline=True)
    embed.add_field(name="Role", value="3️⃣ - Crimson", inline=True)
    embed.add_field(name="Role", value="4️⃣ - Hot Pink", inline=True)
    embed.add_field(name="Role", value="5️⃣ - Magenta", inline=True)
    embed.add_field(name="Role", value="6️⃣ - Chocolate", inline=True)
    embed.add_field(name="Role", value="7️⃣ - Aqua", inline=True)
    embed.add_field(name="Role", value="8️⃣ - Spring green", inline=True)
    embed.add_field(name="Role", value="9️⃣ - Silver", inline=True)
    msg = await message_channel.send(embed = embed)
   
    for emoji in emoji_list:

        await msg.add_reaction(emoji)

@bot.command()
async def delroles(ctx):
 for role in ctx.guild.roles:  
     try:  
        await role.delete()
     except:
        await ctx.send(f"Cannot delete {role.name}")

@bot.command(usage=f"{bot.command_prefix}botinfo", description="get bot info", brief="tools")
async def botinfo(ctx):

    source_button = discord.ui.Button(label="Source", url="https://github.com/Piombacciaio/GeezerBot", emoji="<:GitHub:978680612087005225>")
    embed=discord.Embed(title=TITLE, description=chr(173), color=COLOR)
    embed.add_field(name="Ping:", value=f"{round(bot.latency * 1000, 1)}ms", inline=True)
    embed.add_field(name="Version", value=f"{version}", inline=True)
    embed.add_field(name="Commands", value=len(bot.commands), inline=True)
    embed.add_field(name="Prefix", value=f"{bot.command_prefix}", inline=True)
    embed.add_field(name=f"Changelog v{version}", value=f"Added:\n  - Role colors\n  - Welcome messages", inline=False)
    embed.set_footer(text="Created by: Piombacciaio#2151")
    embed.set_thumbnail(url=ICON)
    view = discord.ui.View()
    view.add_item(source_button)
    await ctx.send(embed=embed, view=view)



#Events
@bot.event
async def on_connect():

    try:
        
        print("" + actual_time() + " | " + Fore.GREEN + "[Event]  " + Fore.RESET + f' | {bot.user} is connected')
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f"{bot.command_prefix}help (not yet implemented)"))

        await bot.wait_until_ready()

        print("" + actual_time() + " | " + Fore.GREEN + "[Event]  " + Fore.RESET + f' | Bot startup completed, waiting for inputs')
        space = ""
        for column in range(int((os.get_terminal_size().columns))):
            space += "_"
        print(space)

    except Exception as e:

        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | Connection has raised an exception: [{e}]')

@bot.event
async def on_command(cmd):

    try:
        
        print("" + actual_time() + " | " + Fore.BLUE + "[Command]" + Fore.RESET + f" | {bot.command_prefix}{cmd.command.name}")

    except Exception as e:
        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | Command usage logging has raised an exception: [{e}]')

@bot.event
async def on_command_error(cmd, error):

    try:

        embed = discord.Embed(title="Error!", description=f"Sorry for the inconvenient, but the following error has occourred\n`{error}`\n{cmd.message.author.mention} Please do not delete your message to allow a better understanding of the problem", color=ERROR_COLOR)
        await cmd.message.reply(content="<@!624712494379827231> please check this. this is the v2", embed=embed, mention_author=False)
        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | The command {cmd.command.name} has raised the following error: [{error}]')

    except Exception as e:

        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | Hilarious, error logging has given an error.... Raised error: [{e}]')

@bot.event
async def on_member_join(member):
    

    with open("main.json", "r+") as f:

        users = json.load(f)

    await update_users(users, member)

    with open("main.json", "w") as f:

        json.dump(users, f, indent=4)
    
    try:

        guild = member.guild
        role_to_add = discord.utils.get(guild.roles, name='Cool People') 
        await member.add_roles(role_to_add)
        embed = discord.Embed(title="New Member!", description=f"Welcome {member.mention}!\nWe hope you will have a good time in {guild.name}!\nIf you want, you can head to <#{ROLE_CHANNEL}> to customize your name's color", color=COLOR)
        embed.set_thumbnail(url=member.avatar_url)
        await bot.get_guild(BOT_GUILD).get_channel(WELCOME_CHANNEL).send(embed=embed)

        
        print("" + actual_time() + " | " + Fore.GREEN + "[Event]  " + Fore.RESET + f" | {Fore.CYAN}Member Joined{Fore.RESET}: {member.name}#{member.discriminator} (ID. {member.id})")

    except Exception as e:

        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | "Member Join" logging has raised an exception: [{e}]')

@bot.event
async def on_member_remove(member):

    try:

        embed = discord.Embed(title="We sadly lost a member!", description=f"Goodbye {member.mention}!\nWe all wish you the best and hope to see you soon!", color=COLOR)
        avatar = member.avatar_url
        embed.set_thumbnail(url=avatar)
        await bot.get_guild(BOT_GUILD).get_channel(WELCOME_CHANNEL).send(embed=embed)
        
        print("" + actual_time() + " | " + Fore.GREEN + "[Event]  " + Fore.RESET + f' | {Fore.YELLOW}Member Left{Fore.RESET}: {member.name}#{member.discriminator} (ID. {member.id})')
    
    except Exception as e:

        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f' | "Member Left" logging has raised an exception: [{e}]')
    
@bot.event
async def on_message(message):

    if message.author.id == bot.user.id:
        return
    
    if message.guild:

        if message.author != message.author.bot:

            with open('main.json', 'r+') as f:
                users = json.load(f)

            await update_users(users, message.author)
            await add_experience(users, message.author, 2.5)
            await lvl_up(users, message.author)

            with open('main.json', 'w') as f:
                json.dump(users, f, indent=4)

    if message.content[:1] == "$":

        await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):

    if user == bot.user:
        pass
        
    else:
        reaction_channel = bot.get_channel(ROLE_CHANNEL)
        guild = reaction.message.guild

        if reaction.message.channel.id != reaction_channel:

            pass

        try: 

            if reaction.emoji == '1️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Gold')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '2️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Scarlet')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '3️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Crimson')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '4️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Hot Pink')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '5️⃣':
                
                role_to_add = discord.utils.get(guild.roles, name='Magenta')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '6️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Chocolate')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '7️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Aqua')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '8️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Spring Green')
                await user.add_roles(role_to_add)
            
            if reaction.emoji == '9️⃣':

                role_to_add = discord.utils.get(guild.roles, name='Silver')
                await user.add_roles(role_to_add)

        except Exception as e:

            
            print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f" | An error as occourred while adding the {reaction.emoji} role: {e}")

@bot.event
async def on_reaction_remove(reaction, user):

    reaction_channel = bot.get_channel(ROLE_CHANNEL)
    guild = reaction.message.guild

    if reaction.message.channel.id != reaction_channel:

        pass

    try: 

        if reaction.emoji == '1️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Gold')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '2️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Scarlet')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '3️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Crimson')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '4️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Hot Pink')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '5️⃣':
            
            role_to_remove = discord.utils.get(guild.roles, name='Magenta')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '6️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Chocolate')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '7️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Aqua')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '8️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Spring Green')
            await user.remove_roles(role_to_remove)
        
        if reaction.emoji == '9️⃣':

            role_to_remove = discord.utils.get(guild.roles, name='Silver')
            await user.remove_roles(role_to_remove)

    except Exception as e:
        
        
        print("" + actual_time() + " | " + Fore.RED + "[Error]  " + Fore.RESET + f" | An error as occourred while adding the {reaction.emoji} role: {e}")



#Run
def run():

    try:
        bot.run(TOKEN)

    except discord.errors.LoginFailure:
        print("" + actual_time() + " | " + f"{Fore.RED} [Error] {Fore.RESET} | Improper token has been passed")
        new_token = input("Provide a valid token >> ")
        
        with open("main.json", "r") as f:
            config = json.load(f)

        config["bot"]["token"] = new_token

        with open("main.json", "w") as f:
            json.dump(config, f, indent=4)

        input("Press ENTER to continue...")
        os.system("cls")

    except Exception as e:
        print("" + actual_time() + " | " + f"{Fore.RED} [Error] {Fore.RESET} | Raised exception: {e}")
        input()

if __name__ == "__main__":
    run()