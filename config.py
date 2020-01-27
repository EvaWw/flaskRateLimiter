import json

class configLimiter(object):
    """Parser the config file and get the value of config"""
    def __init__(self):
        with open('configFile.json') as config_file:
            data = json.load(config_file)

        self.db = data['Redis']['REDIS_DB']
        self.host = data['Redis']['REDIS_HOST']
        self.port = data['Redis']['REDIS_PORT']
        self.passwrd = data['Redis']['REDIS_PASSWORD']
        self.requests = data['timeLimit']['REQUEST_ALLOWED']
        self.freeList = data['freeList']
        time = data['timeLimit']['TIME_SEESION']
        timeSplit = time.split()
        switcher = {
            "hour" : 3600,
            "hours" : 3600,
            "minute" : 60,
            "minutes" : 60,
            "second" : 1,
            "seconds" : 1
        }
        self.timeSession = int(timeSplit[0]) * switcher.get(timeSplit[1], 1)
        
if __name__ == "__main__":
    con =  configLimiter()
    print(con.timeSession)