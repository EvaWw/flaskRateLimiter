from flask import Flask, jsonify, request,Response, abort, render_template
from flask import render_template
from config import configLimiter
import redis

__version__ = "1.0.0"

###########################################
#Class of limiter
#Limit requests by Redis db

#If exceed the limit, return 429 
#and go to error.html
##########################################
class Limiter(object):
    """Limit requests number by remote address"""
    def __init__(self, app):
        #set up redis db
        _config = configLimiter()
        self.REDIS_DB = _config.db
        self.REDIS_HOST = _config.host
        self.REDIS_PORT = _config.port
        self.REDIS_PASSWORD = _config.passwrd
        self.REQUEST_ALLOWED = _config.requests
        self.TIME_SEESION = _config.timeSession
        r = redis.StrictRedis(host=self.REDIS_HOST, port=self.REDIS_PORT, password=self.REDIS_PASSWORD, db=self.REDIS_DB, socket_timeout=30)
        @app.errorhandler(429)
        def handle_exception(e):
            """Return a HTML page for HTTP error 429."""
            n = r.ttl(request.remote_addr) #get the retry-time from redis
            description = "Rate limit exceeded. Try again in " + str(n) + " seconds"
            return render_template("error.html", description = description, code = e.code, name = e.name), 429

        @app.before_request  
        def before_request():
            """access the db and evaluate whether it reach the limit"""
            ip = request.remote_addr
            ip_count = r.get(ip)
            print("ip: %s, ip_count: %s" % (ip, ip_count))
            if not ip_count:
                r.set(ip, 1,ex=self.TIME_SEESION) # set new key, make it be expired in the period
            else:
                r.incr(ip)  # increase the count of the ip
                if int(ip_count) >= self.REQUEST_ALLOWED:
                    return abort(429) #if exceed the limit, raise 429 error
