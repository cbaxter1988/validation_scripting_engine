from abc import abstractmethod, ABC

from vse.core.maps import ACTION_MAP
from vse.handlers import HandlerResult, Handler, DefaultHandler, ParamsSchema

from vse.core.task import VSETask
from vse.core.exceptions import InvalidHandlerErr, MappingAgentError

from abc import ABCMeta
from marshmallow.schema import SchemaMeta


class IMapper(ABC):

    @abstractmethod
    def get_handler(self, task: VSETask) -> Handler:
        pass


class MapAgent:

    def __init__(self, **kwargs):
        self.map = kwargs.get("map", {})
        self.schema = None


class VSEMapAgent(MapAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register_handler(self, action_name, handler, params_schema):
        """Adds new Handler to the Map"""
        try:
            self.__check_handler_params(handler, params_schema)
        except MappingAgentError:
            raise

        if SchemaMeta == params_schema.__class__ and ABCMeta == handler.__class__:
            self.map[action_name] = {}
            self.map[action_name]['handler'] = handler
            self.map[action_name]['params_schema'] = params_schema
            return True
        else:
            raise MappingAgentError(f"Must be the class, not instances {Handler}, {ParamsSchema}' ")

    def get_handler(self, action_name, task: VSETask) -> Handler:
        """returns the requested handler"""
        if not isinstance(task, VSETask):
            raise MappingAgentError(f"Invalid Task Type, Must be of type {VSETask}")

        handler = self.map.get(action_name)
        if handler is False or handler is None:
            raise MappingAgentError(f"{action_name} not found")

        handler_class = handler['handler']
        handler_param_schema = handler['params_schema']

        handler = handler_class(
            name=task.action,
            params=task.params,
            task=task,
            params_schema=handler_param_schema()
        )

        return handler

    def get_handler_count(self):
        """returns total count of current handlers in the map"""
        return len(self.map)

    def delete_handler(self, action_name):
        result = self.map.get(action_name)
        if result:
            del self.map[action_name]
            return True

        return False

    def update(self, h_name, handler, params_schema):
        try:
            self.__check_handler_params(handler, params_schema)
        except MappingAgentError:
            raise

        try:

            if SchemaMeta == params_schema.__class__ and ABCMeta == handler.__class__:
                self.map[h_name]['handler'] = handler
                self.map[h_name]['params_schema'] = params_schema
                return True

        except KeyError:
            return False

    @staticmethod
    def __check_handler_params(handler, params_schema):
        if isinstance(handler, Handler):
            raise MappingAgentError(f"Must be the class, not instances {Handler}' ")

        if isinstance(params_schema, ParamsSchema):
            raise MappingAgentError(f"Must be the class, not instance {ParamsSchema}")


class VSEActionMapper(IMapper):

    def __init__(self):
        self.action_map = ACTION_MAP

    def get_handler(self, task: VSETask) -> Handler:
        """
        Queries the HandlerMap based on the VSETask.action param. If Action is not found, a default Handler
        is returned.

        """
        if isinstance(task, VSETask):
            action = self.action_map.get(task.action, self.action_map.get("default"))

            handler_class = action.get("handler")

            if issubclass(handler_class, DefaultHandler):
                raise InvalidHandlerErr(f"Invalid Handler, Supported Handlers: '{self.action_map.keys()}'")

            handler = handler_class(
                name=task.action,
                params=task.params,
                task=task,
                params_schema=action.get("params_schema")()
            )
            return handler

        raise InvalidHandlerErr("Invalid Type provided, Must be of type Handler()")
