import requests
from threading import Thread
import sqlite3
token = "bot5857334617:AAHAAgaaMlIBco-nhchV8E9_0vakdi8T3_g"


class MySend(Thread):
    def __init__(self, id_tg, msg_tg):
        Thread.__init__(self)
        self.idtg = id_tg
        self.msg = msg_tg

    def run(self):
        """
        url=f'https://api.telegram.org/{token}/forwardMessage'
        params={
            "chat_id": self.idtg,
            "from_chat_id": 202164415,
            "message_id": 6157
        }
        """
        url = f"https://api.telegram.org/{token}/sendMessage"
        params = {
            "chat_id": self.idtg,
            "text": self.msg
        }
        requests.post(url=url, params=params)


msg = '''
Бот снова в исправном состоянии и работает.
Упростил алгоритм поиска фото, от чего выдает результат быстрей и без ошибок
'''

conn = sqlite3.connect('userdata.db')
rq = f"SELECT id from userdata"
for row in conn.execute(rq):
    tg = row[0]
    print(f"Прислано к {tg}")
    MySend(tg, msg).start()

print("Разослано!")
conn.close()