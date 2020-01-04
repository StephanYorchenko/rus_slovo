import sqlite3

import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from src.backend import orfoepy_back
import src.backend.grammar_norms as gm
import src.backend.orthography_back as ob
import src.backend.sql_selections as ss
from src.backend.user_dict import UserDict

class Server:
    keyboards = {0: ['keyboards/keyboard_home.json', 'Вы находитесь в главном меню'],
                 1: ['keyboards/keyboard_type_dictation.json', 'Какой диктант предпочтёте писать?'],
                 2: ['keyboards/keyboard_none.json', 'Рад Вас видеть!'],
                 3: ['keyboards/keyboard_mode_dictation.json', 'Потренируемся или напишем контрольную?'],
                 4: ['keyboards/keyboard_task.json', 'Выберите задание из предложенного списка:'],
                 5: ['keyboards/keyboard_start.json', 'Нажмите, чтобы начать'],
                 6: ['keyboards/keyboard_next.json', 'Выберите дальнейшее действие'],
                 7: [],
                 8: ['keyboards/keyboard_grammar_mode.json', 'Какое задание предпочтёте?'],
                 9: ['keyboards/keyboard_mode_dictation.json', 'Потренируемся или напишем контрольную?'],
                 10: ['keyboards/keyboard_next.json', 'Выберите дальнейшее действие'],
                 13: ['keyboards/keyboard_mode_dictation.json', 'Потренируемся или напишем контрольную?']
                 }

    users = UserDict()

    def __init__(self, token, group_id):
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0

    def send_msg(self, send_id, message=False, keyboard_index=0, start=False):

        """Распределение типов сообщений по методам"""

        if self.users[send_id][0] in {5, 6, 10, 11, 14, 15}:
            self.test_messages(send_id, message, start)
        else:
            self.standard_message(send_id, keyboard_index, message)
        self.random_id += 1

    def test_messages(self, send_id, message, start):

        """Отправка сообщений во время прохождения тестирования"""

        if not start:
            self.vk_api.messages.send(peer_id=send_id,
                                      message=message,
                                      random_id=self.random_id,
                                      keyboard=open(f'keyboards/{send_id}.json', 'r',
                                                    encoding='UTF-8').read())
        else:
            self.start_test_message(send_id)

    def start_test_message(self, send_id):

        """Отправка стартового сообщения при запуске теста"""

        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[5][1],
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[5][0], "r", encoding="UTF-8").read())

    def standard_message(self, send_id, keyboard_index, message):

        """Отправка стандартых сообщений (меню и прочее)"""

        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[keyboard_index][1] if not message else message,
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[keyboard_index][0], "r", encoding="UTF-8").read())

    def start(self):
        # TODO: rewrite this method. It's too large!

        print('@home')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(self.users, event.type, event.object.text, sep='     ')
                peer = event.object.peer_id
                self.users[peer][2] += 1
                if self.users[peer][0] not in {5, 6, 10, 11, 14, 15}:
                    if self.users[peer][0] == -1:
                        self.send_msg(peer, keyboard_index=2)
                        self.keyboards[2][1] = 'Разработано DvaTopora'
                        self.users[peer][0] = 0
                    else:
                        try:
                            next_stat, execute, cont = self.get_action(peer, event.object.text)
                            print(next_stat, execute)
                            self.users[peer][0] = next_stat
                            exec(execute)
                            if cont:
                                continue
                        except IndexError:
                            pass

                    self.send_msg(peer, keyboard_index=self.users[peer][0])

                elif self.users[peer][0] == 5:
                    self.users[peer][1].task[0].get_json_keyboard(exit_button=True)
                    self.send_msg(peer, self.users[peer][1].task[0].word)
                    self.users[peer][0] = 6
                elif self.users[peer][0] == 6:
                    if event.object.text != 'Стоп':
                        kk = self.users[peer][1].current_task
                        check = self.users[peer][1].task[kk].check(event.object.text)
                        if check[0]:
                            if check[1] == 3:
                                self.send_msg(peer, 'Молодец', 2)
                            else:
                                self.send_msg(peer, f'Молодец! Надеюсь, ты занешь что можно говорить и {check[1]}', 2)
                            self.users[peer][1].right += 1
                        else:
                            answer = self.users[peer][1].task[kk].answer
                            self.send_msg(peer, f'Увы, но правильно произносить {answer}', 2)
                        self.users[peer][1].current_task += 1
                        if self.users[peer][1].current_task < 32:
                            kk = self.users[peer][1].current_task
                            self.users[peer][1].task[kk].get_json_keyboard(exit_button=True)
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

                elif self.users[peer][0] == 10:

                    self.users[peer][1].queque[0].get_json_keyboard()
                    self.send_msg(peer,
                                  f'Образуй {self.users[peer][1].queque[0].quest}'
                                  f' слова {self.users[peer][1].queque[0].word}')
                    self.users[peer][0] = 11
                elif self.users[peer][0] == 11:
                    if event.object.text != 'Стоп':
                        kk = self.users[peer][1].current_task
                        if self.users[peer][1].queque[kk].check(event.object.text):
                            self.send_msg(peer, 'Молодец', 2)
                            self.users[peer][1].right += 1
                        else:
                            answer = self.users[peer][1].queque[kk].answer_right
                            self.send_msg(peer, f'Увы, но правильно писать {answer}', 2)
                        self.users[peer][1].current_task += 1
                        if self.users[peer][1].current_task < 16:
                            kk = self.users[peer][1].current_task
                            self.users[peer][1].queque[kk].get_json_keyboard()
                            self.send_msg(peer,
                                          f'Образуй {self.users[peer][1].queque[kk].quest}'
                                          f' слова {self.users[peer][1].queque[kk].word}')
                        else:
                            self.users[peer][0] = 12
                            self.send_msg(peer,
                                          f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/16',
                                          keyboard_index=6)
                    else:
                        self.users[peer][0] = 12
                        self.send_msg(peer, f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/16',
                                      keyboard_index=6)

                elif self.users[peer][0] == 14:

                    self.users[peer][1].queue[0].get_json_keyboard()
                    self.send_msg(peer,
                                  f'Как правильно пишется {self.users[peer][1].queue[0].word}?')
                    self.users[peer][0] = 15

                elif self.users[peer][0] == 15:
                    if event.object.text != 'Стоп':
                        kk = self.users[peer][1].current_task
                        if self.users[peer][1].queue[kk].check(event.object.text):
                            self.send_msg(peer, 'Молодец', 2)
                            self.users[peer][1].right += 1
                        else:
                            answer = self.users[peer][1].queue[kk].answer
                            self.send_msg(peer, f'Увы, но правильно писать {answer}', 2)
                        self.users[peer][1].current_task += 1
                        if self.users[peer][1].current_task < 10:
                            kk = self.users[peer][1].current_task
                            self.users[peer][1].queue[kk].get_json_keyboard()
                            self.send_msg(peer,
                                          f'Как правильно пишется {self.users[peer][1].queue[kk].word}?')
                        else:
                            self.users[peer][0] = 16
                            self.send_msg(peer,
                                          f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/10',
                                          keyboard_index=6)
                    else:
                        self.users[peer][0] = 16
                        self.send_msg(peer, f'{self.get_user_name(peer)}, Ваш результат {self.users[peer][1].right}/16',
                                      keyboard_index=6)

    def get_user_name(self, user_id):

        """ Получаем имя пользователя"""

        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def start_orthoepy_task(self, index, peer):

        """ Запускаем тест по орфоэпии"""

        assert isinstance(index, int), "Wrong index value (must be int())"
        self.users[peer][1] = orfoepy_back.OrthoepyTask(peer, index)
        self.send_msg(peer, start=True)

    def start_grammar_task(self, peer):

        """ Запускаем тест по грамматическим нормам"""

        self.users[peer][1] = gm.GrammarTask(peer)
        self.send_msg(peer, start=True)

    def start_orthography_task(self, peer):

        """ Запускаем тест по орфографии"""

        self.users[peer][1] = ob.OrthographyTask(peer)
        self.send_msg(peer, start=True)

    def get_action(self, peer, button_name):

        """ Getting data from database """

        data = ss.DataSource(r'src/controllers')
        next_stat, execute, cont = data.sql_select('Button',
                                             ['next_stat', 'execute', 'continue'],
                                             {'cur_stat': self.users[peer][0],
                                              'button_name': button_name})[0]
        return next_stat, execute, cont
