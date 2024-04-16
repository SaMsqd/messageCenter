from bot import password
from avito.account import Account
from web import app

# account = Account(profile_id=159470220,
#                   client_id='Pm4BmvaY4LPFHQ6Oo_Hu',
#                   client_secret='qBO1H1ssvcfotR15Nw1Qpxrs_1yG9vyhWb9tbgj5',
#                   proxy=None,
#                   name='Свой гаджет РФ')

# for chat in account.api.chats_queue:
#     print(chat['context']['value']['title'])
#     print(chat['id'])


def get_password():
    return password

