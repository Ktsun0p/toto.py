import discord
from .ping import ping_command
from .avatar import avatar_command
from .summoner import summoner_get_command, summoner_me_command, summoner_user_command, summoner_link_command, summoner_unlink_command
from .image import image_qr_command
from .music import play_command
class command_group(discord.app_commands.Group):
        pass

summoner_commands = command_group(name="summoner", description="League of Legends summoner profiles!")
image_commands = command_group(name="image", description="Generate images")
def setup_commands(tree: discord.app_commands.CommandTree):
    tree.command(name="ping",description="pong")(ping_command)
    
    tree.command(name="play",description="🎶 Play a song in your voice chat!")(play_command)
    
    tree.command(name="stop",description="🎶 Stop the music in your voice chat.")(ping_command)
    tree.command(name="avatar",description="See other people's avatar. (profile picture)")(avatar_command)
    tree.add_command(summoner_commands)
    tree.add_command(image_commands)
    image_commands.command(name="qr-code", description="Create a simple QR code.")(image_qr_command)
    summoner_commands.command(name="me", description="Get your LoL data. Link your account to Discord via `/summoner link` command.")(summoner_me_command)
    summoner_commands.command(name="user", description="View the LoL profile of another Discord user.")(summoner_user_command)
    summoner_commands.command(name="get", description="Get summarized information of League of Legends profiles.")(summoner_get_command)
    summoner_commands.command(name="link", description="Link your LoL profile to your Discord profile.")(summoner_link_command)
    summoner_commands.command(name="unlink", description="Unlink your LoL profile from your Discord profile.")(summoner_unlink_command)

    