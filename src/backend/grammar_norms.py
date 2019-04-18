import json
import sqlite3
import random


class Question:
    def __init__(self, word, answer):
        self.word = word
        self.answer = answer
