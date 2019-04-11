import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

import sqlite3

from src import backend

from collections import defaultdict


class Server:
    keyboards = ['keyboards/keyboard_home.json',
                 'keyboards/keyboard_type_dictation.json',
                 'keyboards/keyboard_none.json',
                 'keyboards/keyboard_mode_dictation.json',
                 'keyboards/keyboard_test.json']
    messages = {'start': 'Рад Вас видеть!',
                'home': 'Вы находитесь в главном меню',
                'about': 'Разработано Drackeland Technology',
                'type_dictation': 'Какой диктант предпочтёте писать?',
                'mode_dictation': 'Потренируемся или напишем контрольную?'
                }
    users = defaultdict(int)

    def __init__(self, token, group_id, server_name: str = "Empty"):
        self.username = ''
        self.cur_keyboard = 0
        self.cur_mes = 'start'
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0
        self.active = 0
        self.queque = []

    def send_msg(self, send_id, message, keyboard_index):
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message,
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[keyboard_index], "r", encoding="UTF-8").read())
        self.random_id += 1

    def start(self):
        k = 0
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.send_msg(event.object.peer_id, self.messages[self.cur_mes], 2)
                self.cur_mes = 'home'
                k = event.object.peer_id
                break
        self.home(k)

    def home(self, peer_id):
        print('@home')
        self.send_msg(peer_id, self.messages[self.cur_mes], self.users[peer_id])
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.get_user_name(event.object.peer_id)
                user_stat = self.users[event.object.peer_id]
                if event.object.text == 'Диктант' and not user_stat:
                    self.cur_mes = 'type_dictation'
                    self.users[event.objecs.peer_id] = 1
                elif event.object.text == 'О боте' and not user_stat:
                    self.send_msg(event.object.peer_id, self.messages['about'], 2)
                elif event.object.text == 'Орфоэпический' and user_stat == 1:
                    self.cur_mes = 'mode_dictation'
                    self.users[event.objecs.peer_id] = 2
                elif event.object.text == 'Контрольная':
                    self.start_contest(event.object.peer_id)
                elif event.object.text == 'Назад':
                    if self.users[event.object.peer_id] == 1:
                        self.users[event.object.peer_id] = 0
                        self.cur_mes = 'home'
                    elif self.users[event.object.peer_id] == 3:
                        self.users[event.object.peer_id] = 1
                        self.cur_mes = 'type_dictation'
                self.send_msg(event.object.peer_id, self.messages[self.cur_mes], self.users[event.object.peer_id])

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        info = self.vk_api.users.get(user_id=user_id)[0]
        if info['id'] not in self.users.keys():
            self.users[info['id']] = User(info['id'],
                                          info['first_name'],
                                          info['last_name'])

    def start_contest(self, peer_id):
        self.active = peer_id
        res = 0
        for i in range(32):
            print(i, 32, sep='/')
            quest = backend.Question()
            self.send_msg(peer_id, quest.quest, 4)
            for event in self.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object.peer_id == peer_id:
                        if quest.task(event.object.text):
                            res += 1
                            self.send_msg(peer_id, 'Молодец', 2)
                        elif event.object.text == 'Стоп':
                            return 0
                        else:
                            self.send_msg(peer_id, f'Увы, но правильно произносить {quest.answer}', 2)
                        break
                    else:
                        self.send_msg(event.object.peer_id,
                                      f'{self.vk_api.users.get(user_id=event.object.peer_id)[0]["first_name"]}, приносим'
                                      f'извинения, но сервер занят(',
                                      2)
                        self.queque.append(event.object.peer_id)

        self.send_msg(peer_id, f'Ваш результат {res}/32', 0)
        for i in self.queque:
            self.send_msg(i,
                          f'{self.vk_api.users.get(user_id=i)[0]["first_name"]},бот освободился, '
                          f'успей потренироваться!',
                          2)
        self.queque = []
        self.active = 0


class User:
    def __init__(self, vk_id, first_name, last_name, action_id=0, cur_answer=None, group_id=None):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name
        self.action_id = action_id
        self.cur_answer = cur_answer
        self.group_id = group_id


class UserGroup:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data

    @staticmethod
    def read_from_db(table_name='Users'):
        con = sqlite3.connect(r'src/rus_slovo.db')
        sql = f'SELECT * FROM {table_name}'
        cur = con.cursor()
        c = list(cur.execute(sql))
        cur.fetchall()
        cur.close()
        con.close()
        return 0
