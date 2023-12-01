import requests,json
from telegram_receiver_list import TOKEN,chat_id_str
import pandas as pd
def get_bot_chat_inbound(TOKEN):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    return requests.get(url).json()

results=get_bot_chat_inbound(TOKEN)
print(results)