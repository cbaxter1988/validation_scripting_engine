# Validation Scripting Engine(VSE)

The Validation Scripting Engine is an auditing system that provides flexibility  when auditing network assets.  The VSE exposes both an XMLRPC and RESTful interface for third-party consumption.

# Installation

The validation scripting engine can be deployed from source in the /dist folder or deployed using docker.  You can also utilized the Cloud hosted API for online demos



## Source:

```bash
git clone https://github.com/cbaxter1988/validation_scripting_engine.git

cd validation_scripting_engine

tar -xzf build/vse-1.0.tar.gz && cd VSE-1.0 && python setup.py install
```



## Docker

```bash
docker pull cbaxter1988/vse

docker run -p 8000:8000 -e APP_PORT 8000 cbaxter1988/vse --serve_rpc
```



## docker-compose:



Deploy xmlrpc service

```yaml
version: "3.1"
services:
    vse_rpc:
        image: cbaxter1988/vse
        ports:
          - 8000:8000
        environment:
          - APP_PORT=8000
          - DEBUG=true
        command: --serve_rpc

```

Deploy RESTFul service

```yaml
version: "3.1"
services:
    vse_rest:
    image: cbaxter1988/vse
    ports:
      - 8070:8070
    environment:
      - APP_PORT=8070
      - DEBUG=true

```

# Core

## Classes

- **VSE**
  - Main class used to facilitate the execution of audits. 
- **VSEAudit**
  - Class used to represent an Audit that will be ran on the system
- **VSETask**
  - Class used to represent a single task within an VSEAudit.  a single VSETask can exists in multiple audits without any relationship.
- **Handler**
  - Class used to proxy  task.action request processed be the VSE.
- **HandlerResult**
  - Return for every VSEAudit ran in the VSE.audits list.
- **VSEMapAgent**
  - Class used to hold the systems active handlers. 

# Examples

**RESTFul API**

- URL: http://io.cbaxterjr.com/api/rest/vse
- Headers:
  - Content-Type: application/json

```python
import requests 

URL = http://io.cbaxterjr.com/api/rest/vse

data = {
        "target": "192.168.1.1",
        "description": "This is My Example Audit",
        "target_facts": {
            "assetHostname ": "r1.bits.local",
            "nodeType": "cisco_ios"
        },
        "fail_limit": 0,
        "tasks": [
            {
                "action": "test_handler",
                "description": "Executes the TestHandler",
                "params": {
                    "poked": True
                },
                "expectation": True
            },
            {
                "action": "h_find_lines",
                "description": "Checks if hostname if configured on device, If Match Pass",
                "params": {
                    "line_spec": "hostname (.*)",
                    "config_str_list": [
                        "hostname r1.bits.local"
                    ]
                },
                "expectation": True
            }
        ]
    }

response = requests.post(url=URL, json=data, headers={"Content-Type": "application/json"})
```





**XMLRPC Client**

```
from vse.api.rpc import VSERPCClient

if __name__ == "__main__":
    data = {
        "target": "192.168.1.1",
        "description": "This is My Example Audit",
        "target_facts": {
            "assetHostname ": "r1.bits.local",
            "nodeType": "cisco_ios"
        },
        "fail_limit": 0,
        "tasks": [
            {
                "action": "test_handler",
                "description": "Executes the TestHandler",
                "params": {
                    "poked": True
                },
                "expectation": True
            },
            {
                "action": "h_find_lines",
                "description": "Checks if hostname if configured on device, If Match Pass",
                "params": {
                    "line_spec": "hostname (.*)",
                    "config_str_list": [
                        "hostname r1.bits.local"
                    ]
                },
                "expectation": True
            }
        ]
    }


    HOST = "io.cbaxterjr.com"
    
    c = VSERPCClient(host=HOST, port=PORT)

    c.run_audit(data)
```







**low-level API**

```python
# Creates new VSE Object
vse = VSE()

# Create 2 Audits
audit1 = VSEAudit(
    target="192.168.1.5",
    name="My Core Switch Audit",
    fail_limit=2
)
audit2 = VSEAudit(
    target="192.168.1.10",
    name="My Core Router Audit",
    fail_limit=0
)


# Create 2 Task
task1 = VSETask(**
                {
                    "action": "test_handler",
                    "description": "Test My API",
                    "params": {
                        "poked": False
                    },
                    "expectation": True
                }
               )

task2 = VSETask(**
                {
                    "action": "test_handler",
                    "description": "Test My API",
                    "params": {
                        "poked": True
                    },
                    "expectation": False
                }
               )

# Adds the tasks above to audit1 
audit1.add_task(task1)
audit1.add_task(task2)

# Adds the tasks above to audit2 
audit2.add_task(task1)
audit2.add_task(task2)

# Adds the audit to the VSE.audits list.
vse.add_audit(audit1)
vse.add_audit(audit2)

#executes the audits and returns the results
results = vse.run()
```

