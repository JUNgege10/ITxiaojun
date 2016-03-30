#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
import commands
import psutil

"""
更新程序守护
"""

sleep = "sleeping"
run = "running"
(status,ret) = commands.getstatusoutput("ps aux | grep -v grep | grep /tools/download/upgrade_download | awk '{print $2}')
(status,ret2) = commands.getstatusoutput("ps aux | grep -v grep | grep /tools/download2/upgrade_download | awk '{print $2}')

try:
   p = psutil.Process(int(ret))
   ITxiaoshou = p.exe()
   print p.exe()
   if os.path.exists(ITxiaoshou):
      if p.status() == sleep or run:
         print "process is already run"
      else:
         os.system("root /bin/bash ITxiaoshou")
   else:
      print "no such dir"
   p = psutil.Process(int(ret2))
   ITxiaopang = p.exe()
   print p.exe()
   if os.path.exists(ITxiopang):
      if p.status() == sleep or run:
         print "process2 is already run"
      else:
         os.system("root /bin/bash ITxiaopang")
   else:
      print "no such dir2"
except Exception,e:
   print ("program error: %s" % str(e))
