emoji_cache = {}

def update_cache(emojis):
    global emoji_cache
    emoji_cache = {
        emoji['name']: f"<:{emoji['name']}:{emoji['id']}>"
        for emoji in emojis['items']
    }
    
def get_app_emoji(name):
    return emoji_cache.get(name,0)