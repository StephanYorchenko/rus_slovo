import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from src.backend import orfoepy_back
import src.backend.grammar_norms as gm
import src.backend.orthography_back as ob

import os

from src.backend.image_creator.creator import HTMLConventor


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

    users = orfoepy_back.UserDict()

    back_button = {1: 0,
                   3: 1,
                   4: 3,
                   9: 8,
                   8: 0,
                   13: 1}

    def __init__(self, token, group_id):
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0

    def send_msg(self, send_id, message=False, keyboard_index=0, start=False):
        if self.users[send_id][0] in {5, 6, 10, 11}:
            if not start:
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=self.random_id,
                                          keyboard=open(f'keyboards/{send_id}.json', 'r',
                                                        encoding='UTF-8').read())

            else:
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
                if self.users[peer][0] not in {5, 6, 10, 11, 14, 15}:
                    if self.users[peer][0] == -1:
                        self.send_msg(peer, keyboard_index=2)
                        self.keyboards[2][1] = 'Разрабоотано DvaTopora'
                        self.users[peer][0] = 0
                    if event.object.text == 'Диктант' and not self.users[peer][0]:
                        self.users[peer][0] = 1
                    elif event.object.text == 'Орфографический' and self.users[peer][0] == 1:
                        self.users[peer][0] = 13
                    elif event.object.text == 'Тренировка' and self.users[peer][0] == 13:
                        self.start_orthography(peer)
                        self.users[peer][0] = 14
                        self.send_msg(peer, start=True)
                        continue
                    elif event.object.text == "Грамматика" and not self.users[peer][0]:
                        self.users[peer][0] = 8
                    elif event.object.text == 'О боте' and not self.users[peer][0]:
                        self.send_msg(peer, keyboard_index=2)
                    elif event.object.text == 'Орфоэпический' and self.users[peer][0] == 1:
                        self.users[peer][0] = 3
                    elif self.users[peer][0] == 3 and event.object.text == 'Тренировка':
                        self.users[peer][0] = 4
                    elif event.object.text == 'Назад' and self.users[peer][0] in self.back_button.keys():
                        self.users[peer][0] = self.back_button[self.users[peer][0]]
                    elif self.users[peer][0] == 4:
                        a = ["Августовский ... занял",
                             "Заняла ... нарвала",
                             "Нарост ... предложу",
                             "Премировать... электропровод"]
                        try:
                            res = a.index(event.object.text)
                            self.start_orthoepy_cont(res + 1, peer)
                            self.users[peer][0] = 5
                            self.send_msg(peer, start=True)
                            continue
                        except ValueError:
                            self.send_msg(peer, 'А виртуальную клавиатуру для кого придумали?', 2)
                    elif self.users[peer][0] == 7:
                        if event.object.text == "Попробовать заново":
                            self.users[peer][0] = 4
                        else:
                            self.users[peer][0] = 0
                    elif self.users[peer][0] == 8 and event.object.text == "Грамматические нормы":
                        self.users[peer][0] = 9
                    elif self.users[peer][0] == 9 and event.object.text == 'Тренировка':
                        self.start_grammar_task(peer)
                        self.users[peer][0] = 10
                        self.send_msg(peer, start=True)
                        continue
                    elif self.users[peer][0] == 12:
                        if event.object.text == "Попробовать заново":
                            self.users[peer][0] = 8
                        else:
                            self.users[peer][0] = 0

                    elif self.users[peer][0] == 16:
                        if event.object.text == "Попробовать заново":
                            self.users[peer][0] = 13
                        else:
                            self.users[peer][0] = 0

                    self.send_msg(peer, keyboard_index=self.users[peer][0])

                elif self.users[peer][0] == 5:
                    self.users[peer][1].task[0].get_json_keyboard(exit_but=True)
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

    def start_orthoepy_cont(self, index, peer):
        assert isinstance(index, int)
        self.users[peer][1] = orfoepy_back.Task(peer, index)

    def start_grammar_task(self, peer):
        self.users[peer][1] = gm.GrammarTask(peer)

    def start_orthography(self, peer):
        self.users[peer][1] = ob.OrthographyTask(peer)
