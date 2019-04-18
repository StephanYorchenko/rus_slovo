import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from src import backend


class Server:
    keyboards = [['keyboards/keyboard_home.json', 'Вы находитесь в главном меню'],
                 ['keyboards/keyboard_type_dictation.json', 'Какой диктант предпочтёте писать?'],
                 ['keyboards/keyboard_none.json', 'Рад Вас видеть!'],
                 ['keyboards/keyboard_mode_dictation.json', 'Потренируемся или напишем контрольную?'],
                 ['keyboards/keyboard_task.json', 'Выберите задание из предложенного списка:'],
                 ['keyboards/keyboard_start.json', 'Нажмите, чтобы начать'],
                 ['keyboards/keyboard_next.json', 'Выберите дальнейшее действие']
                 ]

    users = backend.UserDict()

    def __init__(self, token, group_id):
        self.username = ''
        self.cur_keyboard = 0
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.active = 0
        self.random_id = 0

    def send_msg(self, send_id, message=False, keyboard_index=0):
        if self.users[send_id][0] in {5, 6}:
            try:
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=self.random_id,
                                          keyboard=open(f'keyboards/{send_id}.json', 'r',
                                                        encoding='UTF-8').read())
            except FileNotFoundError:
                self.vk_api.messages.send(peer_id=send_id,
                                          message=self.keyboards[5][1],
                                          random_id=self.random_id,
                                          keyboard=open(self.keyboards[5][0], "r", encoding="UTF-8").read())
        else:
            self.vk_api.messages.send(peer_id=send_id,
                                      message=self.keyboards[keyboard_index][1] if not message else message,
                                      random_id=self.random_id,
                                      keyboard=open(self.keyboards[keyboard_index][0], "r", encoding="UTF-8").read())
        self.random_id += 1

    def start(self):
        print('@home')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(self.users, event.type, event.object.text, sep='     ')
                peer = event.object.peer_id
                self.users[peer][2] += 1
                if self.users[peer][0] not in {5, 6}:
                    if self.users[peer][0] == -1:
                        self.send_msg(peer, keyboard_index=2)
                        self.keyboards[2][1] = 'Разрабоотано DvaTopora'
                        self.users[peer][0] = 0
                    if event.object.text == 'Диктант' and not self.users[peer][0]:
                        self.users[peer][0] = 1
                    elif event.object.text == 'О боте' and not self.users[peer][0]:
                        self.send_msg(peer, keyboard_index=2)
                    elif event.object.text == 'Орфоэпический' and self.users[peer][0] == 1:
                        self.users[peer][0] = 3
                    elif event.object.text == 'Контрольная':
                        self.users[peer][0] = 4
                    elif event.object.text == 'Назад':
                        if self.users[peer][0] == 1:
                            self.users[peer][0] = 0
                        elif self.users[peer][0] == 3:
                            self.users[peer][0] = 1
                        elif self.users[peer][0] == 4:
                            self.users[peer][0] = 3
                    elif self.users[peer][0] == 4:
                        a = ["Августовский ... занял",
                             "Заняла ... нарвала"]
                        try:
                            res = a.index(event.object.text)
                            self.start_cont(res + 1, peer)
                            self.users[peer][0] = 5
                            self.send_msg(peer)
                            continue
                        except ValueError:
                            self.send_msg(peer, 'А виртуальную клавиатуру для кого придумали?', 2)
                    elif self.users[peer][0] == 7:
                        if event.object.text == "Попробовать заново":
                            self.users[peer][0] = 4
                        else:
                            self.users[peer][0] = 0
                    self.send_msg(peer, keyboard_index=self.users[peer][0])
                elif self.users[peer][0] == 5:
                    self.users[peer][1].task[0].get_json_keyboard(exit_but=True)
                    self.send_msg(peer, self.users[peer][1].task[0].word)
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
                            self.users[peer][1].task[kk].get_json_keyboard(exit_but=True)
                            self.send_msg(peer, self.users[peer][1].task[kk].word)
                        else:
                            self.users[peer][0] = 7
                            self.send_msg(peer,
                                          f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/32',
                                          keyboard_index=6)
                    else:
                        self.users[peer][0] = 7
                        self.send_msg(peer, f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/32',
                                      keyboard_index=6)

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def start_cont(self, index, peer):
        assert isinstance(index, int)
        self.users[peer][1] = backend.Task(peer, index)
        print(self.users[peer][1].task[31])
