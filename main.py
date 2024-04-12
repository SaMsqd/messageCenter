from avito.avito_api import AvitoApi
import requests


client_id = '1GQx2lP_yfl6VT8RocTg'

client_secret = 'tLUAc-vrNV7rvdlS8WOmK5wJGlAJem5vCFG8hdqr'
profile_id = 234428796

api = AvitoApi(profile_id=profile_id, client_id=client_id, client_secret=client_secret)
chat_id = api.chats_queue[1]['id']
messages = api.get_chat(chat_id)

for message in messages['messages']:
    if message['content']['text'] == 'Хай':
        api.send_message(chat_id=chat_id, text='Проверка API 2')

