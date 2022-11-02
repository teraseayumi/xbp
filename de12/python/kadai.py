import ctypes
import os
import glob
import time
import threading
import random
import codecs
import sys

#import→外からデータを取り込む
#ctypes→外部関数ライブラリ（他の人が作った機能を使えるようにしたもの？）を使うのを可能にする。
#os→オペレーティングシステム、ソフトウェアとハードウェアを仲介してコンピュータを制御する。
#glob→特定の条件にマッチするファイルを取得してプログラム内で使うのを可能にする。
#threading→マルチスレッドプログラミング（アプリのタスクを複数のスレッドに分けて並行処理する方式）を可能にする。
#codecs→データの符号化や圧縮・解凍
#sys→sysという拡張子を使うのを可能にする？

INTERVAL_SEC = 3
#壁紙が変わるまでの秒数を指定


class BgSlider():#classによってデータを入れる領域と処理の仕方を書く領域を設ける。
    def __init__(self):
        self.index = 0
        self.directory = None

    def setup(self):
        global off
        with codecs.open(r'C:\Users\あゆみ\mygit\xbp\de12\images', 'r', 'utf-8') as f:
            lines = f.readlines()
            self.directory = lines[0].strip()
            #好きな画像をファイルとして取り込む
            #ここがうまくいかない！

    def worker(self):
        path = self.directory + r'\*.jpg'
        path.replace('\\\\', '\\')
        files = glob.glob(path)
        # [print(file) for file in files] # ファイルリストをコンソールにまとめて出力するときに使う
        # file = files[random.randint(0, len(files) - 1)] # ランダムにしたい場合はここを使う
        files = sorted(files) # 順番に表示したい場合はここを使う
        file = files[self.index] # 順番に表示したい場合はここを使う
        print(file)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)
        if self.index == len(files) - 1:
            self.index = 0
        else:
            self.index += 1
        time.sleep(INTERVAL_SEC)

    def schedule(self, interval, f, wait=True):
        base_time = time.time()
        next_time = 0
        while True:#while→指定した条件が真の間、処理を繰り返し実行
            try:
                t = threading.Thread(target=f)
                t.start()
                if wait:
                    t.join()
                next_time = ((base_time - time.time()) % interval) or interval
                time.sleep(next_time)
            except KeyboardInterrupt:
                exit()


if __name__ == "__main__":
    try:
        bg = BgSlider()
        bg.setup()
        bg.schedule(INTERVAL_SEC, bg.worker, False)
    finally:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, None, 0)