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
                 'keyboards/keyboard_task.json']
    messages = {'start': 'Рад Вас видеть!',
                'home': 'Вы находитесь в главном меню',
                'about': 'Разработано Drackeland Technology',
                'type_dictation': 'Какой диктант предпочтёте писать?',
                'mode_dictation': 'Потренируемся или напишем контрольную?',
                'choose_task': 'Выберите задание из предложенного списка:'
                }
    users = defaultdict(lambda: [-1, 0])

    def __init__(self, token, group_id):
        self.username = ''
        self.cur_keyboard = 0
        self.cur_mes = 'start'
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.active = 0
        self.random_id = 0

    def send_msg(self, send_id, message, keyboard_index=0):
        if self.users[send_id][0] in {5, 6}:
            try:
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=self.random_id,
                                          keyboard=open(f'keyboards/{send_id}.json', 'r',
                                                        encoding='UTF-8').read())
            except FileNotFoundError:
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=self.random_id,
                                          keyboard=open(self.keyboards[2], "r", encoding="UTF-8").read())
        else:
            self.vk_api.messages.send(peer_id=send_id,
                                      message=message,
                                      random_id=self.random_id,
                                      keyboard=open(self.keyboards[keyboard_index], "r", encoding="UTF-8").read())
        self.random_id += 1

    def start(self):
        print('@home')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer = event.object.peer_id
                if self.users[peer][0] not in {5, 6}:
                    if self.users[peer][0] == -1:
                        self.send_msg(peer,
                                      self.messages['start'],
                                      2)
                        self.users[peer][0] = 0
                    if event.object.text == 'Диктант' and not self.users[peer][0]:
                        self.cur_mes = 'type_dictation'
                        self.users[peer][0] = 1
                    elif event.object.text == 'О боте' and not self.users[peer][0]:
                        self.send_msg(peer, self.messages['about'], 2)
                    elif event.object.text == 'Орфоэпический' and self.users[peer][0] == 1:
                        self.cur_mes = 'mode_dictation'
                        self.users[peer][0] = 3
                    elif event.object.text == 'Контрольная':
                        self.cur_mes = 'choose_task'
                        self.users[peer][0] = 4
                    elif event.object.text == 'Назад':
                        if self.users[peer][0] == 1:
                            self.users[peer][0] = 0
                            self.cur_mes = 'home'
                        elif self.users[peer][0] == 3:
                            self.users[peer][0] = 1
                            self.cur_mes = 'type_dictation'
                        elif self.users[peer][0] == 4:
                            self.users[peer][0] = 3
                            self.cur_mes = 'mode_dictation'
                    elif self.users[peer][0] == 4:
                        a = ["Августовский ... занял",
                             "Заняла ... нарвала"]
                        res = a.index(event.object.text)
                        self.start_cont(res + 1, peer)
                        self.users[peer][0] = 5
                        self.send_msg(peer,
                                      'Отправьте любой символ чтобы начать',
                                      self.users[peer][0])
                    self.send_msg(peer, self.messages[self.cur_mes], self.users[peer][0])
                elif self.users[peer] == 5:
                    kk = self.users[peer][1].current_task
                    self.users[peer][1].task[kk].get_json_keyboard()
                    self.send_msg(peer, self.users[peer][1].task[kk].word)
                    self.users[peer][0] = 6
                else:
                    if event.object.text != 'Стоп':
                        kk = self.users[peer][1].current_task
                        if self.users[peer][1].task[kk].check(event.object.text):
                            self.send_msg(peer, 'Молодец', 2)
                            self.users[peer][1].right += 1
                        else:
                            answer = self.users[peer][1].task[kk].answer
                            self.send_msg(peer, f'Увы, но правильно произносить {answer}', 2)
                        self.users[peer][1].current_task += 1
                        if self.users[peer][1].current_task < 32:
                            kk = self.users[peer][1].current_task
                            self.users[peer][1].task[kk].get_json_keyboard()
                            self.send_msg(peer, self.users[peer][1].task[kk].word)
                        else:
                            self.send_msg(peer, f'Ваш результат {self.users[peer][1].right}/32', 0)
                            self.users[peer][0]=0
                    else:
                        self.send_msg(peer, f'Ваш результат {self.users[peer][1].right}/32', 0)
                        self.users[peer][0] = 0



    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def start_cont(self, index, peer):
        assert isinstance(index, int)
        self.users[peer][1] = backend.Task(index, peer)

