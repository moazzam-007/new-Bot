from pyrogram import Client
from config import Telegram

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
    client.run()