# Rate limiter

A rate limiter based on Redis with a flask project example
The limiter will limit the requests number in a period of the website
Config the setting of the limiter by configFile.json, default be 100 requests per hour.

---

## Installation

### Install the libraries

```shell
$ pip install -r requirements.txt
```

### Download and Install Redis

Linux or MAC : https://redis.io/
Windows: https://github.com/dmajkic/redis/downloads

Get into your redis folder in shell, open the redis server

```shell
$ redis-server.exe
```

Open another shell window

```shell
$ redis-cli.exe
```

the db can be managed here

### Run the flask project

```shell
$ flask run
```

After running the project, the website can be accessed by the url specified in the shell.(default 127.0.0.1:5000)
The website will return 429 code and secondes you should wait if you reach the limit

### Rate limiter only

Copy the rateLimiter folder and configFile.json into your module folder.
As well as copy the class configLimiter() into your "config.py", or simply copy the config.py file if you do not have a config.py file

```python
from rateLimiter import Limiter

limit = Limiter(YOUR_FLASK_PROJECT_NAME)
```

## Config 

ALL settings are in configFile.json

example:

```json
{
"Redis" : {"REDIS_DB": 0,
            "REDIS_PORT": 6379,
            "REDIS_PASSWORD": "",
            "REDIS_HOST" : "127.0.0.1"},
"timeLimit" : {"REQUEST_ALLOWED" : 2, 
                "TIME_SEESION" : "10 seconds"}
}
```

Redis is for redis db setting
REQUEST_ALLOWED is the number of requests allowed in the period
TIME_SEESION is the time period, can be specified by "number" + "hour"/"hours"/"minute"/"minutes"/"second"/"seconds"

## Test

Copy limiterTest.py and configFileTest.json into your module folder.
Flush the redis db before testing

```shell
$ 127.0.0.1:6379 > flushdb
```

```shell
$ python limiterTest.py
```

Url are specified in configFileTest.json
