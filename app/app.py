#!flask/bin/python
import time
from flask import Flask, jsonify, request, Response
from redis import Redis
import redis, json
app = Flask(__name__)
#r = redis.StrictRedis(host='172.17.0.4', port=6379, db=0)
r = Redis(host='redis', port=6379)

'''
Basic REST-like API
'''

'''
Returns a json 'hello world' message. Logs the IP and timestamp. 
'''
@app.route('/v1/hello-world', methods=['GET'])
@app.route('/v1/hello-world/', methods=['GET'])
def hello_world():
    timestamp = int(time.time())
    ip = request.remote_addr
    r.sadd("logging-test", {'endpoint': 'hello-world', 'timestamp': timestamp, 'ip': ip})
    return jsonify({"message": "hello world"})

'''
For debugging: Deletes a log from the sequence. 
'''
@app.route('/v1/del', methods=['GET'])
def del_log():
    r.spop("logging-test")
    return "deleted"

'''
Returns a JSON formatted timestamp, IP and endpoint for all calls.
'''
@app.route('/v1/logs', methods=['GET'])
@app.route('/v1/logs/', methods=['GET'])
def logs():
    logset = []
    logging = r.smembers('logging-test')
    #Format into JSON string
    for log in logging:
        log= log.replace("'", '"')
        json_log = json.loads(log)
        logs={"ip": json_log["ip"], "timestamp": json_log["timestamp"]}
        endpoint = {"endpoint": json_log["endpoint"], "logs": logs}
        logset.append(endpoint)
    return jsonify({"logset": logset})

'''
Returns a JSON formatted timestamp and IP for all Hello World calls
'''
@app.route('/v1/<endpoint>/logs', methods=['GET'])
@app.route('/v1/<endpoint>/logs/', methods=['GET'])
def hello_world_logs(endpoint):
    logs = []
    logging = r.smembers('logging-test')
    #format into JSON string
    for log in logging:
        log= log.replace("'", '"')
        json_log = json.loads(log)
        if json_log["endpoint"]==endpoint:
            logs.append({"ip": json_log["ip"], "timestamp": json_log["timestamp"]})
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)