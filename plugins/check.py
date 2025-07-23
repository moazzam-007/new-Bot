from pyrogram import Client, filters
from heplers.convert import amazon_convert, convert_rest
import urllib.parse
from config import Telegram


@Client.on_message(filters.regex(r"https?://[^\s]+") & filters.chat(Telegram.CHANNELS))
async def check(client, message):
    print("Plugin triggered for message:", message.caption or message.text)

    completed_urls = []
    text = message.caption or message.text  # Handle both caption and text

    for match in message.matches:
        url = match.group(0)
        if "amzn.to" in url:
            aurl = amazon_convert(url)
            completed_urls.append((url, aurl))
        elif "youtu.be" in url or "t.me" in url or "youtube.com" in url:
            await client.send_message(
                chat_id=Telegram.LOG_GROUP_ID,
                text="This is a youtube or telegram link, please check it manually.\nhttps://t.me/{}/{}".format(
                    message.sender_chat.id, message.id
                ),
            )
        else:
            response = convert_rest(url)
            if response.get("convertedText"):
                aurl = response["convertedText"]
                aurl = urllib.parse.unquote(aurl)
                completed_urls.append((url, aurl))
            else:
                await client.send_message(
                    chat_id=Telegram.LOG_GROUP_ID,
                    text="This is not a supported link, please check it manually.\n{}".format(
                        url
                    ),
                )
                await client.send_message(
                    chat_id=Telegram.LOG_GROUP_ID, text=f"{response}"
                )

    if completed_urls:
        for url, aurl in completed_urls:
            text = text.replace(url, aurl)

        if message.photo:
            await client.send_photo(
                chat_id=Telegram.MAIN_CHAT_ID, photo=message.photo.file_id, caption=text
            )
        else:
            await client.send_message(chat_id=Telegram.MAIN_CHAT_ID, text=text)
    else:
        await client.send_message(
            chat_id=Telegram.LOG_GROUP_ID,
            text="No supported links found in the message.",
        )
