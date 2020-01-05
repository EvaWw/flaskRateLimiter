
from flask import Flask
from rateLimiter import Limiter
import json

app = Flask(__name__)

########################################################################################################
#Call the limiter
#param is the flask app only
#Set configuration param in configFile.json
#TIME_SESSION: time period, format can be "number" + "hour"/"hours"/"minute"/"minutes"/"second"/"seconds"
#REQUESTS_ALLOWED: //number of the requests allowed for a reqester
########################################################################################################
Limiter = Limiter(app) 


from application import routes


