import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from src import backend

from collections import defaultdict


class Server:
    keyboards = ['src/keyboard_home.json',
                 'src/keyboard_type_dictation.json',
                 'src/keyboard_none.json',
                 'src/keyboard_mode_dictation.json',
                 'src/keyboard_test.json']

    def __init__(self, token, group_id, server_name: str = "Empty"):
        self.username = ''
        self.users = defaultdict(str)
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0

    def send_msg(self, send_id, message, keyboard_index):
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message,
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[keyboard_index], "r", encoding="UTF-8").read())
        self.random_id += 1

    def start(self):
        for event in self.long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.username = self.get_user_name(event.object.from_id)
                self.send_msg(event.object.peer_id, 'Рад Вас видеть!', 2)
                self.home(event.object.peer_id)

    def home(self, peer_id):
        print('@home')
        self.send_msg(peer_id, 'Вы находитесь в главном меню', 0)
        for event in self.long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.text == 'Диктант':
                    self.choose_dictation(event.object.peer_id)

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def choose_dictation(self, peer_id):
        print('@cd')
        self.send_msg(peer_id, 'Какой диктант предпочтёте писать?', 1)
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.text == 'Назад':
                    self.home(peer_id)
                elif event.object.text == 'Орфоэпический':
                    self.choose_mode_orfo(peer_id)

    def choose_mode_orfo(self, peer_id):
        print('@choose mode')
        self.send_msg(peer_id, 'Потренируемся или напишем контрольную?', 3)
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.text == 'Назад':
                    self.choose_dictation(peer_id)
                elif event.object.text == 'Контрольная':
                    self.start_contest(peer_id)

    def start_contest(self, peer_id):
        res = 0
        for i in range(32):
            print(i, 32, sep='/')
            quest = backend.Question()
            self.send_msg(peer_id, quest.quest, 4)
            for event in self.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if quest.task(event.object.text):
                        res += 1
                        self.send_msg(peer_id, 'Молодец', 2)
                    else:
                        self.send_msg(peer_id, f'Увы, но правильно произносить {quest.answer}',2)
                    break
        self.send_msg(peer_id, f'Ваш результат {res}/32', 0)
