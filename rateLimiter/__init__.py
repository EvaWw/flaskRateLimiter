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
        self._config = configLimiter()
        self.REQUEST_ALLOWED = self._config.requests
        self.TIME_SEESION =self._config.timeSession
        self.FREELIST = self._config.freeList
        self.redisDB = redis.StrictRedis(host=self._config.host, port=self._config.port, password=self._config.passwrd, db=self._config.db, socket_timeout=30)
        @app.errorhandler(429)
        def handle_exception(e):
            """Return a HTML page for HTTP error 429."""
            self.retryTime = self.redisDB.ttl(request.remote_addr) #get the retry-time from redis
            self.description = "Rate limit exceeded. Try again in " + str(self.retryTime) + " seconds"
            return render_template("error.html", description = self.description, code = e.code, name = e.name), 429

        @app.before_request  
        def before_request():
            """access the db and evaluate whether it reach the limit"""
            self.ip = request.remote_addr
            if self.ip not in self.FREELIST:
                self.ip_count = self.redisDB.get(self.ip)
                print("ip: %s, ip_count: %s" % (self.ip, self.ip_count))
                if not self.ip_count:
                    self.redisDB.set(self.ip, 1,ex=self.TIME_SEESION) # set new key, make it be expired in the period
                else:
                    self.redisDB.incr(self.ip)  # increase the count of the ip
                    if int(self.ip_count) >= self.REQUEST_ALLOWED:
                        return abort(429) #if exceed the limit, raise 429 error
