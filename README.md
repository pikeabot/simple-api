##Docker based Hello World API

Uses Python, Flask, Redis and Docker. 

####GET /v1/hello-world
Returns a hello world message:
Output:
```
{"message" : " hello world"}
```
Format: JSON

####GET /v1/logs
Returns all logging information
Output:
```
Example:
{
  "logset": [
    {
      "endpoint": "hello-world", 
      "logs": {
        "ip": "172.17.42.1", 
        "timestamp": 1453404241
      }
    }, 
    ...
    ]
}
```
Format: JSON

####GET /v1/hello-world/logsReturns:
Returns logs for hello world
Output:
```
Example:
{
  "logs": [
    {
      "ip": "172.17.42.1", 
      "timestamp": 1453404241
    }, 
    ...
    ]
}
```
Format: JSON