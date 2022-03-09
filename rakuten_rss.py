"""楽天RSS用モジュール
"""
from lib.ddeclient import DDEClient
import pandas as pd
import numpy as np
import time 
import traceback
"""
import traceback
try:
    do_stuff()
except Exception:
    print(traceback.format_exc())
"""

def ind():
	indexes = pd.read_csv("TOPIX_weight_jp.csv")

	indexes["コード"] = pd.to_numeric(indexes["コード"], errors='coerce')


	indexes_code = indexes["コード"].astype(int)
	
	for i,j in enumerate(indexes_code):
		indexes_code[i] = str(j) + ".T"
	indexes_code = np.array(indexes_code)
	indexes_code = indexes_code.flatten()

	for i,j in indexes.iterrows():
		# % を除去
		indexes.at[i, "TOPIXに占める個別銘柄のウェイト"] = indexes.loc[i, "TOPIXに占める個別銘柄のウェイト"]
	return [indexes_code, indexes]


def rss(item, k):
	dde_ware = []
	weights = []
	count = 0
	calc = 0
	
	# 以下csvファイルを都合いいようにエディット

	inde = ind()
	indexes_code, indexes = inde[0], inde[1] 
	
	# ddeを取得、格納、ウエイトをかけて計算
	
	for i,j in enumerate(indexes_code, start = k): 
		count += 1
		
		if k==2142 and count == 24:
			continue
		w = indexes["TOPIXに占める個別銘柄のウェイト"][i]
		"""
		if float(w) <= 0.001:
			count -= 1
			continue
		"""
		try:
			dde = DDEClient("rss", indexes_code[i])
		except Exception:
			with open('error.log', 'a') as f:
				traceback.print_exc(file=f)
			dele = False
			#time.sleep(0.1)
			continue
		else:
			dele = True
			dde_ware.append(dde)
		
		if True:	
			try:
				val = dde.request(item).decode("sjis")
			except Exception:
				val = 0
				
			df = pd.read_csv("TOPIX_weight_jp.csv")
			a, b = df["コード"], df["銘柄名"]
			with open('shares.txt', "a", encoding="utf-8", newline='') as f:
				string = str(a[i]) + " " + b[i]+"\n"
				f.write(string)
				pass
		
			if val == ' ':
				continue
			
			calc += float(val) * float(w)
			weights.append(w)
			if count >= 126:
				#print(i)
				break
			if k ==2142 and (count >= 39):
				break


		
				

	pocket = [calc, dde_ware, weights, k+count]
	
	
	return pocket
	

def rss2(item, dde_ware, weights):
	
	"""
	すでに使ったddeのデータで再度指数を計算
	"""
	
	calc = 0
	count = 0
	check_num = 0
	for i,j in enumerate(dde_ware):
		dde = dde_ware[i]
		double_check = False
		while True:	
			try:
				temp =dde.request(item).decode("sjis")
				
			except Exception:
				#print("ココ")
				pass
			else:
				if temp == " ":
					temp = 0
				with open('error.log', 'a') as f:
					try:
						calc += float(temp) * float(weights[i] )
					except:
						traceback.print_exc(file=f)
				break
		
		count += 1
		if count >= 126:
			break	
		else:
			continue
	return calc


def rss_dict(code, *args):
	"""
	楽天RSSから辞書形式で情報を取り出す(複数の詳細情報問い合わせ可）
	Parameters
	----------
	code : str
	args : *str
	Returns
	-------
	dict
	Examples
	----------
	>>>rss_dict('9502.T', '始値','銘柄名称','現在値')
	{'始値': '1739.50', '現在値': '1661.50', '銘柄名称': '中部電力'}
	"""

	dde = DDEClient("rss", str(code))

	
	values ={}
	element = []

	res = {}
	try:
		for item in args:
			res[item] = dde.request(item).decode('sjis').strip()
	except:
		print('fail: code@', code)
		res = {}
	finally:
		dde.__del__()
	return res

def fetch_open(code):
	""" 始値を返す（SQ計算用に関数切り出し,入力int）
	Parameters
	----------
	code : int
	Examples
	---------
	>>> fetch_open(9551)
	50050
	"""

	return float(rss(str(code) + '.T', '始値'))