# -*- coding: utf-8 -*-

import random
import sqlite3
import json


class OrthographyQuestion:
    def __init__(self, type_task, **kwargs):
        self.peer = kwargs['peer']
        if type_task == 1:
            self.answer = kwargs['word']
            self.buttons = [kwargs['answer'], kwargs['wrong']]
            random.shuffle(self.answer)

    def check(self, answer):
        return self.answer == answer

    def get_json_keyboard(self):
        result_dict = {'one_time': False,
                       'buttons': [
                           [
                               {
                                   "action": {
                                       "type": "text",
                                       "label": self.buttons[0]
                                   },
                                   "color": "default"
                               }
                           ],
                           [
                               {
                                   "action": {
                                       "type": "text",
                                       "label": self.buttons[1]
                                   },
                                   "color": "default"
                               }
                           ],
                           [
                               {
                                   'action': {
                                       'type': 'text',
                                       'label': 'Стоп'
                                   },
                                   'color': 'negative'
                               }
                           ]
                       ]}
        with open(f'keyboards/{self.peer}.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result_dict, indent=4, ensure_ascii=False))


class OrthographyTask:
    def __init__(self, peer, type_task):
        self.peer = peer
        self.queue = self.create_task(type_task)
        self.current = 0
        self.right = 0

    def create_task(self, type_task, peer):
        return [OrthographyQuestion(type_task=type_task, peer=peer, word=word, wrong=wrong, answer=answer)
                for word, answer, wrong in self.select_task(type_task)]

    @staticmethod
    def select_task(type_task):
        con = sqlite3.connect(r'src/rus_slovo.db')
        sql = f"SELECT word, answer, wrong FROM orthography WHERE type_task={type_task}"
        cur = con.cursor()
        c = list(cur.execute(sql))
        random.shuffle(c)
        cur.fetchall()
        cur.close()
        con.close()
        return c[:10]


if __name__ == '__main__':
    a = OrthographyQuestion(1, word='предыстория', wrong='предистория')
