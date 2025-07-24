from pyrogram import Client, filters
from heplers.convert import amazon_convert, convert_rest
import urllib.parse
from config import Telegram
import os # For os.remove
from heplers.screenshot_extractor import take_screenshot # For screenshot feature

@Client.on_message(filters.regex(r"https?://[^\s]+") & filters.chat(Telegram.CHANNELS))
async def check(client, message):
    print("Plugin triggered for message:", message.caption or message.text)

    completed_urls = []
    text = message.caption or message.text  # Handle both caption and text
    
    # extracted_screenshot_path = None # Yeh line yahan nahi aani chahiye, function ke andar initialisation hi kaafi hai

    for match in message.matches:
        url = match.group(0)
        if "amzn.to" in url:
            aurl = amazon_convert(url)
            completed_urls.append((url, aurl))
        elif "youtu.be" in url or "t.me" in url or "youtube.com" in url:
            if Telegram.LOG_GROUP_ID:
                await client.send_message(
                    chat_id=Telegram.LOG_GROUP_ID,
                    text="This is a youtube or telegram link, please check it manually.\nhttps://t.me/{}/{}".format(
                        message.sender_chat.id, message.id
                    ),
                    disable_web_page_preview=True
                )
        else:
            response = convert_rest(url)
            if response.get("convertedText"):
                aurl = response["convertedText"]
                aurl = urllib.parse.unquote(aurl)
                completed_urls.append((url, aurl))
            else:
                if Telegram.LOG_GROUP_ID:
                    await client.send_message(
                        chat_id=Telegram.LOG_GROUP_ID,
                        text="This is not a supported link, please check it manually.\n{}".format(
                            url
                        ),
                        disable_web_page_preview=True
                    )
                    await client.send_message(
                        chat_id=Telegram.LOG_GROUP_ID,
                        text=f"{response}",
                        disable_web_page_preview=True
                    )
                else:
                    print(f"LOG_GROUP_ID not set, unable to send log for unsupported link: {url} | Response: {response}")


    if completed_urls:
        final_text = text
        for url, aurl in completed_urls:
            final_text = final_text.replace(url, aurl)

        # --- SCREENSHOT / PHOTO SENDING LOGIC ---
        if message.photo: # Original message mein photo hai
            await client.send_photo(
                chat_id=Telegram.MAIN_CHAT_ID,
                photo=message.photo.file_id,
                caption=final_text # NO disable_web_page_preview here
            )
        else: # Original message mein photo nahi hai, toh screenshot lene ki koshish karein
            product_url_for_screenshot = completed_urls[0][1] # Pehle converted URL ka screenshot

            # Screenshot sirf Amazon/Flipkart links ke liye
            if "amzn.to" in product_url_for_screenshot or "flipkart.com" in product_url_for_screenshot or "fkrt.it" in product_url_for_screenshot:
                extracted_screenshot_path = await take_screenshot(product_url_for_screenshot)
            else:
                print(f"Skipping screenshot for non-Amazon/Flipkart URL: {product_url_for_screenshot}")

            if extracted_screenshot_path:
                try:
                    await client.send_photo(
                        chat_id=Telegram.MAIN_CHAT_ID,
                        photo=extracted_screenshot_path, # Local file path use karein
                        caption=final_text
                        # disable_web_page_preview=True # NO disable_web_page_preview here
                    )
                except Exception as e:
                    print(f"ERROR: Failed to send photo to Telegram: {e}")
                    await client.send_message(
                        chat_id=Telegram.MAIN_CHAT_ID,
                        text=final_text,
                        disable_web_page_preview=True
                    )
                finally:
                    os.remove(extracted_screenshot_path)
            else: # Agar screenshot nahi le paaye, toh sirf text message bhej dein
                await client.send_message(
                    chat_id=Telegram.MAIN_CHAT_ID,
                    text=final_text,
                    disable_web_page_preview=True
                )
        # --- SCREENSHOT / PHOTO SENDING LOGIC ENDS ---

    else:
        if Telegram.LOG_GROUP_ID:
            await client.send_message(
                chat_id=Telegram.LOG_GROUP_ID,
                text="No supported links found in the message.",
                disable_web_page_preview=True
            )
        else:
            print("LOG_GROUP_ID not set, unable to send log: No supported links found.")
