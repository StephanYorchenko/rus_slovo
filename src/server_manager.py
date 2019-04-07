# Импортируем созданный нами класс Server
from server import Server
# Получаем из config.py наш api-token
from config import token


server1 = Server(token, 180661852, "server1")
# vk_api_token - API токен, который мы ранее создали
# 172998024 - id сообщества-бота
# "server1" - имя сервера

#server1.test()
server1.start()