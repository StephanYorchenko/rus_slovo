class Art:
    def __init__(self):
        self.name = 'qwer'

    def tyrol(self):
        return f'----{self.name}-----'

    def main(self, peer):
        print('@')
        exec('print(peer)\nprint(self.tyrol())')


a = Art()
a.main('12')