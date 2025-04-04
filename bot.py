from telethon import TelegramClient, events
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = TelegramClient(
    'bot',
    int(os.getenv('API_ID')),
    os.getenv('API_HASH')
).start(bot_token=os.getenv('BOT_TOKEN'))


@client.on(events.NewMessage(pattern=r'https?://t\.me/(\w+)/(\d+)'))
async def handle_url(event):
    try:
        url = event.text
        match = re.search(r't\.me/(\w+)/(\d+)', url)
        channel = match.group(1)
        msg_id = int(match.group(2))

        msg = await client.get_messages(channel, ids=msg_id)

        if not msg:
            return await event.reply("🚫 Message not found/access denied!")

        if msg.media:
            await client.send_file(
                event.chat_id,
                msg.media,
                caption=f"{msg.text}\n\n🔗 Original post: {url}"
            )
        elif msg.text:
            await event.reply(f"{msg.text}\n\n🔗 {url}")

    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")


print("Bot is running...")
client.run_until_disconnected()