# -*- coding: utf-8 -*-

import random
import json

import src.backend.sql_selections as ss


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
        with open("src/backend/orth.json", "r", encoding="utf-8") as keyboard_file:
            result_dict = json.loads(keyboard_file.read())
            result_dict['buttons'][0][0]["action"]["label"] = self.buttons[0]
            result_dict['buttons'][1][0]["action"]["label"] = self.buttons[1]

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
        data = ss.DataSource(r'src/rus_slovo.db')
        result = data.sql_select('orthography', ['word', 'answer', 'wrong'], {'type_task': 1})
        random.shuffle(result)
        return result[:10]

