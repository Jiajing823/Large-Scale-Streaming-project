__author__ = "Wenjie Chen"
__email__ = "wc2685@columbia.edu"

# from faker import Faker
import faker
import random
import datetime
import uuid
import redis

f1=faker.Factory
rds = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)   # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
rds_type = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

class data_generator:
    """
    A complete CRD
    """
    def __init__(self,ID=None,callednumber=None,teltime=None,teltype=None,charge=None,result=None,type=None):
        self.ID=self.gen_ID()
        self.callednumber=self.gen_callednumber()
        self.teltime=self.gen_teltime()
        self.teltype=self.gen_teltype()
        self.charge=self.gen_charge()
        self.result=self.gen_result()
        self.type=self.gen_type()
        if ID is not None: self.ID=ID
        if callednumber is not None: self.callednumber = callednumber
        if teltime is not None: self.telltime = teltime
        if teltype is not None: self.teltype = teltype
        if charge is not None: self.charge = charge
        if result is not None: self.result = result
        if type is not None: self.type=type
        self.output_redis_2()

    def __str__(self):
        data = str(self.ID)+"|"\
               +str(self.callednumber)+"|"+str(self.teltime)+"|"\
               +str(self.teltype)+"|"+str(self.charge)+"|"+str(self.result)
        return data

    def gen_ID(self):
        return uuid.uuid1()

    def gen_callednumber(self):
        callednumber=f1.create()
        return callednumber.phone_number()

    def gen_teltime(self):
        time=f1.create()
        starttime=time.iso8601(tzinfo=None)
        timedelta=random.randint(0,60*1000)
        return starttime+"|"+str(timedelta)

    def gen_teltype(self):
        if(random.randint(0,1)==0):
            return "SMS"
        else:
            return "VOICE"

    def gen_charge(self):
        return random.random()

    def gen_result(self):
        r=random.randint(0,2)
        if(r==0):
            return "AWNSERED"
        elif (r==1):
            return "BUSY"
        else:
            return "VOICE"

    def gen_type(self):
        r=random.randint(0,5)
        type={
            0: "Business",
            1: "Agency",
            2: "Education",
            3: "Scam",
            4: "Business",
            5: "AD"
        }
        return type.get(r)

    def output_redis_2(self):
        rds_type.set(str(self.callednumber),str(self.type))


class people:
    """
    A unique people with 1-5 telephones makes several calls
    """
    def __init__(self,ID=None,callnumber=None,calltimes=None):
        self.ID=self.gen_ID()
        self.callnumber=self.gen_callnumber()
        self.calltimes=self.gen_calltimes()
        if ID is not None: self.ID=ID
        if callnumber is not None: self.callnumber = callnumber
        if calltimes is not None: self.calltimes=calltimes
        self.data=[]
        self.gen_data()


    def __str__(self):
        fuldata=""
        for i in range(self.calltimes):
            tempdata=str(self.ID)+"|"+str(self.callnumber)+"|"\
                     +(str(self.data[i]))
            self.output_redis_1(self.data[i].ID,tempdata)
            fuldata+=tempdata+"\n"
        return fuldata

    def gen_ID(self):
        return uuid.uuid1()

    def gen_callnumber(self):
        callnumber=f1.create()
        return callnumber.phone_number()

    def gen_calltimes(self):
        return random.randint(1,5)

    def gen_data(self):
        for i in range(self.calltimes):
            data_generator_temp=data_generator()
            self.data.append(data_generator_temp)

    def output_redis_1(self,ID, tempdata):
        rds.set(str(ID),str(tempdata))




# test generate
print("##############test generate###########################")
d1=data_generator(ID=1)
d2=data_generator()
print(d1)
print(d2)
print(d1.type)
p1=people()
# test people
print("##############test people###########################")
print(p1)
# test output_redis
print("##############test output_redis#######################")
print(rds[str(p1.data[0].ID)])
# test iterate redis data
print("##############test iterate redis data#################")
keys=rds.keys()
print(keys)
# test iterate redis_type data
print("##############test iterate redis_type data############")
keys_type=rds_type.keys()
print(keys_type)