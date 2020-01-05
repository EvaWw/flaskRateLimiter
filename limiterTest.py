import os
import unittest
import tempfile
import json
import rateLimiter
import requests
from config import configLimiter

#######################################
#Load the config from config files
#Make sure that you flush the redis db
#######################################

_config = configLimiter()

with open('configFileTest.json') as config_file:
    data = json.load(config_file)

Url = data["Url"]

#########################################################
# Test case for the limiter
# send Get requests to the Url _config.requests times,
# and check the status code
#########################################################
class limiterTester(unittest.TestCase):
    def testLimiter(self): 
        for i in range(_config.requests):
            rq = requests.get(url=Url)
            self.assertNotEqual(rq.status_code, 429)
        rq = requests.get(url=Url)
        self.assertEqual(rq.status_code,429) 

###################################################
#run the unittest
##################################################
if __name__=="__main__":  
    unittest.main() 
