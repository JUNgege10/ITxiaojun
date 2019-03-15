#! /usr/bin/env python
# --*-- coding:utf-8 --*--

#取数据库里所有ip，做fping操作，判断返回值是否为alive，否则触发报警，支持恢复操作

import os
from os import system
import urllib2
import MySQLdb
import commands
from commands import getoutput
import sys
import subprocess
import yaml
import socket
import time
import urllib
import urllib2
import json

name_list = []
name_lists = []
def confload():
    global conf
    conf_path = '/opt/rh/iplist.conf'
    if os.path.exists(conf_path):
        conf = yaml.load(open(conf_path))

def get_count(group):
    confload()
    for i in conf.get('ip_conf'):
        m = []
        m = i.get('%s' % group,None)
        return m

def get_list():
    conn = MySQLdb.connect(host='10.80.2.156',user='open',passwd='jjker1314',db='ass',charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute("select server_wai_ip from server_info where server_wai_ip <> '';")
    ip_list = []
    results = cursor.fetchall()
    result=list(results)
    for r in result:
        ip_list.append(('%s' % r))
    return ip_list
    conn.close()

def get_info(info):
    conn = MySQLdb.connect(host='10.80.2.156',user='open',passwd='jjker1314',db='ass',charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute("select server_name from server_info where server_wai_ip = '%s';" % info)
    ip_list = []
    results = cursor.fetchall()
    result=list(results)
    for r in result:
        ip_list.append(('%s' % r))
    return ", ".join(ip_list)
    conn.close()

def iplist():
    set1 = set(get_count('ip'))
    set2 = set(get_list())
    return list(set1 ^ set2) + get_count('LB')

def alarm(ip,la):
    post_url = 'http://ass.51.com/sms/sms1.php'
    postData  = {'problem':'from BJ-174 Network Abnormal','status':'%s' % la,'host':'%s::%s' % (get_info(ip),ip)}
    req = urllib2.Request(post_url)
    response = urllib2.urlopen(req,urllib.urlencode(postData))
    print response.read()

def files(ip):
    f = file("/opt/rh/iplist.txt","a+")
    f.writelines("%s\n" % ip)
    f.close()

def ofo():
    mylist = []
    mylist = getoutput("cat /opt/rh/iplist.txt")
    mylists = mylist.split('\n')
    myset = list(set(mylists))  #myset是另外一个列表，里面的内容是mylist里面的无重复 项
    for item in myset:
        if int(mylist.count(item)) == int(1):
            print("the %s has found %s" %(item,mylist.count(item)))
            alarm(item,'problem')
        else:                                                                                    
            print("the %s has founds %s" %(item,mylist.count(item)))


def run():
    for i in iplist():
        met = getoutput("/usr/local/sbin/fping %s | awk '{print $1}'" % i)
        ret = getoutput("/usr/local/sbin/fping %s | awk '{print $3}'" % i)
        if ret != 'alive':
            name_list.append(('%s' % met))
        else:                                                                                    
            print "ip-%s status is %s" % (met,ret) 

def runer():
    run()
    time.sleep(10)
    for i in name_list:
        met = getoutput("/usr/local/sbin/fping %s | awk '{print $1}'" % i)
        ret = getoutput("/usr/local/sbin/fping %s | awk '{print $3}'" % i)
        if ret != 'alive':
             print "ip-%s status is %s" % (met,ret)
             files(i)
        else:
             print "ip-%s status is %s" % (met,ret)
 
def runers():
    runer()
    met = []
    met = getoutput("cat /opt/rh/iplist.txt")
    if met != "":
        ofo()
        mes = met.split('\n')
        res = list(set(mes))
        for i in res:
            ret = getoutput("/usr/local/sbin/fping %s | awk '{print $3}'" % i)
            if ret == 'alive':
                alarm(i,"OK")
                os.system("rm -rf /opt/rh/iplist.txt")
            else:
               print "ip-%s status3 is %s" % (i,ret)
    else:
        print "file is empty!"

if __name__ == '__main__':
    try:
        if os.path.exists("/opt/rh/iplist.txt"):
            runers()
        else:
            system("touch /opt/rh/iplist.txt")
            runers()
    except Exception,e:
        print  e
