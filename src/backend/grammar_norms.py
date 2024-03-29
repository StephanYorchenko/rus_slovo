import json
import random

import src.backend.sql_selections as ss


class GrammarQuestion:
    def __init__(self, word, answer_right, answer_wrong, quest, peer):
        self.word = word
        self.answer_right = answer_right
        self.answer_wrong = answer_wrong
        self.quest = quest
        self.peer = peer

    def get_json_keyboard(self):
        answers = [self.answer_wrong, self.answer_right]
        random.shuffle(answers)
        result_dict = {'one_time': False,
                       'buttons': [
                           [
                               {
                                   "action": {
                                       "type": "text",
                                       "label": answers[0]
                                   },
                                   "color": "default"
                               }
                           ],
                           [
                               {
                                   "action": {
                                       "type": "text",
                                       "label": answers[1]
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

    def check(self, answer):
        return self.answer_right == answer

    def __str__(self):
        return f'<--- {self.word}/{self.answer_right} --->'


class GrammarTask:
    def __init__(self, peer):
        self.peer = peer
        self.current_task = 0
        self.right = 0
        self.queque = self.task_creator(self.selector(), peer)

    @staticmethod
    def selector():
        data = ss.DataSource(r'src/rus_slovo.db')
        result = data.sql_select('Grammatical_Norms', ['word1', 'type_word2', 'answer_right', 'answer_wrong'])
        random.shuffle(result)
        return result[:16]

    @staticmethod
    def task_creator(array, peer):
        return [GrammarQuestion(item[0],
                                item[2],
                                item[3],
                                item[1],
                                peer) for item in array]
