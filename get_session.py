from pyrogram import Client

api_id = 10488391
api_hash = "32039877c9cb88f90a63c919977ccd1d"

with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
    print(app.export_session_string())
