# -*- coding: utf-8 -*-

import random
import json
import sqlite3
import src.backend.sql_selections as ss


class Question:

    def __init__(self, answer, peer):
        self.word = str(answer).lower()
        self.answer = answer
        self.peer = peer
        self.list_answers = self.get_list_answers()

    @staticmethod
    def reformat_word(word, k=None):
        word = list(word)
        word[k] = word[k].upper()
        return ''.join(word)

    def get_list_answers(self):
        keys = [i for i in range(len(self.word)) if self.word[i] in list('ёуеыаоэяию')]
        res_list = [self.reformat_word(self.word, x) for x in keys]
        random.shuffle(res_list)
        return res_list

    def get_json_keyboard(self, exit_but=False):
        result_dict = {'one_time': False,
                       'buttons': []}
        for i in self.list_answers:
            print(i)
            k = [{
                "action": {
                    "type": "text",
                    "label": i
                },
                "color": "default"
            }]
            result_dict['buttons'].append(k)
        if exit_but:
            exit = [
                {
                    'action': {
                        'type': 'text',
                        'label': 'Стоп'
                    },
                    'color': 'negative'
                }
            ]
            result_dict['buttons'].append(exit)
        with open(f'keyboards/{self.peer}.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result_dict, indent=4, ensure_ascii=False))

    def check(self, answer):
        if answer != 'электропрОвод' or answer != 'электропровОд':
            return [answer == self.answer, 3]
        else:
            return [True, int(not ['электропрОвод', 'электропровОд'].index(answer))]

    def __str__(self):
        return f'<{self.word}----{self.answer}>'


class Task:
    def __init__(self, peer=0, task=0):
        self.task = self.question_creator(self.selector(task), peer) if task else 0
        self.current_task = 0
        self.right = 0

    @staticmethod
    def selector(index):
        con = sqlite3.connect(r'src/rus_slovo.db')
        sql = "SELECT answer FROM orfo_dictation"
        if index:
            sql += f' WHERE index_task = {index}'
        cur = con.cursor()
        c = list(cur.execute(sql))
        random.shuffle(c)
        cur.fetchall()
        cur.close()
        con.close()
        return c[:32]

    @staticmethod
    def question_creator(array, peer):
        return [Question(i[0], peer) for i in array]


class UserDict(dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, peer_id):
        if peer_id not in self.keys():
            self[peer_id] = [-1, Task(), 0, 0]
        return self[peer_id]

    def __str__(self):
        return f'<------ {len(self.keys())} records---->'

    def get_next_stat(self, peer, button_name):
        """
        Getting new users position in menu
        :param peer: peer of user, takes from vk_api
        :param button_name: name of clicked button from current UI
        :change: current position of user in UI
        """
        data_base = ss.DataSource(r'src/controllers')
        self[peer][0] = data_base.sql_select('Buttons', ['next_stat'], {'current_stat': self[peer][0],
                                                                        'button_name': button_name})
