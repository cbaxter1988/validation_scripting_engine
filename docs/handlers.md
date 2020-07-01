This document will discuss how to create new handlers for the VSE service. There are 3 major steps when establishing new Handlers for the system

- Create Schema that will be used to validate the parameters or options required for your Handler.
  - The ParamsSchema inherits the marshmallow.Schema class.
  - When defining parameters for your Params class use the "fields" module. This module is a the exposed marshmallow.fields module. Please Marshmallow Documentation for more information. [Marshmallow Fields Doc](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html)
- Create CustomHandler Class and add your logic in the specified Handler.execute() method.
- Register Handler in ActionMap. 



Custom Handler Boilerplate

```python
from vse.handlers import Handler, HandlerResult, ParamsSchema, fields


class TestHandlerParams(ParamsSchema):
    poked = fields.Boolean(required=True)


class CustomHandler(Handler): # TODO: Update Handler name
	
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:
  
        ##### CUSTOM_CODE_HERE ######
        
        #############################

        self.check_expectation()
        return self.result
```





Example Handler 

Params Schema:

```python
from marshmallow import fields
from app.vse.handlers.schemas.params import Params


class TestHandlerParams(Params):
    poked = fields.Boolean(required=True)

```



Handler: 

```python
from app.vse.handlers import Handler, HandlerResult


class TestHandler(Handler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:
		##### CUSTOM_CODE_HERE ######
        poked = self.params.get("poked", False)

        if poked:
            self.result.status = True
            self.result.msg = "Hey, You Poked Me"

        else:
     
            self.result.status = False
            self.result.msg = "What do you want?"
        #############################

        self.check_expectation()
        return self.result

```

Action-Map

```python
from app.vse.handlers.schemas.params_test import TestHandlerParams
from app.vse.handlers.test import TestHandler

ACTION_MAP = {
    "test_handler": {
        "handler": TestHandler,
        "params_schema": TestHandlerParams
    }
}
```

