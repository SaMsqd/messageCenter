import requests
import json

proxies = {
    'http': '51.15.241.5:16379'
}

client_id = '1GQx2lP_yfl6VT8RocTg'

client_secret = 'tLUAc-vrNV7rvdlS8WOmK5wJGlAJem5vCFG8hdqr'
user_id = 234428796
headers = {'Authoriztion': 'VDBqyhGASGqpRSoVD0epXAEvDK3-Dm_eRpoJUBXj'}

data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}

response = requests.post('https://api.avito.ru/token/', data=data)
print(response.content)


headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer whgiED96RJOAhXPAnxFUPQA2qJmSEF3KMBMUjRyx'
}

params = {
    'unread_only': 'false',
    'chat_types': 'u2i,u2u',
    'limit': '1',
}
# res = requests.get(headers=headers, params=params, url=f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats')
#
# """
# Алгоритм: Получаем  токен по client_id и client_secret, получаем от пользователя
# client_id(id профиля). Закидываем токен при каждом запросе в header вида
# {'Authorization': 'Bearer <TOKEN>'} и отправляем запросы
# """
# content = json.loads(res.content.decode())

# chat_id = content['chats'][0]['id']
# response = requests.get(headers=headers, url=f'https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/')
# content = json.loads(response.content.decode())
# for message in content['messages']:
#     try:
#         continue
#         print(message['content'])
#     except KeyError:
#         pass


