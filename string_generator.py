from telethon.sync import TelegramClient
from telethon.sessions import StringSession
print("""Please go-to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details""")
APP_ID = int(input("3683760: "))
API_HASH = input("753f879b9411fe8d3d3dc2eb01160eab: ")
with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(client.session.save())
