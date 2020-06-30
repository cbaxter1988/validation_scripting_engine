# Validation Scripting Engine(VSE)

The Validation Scripting Engine is an auidting system that provides
flexibility when interacting with network devices. 

Low-Level API Example: 
```python
from vse.api.rpc.client import VSERPCClient

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
c = VSERPCClient(host="rpc.vsehost.com", port=8000)

resp = c.run_audit(data)

resp_data = resp.get("data")
```