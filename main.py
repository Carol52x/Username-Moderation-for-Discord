import re
import discord
import os

intents = discord.Intents.all()


client = discord.Client(intents=intents)

bad_words = [""]
bad_regex = re.compile(r"\b(bad\w+)\b", re.IGNORECASE)

def is_bad_word(name):
    return name.lower() in bad_words or bad_regex.search(name)

async def send_log(embed):
    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    role = guild.get_role(ROLE_ID)
    message = f"{role.mention} A user has changed their username or nickname."
    await channel.send(message, embed=embed)

@client.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        event_type = "Nickname change"
        before_name = before.nick or before.name
        after_name = after.nick or after.name
    elif before.name != after.name:
        event_type = "Username change"
        before_name = before.name
        after_name = after.name
    else:
        return

    if is_bad_word(after_name):
        embed = discord.Embed(title=f"{event_type} - Bad word detected", color=0xFF0000)
        embed.add_field(name="User", value=f"{before.mention} ({before.id})")
        embed.add_field(name="Before", value=before_name, inline=False)
        embed.add_field(name="After", value=after_name, inline=False)
        await send_log(embed)

GUILD_ID = 1008799938932658269  # Replace with your guild ID
CHANNEL_ID = 1019920099936845865  # Replace with your channel ID
ROLE_ID = 1030091057968459857  # Replace with your role ID to be pinged

bot_token = os.environ.get('BOT_TOKEN')
client.run(bot_token)
