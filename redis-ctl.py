import redis

name = ['hvj','cdvf','defe','vfvf','efd','adsd','vffed','wdww','ggfr','swdd','fff','jkhje','yudh','njndn']
value = ['7384','3221','8763','5453','8930','3922','8932','1483','9876','3283','9322','7843','8390','8745']

class Database:  
    def __init__(self):  
        self.host = '127.0.0.1'  
        self.port = 6379  

    def write(self,mony,deal_number):  
        try:  
            key = mony  
            val = deal_number  
            r = redis.StrictRedis(host=self.host,port=self.port)  
            r.set(key,val)  
        except Exception, exception:  
            print exception  

    def read(self,key):  
        try:  
            r = redis.StrictRedis(host=self.host,port=self.port)  
            value = r.get(key)  
            print value
        except Exception, exception:  
            print exception  

    def reads(self):
        try:
            r = redis.StrictRedis(host=self.host,port=self.port)
            value = r.keys()
            return value
        except Exception, exception:
            print exception

if __name__ == '__main__':  
    db = Database()
    for i in db.reads():
        #db.write(name[i],value[i])
        print i
#        db.read(i)
