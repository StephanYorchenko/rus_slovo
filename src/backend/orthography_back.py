# -*- coding: utf-8 -*-

import random
import sqlite3
import json


class OrthographyQuestion:
    def __init__(self, **kwargs):
        # TODO: add type_task checker
        self.peer = kwargs['peer']
        self.word = kwargs['word']
        self.answer = kwargs['answer']
        self.buttons = [kwargs['answer'], kwargs['wrong']]
        random.shuffle(self.buttons)

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
    def __init__(self, peer):
        # TODO: add type_task arg
        self.peer = peer
        self.queue = self.create_task(peer)
        self.current_task = 0
        self.right = 0

    def create_task(self, peer):
        return [OrthographyQuestion(peer=peer, word=word, wrong=wrong, answer=answer)
                for word, answer, wrong in self.select_task()]

    @staticmethod
    def select_task():
        con = sqlite3.connect(r'src/rus_slovo.db')
        sql = f"SELECT word, answer, wrong FROM orthography WHERE type_task=1"
        # TODO: check what is wrong with select where type is given???
        cur = con.cursor()
        c = list(cur.execute(sql))
        random.shuffle(c)
        cur.fetchall()
        cur.close()
        con.close()
        return c[:10]