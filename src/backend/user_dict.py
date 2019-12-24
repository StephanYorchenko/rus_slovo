from src.backend.sql_selections import DataSource


class UserDict(dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, peer_id):
        if peer_id not in self.keys():
            self[peer_id] = [-1, '', 0, 0]
        return super().__getitem__(peer_id)

    def __str__(self):
        return f'<----{len(self.keys())} records---->'

    def get_next_status(self, peer, button_name):
        """
        Getting new users position in menu
        :param peer: peer of user, takes from vk_api
        :param button_name: name of clicked button from current UI
        :change: current position of user in UI
        """
        data_base = DataSource(r'src/controllers')
        self[peer][0] = data_base.sql_select(
            'Buttons',
            ['next_stat'],
            {'current_stat': self[peer][0], 'button_name': button_name}
        )
