
import pandas as pd
import numpy as np
import time 
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))




if __name__ == "__main__":
    t1 = time.time()
    s = 0
    args = sys.argv 
    count = 0
    """
    if args[1] == "T":
        count = 0
        temp = 0
    else:
        count = 100
        temp=100
    """
    while count <= 9: 
        count += 1
        if True:
            with open('file_'+ str(count) + '.txt', 'r') as f:                           
                try: # 正常に取得するまでループするようになっている
                    a = f.readline()
                    a.rstrip("\n")
                except:
                    with open('f.txt', 'w') as f:
                        f.write("file_"+ str(count)+ ".txt\n")
                    continue
                else:
                    try:
                        float(a)
                    except:
                        pass
                    else:
                        s += float(a)
    print(s)