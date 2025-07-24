# ... (baaki imports aur code) ...

if completed_urls:
    final_text = text
    for url, aurl in completed_urls:
        final_text = final_text.replace(url, aurl)

    # --- SCREENSHOT / PHOTO SENDING LOGIC ---
    if message.photo: # Agar original message mein photo hai
        await client.send_photo(
            chat_id=Telegram.MAIN_CHAT_ID,
            photo=message.photo.file_id,
            caption=final_text
            # disable_web_page_preview=True # <-- YEH LINE HATA DEIN (Line 62 par)
        )
    else: # Agar original message mein photo nahi hai, toh screenshot lene ki koshish karein
        product_url_for_screenshot = completed_urls[0][1] # Converted URL ko use karein

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
                    # disable_web_page_preview=True # <-- YEH LINE HATA DEIN
                )
            except Exception as e:
                print(f"ERROR: Failed to send photo to Telegram: {e}")
                # Agar photo send nahi hoti, toh text message bhej dein
                await client.send_message(
                    chat_id=Telegram.MAIN_CHAT_ID,
                    text=final_text,
                    disable_web_page_preview=True
                )
            finally:
                # Temporary screenshot file ko delete karein
                os.remove(extracted_screenshot_path)
        else: # Agar screenshot nahi le paaye, toh sirf text message bhej dein
            await client.send_message(
                chat_id=Telegram.MAIN_CHAT_ID,
                text=final_text,
                disable_web_page_preview=True
            )
    # --- SCREENSHOT / PHOTO SENDING LOGIC ENDS ---

else:
    # ... (Log group handling for "No supported links found") ...
    if Telegram.LOG_GROUP_ID:
        await client.send_message(
            chat_id=Telegram.LOG_GROUP_ID,
            text="No supported links found in the message.",
            disable_web_page_preview=True
        )
    else:
        print("LOG_GROUP_ID not set, unable to send log: No supported links found.")
