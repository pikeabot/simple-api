#!flask/bin/python
import time
from flask import Flask, jsonify, request
from redis import Redis
import redis
app = Flask(__name__)
#r = redis.StrictRedis(host='172.17.0.3', port=6379, db=0)
r = Redis(host='redis', port=6379)

@app.route('/v1/hello-world', methods=['GET'])
def hello_world():
    timestamp = int(time.time())
    ip = request.remote_addr
    r.set('ip', ip)
    r.set('timestamp', timestamp)
    return jsonify({'message': "hello world"})

@app.route('/v1/logs', methods=['GET'])
def logs():
    try:
        logs=[{"ip": r.get('ip'), "timestamp": r.get("timestamp")}]
    except:
        logs=[{"ip": "", "timestamp": ""}]
    endpoint = [{"endpoint": "hello-world", "logs": logs}]
    return jsonify({"logset": endpoint})

@app.route('/v1/hello-world/logs', methods=['GET'])
def hello_world_logs():
    try:
        logs=[{"ip": r.get('ip'), "timestamp": r.get("timestamp")}]
    except:
        logs=[{"ip": "", "timestamp": ""}]
    return jsonify({'logs': logs})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)