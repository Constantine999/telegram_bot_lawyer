import multiprocessing
import time

from main_tm_botbot import start_bot_aiogram
from main_tm_userbot import start_bot_pyrogram

pr1 = multiprocessing.Process(target=start_bot_pyrogram, name="prc-1")
pr2 = multiprocessing.Process(target=start_bot_aiogram, name="prc-2")

if __name__ == "__main__":
    # multiprocessing.set_start_method('spawn')
    pr1.start()
    time.sleep(1)
    pr2.start()
