#!/usr/bin/python
# -*- coding: utf-8 -*-  
from web import Wootalk
import time,os

w = Wootalk()
while 1:
	w.setUp(30) # 30秒無人回應，自動離開換人/驗證時間
	print w.launch()
