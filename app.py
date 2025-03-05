from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter
from botbuilder.schema import Activity
import asyncio
import logging
from config import DefaultConfig
from bot import VoiceBot

bot = VoiceBot()

app = web.Application()
CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await ADAPTER.process_activity(activity, auth_header, bot.on_turn)
    return web.json_response(response)

# Modifying the below code

def init_func(argv):
    APP = web.Application(middlewares=[aiohttp_error_middleware])
    APP.router.add_post("/api/messages", messages)
    return APP
if __name__ == "__main__":
    APP = init_func(None)

    try:
        web.run_app( APP , host="0.0.0.0", port=CONFIG.PORT)
    except Exception as error:
        raise error
