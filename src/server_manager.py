# Импортируем созданный нами класс Server
from server import Server
# Получаем из config.py наш api-token
from config import token, group_id

server1 = Server(token, group_id, "server1")

server1.start()

