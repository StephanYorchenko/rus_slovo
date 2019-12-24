# -*- coding: utf-8 -*-

import json
import random

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

    def get_json_keyboard(self, exit_button=False):
        result_dict = {'one_time': False,
                       'buttons': []}
        for i in self.list_answers:
            print(i)
            answer_button = [{
                "action": {"type": "text", "label": i},
                "color": "default"
            }]
            result_dict['buttons'].append(answer_button)
        if exit_button:
            result_dict['buttons'].append([{'action': {'type': 'text', 'label': 'Стоп'}, 'color': 'negative'}])
        with open(f'keyboards/{self.peer}.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result_dict, indent=4, ensure_ascii=False))

    def check(self, answer):
        # TODO: remove crutch!
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
        data = ss.DataSource(r'src/rus_slovo.db')
        result = data.sql_select('orfo_dictation', ['answer'], {'index_task': index})
        random.shuffle(result)
        return result[:32]

    @staticmethod
    def question_creator(array, peer):
        return [Question(i[0], peer) for i in array]