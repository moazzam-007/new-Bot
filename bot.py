from pyrogram import Client
from config import Telegram
from flask import Flask # <-- YEH LINE ADD KAREIN
import threading # <-- YEH LINE ADD KAREIN
import os # <-- YEH LINE ADD KAREIN

# Flask app banayein
app = Flask(__name__) # <-- YEH LINE ADD KAREIN

# Dummy route banayein
@app.route('/') # <-- YEH LINE ADD KAREIN
def home(): # <-- YEH LINE ADD KAREIN
    return "Bot is running and listening for Telegram updates!", 200 # <-- YEH LINE ADD KAREIN

# Flask app ko alag thread mein chalane ke liye function
def run_flask_app(): # <-- YEH LINE ADD KAREIN
    port = int(os.environ.get("PORT", 10000)) # Render PORT environment variable deta hai
    app.run(host="0.0.0.0", port=port) # <-- YEH LINE ADD KAREIN

client = Client(
    ":memory:",
    api_id=Telegram.API_ID,
    api_hash=Telegram.API_HASH,
    session_string=Telegram.STRING_SESSION,
    phone_number=Telegram.PHONE_NUMBER,
    plugins=dict(root="plugins"),
    workers=10,
    in_memory=True
)

if __name__ == "__main__":
    # Flask app ko ek alag thread mein start karein
    flask_thread = threading.Thread(target=run_flask_app) # <-- YEH LINE ADD KAREIN
    flask_thread.start() # <-- YEH LINE ADD KAREIN

    # Pyrogram client ko start karein
    client.run()
