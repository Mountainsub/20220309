
import pandas as pd
import numpy as np
import time 
import sys
import os
import random
import math
import datetime
from request.rakuten_rss import rss , rss2 
from lib.ddeclient import DDEClient
  



def calculation(dde_ware, indexes_weight, num):
    calc = rss2("現在値", dde_ware, indexes_weight)
    return calc 

if __name__ == '__main__':
    args = sys.argv # コマンドライン引数として開始地点のインデックスを数字で入力する
    #print(int(args[1]))
    count = 0
    #init = float(args[2])
    t1 = time.time()
    if True:
        array =  rss("現在値",int(args[1]))
        dde_ware, weight = array[1], array[2]
            
        calc = array[0]
        print(calc)
    """
    if count ==0:
        if calc - init > 6 or init - calc > 6:
            calc = init
    """
    print(len(dde_ware))
    firststep = True
    while True:
        if firststep:
            ex = 0
            #firststep = False
        if args[1] == 1512 or 1890:
            print(calc)
            continue   
        count += 1
        try:
            temp = calculation(dde_ware, weight,  calc)
        except Exception:
            ex = calc
        else:
            if not firststep:
                calc += temp - ex
                firststep = False
            else:
                pass
            print(calc)
            ex = temp



        t2 = time.time()

        if t2 - t1 > 0.1:
            number = random.uniform(0.005, 0.015)
            time.sleep(number)
            t1 = time.time()
        
            try:
                calc = ex
            except:
                calc = 0
            #continue               
