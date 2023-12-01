import requests
from telegram_receiver_list import TOKEN,chat_id_str
def send_results_to_tg(message,file_opened):

    def send_message(message):
        message = message
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json()) # this sends the message

    def send_photo(chat_id, file_opened):
        
        method = "sendPhoto"
        params = {'chat_id': chat_id}
        files = {'photo': file_opened}
        resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/"+ method, params, files=files)
        return resp

    for chat_id in chat_id_str:
        send_message(message)
        send_photo(chat_id, file_opened)