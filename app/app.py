#!flask/bin/python
import time
from flask import Flask, jsonify, request
from redis import Redis
import redis, json
app = Flask(__name__)
r = redis.StrictRedis(host='172.17.0.4', port=6379, db=0)
#r = Redis(host='redis', port=6379)

@app.route('/v1/hello-world', methods=['GET'])
@app.route('/v1/hello-world/', methods=['GET'])
def hello_world():
    timestamp = int(time.time())
    ip = request.remote_addr
    r.sadd("logging-test", {'endpoint': 'hello-world', 'timestamp': timestamp, 'ip': ip})
    return jsonify({"message": "hello world"})

@app.route('/v1/logs', methods=['GET'])
@app.route('/v1/logs/', methods=['GET'])
def logs():
    logset = []
    logging = r.smembers('logging-test')
    for log in logging:
        log= log.replace("'", '"')
        json_log = json.loads(log)
        logs={"ip": json_log["ip"], "timestamp": json_log["timestamp"]}
        endpoint = {"endpoint": json_log["endpoint"], "logs": logs}
        logset.append(endpoint)
    return jsonify({"logset": logset})

@app.route('/v1/hello-world/logs', methods=['GET'])
@app.route('/v1/hello-world/logs/', methods=['GET'])
def hello_world_logs():
    logs = []
    logging = r.smembers('logging-test')
    for log in logging:
        log= log.replace("'", '"')
        json_log = json.loads(log)
        if json_log["endpoint"]=="hello-world":
            logs.append({"ip": json_log["ip"], "timestamp": json_log["timestamp"]})
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)