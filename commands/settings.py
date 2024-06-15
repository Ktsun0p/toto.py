import discord
from discord import app_commands
from database import get_collection
from cooldown_manager import CooldownManager

cooldown_manager = CooldownManager()

@app_commands.describe(channel="The channel where the music commands will be sent.")
async def settings_music_channel_command(interaction: discord.Interaction, channel: discord.TextChannel):
    server_id = interaction.guild_id

    # Verificar el cooldown
    if cooldown_manager.is_on_cooldown(server_id):
        remaining_time = cooldown_manager.get_remaining_time(server_id)
        await interaction.response.send_message(
            f"This command is on cooldown. Please try again in {remaining_time} seconds.",
            ephemeral=True
        )
        return
    cooldown_manager.set_cooldown(server_id, 30)

    await interaction.response.defer()
    msg = await interaction.original_response()
    
    collection = get_collection('servers')
    collection.update_one(
        {'server_id': server_id},
        {'$set': {'music_settings.channel': channel.id}}
    )
    
    embed = embed_message(interaction=interaction,desc=f'The music channel has been successfully changed to <#{channel.id}>')
    await msg.edit(embed=embed)
    
@app_commands.describe(role="The role with permission to manage music settings.")
async def settings_music_role_command(interaction: discord.Interaction, role: discord.Role):
    server_id = interaction.guild_id

    # Verificar el cooldown
    if cooldown_manager.is_on_cooldown(server_id):
        remaining_time = cooldown_manager.get_remaining_time(server_id)
        await interaction.response.send_message(
            f"This command is on cooldown. Please try again in {remaining_time} seconds.",
            ephemeral=True
        )
        return
    cooldown_manager.set_cooldown(server_id, 30)
    
    await interaction.response.defer()
    msg = await interaction.original_response()
    
    collection = get_collection('servers')
    collection.update_one(
        {'server_id': server_id},
        {'$set': {'music_settings.role': role.id}}
    )
    embed = embed_message(interaction=interaction,desc=f'The music role has been successfully changed to <@&{role.id}>')
    await msg.edit(embed=embed)

async def settings_music_view_command(interaction: discord.Interaction):
    server_id = interaction.guild_id

    # Verificar el cooldown
    if cooldown_manager.is_on_cooldown(server_id):
        remaining_time = cooldown_manager.get_remaining_time(server_id)
        await interaction.response.send_message(
            f"This command is on cooldown. Please try again in {remaining_time} seconds.",
            ephemeral=True
        )
        return

    # Establecer el cooldown
    cooldown_manager.set_cooldown(server_id, 30)

    await interaction.response.defer()
    msg = await interaction.original_response()
    collection = get_collection('servers')
    server = collection.find_one({'server_id':server_id})
    m_channel = str(server['music_settings']['channel'])
    m_role = str(server['music_settings']['role'])
    description = f'**Music config**:\nChannel:<#{m_channel}>\nRole: <@&{m_role}>'
    embed = embed_message(interaction=interaction,desc=description)
    await msg.edit(embed=embed)
def embed_message(interaction:discord.Interaction,desc:str):
    embed = discord.Embed(color=discord.Color.yellow())
    embed.set_author(name=interaction.client.user.display_name,icon_url=interaction.client.user.display_avatar)
    embed.description = desc
    return embed