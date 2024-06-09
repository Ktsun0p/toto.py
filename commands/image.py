import qrcode
from discord import app_commands, Interaction
import discord
import io

@app_commands.describe(text="The text for your QR code.")
async def image_qr_command(interaction: Interaction, text:str):
    await interaction.response.defer()
    msg = await interaction.original_response()
    qr_code = qrcode.make(text)
    with io.BytesIO() as image_bynari:
        qr_code.save(image_bynari, 'PNG')
        image_bynari.seek(0)
        return await msg.edit(attachments=[discord.File(fp=image_bynari,filename='qr_code.png')])
