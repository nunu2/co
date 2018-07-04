from RAProtect import LineBot
import threading
import json, codecs
    
def login(resp, auth):
	bot = LineBot(resp, auth)

threading.Thread(target=login, args=("1","token disini")).start()
threading.Thread(target=login, args=("2","token disini")).start()
threading.Thread(target=login, args=("3","token disini")).start()
threading.Thread(target=login, args=("4","token disini")).start()
threading.Thread(target=login, args=("5","token disini")).start()

print('Login Berhasil')
