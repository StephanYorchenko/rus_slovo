# -*- coding: utf-8 -*-

import random
import json
import sqlite3



class Question:

    def __init__(self, word, answer):
        self.word = word
        self.answer = answer

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
                    'color':'negative'
                    }
                    ]
            result_dict['buttons'].append(exit)
        with open('keyboards/keyboard_test.json', 'w', encoding='UTF-8') as f:
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

