import re
emoji_cache = {}

def update_cache(emojis):
    global emoji_cache
    emoji_cache = {
        emoji['name']: f"<:{emoji['name']}:{emoji['id']}>"
        for emoji in emojis['items']
    }
    
def get_app_emoji(name):
    return emoji_cache.get(re.sub(r'[^a-zA-Z0-9]', '', name),'<:Toto_Bug:1019280617105522729>')