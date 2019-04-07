# Импортируем созданный нами класс Server
from src.server import Server
# Получаем из config.py наш api-token
from src.config import token, group_id

server1 = Server(token, group_id, "server1")

server1.start()

