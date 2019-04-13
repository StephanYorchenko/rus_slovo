# -*- coding: utf-8 -*-

import random
import json
import sqlite3


class Question:

    def __init__(self, word, answer, peer):
        self.word = word
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
        return answer == self.answer

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
        sql = "SELECT word, answer FROM orfo_dictation"
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
        return [Question(i[0], i[1], peer) for i in array]

