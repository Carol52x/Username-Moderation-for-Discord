import discord
import re
import os
intents = discord.Intents.all()


client = discord.Client(intents=intents)

bad_words = [''] # regex allowed
role_id =  # replace with the ID of the role you want to ping
channel_id =  # replace with the ID of the channel you want to send the embed in

@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        name_type = "Nickname"
        before_name = before.display_name
        after_name = after.display_name
    else:
        name_type = "Username"
        before_name = before.name
        after_name = after.name

    if any(re.findall(rf"\b{word}\b", after_name, re.IGNORECASE) for word in bad_words):
        channel = client.get_channel(channel_id)
        role = after.guild.get_role(role_id)
        embed = discord.Embed(title=f"{name_type} Changed to Bad Word", color=discord.Color.red())
        embed.add_field(name="User", value=f"{after} ({after.id})", inline=False)
        embed.add_field(name="Before", value=before_name, inline=False)
        embed.add_field(name="After", value=after_name, inline=False)
        embed.set_footer(text=f"Timestamp: {after.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
        await channel.send(role.mention, embed=embed)

bot_token = os.getenv("BOT_TOKEN")
client.run(bot_token)
