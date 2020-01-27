import os
import unittest
import tempfile
import json
from application import Limiter
import requests
from config import configLimiter
import random

#######################################
#Load the config from config files
#Make sure that you flush the redis db
#######################################

redisDB = Limiter.redisDB
_config = configLimiter()
limitRq = _config.requests

print(_config.freeList)

with open('configFileTest.json') as config_file:
    data = json.load(config_file)

Url = data["Url"]
IP = data['IP']

#########################################################
# Test case for the limiter
# send Get requests to the Url _config.requests times,
# and check the status code
#########################################################
class limiterTester(unittest.TestCase):
    def testAccess(self):
        """Test whether the website can be accessed when not exceed the limit"""
        redisDB.set(IP,random.randint(1,limitRq-2))
        self.rq = requests.get(url = Url)
        self.assertNotEqual(self.rq.status_code,429)

    def testLimiter(self): 
        """Test rate limiter"""
        redisDB.set(IP,limitRq)
        self.rq = requests.get(url=Url)
        self.assertEqual(self.rq.status_code,429) 

    def testFreeList(self):
        """Test free IP list"""
        for ip in _config.freeList:
            self.proxy = {"http" : "http://"+ip, "https" : "https://" + ip}
            redisDB.set(ip,limitRq)
            self.rq = requests.get(url = Url, proxies=self.proxy)
            self.assertNotEqual(self.rq.status_code,429)
    


###################################################
#run the unittest
##################################################
if __name__=="__main__":  
    unittest.main() 
