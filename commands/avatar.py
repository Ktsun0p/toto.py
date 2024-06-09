from discord import app_commands, Interaction
import discord
@app_commands.describe(user="user")
async def avatar_command(interaction: Interaction, user: discord.User=None):
    if user == None:
        user = interaction.user
    avatar = user.display_avatar.with_size(2048)
    embed = discord.Embed(color=discord.Color.blurple(), title=f"{user}'s Avatar")
    embed.set_image(url=avatar)
    return await interaction.response.send_message(embed=embed)