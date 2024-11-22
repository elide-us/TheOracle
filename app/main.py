import asyncio
from aiohttp import web
from app.discord_bot import start_discord_bot

# Aiohttp handlers
async def handle_health(request):
    return web.Response(text="Bot is running!")

async def init_func(argv):
    # Create aiohttp app
    app = web.Application()
    app.router.add_get('/health', handle_health)

    # Run the Discord bot in the same event loop
    loop = asyncio.get_running_loop()
    loop.create_task(start_discord_bot())  # Schedule the bot to run

    return app
