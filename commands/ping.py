from discord import app_commands, Interaction

async def ping_command(interaction: Interaction):
    return await interaction.response.send_message("pong")