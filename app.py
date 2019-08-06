from src.server import Server
from src.config import token, group_id

server1 = Server(token, group_id)

server1.start()