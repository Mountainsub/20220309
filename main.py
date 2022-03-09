import subprocess
import pandas as pd
import numpy as np
import time 
import sys
import os
import csv
import random
import math
import traceback 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from request.rakuten_rss import rss2 
from lib.ddeclient import DDEClient
import datetime

class Function:
    #並列処理
    def get_lines(cmd):
        '''
        :param cmd: str 実行するコマンド.
        :rtype: generator
        :return: 標準出力 (行毎).
        リアルタイムにファイルの出力を取得error
        '''
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        while True:
            try:
                line = proc.stdout.readline()
            except:
                with open('error.log', 'a') as f:
                    traceback.print_exc(file=f)
            #print(line)
            if line:
                yield line
            if not line and proc.poll() is not None:
                break
        return


    def calculation(dde_ware, indexes_weight):

        calc = rss2("現在値", dde_ware, indexes_weight)
                
        return calc

if __name__ == '__main__':  
    # コマンドライン引数を取得
    args = sys.argv
    # count番目からcount+125番目までデータの総計を出す
    
    
    # コマンドライン引数の１番目で書き込みか読み取りかを選択
    num = args[1]
    temp = 0
    
    if int(num) == 0: #　書き込み
        temp = 0
        box = [0, 245, 603, 842, 1096, 1331, 1584, 1821, 2052]
        
       
        
        count =  box[int(args[2])]
        
        for line in Function.get_lines(cmd='python main2.py ' + str(count)): #+str(init_box[int(args[2])])): # ファイル読み込み　第一引数はスタートナンバー                
            # python main2.pyは計算して書き込みを行うコマンドです。
            string = "file_"+ str(int(args[2])) + ".txt"
            #print(line)
            try:
                f = open(string, 'w') #　上書きモード ,改行なし
                temp = line.decode('sjis')
                # print(temp)
                temp.replace('\n', "")
                temp.replace('\r', "")
                f.write(temp)
                #print(temp)
                f.close() 
                
            except Exception:
                print("error")

            #print("OK") 
    else: #　読み込み
        a = 0
        while True:
            proc = subprocess.Popen('python main3.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = proc.communicate()[0].decode('sjis') # 出力結果を取得
            dt = datetime.datetime.today() # 今日の日時
            
            try:
                with open("Data_20220307.txt","a", newline="") as f:
                    f.write(result.rstrip("\n"))
                #print(result)
                
            except Exception:
                print(traceback.format_exc())
                pass
            
            time.sleep(10)
            a += 1
    



