# -*- coding: utf-8 -*-

import random
import json
import sqlite3



class Question:

    def __init__(self):
        self.dict_words = self.selector('orfo_dictation')
        self.quest = random.choice(list(self.dict_words.keys()))
        self.answer = self.dict_words[self.quest]
        self.ask = self.reformat_word(self.quest)
        self.get_json_keyboard(self.get_list_answers(), True)

    @staticmethod
    def reformat_word(word, k=None):
        if k is None:
            k = random.choice([i for i in range(len(word)) if word[i] in list('ёуеыаоэяию')])
        word = list(word)
        word[k] = word[k].upper()
        return ''.join(word)

    def task(self, answer):
        print(self.answer == answer)
        return answer == self.answer

    def get_list_answers(self):
        keys = [i for i in range(len(self.quest)) if self.quest[i] in list('ёуеыаоэяию')]
        res_list = [self.reformat_word(self.quest, x) for x in keys]
        random.shuffle(res_list)
        return res_list

    @staticmethod
    def get_json_keyboard(list_answers, exit_but=False):
        result_dict = {'one_time': False,
                       'buttons': []}
        for i in list_answers:
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
                    'action':{
                        'type': 'text',
                        'label': 'Стоп'
                        },
                    'color':'default'
                    }
                    ]
            result_dict['buttons'].append(exit)
        with open('src/keyboard_test.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result_dict, indent=4, ensure_ascii=False))

    @staticmethod
    def selector(table_name):
        con = sqlite3.connect(r'src/rus_slovo.db')
        sql = f'SELECT * FROM {table_name}'
        cur = con.cursor()
        c = list(cur.execute(sql))
        cur.fetchall()
        cur.close()
        con.close()
        return {x[1]: x[2] for x in c}

